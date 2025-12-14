"""Tests for MasteringAgent - Mastering chain and final processing.

Reference: Ableton Manual Section 28.26.1 "Dynamics Processing Theory" (page 563)

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

from scripts.dearpygui_controller.agents.mastering_agent import MasteringAgent


class TestMasteringAgentMultiband:
    """Test multiband dynamics configuration.

    Reference: Ableton Manual Section 28.26.1 "Dynamics Processing Theory" (page 563)
    """

    def test_configure_multiband_dynamics(self, mock_mcp_client):
        """Test multiband dynamics configuration.

        Reference: Page 563 - Multiband compression/expansion

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = MasteringAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.configure_multiband_compressor = Mock(
            return_value=Mock(success=True, message="Multiband configured")
        )

        # Act
        result = agent.configure_multiband_dynamics(
            track_index=0, num_bands=3, crossover_low=120, crossover_high=8000
        )

        # Assert
        assert result.success is True
        assert "multiband" in result.message.lower()

    def test_configure_multiband_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        # Arrange
        agent = MasteringAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.configure_multiband_dynamics(track_index=0, num_bands=3)

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
