"""Tests for ArrangerAgent - Arrangement view and automation.

Reference: Ableton Manual Section 4.7 "Editing Breakpoint Envelopes" (page 122)

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

from scripts.dearpygui_controller.agents.arranger_agent import ArrangerAgent


class TestArrangerAgentAutomation:
    """Test automation breakpoint configuration."""

    def test_configure_automation_breakpoints(self, mock_mcp_client):
        """Test automation breakpoint creation."""
        agent = ArrangerAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.add_automation_point = Mock(return_value=Mock(success=True))

        result = agent.configure_automation_breakpoints(
            track_index=0,
            parameter_name="Volume",
            breakpoints=[(0, 0.5), (4, 1.0), (8, 0.5)],
        )

        assert result.success is True
        assert "automation" in result.message.lower()

    def test_configure_automation_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        agent = ArrangerAgent()
        agent.get_mcp_client = Mock(return_value=None)

        result = agent.configure_automation_breakpoints(
            track_index=0, parameter_name="Volume", breakpoints=[(0, 0.5)]
        )

        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
