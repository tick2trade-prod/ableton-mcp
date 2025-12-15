"""Tests for TransitionAgent - Crossfades and transition effects.

Reference: Ableton Manual Section 20.4.2 "Fade and Crossfade Editing" (page 396)

TDD Workflow:
- 🔴 RED: Write failing test
- 🟢 GREEN: Implement minimum code to pass
- 🔄 REFACTOR: Clean up with tests as safety net
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from unittest.mock import Mock

import pytest

from scripts.dearpygui_controller.agents.transition_agent import TransitionAgent


class TestTransitionAgentFades:
    """Test fade curve configuration."""

    def test_configure_fade_curve(self, mock_mcp_client):
        """Test fade curve configuration."""
        agent = TransitionAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_clip_fade = Mock(
            return_value=Mock(success=True, message="Fade configured")
        )

        result = agent.configure_fade_curve(
            track_index=0,
            clip_index=0,
            fade_in=0.5,
            fade_out=1.0,
            curve_type="exponential",
        )

        assert result.success is True
        assert "fade" in result.message.lower()

    def test_configure_fade_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        agent = TransitionAgent()
        agent.get_mcp_client = Mock(return_value=None)

        result = agent.configure_fade_curve(track_index=0, clip_index=0, fade_in=0.5)

        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
