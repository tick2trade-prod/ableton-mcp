"""Tempo-based time system for musical positioning."""

from enum import Enum

from pydantic import BaseModel, Field


class TimeUnit(str, Enum):
    """Musical time units."""

    TICK = "tick"  # 1/96th of a beat (MIDI resolution)
    SIXTEENTH = "16th"  # 1/16th note
    EIGHTH = "8th"  # 1/8th note
    QUARTER = "quarter"  # 1 beat
    HALF = "half"  # 2 beats
    BAR = "bar"  # 4 beats (4/4 time)
    PHRASE = "phrase"  # 4 bars (16 beats)
    SECTION = "section"  # 8 bars (32 beats)


# Multipliers for converting units to beats
UNIT_TO_BEATS = {
    TimeUnit.TICK: 1 / 96,
    TimeUnit.SIXTEENTH: 0.25,
    TimeUnit.EIGHTH: 0.5,
    TimeUnit.QUARTER: 1.0,
    TimeUnit.HALF: 2.0,
    TimeUnit.BAR: 4.0,
    TimeUnit.PHRASE: 16.0,
    TimeUnit.SECTION: 32.0,
}


class TimePosition(BaseModel):
    """Tempo-aware position in musical time.

    Uses bar.beat.tick notation (e.g., 2.3.48 = bar 2, beat 3, tick 48)
    """

    bar: int = Field(ge=0, description="Bar number (0-indexed)")
    beat: int = Field(ge=0, lt=4, description="Beat within bar (0-3)")
    tick: int = Field(ge=0, lt=96, description="Tick within beat (0-95)")

    def to_beats(self) -> float:
        """Convert to absolute beat position."""
        return self.bar * 4 + self.beat + (self.tick / 96.0)

    def to_seconds(self, tempo: float) -> float:
        """Convert to seconds at given tempo (BPM)."""
        beats = self.to_beats()
        return beats * (60.0 / tempo)

    def to_samples(self, tempo: float, sample_rate: int = 44100) -> int:
        """Convert to sample position."""
        seconds = self.to_seconds(tempo)
        return int(seconds * sample_rate)

    @classmethod
    def from_beats(cls, beats: float) -> "TimePosition":
        """Create TimePosition from absolute beats."""
        bar = int(beats // 4)
        remaining = beats - (bar * 4)
        beat = int(remaining)
        tick = int((remaining - beat) * 96)
        return cls(bar=bar, beat=beat, tick=tick)

    @classmethod
    def from_seconds(cls, seconds: float, tempo: float) -> "TimePosition":
        """Create TimePosition from seconds at given tempo."""
        beats = seconds * (tempo / 60.0)
        return cls.from_beats(beats)

    def __str__(self) -> str:
        """Format as bar.beat.tick notation."""
        return f"{self.bar}.{self.beat}.{self.tick:02d}"

    def __repr__(self) -> str:
        return f"TimePosition({self})"

    def __add__(self, other: "Duration") -> "TimePosition":
        """Add a duration to this position."""
        new_beats = self.to_beats() + other.beats
        return TimePosition.from_beats(new_beats)


class Duration(BaseModel):
    """Musical duration with semantic unit."""

    beats: float = Field(gt=0, description="Duration in beats")
    unit: TimeUnit = TimeUnit.QUARTER

    @classmethod
    def from_unit(cls, count: float, unit: TimeUnit) -> "Duration":
        """Create duration from count of a specific unit."""
        beats = count * UNIT_TO_BEATS[unit]
        return cls(beats=beats, unit=unit)

    @classmethod
    def ticks(cls, count: int) -> "Duration":
        """Create duration from tick count."""
        return cls.from_unit(count, TimeUnit.TICK)

    @classmethod
    def sixteenths(cls, count: int) -> "Duration":
        """Create duration from 16th note count."""
        return cls.from_unit(count, TimeUnit.SIXTEENTH)

    @classmethod
    def eighths(cls, count: int) -> "Duration":
        """Create duration from 8th note count."""
        return cls.from_unit(count, TimeUnit.EIGHTH)

    @classmethod
    def quarters(cls, count: int) -> "Duration":
        """Create duration from quarter note count."""
        return cls.from_unit(count, TimeUnit.QUARTER)

    @classmethod
    def bars(cls, count: int) -> "Duration":
        """Create duration from bar count."""
        return cls.from_unit(count, TimeUnit.BAR)

    def to_seconds(self, tempo: float) -> float:
        """Convert to seconds at given tempo."""
        return self.beats * (60.0 / tempo)

    def __str__(self) -> str:
        return f"{self.beats} beats ({self.unit.value})"
