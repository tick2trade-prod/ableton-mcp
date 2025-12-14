"""Tests for AutomationAgent - Parameter automation and envelopes.

Reference: Ableton Manual Section 4.6 "Working with Automation" (page 116)


Reference: Ableton Manual Section 40.5.1 "Navigating Breakpoints" (page 927)
Reference: Ableton Manual Section 6.1 "Arrangement View" (page 145)

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

from scripts.dearpygui_controller.agents.automation_agent import AutomationAgent


class TestAutomationAgentEnvelopes:
    """Test automation envelope creation.

    Reference: Ableton Manual Section 40.5.1 "Navigating Breakpoints" (page 927)
    """

    def test_create_filter_sweep(self, mock_mcp_client):
        """Test filter cutoff sweep automation.

        Reference: Page 927 - Breakpoint automation envelopes

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = AutomationAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.create_automation = Mock(return_value=Mock(success=True))

        # Act
        result = agent.create_filter_sweep(
            track_name="04 - Acid",
            device_index=0,
            start_freq=200,
            end_freq=8000,
            duration_bars=16,
        )

        # Assert
        assert result.success is True
        assert "sweep" in result.message.lower()
        assert result.data["start_freq"] == 200
        assert result.data["end_freq"] == 8000

    def test_create_parameter_automation(self, mock_mcp_client):
        """Test generic parameter automation.

        Reference: Page 927 - Parameter automation

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = AutomationAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.create_automation(
            track_name="02 - Rumble",
            parameter="Roar Drive",
            breakpoints=[(0, 0.3), (8, 0.7), (16, 0.3)],
        )

        # Assert
        assert result.success is True
        assert len(result.data["breakpoints"]) == 3

    def test_create_envelope_curve(self, mock_mcp_client):
        """Test automation with specified curve type.

        Reference: Page 145 - Automation curves

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = AutomationAgent()
        agent._mcp_client = mock_mcp_client

        # Act
        result = agent.create_automation(
            track_name="15 - Riser",
            parameter="Cutoff",
            breakpoints=[(0, 0.0), (16, 1.0)],
            curve="exponential",
        )

        # Assert
        assert result.success is True
        assert result.data["curve"] == "exponential"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
