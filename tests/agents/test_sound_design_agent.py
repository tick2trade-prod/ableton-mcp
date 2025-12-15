"""Tests for SoundDesignAgent - Sound design and synthesis.

Reference: Ableton Manual Section 28.3 "Auto Filter" (page 511)

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

from scripts.dearpygui_controller.agents.sound_design_agent import SoundDesignAgent


class TestSoundDesignAgentFilter:
    """Test filter configuration."""

    def test_configure_auto_filter(self, mock_mcp_client):
        """Test Auto Filter configuration."""
        agent = SoundDesignAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_device_parameter = Mock(
            return_value=Mock(success=True, message="Parameter set")
        )

        result = agent.configure_auto_filter(
            track_index=0, filter_type="lowpass", cutoff_frequency=1000, resonance=0.5
        )

        assert result.success is True
        assert "filter" in result.message.lower()

    def test_configure_auto_filter_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        agent = SoundDesignAgent()
        agent.get_mcp_client = Mock(return_value=None)

        result = agent.configure_auto_filter(
            track_index=0, filter_type="lowpass", cutoff_frequency=1000
        )

        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
