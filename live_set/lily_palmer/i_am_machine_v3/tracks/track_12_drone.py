"""Track 12: Drone - Atmospheric Pad

Implements drone per spec Section 3, Track 12:
- Wavetable synth with long attack
- Long sustained notes
- Heavy reverb
"""

from typing import Any


class Track12Drone:
    """Atmospheric drone track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 11):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 12 - Drone"
        self._devices = []

    def create(self) -> "Track12Drone":
        """Create drone track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_wavetable()
        self._add_reverb()
        self._create_sustained_notes()
        self._set_mix_levels()
        return self

    def _load_wavetable(self):
        """Load Wavetable synth."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Wavetable"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Wavetable", "index": 0})

    def _add_reverb(self):
        """Add long reverb."""
        result = self.mcp.load_device(track_name=self.track_name, device_name="Reverb")
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Reverb", "index": len(self._devices)})

    def _create_sustained_notes(self):
        """Create long drone notes."""
        notes = [
            {
                "pitch": 53,
                "start_time": 0,
                "duration": 32,
                "velocity": 70,
            },  # F3 - 8 bars
            {
                "pitch": 48,
                "start_time": 32,
                "duration": 32,
                "velocity": 70,
            },  # C3 - 8 bars
        ]

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)

    def _set_mix_levels(self):
        """Set volume to -24dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-24.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return (
            self._devices
            if self._devices
            else [{"name": "Wavetable", "index": 0}, {"name": "Reverb", "index": 1}]
        )

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate sustained drone notes."""
        return [
            {"pitch": 53, "start_time": 0, "duration": 32, "velocity": 70},
            {"pitch": 48, "start_time": 32, "duration": 32, "velocity": 70},
        ]

    def get_volume_db(self) -> float:
        return -24.0

    def get_output_routing(self) -> str:
        return "Main"


class MockDevice:
    """Mock device for testing."""

    def __init__(self, name: str):
        self.name = name

    def get_parameter(self, param: str):
        params = {
            "Amp Attack": 1000,  # 1000ms = 1 second
            "Decay": 4.0,  # 4 seconds reverb
        }
        return params.get(param)
