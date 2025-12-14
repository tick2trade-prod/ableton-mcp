"""Signal processing chain schemas."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class FrequencyBand(str, Enum):
    """Standard frequency bands for audio engineering."""

    SUB = "sub"  # 20-60 Hz
    BASS = "bass"  # 60-250 Hz
    LOW_MID = "low_mid"  # 250-500 Hz
    MID = "mid"  # 500-2k Hz
    HIGH_MID = "high_mid"  # 2k-4k Hz
    HIGH = "high"  # 4k-8k Hz
    AIR = "air"  # 8k-20k Hz


# Frequency range definitions
FREQUENCY_BANDS = {
    FrequencyBand.SUB: (20, 60),
    FrequencyBand.BASS: (60, 250),
    FrequencyBand.LOW_MID: (250, 500),
    FrequencyBand.MID: (500, 2000),
    FrequencyBand.HIGH_MID: (2000, 4000),
    FrequencyBand.HIGH: (4000, 8000),
    FrequencyBand.AIR: (8000, 20000),
}


class FilterType(str, Enum):
    """EQ filter types."""

    BELL = "bell"
    LOW_SHELF = "low_shelf"
    HIGH_SHELF = "high_shelf"
    HIGHPASS = "highpass"
    LOWPASS = "lowpass"
    NOTCH = "notch"
    BANDPASS = "bandpass"


class EQOperation(BaseModel):
    """EQ adjustment specification."""

    band: FrequencyBand | None = None
    frequency: int = Field(ge=20, le=20000, description="Center frequency in Hz")
    gain_db: float = Field(ge=-24, le=24, description="Gain in dB")
    q: float = Field(default=1.0, ge=0.1, le=18.0, description="Bandwidth/Q factor")
    filter_type: FilterType = FilterType.BELL

    @classmethod
    def highpass(cls, frequency: int, q: float = 0.707) -> "EQOperation":
        """Create a highpass filter."""
        return cls(
            frequency=frequency,
            gain_db=0,
            q=q,
            filter_type=FilterType.HIGHPASS,
        )

    @classmethod
    def lowpass(cls, frequency: int, q: float = 0.707) -> "EQOperation":
        """Create a lowpass filter."""
        return cls(
            frequency=frequency,
            gain_db=0,
            q=q,
            filter_type=FilterType.LOWPASS,
        )

    @classmethod
    def cut(cls, frequency: int, db: float, q: float = 2.0) -> "EQOperation":
        """Create a cut/boost at frequency."""
        return cls(
            frequency=frequency,
            gain_db=db,
            q=q,
            filter_type=FilterType.BELL,
        )


class DynamicsOperation(BaseModel):
    """Compression/dynamics specification."""

    threshold_db: float = Field(ge=-60, le=0, description="Threshold in dB")
    ratio: float = Field(ge=1.0, le=100.0, description="Compression ratio")
    attack_ms: float = Field(ge=0.01, le=1000, description="Attack time in ms")
    release_ms: float = Field(ge=1, le=5000, description="Release time in ms")
    makeup_gain_db: float = Field(default=0.0, ge=0, le=24)
    knee_db: float = Field(default=0.0, ge=0, le=24)

    @classmethod
    def glue(cls) -> "DynamicsOperation":
        """Classic glue compression settings."""
        return cls(
            threshold_db=-10,
            ratio=4.0,
            attack_ms=30,
            release_ms=200,
            makeup_gain_db=2,
        )

    @classmethod
    def punch(cls) -> "DynamicsOperation":
        """Punchy drum compression."""
        return cls(
            threshold_db=-15,
            ratio=6.0,
            attack_ms=10,
            release_ms=80,
            makeup_gain_db=4,
        )

    @classmethod
    def sidechain(cls) -> "DynamicsOperation":
        """Classic sidechain pump."""
        return cls(
            threshold_db=-20,
            ratio=10.0,
            attack_ms=0.1,
            release_ms=150,
            makeup_gain_db=0,
        )


class SaturationType(str, Enum):
    """Saturation/distortion types."""

    ANALOG_CLIP = "analog_clip"
    SOFT_SINE = "soft_sine"
    MEDIUM_CURVE = "medium_curve"
    HARD_CURVE = "hard_curve"
    WAVESHAPER = "waveshaper"


class SaturationOperation(BaseModel):
    """Saturation/distortion specification."""

    drive_db: float = Field(ge=0, le=24, description="Drive amount in dB")
    type: SaturationType = SaturationType.ANALOG_CLIP
    mix: float = Field(default=1.0, ge=0.0, le=1.0, description="Dry/wet mix")
    output_db: float = Field(default=0.0, ge=-24, le=6)

    @classmethod
    def warm(cls) -> "SaturationOperation":
        """Subtle warmth."""
        return cls(drive_db=3, type=SaturationType.SOFT_SINE, mix=0.5)

    @classmethod
    def crunch(cls) -> "SaturationOperation":
        """Crunchy saturation."""
        return cls(drive_db=8, type=SaturationType.ANALOG_CLIP, mix=1.0)

    @classmethod
    def destroy(cls) -> "SaturationOperation":
        """Heavy distortion."""
        return cls(drive_db=18, type=SaturationType.HARD_CURVE, mix=1.0)


class ProcessingChain(BaseModel):
    """Complete processing chain for a track."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    version: str = "1.0.0"

    # Processing stages
    eq: list[EQOperation] = []
    dynamics: list[DynamicsOperation] = []
    saturation: SaturationOperation | None = None

    # Common techno settings
    bass_mono_freq: int | None = 120  # Hz for Utility bass mono

    # Metadata
    tags: list[str] = []
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def to_device_params(self) -> dict:
        """Convert to Ableton device parameter format."""
        return {
            "eq_bands": [op.model_dump() for op in self.eq],
            "compressor": (
                [op.model_dump() for op in self.dynamics] if self.dynamics else None
            ),
            "saturator": self.saturation.model_dump() if self.saturation else None,
            "utility": {"bass_mono": self.bass_mono_freq},
        }


# ============================================================
# Common Techno Processing Chains
# ============================================================

TECHNO_CHAINS = {
    "kick_punch": ProcessingChain(
        name="Punchy Kick",
        eq=[
            EQOperation.highpass(30),
            EQOperation.cut(200, -3, q=2.0),  # Reduce mud
            EQOperation.cut(4000, 2, q=1.5),  # Click
        ],
        dynamics=[DynamicsOperation.punch()],
        saturation=SaturationOperation.crunch(),
        bass_mono_freq=120,
        tags=["kick", "punchy", "909"],
    ),
    "sub_bass": ProcessingChain(
        name="Sub Bass",
        eq=[
            EQOperation.highpass(30),
            EQOperation.lowpass(200),
        ],
        saturation=SaturationOperation.warm(),
        bass_mono_freq=100,
        tags=["bass", "sub", "clean"],
    ),
    "acid_303": ProcessingChain(
        name="Acid 303",
        eq=[
            EQOperation.highpass(60),
            EQOperation.cut(800, 3, q=4.0),  # Resonance zone
        ],
        saturation=SaturationOperation(
            drive_db=12, type=SaturationType.ANALOG_CLIP, mix=0.8
        ),
        tags=["303", "acid", "squelchy"],
    ),
}
