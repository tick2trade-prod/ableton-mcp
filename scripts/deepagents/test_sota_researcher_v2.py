#!/usr/bin/env python3
"""Tests for SOTA Researcher v2 using DeepAgents."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Module-level marker (required)
pytestmark = pytest.mark.hotpath

from scripts.deepagents.sota_researcher_v2 import (
    _create_research_agent,
    _get_mcp_tools,
    _get_research_agent,
    _normalize_research_questions,
    _validate_prerequisites,
    _validate_topic,
)


@pytest.fixture
def mock_mcp_client():
    """Create a mock MCP client."""
    client = MagicMock()
    tool1 = MagicMock()
    tool1.name = "SearchDocsByLangChain"
    tool2 = MagicMock()
    tool2.name = "get-library-docs"
    client.get_tools = AsyncMock(return_value=[tool1, tool2])
    return client


@pytest.fixture
def mock_deep_agent():
    """Create a mock deep agent."""
    agent = MagicMock()
    agent.ainvoke = AsyncMock(
        return_value={
            "messages": [
                MagicMock(content="Research findings and plan"),
            ]
        }
    )
    return agent


class TestValidatePrerequisites:
    """Test prerequisite validation."""

    def test_validate_prerequisites_missing_mcp_client(self):
        """Test validation fails when MCP client is missing."""
        with patch("scripts.deepagents.sota_researcher_v2.MCP_CLIENT_AVAILABLE", False):
            is_valid, errors = _validate_prerequisites()
            assert not is_valid
            assert any("langchain_mcp_adapters" in e for e in errors)


class TestGetMCPTools:
    """Test MCP tools retrieval."""

    async def test_get_mcp_tools_success(self, mock_mcp_client):
        """Test successful MCP tools retrieval."""
        with patch(
            "scripts.deepagents.sota_researcher_v2._get_mcp_client",
            return_value=mock_mcp_client,
        ):
            tools = await _get_mcp_tools()
            assert len(tools) == 2
            assert tools[0].name == "SearchDocsByLangChain"
            assert tools[1].name == "get-library-docs"

    async def test_get_mcp_tools_no_client(self):
        """Test error when MCP client is not available."""
        with patch(
            "scripts.deepagents.sota_researcher_v2._get_mcp_client", return_value=None
        ):
            with pytest.raises(RuntimeError, match="MCP client not available"):
                await _get_mcp_tools()

    async def test_get_mcp_tools_no_tools(self, mock_mcp_client):
        """Test error when no tools are available."""
        mock_mcp_client.get_tools = AsyncMock(return_value=[])
        with patch(
            "scripts.deepagents.sota_researcher_v2._get_mcp_client",
            return_value=mock_mcp_client,
        ):
            with pytest.raises(RuntimeError, match="No MCP tools available"):
                await _get_mcp_tools()


class TestCreateResearchAgent:
    """Test research agent creation."""

    async def test_create_research_agent_success(
        self, mock_mcp_client, mock_deep_agent
    ):
        """Test successful agent creation."""
        with (
            patch(
                "scripts.deepagents.sota_researcher_v2._get_mcp_tools",
                return_value=[MagicMock(), MagicMock()],
            ),
            patch(
                "deepagents.create_deep_agent",
                return_value=mock_deep_agent,
            ),
            patch("scripts.deepagents.sota_researcher_v2.REQUIRE_VALIDATION", False),
        ):
            agent = await _create_research_agent()
            assert agent == mock_deep_agent

    async def test_create_research_agent_validation_failure(self):
        """Test agent creation fails when validation fails."""
        with (
            patch(
                "scripts.deepagents.sota_researcher_v2._validate_prerequisites",
                return_value=(False, ["Error 1"]),
            ),
            patch("scripts.deepagents.sota_researcher_v2.REQUIRE_VALIDATION", True),
        ):
            with pytest.raises(RuntimeError, match="prerequisites validation failed"):
                await _create_research_agent()

    async def test_create_research_agent_creation_failure(self, mock_mcp_client):
        """Test agent creation fails when create_deep_agent fails."""
        with (
            patch(
                "scripts.deepagents.sota_researcher_v2._get_mcp_tools",
                return_value=[MagicMock()],
            ),
            patch(
                "deepagents.create_deep_agent",
                side_effect=Exception("Creation failed"),
            ),
            patch("scripts.deepagents.sota_researcher_v2.REQUIRE_VALIDATION", False),
        ):
            with pytest.raises(RuntimeError, match="Failed to create research agent"):
                await _create_research_agent()


class TestResearchAndPlan:
    """Test research_and_plan function."""

    async def test_research_and_plan_basic(self, mock_deep_agent):
        """Test basic research and plan."""
        # Import the implementation function directly
        from scripts.deepagents.sota_researcher_v2 import research_and_plan

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            result = await research_and_plan(topic="Test topic")

            assert result["success"] is True
            assert "research_results" in result
            assert "plan" in result
            assert "latency_ms" in result
            assert result["plan"]["agent_generated"] is True
            mock_deep_agent.ainvoke.assert_called_once()

    async def test_research_and_plan_with_questions(self, mock_deep_agent):
        """Test research and plan with research questions."""
        from scripts.deepagents.sota_researcher_v2 import research_and_plan

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            result = await research_and_plan(
                topic="Test topic", research_questions=["Question 1", "Question 2"]
            )

            assert result["success"] is True
            call_args = mock_deep_agent.ainvoke.call_args[0][0]
            assert "Question 1" in call_args["messages"][0]["content"]
            assert "Question 2" in call_args["messages"][0]["content"]

    async def test_research_and_plan_with_output_path(self, mock_deep_agent):
        """Test research and plan with output path."""
        from scripts.deepagents.sota_researcher_v2 import research_and_plan

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = os.path.join(tmpdir, "research.md")
                result = await research_and_plan(
                    topic="Test topic", output_path=output_path
                )

                assert result["success"] is True
                call_args = mock_deep_agent.ainvoke.call_args[0][0]
                assert output_path in call_args["messages"][0]["content"]

    async def test_research_and_plan_agent_failure(self, mock_deep_agent):
        """Test research and plan when agent invocation fails."""
        from scripts.deepagents.sota_researcher_v2 import research_and_plan

        mock_deep_agent.ainvoke = AsyncMock(side_effect=Exception("Agent error"))
        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            with pytest.raises(RuntimeError, match="Research failed"):
                await research_and_plan(topic="Test topic")


class TestResearchOnly:
    """Test research_only function."""

    async def test_research_only_basic(self, mock_deep_agent):
        """Test basic research only."""
        from scripts.deepagents.sota_researcher_v2 import research_only

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            result = await research_only(topic="Test topic")

            assert result["success"] is True
            assert "results" in result
            assert "latency_ms" in result
            mock_deep_agent.ainvoke.assert_called_once()

    async def test_research_only_with_max_results(self, mock_deep_agent):
        """Test research only with max_results."""
        from scripts.deepagents.sota_researcher_v2 import research_only

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            result = await research_only(topic="Test topic", max_results=5)

            assert result["success"] is True
            call_args = mock_deep_agent.ainvoke.call_args[0][0]
            assert "5" in call_args["messages"][0]["content"]

    async def test_research_only_agent_failure(self, mock_deep_agent):
        """Test research only when agent invocation fails."""
        from scripts.deepagents.sota_researcher_v2 import research_only

        mock_deep_agent.ainvoke = AsyncMock(side_effect=Exception("Agent error"))
        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            with pytest.raises(RuntimeError, match="Research failed"):
                await research_only(topic="Test topic")


class TestTopicValidation:
    """Test topic input validation."""

    def test_validate_topic_empty(self):
        """Test validation fails for empty topic."""
        with pytest.raises(ValueError, match="cannot be empty"):
            _validate_topic("")

    def test_validate_topic_whitespace_only(self):
        """Test validation fails for whitespace-only topic."""
        with pytest.raises(ValueError, match="cannot be empty"):
            _validate_topic("   ")

    def test_validate_topic_too_long(self):
        """Test validation fails for topic that's too long."""
        long_topic = "a" * 1001
        with pytest.raises(ValueError, match="too long"):
            _validate_topic(long_topic)

    def test_validate_topic_valid(self):
        """Test validation passes for valid topics."""
        _validate_topic("Valid topic")
        _validate_topic("Another valid topic with special chars: !@#$%")
        _validate_topic("a" * 1000)  # Exactly at limit


class TestResearchQuestionsNormalization:
    """Test _normalize_research_questions function."""

    def test_normalize_none(self):
        """Test normalization of None input."""
        assert _normalize_research_questions(None) is None

    def test_normalize_empty_string(self):
        """Test normalization of empty string."""
        assert _normalize_research_questions("") is None

    def test_normalize_whitespace_only(self):
        """Test normalization of whitespace-only string."""
        assert _normalize_research_questions("   ") is None

    def test_normalize_list_of_strings(self):
        """Test normalization of list of strings."""
        result = _normalize_research_questions(["Q1", "Q2"])
        assert result == ["Q1", "Q2"]

    def test_normalize_single_string(self):
        """Test normalization of single string."""
        result = _normalize_research_questions("single question")
        assert result == ["single question"]

    def test_normalize_json_array_string(self):
        """Test normalization of JSON array string."""
        result = _normalize_research_questions('["Q1", "Q2"]')
        assert result == ["Q1", "Q2"]

    def test_normalize_empty_list(self):
        """Test normalization of empty list."""
        assert _normalize_research_questions([]) is None

    def test_normalize_list_with_none_values(self):
        """Test normalization of list with None values."""
        result = _normalize_research_questions(["Q1", None, "Q2"])
        assert result == ["Q1", "Q2"]

    def test_normalize_list_with_mixed_types(self):
        """Test normalization of list with mixed types."""
        result = _normalize_research_questions(["Q1", 123, "Q2"])
        assert result == ["Q1", "123", "Q2"]

    def test_normalize_tuple(self):
        """Test normalization of tuple input."""
        result = _normalize_research_questions(("Q1", "Q2"))
        assert result == ["Q1", "Q2"]

    def test_normalize_set(self):
        """Test normalization of set input."""
        result = _normalize_research_questions({"Q1", "Q2"})
        # Set order is not guaranteed
        assert len(result) == 2
        assert "Q1" in result
        assert "Q2" in result

    def test_normalize_dict_with_questions_key(self):
        """Test normalization of dict with 'questions' key."""
        result = _normalize_research_questions({"questions": ["Q1", "Q2"]})
        assert result == ["Q1", "Q2"]


class TestAgentCaching:
    """Test agent caching behavior."""

    async def test_agent_caching(self, mock_mcp_client, mock_deep_agent):
        """Test that agent is cached and reused."""
        import scripts.deepagents.sota_researcher_v2 as sota_module

        # Clear cache before test
        sota_module._research_agent_cache = None

        with (
            patch(
                "scripts.deepagents.sota_researcher_v2._get_mcp_tools",
                return_value=[MagicMock()],
            ),
            patch(
                "deepagents.create_deep_agent",
                return_value=mock_deep_agent,
            ) as mock_create,
            patch("scripts.deepagents.sota_researcher_v2.REQUIRE_VALIDATION", False),
        ):
            # First call should create agent
            agent1 = await _get_research_agent()
            assert agent1 == mock_deep_agent

            # Second call should return cached agent
            agent2 = await _get_research_agent()
            assert agent2 == agent1
            assert agent2 == mock_deep_agent

            # Verify create_deep_agent was only called once
            assert mock_create.call_count == 1


class TestInputValidation:
    """Test input validation in research functions."""

    async def test_research_and_plan_empty_topic(self, mock_deep_agent):
        """Test research_and_plan fails with empty topic."""
        from scripts.deepagents.sota_researcher_v2 import research_and_plan

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            with pytest.raises(ValueError, match="cannot be empty"):
                await research_and_plan(topic="")

    async def test_research_and_plan_too_long_topic(self, mock_deep_agent):
        """Test research_and_plan fails with topic that's too long."""
        from scripts.deepagents.sota_researcher_v2 import research_and_plan

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            long_topic = "a" * 1001
            with pytest.raises(ValueError, match="too long"):
                await research_and_plan(topic=long_topic)

    async def test_research_only_empty_topic(self, mock_deep_agent):
        """Test research_only fails with empty topic."""
        from scripts.deepagents.sota_researcher_v2 import research_only

        with patch(
            "scripts.deepagents.sota_researcher_v2._get_research_agent",
            return_value=mock_deep_agent,
        ):
            with pytest.raises(ValueError, match="cannot be empty"):
                await research_only(topic="")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
