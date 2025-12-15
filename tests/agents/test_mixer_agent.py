"""Tests for MixerAgent - Mixer routing and level management.

Reference: Ableton Manual Section 17.7 "Monitoring" (page 366)

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

from scripts.dearpygui_controller.agents.mixer_agent import MixerAgent


class TestMixerAgentSubmixing:
    """Test track routing and submixing."""

    def test_configure_submix_routing(self, mock_mcp_client):
        """Test submix/group track routing."""
        agent = MixerAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_track_routing = Mock(
            return_value=Mock(success=True, message="Routing set")
        )

        result = agent.configure_submix_routing(
            source_tracks=[0, 1, 2], group_track_index=10
        )

        assert result.success is True
        assert "submix" in result.message.lower() or "routing" in result.message.lower()

    def test_configure_submix_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        agent = MixerAgent()
        agent.get_mcp_client = Mock(return_value=None)

        result = agent.configure_submix_routing(
            source_tracks=[0, 1], group_track_index=10
        )

        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
