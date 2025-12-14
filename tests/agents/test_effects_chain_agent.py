"""Tests for EffectsChainAgent - Audio effects and rack configuration.

Reference: Ableton Manual Section 18.1 "Audio Effect Racks" (page 445)


Reference: Ableton Manual Section 24.4 "Chain List" (page 445)
Reference: Ableton Manual Section 17.5.2 "Making Use of Internal Routing" (page 363)

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

from scripts.dearpygui_controller.agents.effects_chain_agent import (
    EffectsChainAgent,
)


class TestEffectsChainAgentRackRouting:
    """Test effect rack creation and chain routing.

    Reference: Ableton Manual Section 24.4 "Chain List" (page 445)
    """

    def test_create_effect_rack_basic(self, mock_mcp_client):
        """Test creating a basic effect rack.

        Reference: Page 445 - Chain List represents branching point for signals

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = EffectsChainAgent()
        agent._mcp_client = mock_mcp_client
        track_index = 0
        rack_name = "Parallel Compression"

        # Act
        result = agent.create_effect_rack(track_index=track_index, rack_name=rack_name)

        # Assert
        assert result.success is True
        assert "rack" in result.message.lower()
        mock_mcp_client.create_effect_rack.assert_called_once_with(
            track_index=track_index, name=rack_name
        )

    def test_add_parallel_chains(self, mock_mcp_client):
        """Test adding parallel chains to effect rack.

        Reference: Page 445 - Signals branch at Chain List

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = EffectsChainAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.add_chain_to_rack = Mock(return_value=Mock(success=True))

        # Act
        result = agent.create_effect_rack(
            track_index=0, rack_name="Multi-FX", num_chains=3
        )

        # Assert
        assert result.success is True
        # Should create rack + add 3 chains
        assert mock_mcp_client.add_chain_to_rack.call_count == 3

    def test_configure_chain_selector_zones(self, mock_mcp_client):
        """Test configuring chain selector zones.

        Reference: Page 445 - Chain selector determines which chains play

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = EffectsChainAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_chain_selector_zone = Mock(return_value=Mock(success=True))

        # Act
        result = agent.configure_chain_selector(
            track_index=0, rack_index=0, chain_index=0, zone_min=0, zone_max=42
        )

        # Assert
        assert result.success is True
        mock_mcp_client.set_chain_selector_zone.assert_called_once()

    def test_map_macro_controls(self, mock_mcp_client):
        """Test mapping parameters to macro controls.

        Reference: Page 457 - Macro Control Variations

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = EffectsChainAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.map_to_macro = Mock(return_value=Mock(success=True))

        # Act
        result = agent.map_macro_control(
            track_index=0,
            rack_index=0,
            macro_index=0,
            device_index=1,
            parameter_name="Frequency",
        )

        # Assert
        assert result.success is True
        mock_mcp_client.map_to_macro.assert_called_once()

    def test_create_effect_rack_no_mcp_client(self):
        """Test graceful handling when MCP client not available.

        🔴 RED: This test should fail - mock mode doesn't exist yet
        """
        # Arrange
        agent = EffectsChainAgent()
        agent.get_mcp_client = Mock(return_value=None)

        # Act
        result = agent.create_effect_rack(track_index=0, rack_name="Test Rack")

        # Assert
        assert result.success is True
        assert "mock" in result.message.lower()


class TestEffectsChainAgentSignalRouting:
    """Test internal routing within racks.

    Reference: Ableton Manual Section 17.5.2 "Making Use of Internal Routing" (page 363)
    """

    def test_configure_chain_routing(self, mock_mcp_client):
        """Test configuring chain routing points.

        Reference: Page 363 - Pre FX, Post FX, Post Mixer routing points

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = EffectsChainAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.set_chain_routing = Mock(return_value=Mock(success=True))

        # Act
        result = agent.configure_chain_routing(
            track_index=0, rack_index=0, chain_index=0, routing_point="Post FX"
        )

        # Assert
        assert result.success is True
        mock_mcp_client.set_chain_routing.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
