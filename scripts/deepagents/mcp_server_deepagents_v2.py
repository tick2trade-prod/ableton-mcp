#!/usr/bin/env python3
"""DeepAgents MCP server for Cursor integration.

Exposes DeepAgents capabilities via Model Context Protocol (MCP).
Supports specialized agent types including SOTA researcher v2.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path
from typing import Any

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Suppress Opik tracing export errors (non-critical)
logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

try:
    from mcp.server.fastmcp import FastMCP

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    FastMCP = None

# Use OpenTelemetry-configured tracer (no Opik dependency) and lazy loader
try:
    from libs.mcp_utils.lazy_loader import LazyLoader  # noqa: E402
    from libs.mcp_utils.opentelemetry_config import (
        get_opentelemetry_tracer,  # noqa: E402
    )
except ImportError:
    LazyLoader = None
    get_opentelemetry_tracer = None

tracer = get_opentelemetry_tracer("deepagents-mcp") if get_opentelemetry_tracer else None

# Lazy load SOTA researcher v2 functions (only if needed)
_sota_researcher_loader = None
if LazyLoader:
    _sota_researcher_loader = LazyLoader(
        lambda: __import__(
            "scripts.deepagents.sota_researcher_v2",
            fromlist=["research_and_plan", "research_only", "_get_research_agent"],
        )
    )

# Agent registry
_agents: dict[str, Any] = {}
_agent_counter = 0


async def create_agent_legacy(
    agent_type: str,
    config: dict | None = None,
) -> dict[str, Any]:
    """Create a DeepAgent instance.

    Supports specialized agent types:
    - "sota-researcher": Creates a SOTA researcher v2 agent

    Args:
        agent_type: Type of agent to create
        config: Agent configuration

    Returns:
        dict with agent_id and status
    """
    global _agent_counter

    span_context = tracer.start_as_current_span("deepagents.create") if tracer else None
    span = span_context.__enter__() if span_context else None

    if span:
        span.set_attribute("deepagents.agent_type", agent_type)

        _agent_counter += 1
        agent_id = f"agent_{agent_type}_{_agent_counter}"

        # Handle specialized agent types
        if agent_type == "sota-researcher":
            # For SOTA researcher, we don't create the agent immediately
            # It will be created lazily when first used
            agent_info = {
                "id": agent_id,
                "type": agent_type,
                "config": config or {},
                "created_at": time.time(),
                "status": "created",
                "specialized": True,  # Mark as specialized agent
            }
        else:
            # Generic agent creation
            agent_info = {
                "id": agent_id,
                "type": agent_type,
                "config": config or {},
                "created_at": time.time(),
                "status": "created",
            }

        _agents[agent_id] = agent_info

        if span:
            span.set_attribute("deepagents.agent_created", True)
            span.set_attribute("deepagents.agent_id", agent_id)
        if span_context:
            span_context.__exit__(None, None, None)

        return {"agent_id": agent_id, "agent_type": agent_type, "status": "created"}


async def run_agent(
    agent_id: str,
    task: str,
    context: dict | None = None,
) -> dict[str, Any]:
    """Run a DeepAgent task.

    Supports specialized agent types:
    - "sota-researcher": Routes to SOTA researcher v2 functions

    Args:
        agent_id: Agent ID to run
        task: Task description
        context: Task context (for specialized agents, may contain:
                 - research_questions: list of questions (for sota-researcher)
                 - output_path: path to save results (for sota-researcher)
                 - max_results: max results count (for sota-researcher))

    Returns:
        dict with result and metrics
    """
    span_context = tracer.start_as_current_span("deepagents.run") if tracer else None
    span = span_context.__enter__() if span_context else None

    if span:
        span.set_attribute("deepagents.agent_id", agent_id)
        span.set_attribute("deepagents.task", task[:100])

        if agent_id not in _agents:
            return {"success": False, "error": f"Agent {agent_id} not found"}

        agent_info = _agents[agent_id]
        agent_info["status"] = "running"

        start_time = time.time()

        # Handle specialized agent types
        if agent_info.get("type") == "sota-researcher":
            try:
                # Lazy load SOTA researcher module
                if _sota_researcher_loader:
                    sota_module = _sota_researcher_loader.get()
                else:
                    from scripts.deepagents import (
                        sota_researcher_v2 as sota_module,  # noqa: E402
                    )

                # Extract context parameters
                research_questions = context.get("research_questions") if context else None
                output_path = context.get("output_path") if context else None
                max_results = context.get("max_results", 10) if context else 10

                # Determine if this is a research_and_plan or research_only task
                # If research_questions or output_path is provided, use research_and_plan
                # Otherwise, use research_only
                if research_questions is not None or output_path is not None:
                    # Use research_and_plan
                    result = await sota_module.research_and_plan(
                        topic=task,
                        research_questions=research_questions,
                        output_path=output_path,
                    )
                else:
                    # Use research_only
                    result = await sota_module.research_only(
                        topic=task,
                        max_results=max_results,
                    )

                latency = (time.time() - start_time) * 1000
                agent_info["status"] = "completed"
                agent_info["last_run"] = time.time()

                if span:
                    span.set_attribute("deepagents.latency_ms", latency)
                    span.set_attribute("deepagents.success", True)
                if span_context:
                    span_context.__exit__(None, None, None)

                return {
                    "success": True,
                    "result": result,
                    "latency_ms": latency,
                }
            except Exception as e:
                agent_info["status"] = "error"
                if span:
                    span.set_attribute("deepagents.success", False)
                    span.set_attribute("deepagents.error", str(e))
                if span_context:
                    span_context.__exit__(type(e), e, None)
                return {
                    "success": False,
                    "error": f"SOTA researcher execution failed: {e}",
                }

        # Generic agent execution (legacy behavior)
        await asyncio.sleep(0.01)
        result = {
            "output": f"Executed task: {task[:50]}...",
            "agent_type": agent_info["type"],
        }

        latency = (time.time() - start_time) * 1000

        agent_info["status"] = "completed"
        agent_info["last_run"] = time.time()

        if span:
            span.set_attribute("deepagents.latency_ms", latency)
            span.set_attribute("deepagents.success", True)
        if span_context:
            span_context.__exit__(None, None, None)

        return {
            "success": True,
            "result": result,
            "latency_ms": latency,
        }


async def list_agents() -> list[dict[str, Any]]:
    """List all available DeepAgents.

    Returns:
        list of agent info dicts
    """
    span_context = tracer.start_as_current_span("deepagents.list") if tracer else None
    span = span_context.__enter__() if span_context else None

    agents_list = [
        {"id": a["id"], "type": a["type"], "status": a["status"]} for a in _agents.values()
    ]

    if span:
        span.set_attribute("deepagents.count", len(agents_list))
    if span_context:
        span_context.__exit__(None, None, None)

    return agents_list


async def get_agent_status(agent_id: str) -> dict[str, Any]:
    """Get DeepAgent status.

    Args:
        agent_id: Agent ID

    Returns:
        dict with agent status
    """
    span_context = tracer.start_as_current_span("deepagents.status") if tracer else None
    span = span_context.__enter__() if span_context else None

    if agent_id not in _agents:
        if span_context:
            span_context.__exit__(None, None, None)
        return {"error": f"Agent {agent_id} not found"}

    agent_info = _agents[agent_id]
    status = {
        "id": agent_info["id"],
        "type": agent_info["type"],
        "status": agent_info["status"],
        "created_at": agent_info["created_at"],
        "last_run": agent_info.get("last_run"),
    }

    if span:
        span.set_attribute("deepagents.status", status["status"])
    if span_context:
        span_context.__exit__(None, None, None)

    return status


async def delete_agent(agent_id: str) -> dict[str, Any]:
    """Delete a DeepAgent.

    Args:
        agent_id: Agent ID to delete

    Returns:
        dict with deletion status
    """
    span_context = tracer.start_as_current_span("deepagents.delete") if tracer else None
    span = span_context.__enter__() if span_context else None

    if agent_id in _agents:
        del _agents[agent_id]
        if span:
            span.set_attribute("deepagents.deleted", True)
        if span_context:
            span_context.__exit__(None, None, None)
        return {"success": True, "deleted": agent_id}

    if span_context:
        span_context.__exit__(None, None, None)
    return {"success": False, "error": f"Agent {agent_id} not found"}


# Create FastMCP server
if MCP_AVAILABLE:
    mcp = FastMCP("deepagents", json_response=True)

    # Performance: Lazy load adapter (avoids import overhead if not used)
    # Try to load adapter, but fall back to legacy functions if not available
    _adapter = None
    try:
        if LazyLoader:
            try:
                _adapter_loader = LazyLoader(
                    lambda: __import__(
                        "libs.mcp_utils.deepagents_adapter", fromlist=["get_adapter"]
                    ).get_adapter()
                )
                _adapter = _adapter_loader.get()
            except (ImportError, AttributeError, ModuleNotFoundError):
                _adapter = None
        else:
            try:
                from libs.mcp_utils.deepagents_adapter import get_adapter  # noqa: E402

                _adapter = get_adapter()
            except (ImportError, AttributeError, ModuleNotFoundError):
                _adapter = None
    except (ImportError, AttributeError, ModuleNotFoundError):
        # Adapter not available, use legacy functions
        _adapter = None

    # Store references to underlying functions to avoid recursion
    _create_agent_legacy_impl = create_agent_legacy
    _run_agent_impl = run_agent
    _list_agents_impl = list_agents
    _get_agent_status_impl = get_agent_status
    _delete_agent_impl = delete_agent

    @mcp.tool()
    async def create_agent(
        agent_type: str,
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a DeepAgent instance.

        Supports specialized agent types:
        - "sota-researcher": Creates a SOTA researcher v2 agent

        Args:
            agent_type: Type of agent to create
            config: Agent configuration

        Returns:
            dict with agent_id and status
        """
        # Use adapter if available, otherwise use legacy implementation
        if _adapter:
            try:
                return await _adapter.create_agent(agent_type, config)
            except (AttributeError, NotImplementedError):
                # Adapter doesn't support this, fall back to legacy
                pass
        return await _create_agent_legacy_impl(agent_type, config)

    @mcp.tool()
    async def run_agent(  # noqa: F811
        agent_id: str,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run a DeepAgent task.

        Supports specialized agent types:
        - "sota-researcher": Routes to SOTA researcher v2 functions
          Context may include: research_questions, output_path, max_results

        Args:
            agent_id: Agent ID to run
            task: Task description
            context: Task context (for specialized agents)

        Returns:
            dict with result and metrics
        """
        # Use adapter if available, otherwise use legacy implementation
        if _adapter:
            try:
                return await _adapter.run_agent(agent_id, task, context)
            except (AttributeError, NotImplementedError):
                # Adapter doesn't support this, fall back to legacy
                pass
        return await _run_agent_impl(agent_id, task, context)

    @mcp.tool()
    async def list_agents() -> list[dict[str, Any]]:
        """List all available DeepAgents.

        Returns:
            list of agent info dicts
        """
        return await _list_agents_impl()

    @mcp.tool()
    async def get_agent_status(agent_id: str) -> dict[str, Any]:
        """Get DeepAgent status.

        Args:
            agent_id: Agent ID

        Returns:
            dict with agent status
        """
        return await _get_agent_status_impl(agent_id)

    @mcp.tool()
    async def delete_agent(agent_id: str) -> dict[str, Any]:  # noqa: F811
        """Delete a DeepAgent.

        Args:
            agent_id: Agent ID to delete

        Returns:
            dict with deletion status
        """
        # Use adapter if available, otherwise use legacy implementation
        if _adapter:
            try:
                return await _adapter.delete_agent(agent_id)
            except (AttributeError, NotImplementedError):
                # Adapter doesn't support this, fall back to legacy
                pass
        return await _delete_agent_impl(agent_id)
else:
    mcp = None


if __name__ == "__main__":
    if MCP_AVAILABLE and mcp:
        mcp.run(transport="stdio")
    else:
        print("MCP not available. Running in standalone mode.")
        print("Available functions: create_agent, run_agent, list_agents, get_agent_status")
