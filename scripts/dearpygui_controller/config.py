"""Configuration for the DearPyGUI controller."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class TrackConfig:
    """Configuration for a single track."""

    index: int
    name: str
    track_type: str  # "midi" or "audio"
    role: str  # "rhythm", "texture", "harmony", "vocal", "fx"
    spectral_low: int
    spectral_high: int
    devices: list[str] = field(default_factory=list)


# 16 Track definitions from spec
TRACKS: list[TrackConfig] = [
    TrackConfig(
        0,
        "01-Kick",
        "midi",
        "rhythm",
        40,
        150,
        ["Drum Sampler", "Channel EQ", "Saturator"],
    ),
    TrackConfig(
        1, "02-Rumble", "audio", "texture", 30, 100, ["Reverb", "Roar", "Compressor"]
    ),
    TrackConfig(
        2,
        "03-RollingBass",
        "midi",
        "rhythm",
        100,
        400,
        ["Operator", "Channel EQ", "Compressor"],
    ),
    TrackConfig(
        3, "04-Acid", "midi", "lead", 100, 5000, ["Operator", "Auto Filter", "Redux"]
    ),
    TrackConfig(
        4,
        "05-ClosedHats",
        "midi",
        "rhythm",
        5000,
        15000,
        ["Drum Sampler", "Channel EQ"],
    ),
    TrackConfig(
        5, "06-OpenHats", "midi", "rhythm", 4000, 12000, ["Drum Sampler", "Channel EQ"]
    ),
    TrackConfig(6, "07-Clap", "midi", "rhythm", 400, 3000, ["Drum Sampler", "Reverb"]),
    TrackConfig(
        7, "08-LowTom", "midi", "rhythm", 60, 500, ["Drum Sampler", "Channel EQ"]
    ),
    TrackConfig(
        8, "09-Glitch", "midi", "texture", 200, 15000, ["Simpler", "Beat Repeat"]
    ),
    TrackConfig(
        9, "10-Ride", "midi", "rhythm", 2000, 18000, ["Drum Sampler", "Channel EQ"]
    ),
    TrackConfig(
        10,
        "11-SynthStab",
        "midi",
        "harmony",
        200,
        10000,
        ["Wavetable", "Echo", "Reverb"],
    ),
    TrackConfig(
        11, "12-Drone", "midi", "harmony", 50, 8000, ["Operator", "Reverb", "Chorus"]
    ),
    TrackConfig(
        12,
        "13-Vocal",
        "audio",
        "vocal",
        100,
        8000,
        ["Channel EQ", "Compressor", "Reverb"],
    ),
    TrackConfig(13, "14-VocalFX", "audio", "vocal", 200, 15000, ["Echo", "Reverb"]),
    TrackConfig(14, "15-Riser", "midi", "fx", 200, 15000, ["Operator", "Auto Filter"]),
    TrackConfig(15, "16-Impact", "midi", "fx", 30, 10000, ["Drum Sampler", "Reverb"]),
]


@dataclass
class OllamaConfig:
    """Ollama LLM configuration."""

    model: str = "llama3"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7


@dataclass
class AbletonConfig:
    """Ableton MCP connection configuration."""

    host: str = "127.0.0.1"
    port: int = 9877
    timeout: float = 15.0


@dataclass
class AgentConfig:
    """Agent behavior configuration."""

    verbose: bool = True
    max_retries: int = 3


@dataclass
class ControllerConfig:
    """Main controller configuration."""

    # Session settings
    tempo: float = 136.0
    key: str = "F"
    scale: str = "minor"

    # Sub-configurations
    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    ableton: AbletonConfig = field(default_factory=AbletonConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)

    # Paths
    project_root: Path = field(
        default_factory=lambda: Path(__file__).parent.parent.parent
    )

    @property
    def tracks(self) -> list[TrackConfig]:
        """Return all track configurations."""
        return TRACKS

    @property
    def track_count(self) -> int:
        """Return total number of tracks."""
        return len(TRACKS)


# Singleton configuration
_config: Optional[ControllerConfig] = None


def get_config() -> ControllerConfig:
    """Get the controller configuration singleton."""
    global _config
    if _config is None:
        _config = ControllerConfig()
    return _config


def reset_config() -> None:
    """Reset configuration singleton (for testing)."""
    global _config
    _config = None
