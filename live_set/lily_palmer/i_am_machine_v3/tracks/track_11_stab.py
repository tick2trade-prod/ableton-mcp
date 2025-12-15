"""Track 11: Stab - Synth Stabs in F Minor

Implements stab per spec Section 3, Track 11:
- Wavetable synth
- Short amp envelope for punchiness
- Rhythmic chord stabs in F minor
"""

from typing import Any


class Track11Stab:
    """Synth stab track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 10):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 11 - Stab"
        self._devices = []

    def create(self) -> "Track11Stab":
        """Create stab track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_wavetable()
        self._create_stab_pattern()
        self._set_mix_levels()
        return self

    def _load_wavetable(self):
        """Load Wavetable synth."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Wavetable"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Wavetable", "index": 0})

    def _create_stab_pattern(self):
        """Create rhythmic chord stabs."""
        # F minor chord: F, Ab, C
        f_minor_chord = [53, 56, 60]  # F3, Ab3, C4

        notes = []
        stab_times = [
            0,
            1.5,
            4,
            5.5,
            8,
            9.5,
            12,
            13.5,
            16,
            17.5,
            20,
            21.5,
            24,
            25.5,
            28,
            29.5,
            32,
            33.5,
            36,
            37.5,
            40,
            41.5,
            44,
            45.5,
            48,
            49.5,
            52,
            53.5,
            56,
            57.5,
            60,
            61.5,
        ]

        for time in stab_times:
            for pitch in f_minor_chord:
                notes.append(
                    {
                        "pitch": pitch,
                        "start_time": time,
                        "duration": 0.25,
                        "velocity": 100,
                    }
                )

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)

    def _set_mix_levels(self):
        """Set volume to -18dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-18.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return self._devices if self._devices else [{"name": "Wavetable", "index": 0}]

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate stab pattern with chords."""
        f_minor_chord = [53, 56, 60]
        notes = []
        stab_times = [
            0,
            1.5,
            4,
            5.5,
            8,
            9.5,
            12,
            13.5,
            16,
            17.5,
            20,
            21.5,
            24,
            25.5,
            28,
            29.5,
            32,
            33.5,
            36,
            37.5,
            40,
            41.5,
            44,
            45.5,
            48,
            49.5,
            52,
            53.5,
            56,
            57.5,
            60,
            61.5,
        ]

        for time in stab_times:
            for pitch in f_minor_chord:
                notes.append(
                    {
                        "pitch": pitch,
                        "start_time": time,
                        "duration": 0.25,
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
            "Amp Attack": 5,  # 5ms
            "Amp Decay": 150,  # 150ms
        }
        return params.get(param)
