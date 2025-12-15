"""Tests for ReturnTrackAgent - Return track and send management.

Reference: Ableton Manual Section 17.5 "Return Tracks" (page 357)


Reference: Ableton Manual Section 18.4 "Return Tracks" (page 381)
Reference: Ableton Manual Section 18.1 "The Live Mixer - Sends" (page 376)

TDD Workflow:
- 🔴 RED: Write failing test
- 🟢 GREEN: Implement minimum code to pass
- 🔄 REFACTOR: Clean up with tests as safety net
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from unittest.mock import Mock

import pytest

from scripts.dearpygui_controller.agents.return_track_agent import (
    ReturnTrackAgent,
)


class TestReturnTrackAgentManagement:
    """Test return track creation and management.

    Reference: Ableton Manual Section 18.4 "Return Tracks" (page 381)
    """

    def test_create_reverb_return(self, mock_mcp_client):
        """Test creating reverb return track.

        Reference: Page 381 - Return tracks for spatial effects

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = ReturnTrackAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.create_return_track = Mock(return_value=Mock(success=True))
        mock_mcp_client.load_device = Mock(return_value=Mock(success=True))

        # Act
        result = agent.create_return_track(
            name="Reverb",
            device="Hybrid Reverb",
            preset="Dark Hall",
        )

        # Assert
        assert result.success is True
        assert "reverb" in result.message.lower()
        mock_mcp_client.create_return_track.assert_called()

    def test_set_send_levels(self, mock_mcp_client):
        """Test setting send levels for tracks.

        Reference: Page 376 - Send knobs and routing

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = ReturnTrackAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.set_send_level(
            track_name="07 - Clap",
            return_track="Reverb",
            send_level=0.45,
        )

        # Assert
        assert result.success is True
        assert result.data["send_level"] == 0.45

    def test_automate_send(self, mock_mcp_client):
        """Test automating send levels for transitions.

        Reference: Page 376 - Send automation

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = ReturnTrackAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.automate_send(
            track_name="11 - Stabs",
            return_track="Delay",
            start_value=0.0,
            end_value=0.8,
            duration_bars=8,
        )

        # Assert
        assert result.success is True
        assert result.data["start_value"] == 0.0
        assert result.data["end_value"] == 0.8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
