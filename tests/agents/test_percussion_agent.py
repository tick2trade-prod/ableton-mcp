"""Tests for PercussionAgent - Drum rack and percussion setup.

Reference: Ableton Manual Section 30.5 "Drum Racks" (page 797)


Reference: Ableton Manual Section 34.3.1 "Loop Selector" (page 797)
Reference: Ableton Manual Section 24.4.1 "Drum Rack Basics" (page 446)

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

from scripts.dearpygui_controller.agents.percussion_agent import PercussionAgent


class TestPercussionAgentDrumRack:
    """Test drum rack configuration.

    Reference: Ableton Manual Section 24.4.1 "Drum Rack Basics" (page 446)
    """

    def test_configure_drum_rack_basic(self, mock_mcp_client):
        """Test basic drum rack configuration.

        Reference: Page 446 - Drum Rack 4x4 pad layout

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = PercussionAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.configure_drum_rack(track_index=0, pad_layout="4x4")

        # Assert
        assert result.success is True
        assert "drum rack" in result.message.lower()

    def test_configure_drum_rack_choke_groups(self, mock_mcp_client):
        """Test drum rack choke group configuration.

        Reference: Page 446 - Choke groups for hi-hats

        🔴 RED: This test should fail - choke group parameter doesn't exist yet
        """
        # Arrange
        agent = PercussionAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_pad_choke_group = Mock(return_value=Mock(success=True))

        # Act
        result = agent.configure_drum_rack(
            track_index=0, choke_groups={"closed_hat": [42], "open_hat": [46]}
        )

        # Assert
        assert result.success is True
        mock_mcp_client.set_pad_choke_group.assert_called()

    def test_configure_drum_rack_no_mcp_client(self):
        """Test graceful handling when MCP client not available.

        🔴 RED: This test should fail - mock mode doesn't exist yet
        """
        # Arrange
        agent = PercussionAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.configure_drum_rack(track_index=0, pad_layout="4x4")

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
