"""Tests for SynthesizerAgent - Synthesizer device configuration.

Reference: Ableton Manual Section 30.13.2 "Oscillators" (page 742)
Reference: Ableton Manual Section 30.10.8 "The Filter/Global Tab" (page 715)

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

from scripts.dearpygui_controller.agents.synthesizer_agent import SynthesizerAgent


class TestSynthesizerAgentWavetable:
    """Test Wavetable synthesizer configuration.

    Reference: Ableton Manual Section 30.13.2 "Oscillators" (page 742)
    """

    def test_configure_wavetable_basic(self, mock_mcp_client):
        """Test basic Wavetable configuration.

        Reference: Page 742 - Wavetable oscillator position and warp

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = SynthesizerAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.configure_wavetable(
            track_index=0, oscillator_position=0.5, warp_mode="Bend"
        )

        # Assert
        assert result.success is True
        assert "wavetable" in result.message.lower()

    def test_configure_wavetable_filter(self, mock_mcp_client):
        """Test Wavetable filter configuration.

        Reference: Page 715 - Filter types and parameters

        🔴 RED: This test should fail - filter parameter doesn't exist yet
        """
        # Arrange
        agent = SynthesizerAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_device_parameter = Mock(return_value=Mock(success=True))

        # Act
        result = agent.configure_wavetable(
            track_index=0,
            filter_type="Lowpass",
            filter_frequency=1000,
            filter_resonance=0.5,
        )

        # Assert
        assert result.success is True
        assert mock_mcp_client.set_device_parameter.call_count >= 3

    def test_configure_wavetable_modulation(self, mock_mcp_client):
        """Test Wavetable modulation matrix.

        Reference: Page 742 - Modulation routing

        🔴 RED: This test should fail - modulation parameter doesn't exist yet
        """
        # Arrange
        agent = SynthesizerAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_modulation_routing = Mock(return_value=Mock(success=True))

        # Act
        result = agent.configure_wavetable(
            track_index=0,
            modulation_source="LFO 1",
            modulation_target="Osc Position",
            modulation_amount=0.7,
        )

        # Assert
        assert result.success is True
        mock_mcp_client.set_modulation_routing.assert_called_once()

    def test_configure_wavetable_no_mcp_client(self):
        """Test graceful handling when MCP client not available.

        🔴 RED: This test should fail - mock mode doesn't exist yet
        """
        # Arrange
        agent = SynthesizerAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.configure_wavetable(track_index=0, oscillator_position=0.5)

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
