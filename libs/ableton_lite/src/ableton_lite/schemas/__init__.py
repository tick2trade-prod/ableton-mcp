"""Pydantic schemas for AbletonLite V3."""

from ableton_lite.schemas.crew import (
    AgentCapability,
    AgentRole,
    Crew,
    CrewAgent,
    CrewTask,
)
from ableton_lite.schemas.instrument import (
    Instrument,
    InstrumentCategory,
    InstrumentPreset,
)
from ableton_lite.schemas.pattern import Note, Pattern, PatternType, Scale
from ableton_lite.schemas.processing import (
    DynamicsOperation,
    EQOperation,
    FrequencyBand,
    ProcessingChain,
    SaturationOperation,
)
from ableton_lite.schemas.time import Duration, TimePosition, TimeUnit

__all__ = [
    # Time
    "TimeUnit",
    "TimePosition",
    "Duration",
    # Pattern
    "Note",
    "Pattern",
    "PatternType",
    "Scale",
    # Instrument
    "Instrument",
    "InstrumentCategory",
    "InstrumentPreset",
    # Processing
    "FrequencyBand",
    "EQOperation",
    "DynamicsOperation",
    "SaturationOperation",
    "ProcessingChain",
    # Crew
    "AgentRole",
    "AgentCapability",
    "CrewAgent",
    "CrewTask",
    "Crew",
]
