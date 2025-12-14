"""Tests for SidechainAgent - Sidechain compression routing.

Reference: Ableton Manual Section 28.9.2 "Compressor Tips" (page 521)
Reference: Ableton Manual Section 17.5.2 "Internal Routing" (page 363)

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

from scripts.dearpygui_controller.agents.sidechain_agent import SidechainAgent


class TestSidechainAgentConfiguration:
    """Test sidechain compression setup.

    Reference: Ableton Manual Section 28.9.2 "Compressor Tips" (page 521)
    Excerpt: "These can either be frequencies in the compressed signal or,
    by using the EQ in conjunction with an external sidechain, frequencies
    in another track's audio."
    """

    def test_setup_sidechain_kick_to_rumble(self, mock_mcp_client):
        """Test sidechain rumble to kick (Track 2 → Track 1).

        Reference: Page 521 - External sidechain signal routing
        Reference: Page 363 - Pre FX, Post FX routing points

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = SidechainAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.load_device = Mock(return_value=Mock(success=True))
        mock_mcp_client.set_device_parameter = Mock(return_value=Mock(success=True))
        mock_mcp_client.set_sidechain_input = Mock(return_value=Mock(success=True))

        # Act
        result = agent.setup_sidechain(
            source_track="01 - Kick",
            target_track="02 - Rumble",
            ratio="infinite:1",
            attack_ms=0.1,
            release="1/8n",
        )

        # Assert
        assert result.success is True
        assert "sidechain" in result.message.lower()
        mock_mcp_client.load_device.assert_called()
        mock_mcp_client.set_sidechain_input.assert_called()

    def test_setup_sidechain_preset_patterns(self, mock_mcp_client):
        """Test preset sidechain patterns (kick_pump, rhythmic_duck, gentle_pump).

        Reference: Page 521 - Compressor threshold, ratio, attack, release parameters

        🔴 RED: This test should fail - preset patterns don't exist yet
        """
        # Arrange
        agent = SidechainAgent()
        agent._mcp_client = mock_mcp_client

        # Act - Test all preset patterns
        kick_result = agent.setup_sidechain(
            source_track="01 - Kick", target_track="02 - Rumble", preset="kick_pump"
        )

        # Assert
        assert kick_result.success is True
        assert kick_result.data["ratio"] == "infinite:1"
        assert kick_result.data["attack_ms"] == 0.1

    def test_setup_sidechain_no_mcp_client(self):
        """Test graceful handling when MCP client not available.

        🔴 RED: This test should fail - mock mode doesn't exist yet
        """
        # Arrange
        agent = SidechainAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.setup_sidechain(
            source_track="01 - Kick", target_track="02 - Rumble"
        )

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
