#!/usr/bin/env python3
"""Tests for autonomous-code-streaming-refactor-orchestrator-v1 with DeepAgents integration."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest

# Module-level marker (required for production tests)
pytestmark = pytest.mark.hotpath

# Direct import instead of dynamic import
from scripts.deepagents import autonomous_code_streaming_refactor_orchestrator_v1


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client."""
    from langchain_core.tools import BaseTool

    class MockTool(BaseTool):
        name: str = "mock_tool"
        description: str = "Mock tool for testing"

        def _run(self, *args, **kwargs):
            return {"result": "mock"}

        async def _arun(self, *args, **kwargs):
            return {"result": "mock"}

    client = MagicMock()
    tool1 = MockTool(name="hybrid_search")
    tool2 = MockTool(name="structure_aware_search")
    tool3 = MockTool(name="write_todos")
    client.get_tools = AsyncMock(return_value=[tool1, tool2, tool3])
    return client


@pytest.fixture
def mock_deepagent():
    """Mock deepagent."""
    from langchain_core.messages import AIMessage, HumanMessage

    agent = MagicMock()
    # Return proper LangGraph state format
    agent.ainvoke = AsyncMock(
        return_value={
            "messages": [
                HumanMessage(content="test"),
                AIMessage(content="Refactoring analysis completed: Found 5 opportunities..."),
            ]
        }
    )
    return agent


@pytest.fixture
def mock_ollama():
    """Mock Ollama for streaming."""
    mock_llm = MagicMock()
    mock_llm.astream = AsyncMock()

    async def mock_stream(prompt):
        chunks = ["def refactored", "_code", "():\n    ", "return True"]
        for chunk in chunks:
            mock_chunk = MagicMock()
            mock_chunk.content = chunk
            yield mock_chunk

    mock_llm.astream.return_value = mock_stream("")
    return mock_llm


@pytest.mark.asyncio
async def test_get_mcp_tools(mock_mcp_client):
    """Test getting MCP tools."""
    with patch.object(
        autonomous_code_streaming_refactor_orchestrator_v1._mcp_client_loader,
        "get",
        return_value=mock_mcp_client,
    ):
        tools = await autonomous_code_streaming_refactor_orchestrator_v1._get_mcp_tools()
        assert len(tools) == 3
        assert tools[0].name == "hybrid_search"
        assert tools[1].name == "structure_aware_search"


@pytest.mark.asyncio
async def test_create_refactor_agent(mock_mcp_client, mock_deepagent):
    """Test creating refactor agent."""
    with patch.object(
        autonomous_code_streaming_refactor_orchestrator_v1._mcp_client_loader,
        "get",
        return_value=mock_mcp_client,
    ):
        with patch("deepagents.create_deep_agent", return_value=mock_deepagent):
            agent = await autonomous_code_streaming_refactor_orchestrator_v1._get_refactor_agent()
            assert agent is not None


@pytest.mark.asyncio
async def test_analyze_codebase_for_refactoring(mock_mcp_client, mock_deepagent):
    """Test analyze_codebase_for_refactoring function."""
    with patch.object(
        autonomous_code_streaming_refactor_orchestrator_v1._mcp_client_loader,
        "get",
        return_value=mock_mcp_client,
    ):
        with patch("deepagents.create_deep_agent", return_value=mock_deepagent):
            # Clear cache to ensure fresh agent
            autonomous_code_streaming_refactor_orchestrator_v1._refactor_agent_cache = None

            # Patch validation to skip in tests
            with patch.object(
                autonomous_code_streaming_refactor_orchestrator_v1, "REQUIRE_VALIDATION", False
            ):
                tools = await mock_mcp_client.get_tools()
                with patch.object(
                    autonomous_code_streaming_refactor_orchestrator_v1,
                    "_get_mcp_tools",
                    return_value=tools,
                ):
                    result = await autonomous_code_streaming_refactor_orchestrator_v1.analyze_codebase_for_refactoring(
                        target_path="scripts/deepagents/",
                        refactoring_goals=["Improve error handling", "Add type hints"],
                    )
                    assert result["success"] is True
                    assert "analysis" in result
                    assert "latency_ms" in result
                    assert result["analysis"]["agent_generated"] is True


@pytest.mark.asyncio
async def test_stream_refactor_code(mock_ollama):
    """Test stream_refactor_code function."""
    test_code = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""

    with patch("langchain_ollama.ChatOllama", return_value=mock_ollama):
        with patch.object(
            autonomous_code_streaming_refactor_orchestrator_v1, "OLLAMA_AVAILABLE", True
        ):
            result = await autonomous_code_streaming_refactor_orchestrator_v1.stream_refactor_code(
                code=test_code,
                refactoring_type="improve_error_handling",
                model="codellama",
            )
            assert result["success"] is True
            assert "refactored_code" in result
            assert "latency_ms" in result


@pytest.mark.asyncio
async def test_stream_refactor_code_without_ollama():
    """Test stream_refactor_code when Ollama is not available."""
    test_code = "def test(): pass"

    with patch.object(
        autonomous_code_streaming_refactor_orchestrator_v1, "OLLAMA_AVAILABLE", False
    ):
        result = await autonomous_code_streaming_refactor_orchestrator_v1.stream_refactor_code(
            code=test_code,
            refactoring_type="improve_error_handling",
        )
        # Should return original code when Ollama unavailable
        assert result["success"] is True
        assert result["refactored_code"] == test_code


@pytest.mark.asyncio
async def test_orchestrate_refactoring_workflow(mock_mcp_client, mock_deepagent):
    """Test orchestrate_refactoring_workflow function."""
    with patch.object(
        autonomous_code_streaming_refactor_orchestrator_v1._mcp_client_loader,
        "get",
        return_value=mock_mcp_client,
    ):
        with patch("deepagents.create_deep_agent", return_value=mock_deepagent):
            autonomous_code_streaming_refactor_orchestrator_v1._refactor_agent_cache = None
            with patch.object(
                autonomous_code_streaming_refactor_orchestrator_v1, "REQUIRE_VALIDATION", False
            ):
                tools = await mock_mcp_client.get_tools()
                with patch.object(
                    autonomous_code_streaming_refactor_orchestrator_v1,
                    "_get_mcp_tools",
                    return_value=tools,
                ):
                    result = await autonomous_code_streaming_refactor_orchestrator_v1.orchestrate_refactoring_workflow(
                        target_path="scripts/deepagents/create_new_agent_v1.py",
                        workflow_steps=["setup", "analysis", "refactor"],
                    )
                    assert result["success"] is True
                    assert "workflow_results" in result
                    assert "latency_ms" in result
                    assert result["workflow_results"]["agent_generated"] is True


@pytest.mark.asyncio
async def test_analyze_codebase_error_handling(mock_mcp_client):
    """Test error handling in analyze_codebase_for_refactoring."""
    mock_agent = MagicMock()
    mock_agent.ainvoke = AsyncMock(side_effect=Exception("Test error"))

    with patch.object(
        autonomous_code_streaming_refactor_orchestrator_v1._mcp_client_loader,
        "get",
        return_value=mock_mcp_client,
    ):
        with patch("deepagents.create_deep_agent", return_value=mock_agent):
            autonomous_code_streaming_refactor_orchestrator_v1._refactor_agent_cache = None
            with patch.object(
                autonomous_code_streaming_refactor_orchestrator_v1, "REQUIRE_VALIDATION", False
            ):
                tools = await mock_mcp_client.get_tools()
                with patch.object(
                    autonomous_code_streaming_refactor_orchestrator_v1,
                    "_get_mcp_tools",
                    return_value=tools,
                ):
                    result = await autonomous_code_streaming_refactor_orchestrator_v1.analyze_codebase_for_refactoring(
                        target_path="scripts/deepagents/",
                    )
                    assert result["success"] is False
                    assert "error" in result


@pytest.mark.asyncio
async def test_stream_refactor_code_callback(mock_ollama):
    """Test stream_refactor_code with callback function."""
    test_code = "def test(): pass"
    callback_chunks = []

    async def callback(chunk: str):
        callback_chunks.append(chunk)

    with patch("langchain_ollama.ChatOllama", return_value=mock_ollama):
        with patch.object(
            autonomous_code_streaming_refactor_orchestrator_v1, "OLLAMA_AVAILABLE", True
        ):
            # Patch the implementation to use callback
            original_impl = (
                autonomous_code_streaming_refactor_orchestrator_v1._stream_refactor_code_impl
            )

            async def impl_with_callback(
                code, refactoring_type, model="codellama", callback_func=None
            ):
                return await original_impl(code, refactoring_type, model, callback_func)

            with patch.object(
                autonomous_code_streaming_refactor_orchestrator_v1,
                "_stream_refactor_code_impl",
                side_effect=impl_with_callback,
            ):
                result = (
                    await autonomous_code_streaming_refactor_orchestrator_v1.stream_refactor_code(
                        code=test_code,
                        refactoring_type="improve_error_handling",
                    )
                )
                assert result["success"] is True
