"""Tests for ModulationAgent - LFO and modulation configuration.

Reference: Ableton Manual Section 30.13.5 "Modulation Matrix" (page 748)

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

from scripts.dearpygui_controller.agents.modulation_agent import ModulationAgent


class TestModulationAgentLFO:
    """Test LFO and envelope configuration."""

    def test_configure_lfo(self, mock_mcp_client):
        """Test LFO configuration."""
        agent = ModulationAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_lfo_parameter = Mock(
            return_value=Mock(success=True, message="LFO configured")
        )

        result = agent.configure_lfo(track_index=0, lfo_index=0, rate=0.5, shape="Sine")

        assert result.success is True
        assert "lfo" in result.message.lower()

    def test_configure_lfo_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        agent = ModulationAgent()
        agent.get_mcp_client = Mock(return_value=None)

        result = agent.configure_lfo(track_index=0, lfo_index=0, rate=0.5)

        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
