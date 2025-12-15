"""Tests for SamplerAgent - Sample manipulation and granular synthesis.

Reference: Ableton Manual Section 30.10 "Sampler" (page 701)


Reference: Ableton Manual Section 30.4.2 "Drum Sampler Playback" (page 660)
Reference: Ableton Manual Section 28.31 "Granulator III" (page 579)

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

from scripts.dearpygui_controller.agents.sampler_agent import SamplerAgent


class TestSamplerAgentSliceMode:
    """Test sample slicing functionality.

    Reference: Ableton Manual Section 30.4.2 "Drum Sampler Playback" (page 660)
    """

    def test_load_sample_slice_mode(self, mock_mcp_client):
        """Test loading sample in slice mode for vocal chops.

        Reference: Page 660 - Slice mode playback effects

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = SamplerAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.load_device = Mock(return_value=Mock(success=True))
        mock_mcp_client.load_sample = Mock(return_value=Mock(success=True))
        mock_mcp_client.set_device_parameter = Mock(return_value=Mock(success=True))

        # Act
        result = agent.load_sample(
            track_name="14 - Vocal FX",
            sample_path="/path/to/vocal.wav",
            mode="slice",
            slice_count=32,
        )

        # Assert
        assert result.success is True
        assert "slice" in result.message.lower()
        mock_mcp_client.load_sample.assert_called()

    def test_random_slice_triggering(self, mock_mcp_client):
        """Test random slice triggering for glitch percussion.

        Reference: Page 660 - Playback mode configuration

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = SamplerAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.setup_random_slicing(
            track_name="09 - Glitch",
            slice_count=16,
            randomize=True,
        )

        # Assert
        assert result.success is True
        assert result.data["randomize"] is True

    def test_load_sample_no_mcp_client(self):
        """Test graceful handling when MCP client not available.

        🔴 RED: This test should fail - mock mode doesn't exist yet
        """
        # Arrange
        agent = SamplerAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.load_sample(
            track_name="14 - Vocal FX",
            sample_path="/path/to/vocal.wav",
            mode="slice",
        )

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


class TestSamplerAgentGranular:
    """Test granular synthesis functionality.

    Reference: Ableton Manual Section 28.31 "Granulator III" (page 579)
    """

    def test_setup_granular_synthesis(self, mock_mcp_client):
        """Test granular synthesis setup for vocal FX.

        Reference: Page 579 - Granulator III parameters

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = SamplerAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.load_device = Mock(return_value=Mock(success=True))
        mock_mcp_client.set_device_parameter = Mock(return_value=Mock(success=True))

        # Act
        result = agent.setup_granular(
            track_name="14 - Vocal FX",
            grain_size_ms=50,
            density=0.7,
            randomize_pitch=True,
        )

        # Assert
        assert result.success is True
        assert "granular" in result.message.lower()
        assert result.data["grain_size_ms"] == 50
        assert result.data["density"] == 0.7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
