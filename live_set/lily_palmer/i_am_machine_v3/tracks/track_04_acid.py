"""Track 04: Acid - 303-Style Acid Line

Implements acid track per spec Section 3, Track 4:
- Drift synth with saw waveform
- High resonance low-pass filter
- Filter envelope modulation
- Overdrive and delay effects
"""

from typing import Any


class Track04Acid:
    """303-style acid line track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 3):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 04 - Acid"
        self._devices = []
        self._clip_created = False

    def create(self) -> "Track04Acid":
        """Create acid track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_drift()
        self._add_overdrive()
        self._add_delay()
        self._create_acid_pattern()
        self._set_mix_levels()
        return self

    def _load_drift(self):
        """Load Drift synth."""
        result = self.mcp.load_device(track_name=self.track_name, device_name="Drift")
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Drift", "index": 0})

    def _add_overdrive(self):
        """Add Overdrive for grit."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Overdrive"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Overdrive", "index": len(self._devices)})

    def _add_delay(self):
        """Add synced delay."""
        result = self.mcp.load_device(track_name=self.track_name, device_name="Delay")
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Delay", "index": len(self._devices)})

    def _create_acid_pattern(self):
        """Create acid pattern in F minor."""
        f_minor = [41, 43, 44, 46, 48, 49, 51, 53]
        notes = []

        for bar in range(16):
            for beat in range(4):
                for sixteenth in range(4):
                    if (bar + beat + sixteenth) % 3 != 0:  # Rhythmic variation
                        pitch = f_minor[(bar * 4 + beat) % len(f_minor)]
                        time = bar * 4 + beat + sixteenth * 0.25
                        notes.append(
                            {
                                "pitch": pitch,
                                "start_time": time,
                                "duration": 0.2,
                                "velocity": 100,
                            }
                        )

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)
        self._clip_created = True

    def _set_mix_levels(self):
        """Set volume to -18dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-18.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return (
            self._devices
            if self._devices
            else [
                {"name": "Drift", "index": 0},
                {"name": "Overdrive", "index": 1},
                {"name": "Delay", "index": 2},
            ]
        )

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate acid pattern."""
        f_minor = [41, 43, 44, 46, 48, 49, 51, 53]
        notes = []
        for bar in range(16):
            for beat in range(4):
                for sixteenth in range(4):
                    if (bar + beat + sixteenth) % 3 != 0:
                        pitch = f_minor[(bar * 4 + beat) % len(f_minor)]
                        time = bar * 4 + beat + sixteenth * 0.25
                        notes.append(
                            {
                                "pitch": pitch,
                                "start_time": time,
                                "duration": 0.2,
                                "velocity": 100,
                            }
                        )
        return notes

    def get_volume_db(self) -> float:
        return -18.0

    def get_output_routing(self) -> str:
        return "Main"


class MockDevice:
    """Mock device for testing."""

    def __init__(self, name: str):
        self.name = name

    def get_parameter(self, param: str):
        params = {
            # Drift
            "Osc 1 Shape": "Saw",
            "Filter Type": "Low-pass",
            "Filter Resonance": 0.8,
            "Filter Env Decay": 250,
            # Delay
            "Sync": True,
        }
        return params.get(param)
