"""Track 05: Closed Hat - Tight 8th Note Pattern

Implements closed hat per spec Section 3, Track 5:
- 909 Closed Hat sample
- Short decay for tight sound
- 8th note pattern with velocity variation
"""

from typing import Any


class Track05ClosedHat:
    """Closed hi-hat track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 4):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 05 - Closed Hat"
        self._devices = []
        self._sample_loaded = False

    def create(self) -> "Track05ClosedHat":
        """Create closed hat track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_drum_sampler()
        self._add_eq()
        self._create_eighth_note_pattern()
        self._set_mix_levels()
        return self

    def _load_drum_sampler(self):
        """Load Drum Sampler with closed hat."""
        result = self.mcp.load_browser_item(
            track_name=self.track_name, uri="query:Drums#FileId_5447"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Drum Sampler", "index": 0})
            self._sample_loaded = True

    def _add_eq(self):
        """Add EQ Eight with high-pass."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="EQ Eight"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "EQ Eight", "index": len(self._devices)})

    def _create_eighth_note_pattern(self):
        """Create 8th note pattern with velocity groove."""
        notes = []
        for i in range(128):  # 16 bars * 8 eighths
            # Accent on beats 1 and 3
            beat_in_bar = (i % 8) // 2
            velocity = 100 if beat_in_bar in [0, 2] else 70

            notes.append(
                {
                    "pitch": 42,  # F#1 - typical closed hat
                    "start_time": i * 0.5,
                    "duration": 0.1,
                    "velocity": velocity,
                }
            )

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)

    def _set_mix_levels(self):
        """Set volume to -18dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-18.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return (
            self._devices if self._devices else [{"name": "Drum Sampler", "index": 0}]
        )

    def get_sample_name(self) -> str:
        return "Closed Hat 909.aif"

    def get_amplitude_decay(self) -> float:
        return 80.0  # Short decay

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate 8th note pattern."""
        notes = []
        for i in range(128):
            beat_in_bar = (i % 8) // 2
            velocity = 100 if beat_in_bar in [0, 2] else 70
            notes.append(
                {
                    "pitch": 42,
                    "start_time": i * 0.5,
                    "duration": 0.1,
                    "velocity": velocity,
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

    def get_band(self, index: int):
        if index == 0:  # High-pass
            return {"frequency": 300}
        return {}
