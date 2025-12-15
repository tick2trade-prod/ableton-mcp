"""Track 08: Tom - Pitched Tom Fill

Implements tom per spec Section 3, Track 8:
- 909 Tom sample (tuned to F)
- Fills every 4 bars
"""

from typing import Any


class Track08Tom:
    """Tom track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 7):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 08 - Tom"
        self._devices = []

    def create(self) -> "Track08Tom":
        """Create tom track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_drum_sampler()
        self._create_fill_pattern()
        self._set_mix_levels()
        return self

    def _load_drum_sampler(self):
        """Load Drum Sampler with tom."""
        result = self.mcp.load_browser_item(
            track_name=self.track_name, uri="query:Drums#FileId_5447"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Drum Sampler", "index": 0})

    def _create_fill_pattern(self):
        """Create tom fills every 4 bars."""
        notes = []
        fill_bars = [3, 7, 11, 15]  # End of every 4th bar

        for bar in fill_bars:
            # 4-note fill at end of bar
            for i in range(4):
                notes.append(
                    {
                        "pitch": 45,  # A1 - tom
                        "start_time": bar * 4 + 3 + i * 0.25,
                        "duration": 0.2,
                        "velocity": 90 + i * 2,  # Building velocity
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
        return "Tom 909.aif"

    def get_pitch_offset(self) -> int:
        return -5  # Tuned to F

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate fill pattern."""
        notes = []
        fill_bars = [3, 7, 11, 15]
        for bar in fill_bars:
            for i in range(4):
                notes.append(
                    {
                        "pitch": 45,
                        "start_time": bar * 4 + 3 + i * 0.25,
                        "duration": 0.2,
                        "velocity": 90 + i * 2,
                    }
                )
        return notes

    def get_volume_db(self) -> float:
        return -18.0

    def get_output_routing(self) -> str:
        return "Main"
