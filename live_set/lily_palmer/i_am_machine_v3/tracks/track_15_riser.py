"""Track 15: Riser - Building Sweep."""

from typing import Any


class Track15Riser:
    """Riser track."""

    def __init__(self, mcp_client: Any, track_index: int = 14):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 15 - Riser"
        self._devices = []

    def create(self) -> "Track15Riser":
        self.mcp.create_midi_track(self.track_name)
        self._devices = [
            {"name": "Wavetable", "index": 0},
            {"name": "Auto Filter", "index": 1},
        ]
        return self

    def get_effects_chain(self) -> list:
        return self._devices or [
            {"name": "Wavetable", "index": 0},
            {"name": "Auto Filter", "index": 1},
        ]

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        return [{"pitch": 53, "start_time": 48, "duration": 16, "velocity": 100}]

    def get_volume_db(self) -> float:
        return -15.0

    def get_output_routing(self) -> str:
        return "Main"


class MockDevice:
    def __init__(self, name: str):
        self.name = name

    def get_parameter(self, param: str):
        return {"Osc 2 Wave": "Noise", "LFO Amount": 0.8}.get(param)
