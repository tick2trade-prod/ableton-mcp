"""Tests for BrowserAgent - Sample and preset browser integration.

Reference: Ableton Manual Section 5.3 "Searching and Filtering" (page 120)
Reference: Ableton Manual Section 5.4 "Hot-Swap Mode" (page 123)

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

from scripts.dearpygui_controller.agents.browser_agent import BrowserAgent


class TestBrowserAgentSearch:
    """Test browser search functionality.

    Reference: Ableton Manual Section 5.3 "Searching and Filtering" (page 120)
    """

    def test_search_samples(self, mock_mcp_client):
        """Test sample search using Sound Similarity.

        Reference: Page 120 - Sound Similarity search

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = BrowserAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.search_browser = Mock(
            return_value=Mock(success=True, data={"results": ["kick.wav"]})
        )

        # Act
        result = agent.search_samples(
            query="909 kick",
            category="Drums",
            tags=["kick", "909"],
        )

        # Assert
        assert result.success is True
        assert "results" in result.data

    def test_load_preset_by_similarity(self, mock_mcp_client):
        """Test loading preset using Sound Similarity.

        Reference: Page 120 - Sound Similarity for presets

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # Arrange
        agent = BrowserAgent()
        agent._mcp_client = mock_mcp_client
        mock_mcp_client.search_similar_presets = Mock(
            return_value=Mock(
                success=True,
                data={"results": [{"name": "Similar Bass", "similarity": 0.85}]},
            )
        )
        mock_mcp_client.load_preset = Mock(return_value=Mock(success=True))

        # Act
        result = agent.load_similar_preset(
            track_name="03 - FM Bass",
            reference_preset="Dark Bass",
            device="Operator",
        )

        # Assert
        assert result.success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
