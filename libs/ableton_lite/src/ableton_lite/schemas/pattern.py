"""Pattern and note schemas for musical content."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ableton_lite.schemas.time import Duration, TimePosition


class PatternType(str, Enum):
    """Pattern categories for techno."""

    KICK = "kick"
    SNARE = "snare"
    HIHAT = "hihat"
    CLAP = "clap"
    PERC = "perc"
    BASS = "bass"
    LEAD = "lead"
    PAD = "pad"
    ARP = "arp"
    STAB = "stab"
    FX = "fx"
    RISER = "riser"
    IMPACT = "impact"


class Scale(str, Enum):
    """Common scales for techno."""

    MINOR = "minor"
    MAJOR = "major"
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    MIXOLYDIAN = "mixolydian"
    HARMONIC_MINOR = "harmonic_minor"
    MELODIC_MINOR = "melodic_minor"
    CHROMATIC = "chromatic"


# Scale intervals from root (in semitones)
SCALE_INTERVALS = {
    Scale.MINOR: [0, 2, 3, 5, 7, 8, 10],
    Scale.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    Scale.DORIAN: [0, 2, 3, 5, 7, 9, 10],
    Scale.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],
    Scale.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
    Scale.HARMONIC_MINOR: [0, 2, 3, 5, 7, 8, 11],
    Scale.MELODIC_MINOR: [0, 2, 3, 5, 7, 9, 11],
    Scale.CHROMATIC: list(range(12)),
}

# Note names for display
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_note_name(pitch: int) -> str:
    """Convert MIDI pitch to note name (e.g., 60 -> C4)."""
    octave = (pitch // 12) - 1
    note = NOTE_NAMES[pitch % 12]
    return f"{note}{octave}"


def note_name_to_midi(name: str) -> int:
    """Convert note name to MIDI pitch (e.g., C4 -> 60)."""
    # Parse note and octave
    for i, n in enumerate(NOTE_NAMES):
        if name.startswith(n):
            note_idx = i
            octave = int(name[len(n) :])
            return (octave + 1) * 12 + note_idx
    raise ValueError(f"Invalid note name: {name}")


class Note(BaseModel):
    """Single MIDI note with musical semantics."""

    pitch: int = Field(ge=0, le=127, description="MIDI pitch (C-1=0, C4=60)")
    position: TimePosition
    duration: Duration
    velocity: int = Field(ge=0, le=127, default=100)
    mute: bool = False

    # Optional semantic info
    note_name: str | None = None
    scale_degree: int | None = None  # 1-7 in current scale

    def model_post_init(self, __context: Any) -> None:
        """Auto-populate note_name if not provided."""
        if self.note_name is None:
            object.__setattr__(self, "note_name", midi_to_note_name(self.pitch))

    def to_ableton_dict(self) -> dict[str, Any]:
        """Convert to Ableton MCP note format."""
        return {
            "pitch": self.pitch,
            "start_time": self.position.to_beats(),
            "duration": self.duration.beats,
            "velocity": self.velocity,
            "mute": self.mute,
        }

    @classmethod
    def from_ableton_dict(cls, data: dict[str, Any]) -> "Note":
        """Create from Ableton MCP note format."""
        return cls(
            pitch=data["pitch"],
            position=TimePosition.from_beats(data["start_time"]),
            duration=Duration(beats=data["duration"]),
            velocity=data.get("velocity", 100),
            mute=data.get("mute", False),
        )


class Pattern(BaseModel):
    """Reusable, versioned musical pattern."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: PatternType
    version: str = "1.0.0"  # Semantic versioning

    # Musical context
    key: str = "C"  # Root note
    scale: Scale = Scale.MINOR
    tempo_min: int = Field(default=120, ge=60, le=200)
    tempo_max: int = Field(default=140, ge=60, le=200)

    # Pattern data
    length_bars: int = Field(default=4, ge=1, le=64)
    notes: list[Note]

    # Metadata
    tags: list[str] = []
    source: str | None = None  # Original track reference
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def to_ableton_notes(self) -> list[dict[str, Any]]:
        """Convert all notes to Ableton MCP format."""
        return [note.to_ableton_dict() for note in self.notes]

    @classmethod
    def from_ableton_notes(
        cls,
        name: str,
        type: PatternType,
        notes: list[dict[str, Any]],
        length_bars: int = 4,
        **kwargs,
    ) -> "Pattern":
        """Create pattern from Ableton MCP notes."""
        return cls(
            name=name,
            type=type,
            length_bars=length_bars,
            notes=[Note.from_ableton_dict(n) for n in notes],
            **kwargs,
        )

    def shift_to_key(self, new_key: str) -> "Pattern":
        """Transpose pattern to new key (returns new pattern)."""
        current_root = note_name_to_midi(f"{self.key}0") % 12
        new_root = note_name_to_midi(f"{new_key}0") % 12
        shift = new_root - current_root

        new_notes = []
        for note in self.notes:
            new_pitch = max(0, min(127, note.pitch + shift))
            new_note = note.model_copy(update={"pitch": new_pitch, "note_name": None})
            new_notes.append(new_note)

        return self.model_copy(
            update={
                "id": str(uuid.uuid4()),
                "key": new_key,
                "notes": new_notes,
                "version": self._increment_version(),
            }
        )

    def _increment_version(self) -> str:
        """Increment patch version."""
        parts = self.version.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
