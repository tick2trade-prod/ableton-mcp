#!/usr/bin/env python3
"""DeepAgents MCP server for create-new-agent integration.

Exposes create_new_agent_v1 capabilities via Model Context Protocol (MCP).
"""

import logging
import sys
import time
from contextlib import nullcontext
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

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

from app.mcp.lazy_loader import LazyLoader
from app.mcp.opentelemetry_config import get_opentelemetry_tracer

tracer = get_opentelemetry_tracer("create-new-agent-mcp") if get_opentelemetry_tracer else None

# Lazy loader for create_new_agent_v1 module
_create_new_agent_loader: Any = None
if LazyLoader:
    _create_new_agent_loader = LazyLoader(
        lambda: __import__(
            "scripts.deepagents.create_new_agent_v1",
            fromlist=["create_agent_spec", "generate_agent_files", "validate_agent_files"],
        )
    )


async def create_agent_legacy(
    agent_type: str,
    config: dict | None = None,
) -> dict[str, Any]:
    """Create a DeepAgent instance (for create-new-agent type).

    Args:
        agent_type: Type of agent to create (e.g., "create-new-agent")
        config: Agent configuration

    Returns:
        dict with agent_id and status
    """
    if agent_type != "create-new-agent":
        return {"success": False, "error": f"Unknown agent type: {agent_type}"}

    return {
        "agent_id": "create-new-agent-1",
        "agent_type": agent_type,
        "status": "created",
        "capabilities": ["create_agent_spec", "generate_agent_files", "validate_agent_files"],
    }


async def _run_agent_impl(
    agent_id: str,
    task: str,
    context: dict | None = None,
) -> dict[str, Any]:
    """Run a create-new-agent task (implementation).

    Args:
        agent_id: Agent ID (should be "create-new-agent-1")
        task: Task description (agent name or description)
        context: Task context with operation type and parameters

    Returns:
        dict with result and metrics
    """
    span_context = tracer.start_as_current_span("create_new_agent.run") if tracer else nullcontext()
    with span_context as span:
        if span:
            span.set_attribute("create_new_agent.agent_id", agent_id)
            span.set_attribute("create_new_agent.task", task[:100])

        if agent_id != "create-new-agent-1":
            return {"success": False, "error": f"Agent {agent_id} not found"}

        try:
            create_new_agent_module = (
                _create_new_agent_loader.get() if _create_new_agent_loader else None
            )
            if not create_new_agent_module:
                # Fallback: try direct import
                from scripts.deepagents import create_new_agent_v1

                create_new_agent_module = create_new_agent_v1
        except ImportError as e:
            return {"success": False, "error": f"Failed to import create_new_agent_v1: {e}"}

        context = context or {}
        operation = context.get("operation", "create_agent_spec")

        start_time = time.time()

        try:
            if operation == "create_agent_spec":
                agent_name = context.get("agent_name", task)
                description = context.get("description", task)
                requirements = context.get("requirements")
                result = await create_new_agent_module.create_agent_spec(
                    agent_name=agent_name,
                    description=description,
                    requirements=requirements,
                )
            elif operation == "generate_agent_files":
                spec = context.get("spec", {})
                output_dir = context.get("output_dir")
                result = await create_new_agent_module.generate_agent_files(
                    spec=spec,
                    output_dir=output_dir,
                )
            elif operation == "validate_agent_files":
                files = context.get("files", {})
                result = await create_new_agent_module.validate_agent_files(files=files)
            else:
                result = {"success": False, "error": f"Unknown operation: {operation}"}

            latency = (time.time() - start_time) * 1000
            if span:
                span.set_attribute("create_new_agent.latency_ms", latency)
                span.set_attribute("create_new_agent.success", result.get("success", False))

            return {
                "success": result.get("success", False),
                "result": result,
                "latency_ms": latency,
            }
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            if span:
                span.set_attribute("create_new_agent.latency_ms", latency)
                span.set_attribute("create_new_agent.success", False)
            return {
                "success": False,
                "error": str(e),
                "latency_ms": latency,
            }


async def _list_agents_impl() -> list[dict[str, Any]]:
    """List all available DeepAgents (implementation)."""
    return [{"id": "create-new-agent-1", "type": "create-new-agent", "status": "created"}]


async def _get_agent_status_impl(agent_id: str) -> dict[str, Any]:
    """Get DeepAgent status (implementation)."""
    if agent_id == "create-new-agent-1":
        return {
            "id": agent_id,
            "type": "create-new-agent",
            "status": "created",
        }
    return {"error": f"Agent {agent_id} not found"}


async def _delete_agent_impl(agent_id: str) -> dict[str, Any]:
    """Delete a DeepAgent (implementation)."""
    if agent_id == "create-new-agent-1":
        return {"success": True, "deleted": agent_id}
    return {"success": False, "error": f"Agent {agent_id} not found"}


# Create FastMCP server
if MCP_AVAILABLE:
    mcp = FastMCP("create-new-agent-mcp", json_response=True)

    @mcp.tool()
    async def create_agent(
        agent_type: str,
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a DeepAgent instance.

        Args:
            agent_type: Type of agent to create (e.g., "create-new-agent")
            config: Agent configuration

        Returns:
            dict with agent_id and status
        """
        return await create_agent_legacy(agent_type, config)

    # Store references to underlying functions
    _create_agent_legacy_impl = create_agent_legacy

    @mcp.tool()
    async def run_agent(
        agent_id: str,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run a create-new-agent task.

        Args:
            agent_id: Agent ID
            task: Task description
            context: Task context with operation, agent_name, description, etc.

        Returns:
            dict with result and metrics
        """
        return await _run_agent_impl(agent_id, task, context)

    @mcp.tool()
    async def list_agents() -> list[dict[str, Any]]:
        """List all available DeepAgents."""
        return await _list_agents_impl()

    @mcp.tool()
    async def get_agent_status(agent_id: str) -> dict[str, Any]:
        """Get DeepAgent status."""
        return await _get_agent_status_impl(agent_id)

    @mcp.tool()
    async def delete_agent(agent_id: str) -> dict[str, Any]:
        """Delete a DeepAgent."""
        return await _delete_agent_impl(agent_id)
else:
    mcp = None


if __name__ == "__main__":
    if MCP_AVAILABLE and mcp:
        mcp.run(transport="stdio")
    else:
        print("MCP not available")
