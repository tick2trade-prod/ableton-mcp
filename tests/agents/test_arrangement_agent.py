"""Tests for ArrangementAgent - Clip and scene management in session view.

Reference: Ableton Manual Section 13.8 "Clip Launch Settings" (page 340)


Reference: Ableton Manual Section 16.1 "The Launch Controls" (page 340)

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

from scripts.dearpygui_controller.agents.arrangement_agent import ArrangementAgent


class TestArrangementAgentClipLaunchSettings:
    """Test clip launch settings configuration.

    Reference: Ableton Manual Section 16.1 "The Launch Controls" (page 340)
    """

    def test_configure_clip_launch_mode_trigger(self, mock_mcp_client):
        """Test configuring clip launch mode to Trigger.

        Reference: Page 340 - Trigger mode launches clip and continues playing

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = ArrangementAgent()
        agent._mcp_client = mock_mcp_client
        track_index = 0
        clip_index = 0
        launch_mode = "trigger"

        # Act
        result = agent.configure_clip_launch_settings(
            track_index=track_index, clip_index=clip_index, launch_mode=launch_mode
        )

        # Assert
        assert result.success is True
        assert "launch mode" in result.message.lower()
        mock_mcp_client.set_clip_launch_mode.assert_called_once_with(
            track_index=track_index, clip_index=clip_index, mode=launch_mode
        )

    def test_configure_clip_launch_mode_gate(self, mock_mcp_client):
        """Test configuring clip launch mode to Gate.

        Reference: Page 340 - Gate mode plays while button held

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = ArrangementAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.configure_clip_launch_settings(
            track_index=1, clip_index=0, launch_mode="gate"
        )

        # Assert
        assert result.success is True
        mock_mcp_client.set_clip_launch_mode.assert_called_once()

    def test_configure_clip_launch_quantization(self, mock_mcp_client):
        """Test configuring clip launch quantization.

        Reference: Page 340 - Quantization determines when clip starts

        🔴 RED: This test should fail - quantization parameter doesn't exist yet
        """
        # Arrange
        agent = ArrangementAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.configure_clip_launch_settings(
            track_index=0, clip_index=0, launch_mode="trigger", quantization="1 Bar"
        )

        # Assert
        assert result.success is True
        mock_mcp_client.set_clip_quantization.assert_called_once_with(
            track_index=0, clip_index=0, quantization="1 Bar"
        )

    def test_configure_follow_action(self, mock_mcp_client):
        """Test configuring clip follow actions.

        Reference: Page 340 - Follow actions determine what happens after clip plays

        🔴 RED: This test should fail - follow action parameter doesn't exist yet
        """
        # Arrange
        agent = ArrangementAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.configure_clip_launch_settings(
            track_index=0,
            clip_index=0,
            launch_mode="trigger",
            follow_action_a="Next",
            follow_action_time=4.0,  # 4 bars
        )

        # Assert
        assert result.success is True
        mock_mcp_client.set_follow_action.assert_called_once()

    def test_configure_clip_launch_settings_invalid_mode(self, mock_mcp_client):
        """Test error handling for invalid launch mode.

        🔴 RED: This test should fail - validation doesn't exist yet
        """
        # Arrange
        agent = ArrangementAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.configure_clip_launch_settings(
            track_index=0, clip_index=0, launch_mode="invalid_mode"
        )

        # Assert
        assert result.success is False
        assert "invalid" in result.message.lower() or "mode" in result.message.lower()

    def test_configure_clip_launch_settings_no_mcp_client(self, mock_agent_logger):
        """Test graceful handling when MCP client is not available.

        🔴 RED: This test should fail - mock mode doesn't exist yet
        """
        # Arrange
        agent = ArrangementAgent()
        # Mock get_mcp_client to return None
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.configure_clip_launch_settings(
            track_index=0, clip_index=0, launch_mode="trigger"
        )

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


class TestArrangementAgentSceneManagement:
    """Test scene management functionality.

    Reference: Ableton Manual Section 7.4.3 "Editing Scenes" (page 176)
    """

    def test_configure_scene_launch(self, mock_mcp_client):
        """Test configuring scene launch behavior.

        Reference: Page 176 - Scene launch behavior configuration

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = ArrangementAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_scene_launch_mode = Mock(return_value=Mock(success=True))

        # Act
        result = agent.configure_scene_launch(scene_index=0, launch_mode="immediate")

        # Assert
        assert result.success is True
        mock_mcp_client.set_scene_launch_mode.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
