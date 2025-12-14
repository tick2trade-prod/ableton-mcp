"""Track structure models (Pydantic 2.x).

Version: 1.0.0

Models for validating track configurations for Ableton Live projects.
Supports type-safe, validated track generation with MIDI, devices, and routing.
"""

from enum import Enum
from typing import Annotated, Self

from pydantic import Field, field_validator, model_validator

from .base import ModernBaseModel


class TrackType(str, Enum):
    """Supported track types for Ableton Live."""

    KICK = "kick"
    BASS = "bass"
    SYNTH = "synth"
    DRUM = "drum"
    VOCAL = "vocal"
    FX = "fx"
    AUDIO = "audio"
    RETURN = "return"
    MASTER = "master"


class MIDINote(ModernBaseModel):
    """MIDI note with validation.

    Attributes:
        pitch: MIDI pitch (0-127)
        start_time: Start time in beats (0.0+)
        duration: Duration in beats (0.0-16.0)
        velocity: Note velocity (0-127)
    """

    pitch: Annotated[int, Field(ge=0, le=127, description="MIDI pitch (0-127)")]
    start_time: Annotated[float, Field(ge=0.0, description="Start time in beats")]
    duration: Annotated[float, Field(gt=0.0, le=16.0, description="Duration in beats")]
    velocity: Annotated[int, Field(ge=0, le=127, description="Note velocity")]

    @field_validator("duration")
    @classmethod
    def validate_duration(cls, v: float, info) -> float:
        """Ensure duration is reasonable for a single clip."""
        if v > 16.0:
            raise ValueError(f"Duration {v} exceeds maximum 16 beats")
        return v


class DeviceConfig(ModernBaseModel):
    """Device configuration with parameters.

    Attributes:
        name: Device name (e.g., "Drum Sampler", "Channel EQ")
        parameters: Device parameter values {param_name: value}
        fallback: Optional fallback device name if primary not found
    """

    name: str
    parameters: dict[str, float] = Field(default_factory=dict)
    fallback: str | None = None

    @field_validator("parameters")
    @classmethod
    def validate_parameter_values(cls, v: dict[str, float]) -> dict[str, float]:
        """Validate parameter values are in valid range."""
        for param, value in v.items():
            if not (-1000.0 <= value <= 1000.0):
                raise ValueError(f"Parameter {param} value {value} out of range")
        return v


class TrackConfig(ModernBaseModel):
    """Complete track configuration.

    Attributes:
        index: Track index (0-based)
        name: Track name (e.g., "Track 01 - Kick")
        track_type: Track type enum
        color: Hex color code (e.g., "#FF0000")
        volume_db: Volume in dB (-60.0 to +6.0)
        pan: Pan position (-1.0 to +1.0)
        devices: List of device configurations
        midi_clips: List of MIDI clips (each clip is a list of notes)
        audio_routing: Optional audio routing destination
    """

    index: Annotated[int, Field(ge=0, le=99)]
    name: Annotated[str, Field(pattern=r"^Track \d{2} - .+$")]
    track_type: TrackType
    color: Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{6}$")]
    volume_db: Annotated[float, Field(ge=-60.0, le=6.0)]
    pan: Annotated[float, Field(ge=-1.0, le=1.0)]
    devices: list[DeviceConfig] = Field(default_factory=list)
    midi_clips: list[list[MIDINote]] = Field(default_factory=list)
    audio_routing: str | None = None

    @field_validator("name")
    @classmethod
    def validate_track_name(cls, v: str, info) -> str:
        """Ensure track name matches index."""
        # Pydantic 2.x: info.data instead of values
        index = info.data.get("index")
        if index is not None:
            expected_prefix = f"Track {index + 1:02d}"
            if not v.startswith(expected_prefix):
                raise ValueError(f"Track name must start with '{expected_prefix}'")
        return v


class ProjectConfig(ModernBaseModel):
    """Complete project configuration.

    Attributes:
        name: Project name
        tempo: BPM (100-200)
        time_signature: Time signature tuple (numerator, denominator)
        total_bars: Total number of bars in project
        tracks: List of track configurations
    """

    name: str
    tempo: Annotated[int, Field(ge=100, le=200, default=136)]
    time_signature: tuple[int, int] = Field(default=(4, 4))
    total_bars: Annotated[int, Field(ge=16, le=256, default=64)]
    tracks: list[TrackConfig] = Field(default_factory=list)

    @model_validator(mode="after")  # Pydantic 2.x: mode parameter
    def validate_track_indices(self) -> Self:
        """Ensure track indices are sequential and unique."""
        if not self.tracks:
            return self

        indices = [t.index for t in self.tracks]
        if len(indices) != len(set(indices)):
            raise ValueError("Duplicate track indices found")

        # Check for sequential indices (0 to n-1)
        expected = list(range(len(self.tracks)))
        if sorted(indices) != expected:
            raise ValueError(
                f"Track indices must be sequential 0 to {len(self.tracks) - 1}"
            )

        return self

    @field_validator("time_signature")
    @classmethod
    def validate_time_signature(cls, v: tuple[int, int]) -> tuple[int, int]:
        """Validate time signature is common/valid."""
        numerator, denominator = v
        if numerator < 1 or numerator > 32:
            raise ValueError(f"Time signature numerator {numerator} out of range")
        if denominator not in [2, 4, 8, 16]:
            raise ValueError(f"Time signature denominator {denominator} not supported")
        return v
