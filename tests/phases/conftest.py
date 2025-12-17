"""Pytest fixtures for phase-based TDD tests.

These fixtures provide:
- Live session connection via MCP
- Track state verification helpers
- Clip and note assertion utilities
"""

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def state_dir(project_root: Path) -> Path:
    """Get state directory path."""
    return project_root / "state" / "tracks"


@pytest.fixture
def load_track_spec(state_dir: Path):
    """Load track specification from state file.

    Usage:
        def test_kick(load_track_spec):
            spec = load_track_spec("kick")
            assert spec["device"] == "Drum Rack"
    """

    def _load(track_name: str) -> dict[str, Any]:
        spec_path = state_dir / f"{track_name}.json"
        if not spec_path.exists():
            pytest.skip(f"Track spec not found: {spec_path}")
        return json.loads(spec_path.read_text())

    return _load


@pytest.fixture
def session():
    """Mock session fixture for testing without live Ableton connection.

    In production, this would connect to Ableton via MCP.
    For unit tests, it returns mock data.
    """

    class MockSession:
        """Mock MCP session for testing."""

        def __init__(self):
            self._tracks: list[dict] = []
            self._return_tracks: list[dict] = []
            self._clips: dict[tuple[int, int], dict] = {}

        def get_tracks(self) -> list[dict]:
            """Get all tracks."""
            return self._tracks

        def get_track_info(self, index: int) -> dict:
            """Get track info by index."""
            if index < len(self._tracks):
                return self._tracks[index]
            return {}

        def get_track_by_name(self, name: str) -> dict | None:
            """Get track by name."""
            for track in self._tracks:
                if track.get("name") == name:
                    return track
            return None

        def get_return_tracks(self) -> list[dict]:
            """Get return tracks."""
            return self._return_tracks

        def get_clip(self, track_index: int, clip_index: int) -> dict | None:
            """Get clip by track and clip index."""
            return self._clips.get((track_index, clip_index))

        # Test setup helpers

        def add_track(self, track: dict) -> None:
            """Add track for testing."""
            self._tracks.append(track)

        def add_return_track(self, track: dict) -> None:
            """Add return track for testing."""
            self._return_tracks.append(track)

        def add_clip(self, track_index: int, clip_index: int, clip: dict) -> None:
            """Add clip for testing."""
            self._clips[(track_index, clip_index)] = clip

    return MockSession()


@pytest.fixture
def live_session():
    """Live session fixture that connects to actual Ableton.

    Requires:
    - Ableton Live running
    - AbletonMCP Remote Script active
    - MCP Server running

    Skip if not available.
    """
    try:
        # TODO: Import actual MCP client when available
        # from libs.ableton_lite import AbletonMCPClient
        # return AbletonMCPClient()
        pytest.skip("Live session not implemented yet")
    except Exception as e:
        pytest.skip(f"Could not connect to Ableton: {e}")


# Markers for test categorization


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "suite: mark test as requiring Ableton Suite")
    config.addinivalue_line(
        "markers", "live: mark test as requiring live Ableton connection"
    )
    config.addinivalue_line("markers", "drums: mark test as drums lane (Lane 1)")
    config.addinivalue_line("markers", "bass: mark test as bass lane (Lane 2)")
    config.addinivalue_line("markers", "synths: mark test as synths lane (Lane 3)")
    config.addinivalue_line("markers", "vocals: mark test as vocals/FX lane (Lane 4)")
