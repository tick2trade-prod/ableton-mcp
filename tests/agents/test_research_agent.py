"""Tests for ResearchAgent - Web research and documentation search.

Reference: Ableton Manual Section 1 "General Documentation" (page 1)


TDD Workflow:
- 🔴 RED: Write failing test
- 🟢 GREEN: Implement minimum code to pass
- 🔄 REFACTOR: Clean up with tests as safety net
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


import pytest

from scripts.dearpygui_controller.agents.research_agent import ResearchAgent


class TestResearchAgent:
    """Test ResearchAgent basic functionality."""

    @pytest.mark.asyncio
    async def test_execute_returns_success(self):
        """Test that execute method returns success result."""
        agent = ResearchAgent()

        result = await agent.execute(topic="Ableton techno production")

        assert result.success is True
        assert "research" in result.message.lower()

    @pytest.mark.asyncio
    async def test_execute_with_empty_topic(self):
        """Test handling of empty research topic."""
        agent = ResearchAgent()

        result = await agent.execute(topic="")

        # Should still succeed (graceful handling)
        assert result.success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
