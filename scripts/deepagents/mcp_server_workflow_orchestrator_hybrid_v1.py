#!/usr/bin/env python3
"""MCP server for Workflow Orchestrator Hybrid v1.

Exposes workflow orchestration capabilities via Model Context Protocol (MCP).
Uses Ollama for cost-free LLM operations (replaces Claude API).
"""

import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Suppress OpenTelemetry tracing export errors
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

tracer = get_opentelemetry_tracer("workflow-orchestrator-hybrid-mcp")

# Lazy loader for workflow_orchestrator_hybrid_v1 module
_workflow_orchestrator_loader: Any = None
if LazyLoader:
    _workflow_orchestrator_loader = LazyLoader(
        lambda: __import__(
            "scripts.deepagents.workflow_orchestrator_hybrid_v1", fromlist=["orchestrate_workflow"]
        )
    )


# Store references to underlying functions to avoid recursion
async def _orchestrate_workflow_impl(
    feature_name: str,
    workflow_steps: list[str] | None = None,
    resume_from: str | None = None,
    workflow_id: str | None = None,
) -> dict[str, Any]:
    """Internal implementation of orchestrate_workflow."""
    if _workflow_orchestrator_loader:
        module = _workflow_orchestrator_loader.get()
        return await module.orchestrate_workflow(
            feature_name, workflow_steps, resume_from, workflow_id
        )
    else:
        from scripts.deepagents import workflow_orchestrator_hybrid_v1

        return await workflow_orchestrator_hybrid_v1.orchestrate_workflow(
            feature_name, workflow_steps, resume_from, workflow_id
        )


# Create FastMCP server
if MCP_AVAILABLE and FastMCP is not None:
    mcp = FastMCP("workflow-orchestrator-hybrid", json_response=True)

    @mcp.tool()
    async def orchestrate_workflow(
        feature_name: str,
        workflow_steps: list[str] | None = None,  # noqa: UP007
        resume_from: str | None = None,  # noqa: UP007
        workflow_id: str | None = None,  # noqa: UP007
    ) -> dict[str, Any]:
        """Orchestrate a complete development workflow.

        Args:
            feature_name: Name of feature to implement
            workflow_steps: Optional list of steps to execute (default: all steps)
            resume_from: Optional step to resume from (uses state persistence)
            workflow_id: Optional workflow ID for resume (default: deterministic from feature_name)

        Returns:
            dict with workflow results

        Workflow Steps:
            - setup: Create branch, initialize structure
            - planning: Research patterns, create plan
            - implementation: Write tests, implement code
            - validation: Run tests, validate changes
            - review: Generate review checklist
            - pr_creation: Create pull request
        """
        with tracer.start_as_current_span("workflow_orchestrator.orchestrate") as span:
            span.set_attribute("workflow_orchestrator.feature_name", feature_name)

            result = await _orchestrate_workflow_impl(
                feature_name, workflow_steps, resume_from, workflow_id
            )

            span.set_attribute("workflow_orchestrator.success", result.get("success", False))
            span.set_attribute("workflow_orchestrator.latency_ms", result.get("latency_ms", 0))

            return result

    if __name__ == "__main__":
        mcp.run()

else:
    # Fallback if FastMCP not available
    logger = logging.getLogger("workflow-orchestrator-hybrid-mcp")
    logger.error("FastMCP not available. Install with: uv sync")
