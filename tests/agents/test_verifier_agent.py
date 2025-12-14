"""Tests for VerifierAgent - Spectrum and signal analysis.

Reference: Ableton Manual Section 28.51 "Spectrum" (page 620)

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

from scripts.dearpygui_controller.agents.verifier_agent import VerifierAgent


class TestVerifierAgentSpectrum:
    """Test spectrum analysis configuration."""

    def test_configure_spectrum_analyzer(self, mock_mcp_client):
        """Test spectrum analyzer configuration."""
        agent = VerifierAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.load_device = Mock(
            return_value=Mock(success=True, message="Spectrum analyzer configured")
        )

        result = agent.configure_spectrum_analyzer(
            track_index=0, block_size=2048, display_range=(-60, 0)
        )

        assert result.success is True
        assert "spectrum" in result.message.lower()

    def test_configure_spectrum_no_mcp_client(self):
        """Test graceful handling when MCP client not available."""
        agent = VerifierAgent()
        agent.get_mcp_client = Mock(return_value=None)

        result = agent.configure_spectrum_analyzer(track_index=0, block_size=2048)

        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
