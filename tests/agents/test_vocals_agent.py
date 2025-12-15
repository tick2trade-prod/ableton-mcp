"""Tests for VocalsAgent - Vocal processing and effects.

Reference: Ableton Manual Section 28.13 "Corpus" (page 530)

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

from scripts.dearpygui_controller.agents.vocals_agent import VocalsAgent


class TestVocalsAgentProcessing:
    """Test vocal processing configuration."""

    def test_configure_vocal_chain(self, mock_mcp_client):
        """Test vocal processing chain configuration."""
        agent = VocalsAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.load_device = Mock(
            return_value=Mock(success=True, message="Device loaded")
        )

        result = agent.configure_vocal_chain(
            track_index=0, eq_enabled=True, compressor_enabled=True, reverb_amount=0.3
        )

        assert result.success is True
        assert "vocal" in result.message.lower()

    def test_configure_vocal_chain_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        agent = VocalsAgent()
        agent.get_mcp_client = Mock(return_value=None)

        result = agent.configure_vocal_chain(track_index=0, eq_enabled=True)

        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
