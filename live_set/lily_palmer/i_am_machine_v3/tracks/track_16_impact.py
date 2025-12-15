"""Track 16: Impact - Downbeat Hit."""

from typing import Any


class Track16Impact:
    """Impact track."""

    def __init__(self, mcp_client: Any, track_index: int = 15):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 16 - Impact"
        self._devices = []

    def create(self) -> "Track16Impact":
        self.mcp.create_midi_track(self.track_name)
        self._devices = [
            {"name": "Simpler", "index": 0},
            {"name": "Reverb", "index": 1},
        ]
        return self

    def get_effects_chain(self) -> list:
        return self._devices or [
            {"name": "Simpler", "index": 0},
            {"name": "Reverb", "index": 1},
        ]

    def get_sample_name(self) -> str:
        return "Impact Hit.aif"

    def get_midi_notes(self, clip_index: int = 0) -> list:
        return [{"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 127}]

    def get_volume_db(self) -> float:
        return -12.0

    def get_output_routing(self) -> str:
        return "Main"
