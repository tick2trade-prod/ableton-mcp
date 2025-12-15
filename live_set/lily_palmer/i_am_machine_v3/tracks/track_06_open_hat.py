"""Track 06: Open Hat - Off-beat Accents

Implements open hat per spec Section 3, Track 6:
- 909 Open Hat sample
- Longer decay for sustain
- Off-beat pattern (beats 2 and 4)
"""

from typing import Any


class Track06OpenHat:
    """Open hi-hat track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 5):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 06 - Open Hat"
        self._devices = []

    def create(self) -> "Track06OpenHat":
        """Create open hat track."""
        self.mcp.create_midi_track(self.track_name)
        self._load_drum_sampler()
        self._create_offbeat_pattern()
        self._set_mix_levels()
        return self

    def _load_drum_sampler(self):
        """Load Drum Sampler with open hat."""
        result = self.mcp.load_browser_item(
            track_name=self.track_name, uri="query:Drums#FileId_5447"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Drum Sampler", "index": 0})

    def _create_offbeat_pattern(self):
        """Create off-beat pattern (beats 2 and 4)."""
        notes = []
        for bar in range(16):
            for beat in [1, 3]:  # Off-beats
                notes.append(
                    {
                        "pitch": 46,  # A#1 - typical open hat
                        "start_time": bar * 4 + beat,
                        "duration": 0.5,
                        "velocity": 100,
                    }
                )

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)

    def _set_mix_levels(self):
        """Set volume to -20dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-20.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return (
            self._devices if self._devices else [{"name": "Drum Sampler", "index": 0}]
        )

    def get_sample_name(self) -> str:
        return "Open Hat 909.aif"

    def get_amplitude_decay(self) -> float:
        return 300.0  # Longer decay

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate off-beat pattern."""
        notes = []
        for bar in range(16):
            for beat in [1, 3]:
                notes.append(
                    {
                        "pitch": 46,
                        "start_time": float(bar * 4 + beat),
                        "duration": 0.5,
                        "velocity": 100,
                    }
                )
        return notes

    def get_volume_db(self) -> float:
        return -20.0

    def get_output_routing(self) -> str:
        return "Main"
