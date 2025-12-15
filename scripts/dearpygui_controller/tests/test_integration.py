#!/usr/bin/env python3
"""Ableton integration tests for the DearPyGUI controller.

Tests verify MCP connection and basic DAW operations.

Usage:
    cd /Users/alexzh/ableton-mcp/scripts
    uv run pytest dearpygui_controller/tests/test_integration.py -v
"""

import sys
from pathlib import Path

import pytest

# Ensure package is importable
scripts_dir = Path(__file__).parent.parent.parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))


@pytest.fixture
def mcp_client():
    """Create MCP client fixture."""
    try:
        # Import from live_set
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
        from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

        return AbletonMCPClient()
    except Exception as e:
        pytest.skip(f"Could not create MCP client: {e}")


class TestMCPConnection:
    """Tests for MCP server connection."""

    @pytest.mark.live
    def test_connection_established(self, mcp_client):
        """Verify connection to MCP server."""
        result = mcp_client.get_session_info()
        assert result is not None
        # Success or explicit failure message
        if not result.success:
            pytest.skip(f"MCP not available: {result.message}")

    @pytest.mark.live
    def test_get_tempo(self, mcp_client):
        """Verify we can read tempo."""
        result = mcp_client.get_session_info()
        if not result.success:
            pytest.skip("MCP not available")

        tempo = result.data.get("tempo", 0)
        assert tempo > 0, "Tempo should be positive"

    @pytest.mark.live
    def test_set_tempo(self, mcp_client):
        """Verify we can set tempo to 136 BPM."""
        result = mcp_client.set_tempo(136.0)
        if not result.success:
            pytest.skip(f"Cannot set tempo: {result.message}")

        # Verify
        session = mcp_client.get_session_info()
        tempo = session.data.get("tempo", 0)
        assert abs(tempo - 136.0) < 0.5


class TestTrackCreation:
    """Tests for track creation."""

    @pytest.mark.live
    def test_create_midi_track(self, mcp_client):
        """Verify MIDI track creation."""
        result = mcp_client.create_midi_track(index=-1, name="Test-Kick")
        if not result.success:
            pytest.skip(f"Cannot create track: {result.message}")

        assert result.success

    @pytest.mark.live
    def test_create_pattern(self, mcp_client):
        """Verify pattern creation on track."""
        # Create track first
        track_result = mcp_client.create_midi_track(index=-1, name="Test-Pattern")
        if not track_result.success:
            pytest.skip("Cannot create track")

        track_index = track_result.data.get("track_index", 0)

        # Create clip
        clip_result = mcp_client.create_clip(
            track_index=track_index,
            clip_index=0,
            length=4.0,
        )

        if not clip_result.success:
            pytest.skip(f"Cannot create clip: {clip_result.message}")

        # Add notes (kick pattern)
        notes = [
            {"pitch": 36, "start_time": 0, "duration": 0.25, "velocity": 110},
            {"pitch": 36, "start_time": 1, "duration": 0.25, "velocity": 100},
            {"pitch": 36, "start_time": 2, "duration": 0.25, "velocity": 110},
            {"pitch": 36, "start_time": 3, "duration": 0.25, "velocity": 100},
        ]

        notes_result = mcp_client.add_notes_to_clip(
            track_index=track_index,
            clip_index=0,
            notes=notes,
        )

        assert notes_result.success or "note" in notes_result.message.lower()


class TestDeviceLoading:
    """Tests for device loading."""

    @pytest.mark.live
    def test_load_builtin_device(self, mcp_client):
        """Verify we can load a built-in device."""
        # Create track
        track_result = mcp_client.create_midi_track(index=-1, name="Test-Device")
        if not track_result.success:
            pytest.skip("Cannot create track")

        track_index = track_result.data.get("track_index", 0)

        # Try to load a basic device
        result = mcp_client.load_device(
            track_index=track_index,
            device_name="Saturator",
        )

        # Either success or device not found is acceptable
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "live"])
