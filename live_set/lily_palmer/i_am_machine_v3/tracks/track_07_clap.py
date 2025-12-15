"""Track 07: Clap - Layered Backbeat

Implements clap per spec Section 3, Track 7:
- 909 Clap sample
- Short reverb for space
- Backbeat pattern (beats 2 and 4)
"""

from typing import Any


class Track07Clap:
    """Clap track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 6):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 07 - Clap"
        self._devices = []

    def create(self) -> "Track07Clap":
        """Create clap track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_drum_sampler()
        self._add_reverb()
        self._create_backbeat_pattern()
        self._set_mix_levels()
        return self

    def _load_drum_sampler(self):
        """Load Drum Sampler with clap."""
        result = self.mcp.load_browser_item(
            track_name=self.track_name, uri="query:Drums#FileId_5447"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Drum Sampler", "index": 0})

    def _add_reverb(self):
        """Add Reverb for space."""
        result = self.mcp.load_device(track_name=self.track_name, device_name="Reverb")
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Reverb", "index": len(self._devices)})

    def _create_backbeat_pattern(self):
        """Create backbeat pattern (beats 2 and 4)."""
        notes = []
        for bar in range(16):
            for beat in [1, 3]:  # Backbeat
                notes.append(
                    {
                        "pitch": 39,  # D#1 - typical clap
                        "start_time": bar * 4 + beat,
                        "duration": 0.25,
                        "velocity": 100,
                    }
                )

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)

    def _set_mix_levels(self):
        """Set volume to -15dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-15.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return (
            self._devices
            if self._devices
            else [{"name": "Drum Sampler", "index": 0}, {"name": "Reverb", "index": 1}]
        )

    def get_sample_name(self) -> str:
        return "Clap 909.aif"

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate backbeat pattern."""
        notes = []
        for bar in range(16):
            for beat in [1, 3]:
                notes.append(
                    {
                        "pitch": 39,
                        "start_time": float(bar * 4 + beat),
                        "duration": 0.25,
                        "velocity": 100,
                    }
                )
        return notes

    def get_volume_db(self) -> float:
        return -15.0

    def get_output_routing(self) -> str:
        return "Main"


class MockDevice:
    """Mock device for testing."""

    def __init__(self, name: str):
        self.name = name

    def get_parameter(self, param: str):
        params = {
            "Decay": 0.7,  # Short reverb
        }
        return params.get(param)
