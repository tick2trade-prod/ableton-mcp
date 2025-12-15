"""Tests for GrooveAgent - Groove templates and quantization.

Reference: Ableton Manual Section 13.1.4 "Groove Pool" (page 326)


Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)
Reference: Ableton Manual Section 10.5.12 "Editing Velocities" (page 258)

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

from scripts.dearpygui_controller.agents.groove_agent import GrooveAgent


class TestGrooveAgentTemplates:
    """Test groove template application.

    Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)
    """

    def test_apply_swing_16_99(self, mock_mcp_client):
        """Test applying Swing 16-99 groove to hi-hat tracks.

        Reference: Page 326 - Groove Pool and swing settings

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = GrooveAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.apply_groove = Mock(return_value=Mock(success=True))
        mock_mcp_client.set_clip_property = Mock(return_value=Mock(success=True))

        # Act
        result = agent.apply_groove(
            track_name="05 - Closed Hat",
            groove_name="Swing 16-99",
            intensity=0.15,
        )

        # Assert
        assert result.success is True
        assert "swing" in result.message.lower()
        assert result.data["intensity"] == 0.15

    def test_quantize_clip(self, mock_mcp_client):
        """Test clip quantization settings.

        Reference: Page 326 - Quantization controls

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = GrooveAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.quantize_clip(
            track_name="01 - Kick",
            clip_index=0,
            quantize_to="1/16",
            amount=1.0,
        )

        # Assert
        assert result.success is True
        assert result.data["quantize_to"] == "1/16"
        assert result.data["amount"] == 1.0

    def test_humanize_velocities(self, mock_mcp_client):
        """Test velocity humanization.

        Reference: Page 258 - Editing velocities

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = GrooveAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.humanize_velocities(
            track_name="06 - Open Hat",
            clip_index=0,
            random_amount=0.10,
        )

        # Assert
        assert result.success is True
        assert result.data["random_amount"] == 0.10

    def test_apply_groove_no_mcp_client(self):
        """Test graceful handling when MCP client not available.

        🔴 RED: This test should fail - mock mode doesn't exist yet
        """
        # Arrange
        agent = GrooveAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.apply_groove(
            track_name="05 - Closed Hat",
            groove_name="Swing 16-99",
        )

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
