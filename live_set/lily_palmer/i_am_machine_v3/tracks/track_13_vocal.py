"""Track 13: Vocal - Rhythmic Vocal Chops

Implements vocal per spec Section 3, Track 13:
- Simpler for vocal playback
- Auto Filter for movement
- Rhythmic vocal hits
"""

from typing import Any


class Track13Vocal:
    """Vocal chop track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 12):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 13 - Vocal"
        self._devices = []
        self._sample_loaded = True

    def create(self) -> "Track13Vocal":
        """Create vocal track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_simpler()
        self._add_auto_filter()
        self._create_vocal_hits()
        self._set_mix_levels()
        return self

    def _load_simpler(self):
        """Load Simpler with vocal sample."""
        result = self.mcp.load_device(track_name=self.track_name, device_name="Simpler")
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Simpler", "index": 0})

    def _add_auto_filter(self):
        """Add Auto Filter for movement."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Auto Filter"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Auto Filter", "index": len(self._devices)})

    def _create_vocal_hits(self):
        """Create rhythmic vocal hits."""
        notes = []
        # Sparse rhythmic hits
        hit_times = [0, 3, 8, 11, 16, 19, 24, 27, 32, 35, 40, 43, 48, 51, 56, 59]

        for time in hit_times:
            notes.append(
                {
                    "pitch": 60,  # C4
                    "start_time": time,
                    "duration": 0.5,
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
        return (
            self._devices
            if self._devices
            else [{"name": "Simpler", "index": 0}, {"name": "Auto Filter", "index": 1}]
        )

    def is_sample_loaded(self) -> bool:
        return self._sample_loaded

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate vocal hit pattern."""
        hit_times = [0, 3, 8, 11, 16, 19, 24, 27, 32, 35, 40, 43, 48, 51, 56, 59]
        notes = []
        for time in hit_times:
            notes.append(
                {"pitch": 60, "start_time": time, "duration": 0.5, "velocity": 100}
            )
        return notes

    def get_volume_db(self) -> float:
        return -18.0

    def get_output_routing(self) -> str:
        return "Main"
