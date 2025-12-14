"""Tests for ComposerAgent - MIDI patterns and note composition.

Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)

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

from scripts.dearpygui_controller.agents.composer_agent import ComposerAgent


class TestComposerAgentGroove:
    """Test groove and quantization configuration.

    Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)
    """

    def test_apply_groove_basic(self, mock_mcp_client):
        """Test basic groove application.

        Reference: Page 326 - Groove Pool timing and velocity

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = ComposerAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_clip_groove = Mock(
            return_value=Mock(success=True, message="Groove applied")
        )

        # Act
        result = agent.apply_groove(
            track_index=0, clip_index=0, groove_name="MPC-60", groove_amount=0.5
        )

        # Assert
        assert result.success is True
        assert "groove" in result.message.lower()

    def test_apply_groove_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        # Arrange
        agent = ComposerAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.apply_groove(track_index=0, clip_index=0, groove_name="MPC-60")

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
