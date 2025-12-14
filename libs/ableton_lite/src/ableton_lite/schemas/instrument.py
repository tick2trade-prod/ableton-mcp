"""Instrument catalog schemas."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from ableton_lite.schemas.pattern import PatternType


class InstrumentCategory(str, Enum):
    """Instrument categories for techno production."""

    DRUM_MACHINE = "drum_machine"
    DRUM_SAMPLER = "drum_sampler"
    SYNTH_BASS = "synth_bass"
    SYNTH_LEAD = "synth_lead"
    SYNTH_PAD = "synth_pad"
    SYNTH_PLUCK = "synth_pluck"
    SAMPLER = "sampler"
    FX = "fx"
    UTILITY = "utility"


class Instrument(BaseModel):
    """Base instrument definition."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: InstrumentCategory

    # Ableton integration
    ableton_path: str | None = None  # Browser path
    ableton_device: str | None = None  # Device name to load

    # Sound characteristics
    frequency_min: int = Field(default=20, ge=20, le=20000)
    frequency_max: int = Field(default=20000, ge=20, le=20000)
    typical_velocity: int = Field(default=100, ge=0, le=127)

    # Recommended processing
    recommended_fx: list[str] = []

    # What patterns this works for
    suitable_for: list[PatternType] = []

    # Metadata
    tags: list[str] = []
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class InstrumentPreset(Instrument):
    """Instrument with specific preset settings."""

    # Preset-specific settings
    parameters: dict[str, float] = {}

    # Source/lineage
    based_on: str | None = None  # Parent instrument ID
    version: str = "1.0.0"


# ============================================================
# Techno Instrument Catalog
# ============================================================

TECHNO_DRUMS = {
    "909_kick": Instrument(
        name="909 Kick",
        category=InstrumentCategory.DRUM_MACHINE,
        ableton_device="Drum Sampler",
        frequency_min=30,
        frequency_max=200,
        typical_velocity=110,
        recommended_fx=["Saturator", "Channel EQ", "Utility"],
        suitable_for=[PatternType.KICK],
        tags=["909", "classic", "punchy"],
    ),
    "909_snare": Instrument(
        name="909 Snare",
        category=InstrumentCategory.DRUM_MACHINE,
        ableton_device="Drum Sampler",
        frequency_min=100,
        frequency_max=8000,
        typical_velocity=100,
        recommended_fx=["Saturator", "Reverb"],
        suitable_for=[PatternType.SNARE],
        tags=["909", "snappy"],
    ),
    "909_clap": Instrument(
        name="909 Clap",
        category=InstrumentCategory.DRUM_MACHINE,
        ableton_device="Drum Sampler",
        frequency_min=500,
        frequency_max=12000,
        typical_velocity=110,
        recommended_fx=["Reverb", "Delay"],
        suitable_for=[PatternType.CLAP],
        tags=["909", "tight"],
    ),
    "909_hihat": Instrument(
        name="909 Hi-Hat",
        category=InstrumentCategory.DRUM_MACHINE,
        ableton_device="Drum Sampler",
        frequency_min=2000,
        frequency_max=18000,
        typical_velocity=90,
        recommended_fx=["Channel EQ"],
        suitable_for=[PatternType.HIHAT],
        tags=["909", "crisp"],
    ),
}

TECHNO_BASS = {
    "sub_bass": Instrument(
        name="Sub Bass",
        category=InstrumentCategory.SYNTH_BASS,
        ableton_device="Analog",
        frequency_min=30,
        frequency_max=150,
        typical_velocity=100,
        recommended_fx=["Saturator", "Utility"],
        suitable_for=[PatternType.BASS],
        tags=["sub", "rumble", "foundation"],
    ),
    "303_acid": Instrument(
        name="303 Acid Bass",
        category=InstrumentCategory.SYNTH_BASS,
        ableton_device="Analog",
        frequency_min=50,
        frequency_max=5000,
        typical_velocity=100,
        recommended_fx=["Saturator", "Auto Filter", "Delay"],
        suitable_for=[PatternType.BASS, PatternType.LEAD],
        tags=["303", "acid", "resonant", "squelchy"],
    ),
    "moog_bass": Instrument(
        name="Moog-Style Bass",
        category=InstrumentCategory.SYNTH_BASS,
        ableton_device="Analog",
        frequency_min=40,
        frequency_max=2000,
        typical_velocity=110,
        recommended_fx=["Saturator", "Compressor"],
        suitable_for=[PatternType.BASS],
        tags=["moog", "fat", "warm"],
    ),
}

TECHNO_SYNTHS = {
    "pad_evolving": Instrument(
        name="Evolving Pad",
        category=InstrumentCategory.SYNTH_PAD,
        ableton_device="Wavetable",
        frequency_min=100,
        frequency_max=8000,
        typical_velocity=80,
        recommended_fx=["Reverb", "Delay", "Chorus"],
        suitable_for=[PatternType.PAD],
        tags=["atmospheric", "evolving", "texture"],
    ),
    "stab_short": Instrument(
        name="Short Stab",
        category=InstrumentCategory.SYNTH_PLUCK,
        ableton_device="Analog",
        frequency_min=200,
        frequency_max=6000,
        typical_velocity=90,
        recommended_fx=["Reverb", "Delay"],
        suitable_for=[PatternType.STAB],
        tags=["punchy", "chord", "offbeat"],
    ),
    "lead_saw": Instrument(
        name="Saw Lead",
        category=InstrumentCategory.SYNTH_LEAD,
        ableton_device="Analog",
        frequency_min=200,
        frequency_max=8000,
        typical_velocity=100,
        recommended_fx=["Delay", "Reverb", "Chorus"],
        suitable_for=[PatternType.LEAD, PatternType.ARP],
        tags=["bright", "cutting", "melodic"],
    ),
}


def get_instrument_catalog() -> dict[str, Instrument]:
    """Get complete techno instrument catalog."""
    return {**TECHNO_DRUMS, **TECHNO_BASS, **TECHNO_SYNTHS}
