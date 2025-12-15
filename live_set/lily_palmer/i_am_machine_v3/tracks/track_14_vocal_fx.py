"""Track 14: Vocal FX - Processed Vocal Textures."""

from typing import Any


class Track14VocalFx:
    """Vocal FX track."""

    def __init__(self, mcp_client: Any, track_index: int = 13):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 14 - Vocal FX"
        self._devices = []

    def create(self) -> "Track14VocalFx":
        self.mcp.create_midi_track(self.track_name)
        self._devices = [
            {"name": "Simpler", "index": 0},
            {"name": "Delay", "index": 1},
            {"name": "Reverb", "index": 2},
        ]
        return self

    def get_effects_chain(self) -> list:
        return self._devices or [
            {"name": "Simpler", "index": 0},
            {"name": "Delay", "index": 1},
            {"name": "Reverb", "index": 2},
        ]

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        return [
            {"pitch": 60, "start_time": t, "duration": 1.0, "velocity": 80}
            for t in [8, 24, 40, 56]
        ]

    def get_volume_db(self) -> float:
        return -22.0

    def get_output_routing(self) -> str:
        return "Main"


class MockDevice:
    def __init__(self, name: str):
        self.name = name

    def get_parameter(self, param: str):
        return {"Mix": 0.8}.get(param)
