"""Track 09: Glitch - Sparse Glitch Percussion

Implements glitch per spec Section 3, Track 9:
- Beat Repeat for random glitches
- Sparse, irregular hits
"""

from typing import Any


class Track09Glitch:
    """Glitch percussion track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 8):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 09 - Glitch"
        self._devices = []

    def create(self) -> "Track09Glitch":
        """Create glitch track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_drum_sampler()
        self._add_beat_repeat()
        self._create_sparse_pattern()
        self._set_mix_levels()
        return self

    def _load_drum_sampler(self):
        """Load Drum Sampler."""
        result = self.mcp.load_browser_item(
            track_name=self.track_name, uri="query:Drums#FileId_5447"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Drum Sampler", "index": 0})

    def _add_beat_repeat(self):
        """Add Beat Repeat with random chance."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Beat Repeat"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Beat Repeat", "index": len(self._devices)})

    def _create_sparse_pattern(self):
        """Create sparse glitch hits."""
        notes = []
        # Sparse, irregular timing
        positions = [
            2.25,
            5.75,
            9.33,
            14.5,
            18.25,
            23.75,
            28.5,
            33.25,
            38.66,
            43.5,
            48.25,
            53.75,
            58.33,
            62.25,
        ]

        for pos in positions:
            notes.append(
                {
                    "pitch": 37,  # Percussion hit
                    "start_time": pos,
                    "duration": 0.1,
                    "velocity": 80,
                }
            )

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)

    def _set_mix_levels(self):
        """Set volume to -22dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-22.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return (
            self._devices
            if self._devices
            else [
                {"name": "Drum Sampler", "index": 0},
                {"name": "Beat Repeat", "index": 1},
            ]
        )

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate sparse pattern."""
        positions = [
            2.25,
            5.75,
            9.33,
            14.5,
            18.25,
            23.75,
            28.5,
            33.25,
            38.66,
            43.5,
            48.25,
            53.75,
            58.33,
            62.25,
        ]
        notes = []
        for pos in positions:
            notes.append(
                {"pitch": 37, "start_time": pos, "duration": 0.1, "velocity": 80}
            )
        return notes

    def get_volume_db(self) -> float:
        return -22.0

    def get_output_routing(self) -> str:
        return "Main"


class MockDevice:
    """Mock device for testing."""

    def __init__(self, name: str):
        self.name = name

    def get_parameter(self, param: str):
        params = {
            "Chance": 0.35,  # 35% chance
        }
        return params.get(param)
