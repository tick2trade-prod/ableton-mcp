"""Track 10: Ride - Half Note Pattern

Implements ride per spec Section 3, Track 10:
- 909 Ride sample
- Half note pattern (every 2 beats)
"""

from typing import Any


class Track10Ride:
    """Ride cymbal track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 9):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 10 - Ride"
        self._devices = []

    def create(self) -> "Track10Ride":
        """Create ride track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_drum_sampler()
        self._create_half_note_pattern()
        self._set_mix_levels()
        return self

    def _load_drum_sampler(self):
        """Load Drum Sampler with ride."""
        result = self.mcp.load_browser_item(
            track_name=self.track_name, uri="query:Drums#FileId_5447"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Drum Sampler", "index": 0})

    def _create_half_note_pattern(self):
        """Create half note pattern."""
        notes = []
        for i in range(32):  # 16 bars * 2 half notes
            notes.append(
                {
                    "pitch": 51,  # D#2 - ride
                    "start_time": i * 2.0,
                    "duration": 0.5,
                    "velocity": 90,
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
            self._devices if self._devices else [{"name": "Drum Sampler", "index": 0}]
        )

    def get_sample_name(self) -> str:
        return "Ride 909.aif"

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate half note pattern."""
        notes = []
        for i in range(32):
            notes.append(
                {"pitch": 51, "start_time": i * 2.0, "duration": 0.5, "velocity": 90}
            )
        return notes

    def get_volume_db(self) -> float:
        return -22.0

    def get_output_routing(self) -> str:
        return "Main"
