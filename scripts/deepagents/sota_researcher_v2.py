#!/usr/bin/env python3
"""MCP server for SOTA researcher DeepAgent.

Provides MCP tools for state-of-the-art research and planning capabilities.
Uses deepagents create_deep_agent for automatic orchestration with MCP tools:
- docs-langchain: Searches LangChain documentation
- Context7: Retrieves library documentation
- indexing-semantic-search-v2: Semantic search from codebase
- tavily-remote-mcp: Web search for real-time information
- filesystem: Built-in filesystem middleware for file operations
- memory: Memory persistence (via MCP if available)

This v2 implementation uses deepagents for automatic orchestration, reducing
manual code by ~60% while improving performance through built-in capabilities.

Model Configuration:
- Sequential-thinking MCP server uses Ollama model configured in ~/.cursor/mcp.json
- Default model: codellama-34b-optimized:latest
- Configure via OLLAMA_MODEL environment variable in sequential-thinking MCP server config
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Validation mode: require proper setup instead of graceful degradation
REQUIRE_VALIDATION = (
    os.environ.get("SOTA_RESEARCHER_REQUIRE_VALIDATION", "true").lower() == "true"
)

# Timeout configuration (in seconds)
# research_only: Quick research with shorter timeout
RESEARCH_ONLY_TIMEOUT = int(
    os.environ.get("SOTA_RESEARCHER_ONLY_TIMEOUT", "300")
)  # 5 minutes default
# research_and_plan: Comprehensive research with longer timeout
RESEARCH_AND_PLAN_TIMEOUT = int(
    os.environ.get("SOTA_RESEARCHER_PLAN_TIMEOUT", "600")
)  # 10 minutes default


def _validate_prerequisites() -> tuple[bool, list[str]]:
    """Validate all prerequisites are properly configured.

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check deepagents availability
    try:
        from deepagents import create_deep_agent
    except ImportError:
        errors.append("deepagents is not installed. Install with: uv sync")

    # Check MCP client availability
    if not MCP_CLIENT_AVAILABLE:
        errors.append("langchain_mcp_adapters is not installed. Install with: uv sync")

    # Check MCP config exists
    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    if not mcp_config_path.exists():
        errors.append(
            f"MCP config file not found: {mcp_config_path}. "
            "Run installer: ./scripts/deepagents/install_sota_researcher_v2.sh"
        )
    else:
        # Validate at least one MCP server is configured
        try:
            with open(mcp_config_path) as f:
                config = json.load(f)
            mcp_servers = config.get("mcpServers", {})
            if not mcp_servers:
                errors.append(
                    "No MCP servers configured. "
                    "Run installer: ./scripts/deepagents/install_sota_researcher_v2.sh"
                )
        except Exception as e:
            errors.append(f"Error reading MCP config: {e}")

    return len(errors) == 0, errors


# Suppress OpenTelemetry tracing export errors (non-critical)
logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

# Setup logger for SOTA researcher
logger = logging.getLogger("sota-researcher")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

try:
    from mcp.server.fastmcp import FastMCP

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    FastMCP = None

# Use OpenTelemetry-configured tracer (no Opik dependency)
from libs.mcp_utils.lazy_loader import LazyLoader  # noqa: E402
from libs.mcp_utils.mcp_utils import normalize_mcp_server_config  # noqa: E402
from libs.mcp_utils.opentelemetry_config import get_opentelemetry_tracer  # noqa: E402

tracer = get_opentelemetry_tracer("sota-researcher-mcp")

# MCP Client for calling other MCP servers
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient

    MCP_CLIENT_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    MultiServerMCPClient = None

# H001/H002: Lazy Loading with Instance Caching
_mcp_client_loader = LazyLoader(
    lambda: _create_mcp_client() if MCP_CLIENT_AVAILABLE else None
)

# Agent caching: Store cached agent instance
_research_agent_cache: Any = None
_research_agent_lock = None


def _create_mcp_client() -> Any:
    """Create MCP client for calling other MCP servers."""
    if not MCP_CLIENT_AVAILABLE:
        return None

    # Load MCP configuration from ~/.cursor/mcp.json
    import json
    from pathlib import Path

    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    if not mcp_config_path.exists():
        return None

    try:
        with open(mcp_config_path) as f:
            config = json.load(f)

        # Convert Cursor MCP config format to MultiServerMCPClient format
        client_config = {}
        for server_name, server_config in config.get("mcpServers", {}).items():
            # Filter for the MCPs we need: langchain-docs, context7, sequential-thinking,
            # indexing-semantic-search-v2, filesystem, memory, tavily-remote-mcp
            if server_name in [
                "docs-langchain",
                "Context7",
                "sequential-thinking",
                "indexing-semantic-search-v2",
                "filesystem",
                "memory",
                "tavily-remote-mcp",
            ]:
                # Handle URL-based MCPs (Context7, docs-langchain)
                if "url" in server_config:
                    client_config[server_name] = {
                        "transport": "sse",
                        "url": server_config["url"],
                    }
                # Handle stdio-based MCPs (sequential-thinking, indexing-semantic-search-v2, etc.)
                elif "command" in server_config:
                    # Use standardized MCP server config normalization
                    # This resolves uv/uvx paths and ensures PATH is set correctly
                    normalized_config = normalize_mcp_server_config(server_config)

                    client_config[server_name] = {
                        "transport": "stdio",
                        "command": normalized_config["command"],
                        "args": normalized_config.get("args", []),
                        "env": normalized_config.get("env", {}),
                    }

        if client_config:
            return MultiServerMCPClient(client_config)
    except Exception:
        # If MCP client creation fails, return None (graceful degradation)
        return None

    return None


def _get_mcp_client() -> Any:
    """Get cached MCP client instance."""
    return _mcp_client_loader.get()


async def _get_mcp_tools() -> list[Any]:
    """Get all MCP tools from configured servers.

    Returns:
        List of MCP tools

    Raises:
        RuntimeError: If MCP client is not available or tools cannot be retrieved
    """
    mcp_client = _get_mcp_client()
    if not mcp_client:
        raise RuntimeError(
            "MCP client not available. "
            "Run installer: ./scripts/deepagents/install_sota_researcher_v2.sh"
        )

    try:
        tools = await mcp_client.get_tools()
        if not tools:
            raise RuntimeError(
                "No MCP tools available. Check that MCP servers are running and configured."
            )
        return list(tools)
    except Exception as e:
        raise RuntimeError(
            f"Failed to get MCP tools: {e}. Check that MCP servers are running and accessible."
        ) from e


def _validate_topic(topic: str) -> None:
    """Validate research topic parameter.

    Args:
        topic: Research topic to validate

    Raises:
        ValueError: If topic is invalid (empty, too long, etc.)
    """
    if not topic or not topic.strip():
        raise ValueError(
            "Topic cannot be empty. Please provide a non-empty research topic."
        )
    if len(topic) > 1000:
        raise ValueError(
            f"Topic is too long (max 1000 characters, got {len(topic)}). "
            "Please provide a more concise topic."
        )


def _normalize_research_questions(value: Any) -> list[str] | None:  # noqa: UP007
    """Normalize research_questions parameter to handle various input formats.

    This function handles edge cases that might occur when Cursor's AI parses
    natural language prompts and extracts research_questions incorrectly.

    Handles:
    - None -> None
    - List[str] -> List[str] (with string conversion)
    - List[Any] -> List[str] (converts all items to strings, filters None)
    - str -> List[str] (single string wrapped in list, or JSON parsed)
    - tuple, set, other iterables -> List[str]
    - dict -> Attempts to extract questions from dict structure
    - Empty string -> None (treated as no questions)

    Args:
        value: The research_questions value to normalize

    Returns:
        Normalized list of strings, or None if no questions provided

    Examples:
        >>> _normalize_research_questions(["Q1", "Q2"])
        ['Q1', 'Q2']
        >>> _normalize_research_questions("single question")
        ['single question']
        >>> _normalize_research_questions('["Q1", "Q2"]')
        ['Q1', 'Q2']
        >>> _normalize_research_questions(None)
        None
        >>> _normalize_research_questions("")
        None
    """
    # Handle None explicitly
    if value is None:
        return None

    # Handle empty string (treat as None - no questions provided)
    if isinstance(value, str) and not value.strip():
        return None

    # Handle string input (could be JSON, single question, or natural language)
    if isinstance(value, str):
        # Try to parse as JSON first (handles JSON array strings)
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                # JSON array - normalize items to strings
                normalized = [
                    str(q).strip() for q in parsed if q is not None and str(q).strip()
                ]
                return normalized if normalized else None
            elif isinstance(parsed, dict):
                # JSON object - try to extract questions from common keys
                for key in ["questions", "research_questions", "items", "list"]:
                    if key in parsed and isinstance(parsed[key], list):
                        normalized = [
                            str(q).strip()
                            for q in parsed[key]
                            if q is not None and str(q).strip()
                        ]
                        return normalized if normalized else None
                # If no list found, treat the whole dict as a single question
                return [str(value)]
            else:
                # Single JSON value - wrap in list
                return [str(parsed).strip()] if str(parsed).strip() else None
        except (json.JSONDecodeError, TypeError):
            # Not JSON - treat as a single question string
            return [value.strip()] if value.strip() else None

    # Handle list input
    if isinstance(value, list):
        if not value:
            # Empty list - return None (no questions provided)
            return None
        # Normalize all items to strings, filter out None and empty strings
        normalized = [str(q).strip() for q in value if q is not None and str(q).strip()]
        return normalized if normalized else None

    # Handle dict input (Cursor might extract as {"questions": [...]})
    if isinstance(value, dict):
        # Try to extract questions from common keys
        for key in ["questions", "research_questions", "items", "list", "value"]:
            if key in value:
                return _normalize_research_questions(value[key])
        # If no recognized key, convert dict to string representation
        return [str(value)]

    # Handle other iterable types (tuple, set, etc.)
    try:
        if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
            normalized = [
                str(q).strip() for q in value if q is not None and str(q).strip()
            ]
            return normalized if normalized else None
    except (TypeError, ValueError):
        pass

    # Fallback: convert single value to string and wrap in list
    try:
        str_value = str(value).strip()
        return [str_value] if str_value else None
    except (TypeError, ValueError):
        # Last resort: return None if conversion fails
        return None


async def _create_research_agent() -> Any:
    """Create a deepagent configured for research tasks.

    Returns:
        Compiled deepagent ready for research tasks

    Raises:
        RuntimeError: If prerequisites are not met or agent creation fails
    """
    from deepagents import create_deep_agent

    # Validate prerequisites
    if REQUIRE_VALIDATION:
        is_valid, errors = _validate_prerequisites()
        if not is_valid:
            error_msg = (
                "SOTA Researcher prerequisites validation failed:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )
            error_msg += "\n\nTroubleshooting steps:"
            error_msg += (
                "\n1. Run installer: ./scripts/deepagents/install_sota_researcher_v2.sh"
            )
            error_msg += "\n2. Verify dependencies: uv run python scripts/deepagents/validate_sota_researcher_v2.py"
            error_msg += "\n3. Check MCP configuration: cat ~/.cursor/mcp.json"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    # Get MCP tools
    try:
        mcp_tools = await _get_mcp_tools()
    except RuntimeError as e:
        raise RuntimeError(
            f"Failed to get MCP tools: {e}. "
            "Ensure MCP servers are configured in ~/.cursor/mcp.json. "
            "Run installer: ./scripts/deepagents/install_sota_researcher_v2.sh"
        ) from e

    # Enhanced research system prompt with explicit deepagents capabilities
    research_prompt = """You are an expert SOTA (State-of-the-Art) researcher specializing in software engineering, machine learning, and technology research.

Your goal is to conduct comprehensive research using multiple information sources and create actionable plans.

## Available Research Tools

You have access to the following research tools:
- **docs-langchain**: Search LangChain documentation
- **Context7**: Retrieve library documentation (langchain, pydantic, fastapi)
- **indexing-semantic-search-v2**: Semantic search from codebase
- **tavily-remote-mcp**: Web search for real-time information
- **sequential-thinking**: Structured thinking for complex problems

## DeepAgents Built-in Capabilities

You have access to powerful built-in tools from deepagents:

### Planning Tool: `write_todos`
- Use `write_todos` to break down complex research tasks into manageable steps
- Track progress as you complete each research step
- Adapt your plan based on findings

### Filesystem Tools: `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`
- Use `write_file` to save large research results and manage context
- Use `read_file` to retrieve previously saved research
- Use `edit_file` to update research documents incrementally
- These tools prevent context window overflow by offloading content to files

### SubAgent Tool: `task`
- Use the `task` tool to spawn specialized subagents for independent research questions
- Subagents provide context isolation and can work in parallel
- Delegate complex sub-questions to subagents to keep your main context clean

## Research Workflow

1. **Plan First**: Use `write_todos` to break down complex research tasks into discrete steps
2. **Gather Information**: Use relevant research tools to collect information from multiple sources
3. **Manage Context**: Use `write_file` to save large findings and prevent context overflow
4. **Parallelize**: Use `task` tool to spawn subagents for independent research questions
5. **Synthesize**: Combine findings from multiple sources and subagents
6. **Create Plan**: Structure findings into actionable steps with clear next actions
7. **Save Results**: Use `write_file` to save final research results for future reference

## Best Practices

- **Always plan first**: Use `write_todos` for multi-step research tasks to stay organized
- **Save frequently**: Use `write_file` to save large research results and manage context window
- **Use subagents**: Spawn subagents for independent research questions to parallelize work
- **Synthesize before responding**: Combine findings from multiple sources before providing final answer
- **Cite sources**: Always cite sources when providing information
- **Create actionable plans**: Structure findings into clear, actionable steps with specific next actions
- **Adapt strategy**: Modify your research approach based on what you discover
"""

    # Create agent with MCP tools
    try:
        agent = create_deep_agent(
            tools=mcp_tools,
            system_prompt=research_prompt,
        )
        return agent
    except ImportError as e:
        raise RuntimeError(
            f"Failed to import deepagents: {e}. "
            "Install with: uv sync. "
            "See: https://docs.langchain.com/oss/python/deepagents/overview"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to create research agent: {e}. "
            "Check that deepagents is properly installed and MCP tools are available. "
            "Run installer: ./scripts/deepagents/install_sota_researcher_v2.sh"
        ) from e


async def _get_research_agent() -> Any:
    """Get cached research agent instance.

    Returns:
        Cached research agent, creating it if needed

    Raises:
        RuntimeError: If agent creation fails
    """
    global _research_agent_cache

    # Return cached agent if available
    if _research_agent_cache is not None:
        return _research_agent_cache

    # Create and cache agent
    _research_agent_cache = await _create_research_agent()
    logger.info("Research agent created and cached")
    return _research_agent_cache


# Note: Using Optional[...] instead of | None for FastMCP compatibility
# FastMCP's type validation doesn't handle union types with | None syntax well
async def research_and_plan(
    topic: str,
    research_questions: list[str] | None = None,  # type: ignore[assignment]  # FastMCP compatibility
    output_path: str | None = None,  # type: ignore[assignment]  # FastMCP compatibility
) -> dict[str, Any]:
    """Conduct SOTA research and create a plan using DeepAgents.

    Uses deepagents create_deep_agent for automatic orchestration with MCP tools.
    The agent automatically plans, researches, synthesizes, and creates actionable plans.

    Args:
        topic: Research topic
        research_questions: Optional list of specific research questions
        output_path: Optional path to save research results

    Returns:
        dict with research results and plan (agent-generated content)
    """
    start_time = time.perf_counter()
    with tracer.start_as_current_span("sota_researcher.research_and_plan") as span:
        span.set_attribute("sota_researcher.topic", topic[:100] if topic else "")
        span.set_attribute("sota_researcher.has_questions", bool(research_questions))
        span.set_attribute(
            "sota_researcher.num_questions",
            len(research_questions) if research_questions else 0,
        )
        span.set_attribute("sota_researcher.timeout_seconds", RESEARCH_AND_PLAN_TIMEOUT)

        # Validate topic input
        with tracer.start_as_current_span(
            "sota_researcher.validate_topic"
        ) as validate_span:
            try:
                _validate_topic(topic)
                validate_span.set_attribute("sota_researcher.validation_passed", True)
            except ValueError as e:
                validate_span.set_attribute("sota_researcher.validation_passed", False)
                validate_span.set_attribute("sota_researcher.validation_error", str(e))
                logger.error(f"Invalid topic: {e}")
                raise

        # Get cached research agent
        with tracer.start_as_current_span("sota_researcher.get_agent") as agent_span:
            agent = await _get_research_agent()
            agent_span.set_attribute(
                "sota_researcher.agent_cached", _research_agent_cache is not None
            )

        # Build research prompt
        if research_questions:
            questions_text = "\n".join(f"- {q}" for q in research_questions)
            prompt = f"""Research the following topic and create a comprehensive plan:

**Topic:** {topic}

**Research Questions:**
{questions_text}

Please:
1. Use `write_todos` to plan your research approach
2. Conduct thorough research using available tools
3. Synthesize findings into a structured plan
4. Save results to {output_path} if specified
"""
        else:
            output_instruction = (
                f"Save results to {output_path}"
                if output_path
                else "Optionally save results to a file"
            )
            prompt = f"""Research the following topic and create a comprehensive plan:

**Topic:** {topic}

Please:
1. Use `write_todos` to plan your research approach
2. Conduct thorough research using available tools
3. Synthesize findings into a structured plan
4. {output_instruction}
"""

        # Invoke agent with timeout
        try:
            with tracer.start_as_current_span(
                "sota_researcher.agent_invoke"
            ) as invoke_span:
                invoke_span.set_attribute("sota_researcher.prompt_length", len(prompt))
                invoke_span.set_attribute(
                    "sota_researcher.timeout_seconds", RESEARCH_AND_PLAN_TIMEOUT
                )

                result = await asyncio.wait_for(
                    agent.ainvoke({"messages": [{"role": "user", "content": prompt}]}),
                    timeout=RESEARCH_AND_PLAN_TIMEOUT,
                )
                invoke_span.set_attribute("sota_researcher.completed", True)
        except TimeoutError:
            latency_ms = (time.perf_counter() - start_time) * 1000
            span.set_attribute("sota_researcher.latency_ms", latency_ms)
            span.set_attribute("sota_researcher.timed_out", True)
            span.set_attribute(
                "sota_researcher.timeout_seconds", RESEARCH_AND_PLAN_TIMEOUT
            )
            logger.error(
                f"Research and plan timed out after {RESEARCH_AND_PLAN_TIMEOUT}s"
            )
            return {
                "success": False,
                "error": f"Research timed out after {RESEARCH_AND_PLAN_TIMEOUT} seconds. "
                "The agent may be stuck in a loop or processing too much information. "
                "Try reducing the scope of research or increasing timeout.",
                "latency_ms": latency_ms,
                "timed_out": True,
            }
        except Exception as e:
            logger.error(f"Agent invocation failed: {e}", exc_info=True)
            raise RuntimeError(
                f"Research failed: {e}. "
                "This may indicate an issue with the agent, MCP tools, or model. "
                "Check logs for details and verify MCP servers are running."
            ) from e

        # Extract final message
        final_message = result["messages"][-1]
        content = (
            final_message.content
            if hasattr(final_message, "content")
            else str(final_message)
        )

        # Measure latency
        latency_ms = (time.perf_counter() - start_time) * 1000
        span.set_attribute("sota_researcher.latency_ms", latency_ms)

        return {
            "success": True,
            "research_results": {
                "agent_response": content,
                "messages": [str(msg) for msg in result["messages"]],
            },
            "plan": {
                "agent_generated": True,
                "content": content,
            },
            "latency_ms": latency_ms,
        }


async def research_only(
    topic: str,
    max_results: int = 10,
) -> dict[str, Any]:
    """Conduct research only (no planning) using DeepAgents.

    Uses deepagents create_deep_agent for automatic research orchestration.
    The agent automatically researches and synthesizes findings.

    Args:
        topic: Research topic
        max_results: Maximum number of research results (hint for agent)

    Returns:
        dict with research results (agent-generated content)
    """
    start_time = time.perf_counter()
    with tracer.start_as_current_span("sota_researcher.research_only") as span:
        span.set_attribute("sota_researcher.topic", topic[:100] if topic else "")
        span.set_attribute("sota_researcher.max_results", max_results)
        span.set_attribute("sota_researcher.timeout_seconds", RESEARCH_ONLY_TIMEOUT)

        # Validate topic input
        with tracer.start_as_current_span(
            "sota_researcher.validate_topic"
        ) as validate_span:
            try:
                _validate_topic(topic)
                validate_span.set_attribute("sota_researcher.validation_passed", True)
            except ValueError as e:
                validate_span.set_attribute("sota_researcher.validation_passed", False)
                validate_span.set_attribute("sota_researcher.validation_error", str(e))
                logger.error(f"Invalid topic: {e}")
                raise

        # Get cached research agent
        with tracer.start_as_current_span("sota_researcher.get_agent") as agent_span:
            agent = await _get_research_agent()
            agent_span.set_attribute(
                "sota_researcher.agent_cached", _research_agent_cache is not None
            )

        # Build research prompt
        prompt = f"""Research the following topic and provide comprehensive findings:

**Topic:** {topic}

Please:
1. Conduct thorough research using available tools
2. Aim to gather approximately {max_results} key findings
3. Synthesize information from multiple sources
4. Provide a well-structured summary of your findings

IMPORTANT: Keep your response concise. Limit your research to approximately {max_results} key findings."""

        # Invoke agent with timeout
        try:
            with tracer.start_as_current_span(
                "sota_researcher.agent_invoke"
            ) as invoke_span:
                invoke_span.set_attribute("sota_researcher.prompt_length", len(prompt))
                invoke_span.set_attribute(
                    "sota_researcher.timeout_seconds", RESEARCH_ONLY_TIMEOUT
                )

                result = await asyncio.wait_for(
                    agent.ainvoke({"messages": [{"role": "user", "content": prompt}]}),
                    timeout=RESEARCH_ONLY_TIMEOUT,
                )
                invoke_span.set_attribute("sota_researcher.completed", True)
        except TimeoutError:
            latency_ms = (time.perf_counter() - start_time) * 1000
            span.set_attribute("sota_researcher.latency_ms", latency_ms)
            span.set_attribute("sota_researcher.timed_out", True)
            span.set_attribute("sota_researcher.timeout_seconds", RESEARCH_ONLY_TIMEOUT)
            logger.error(f"Research only timed out after {RESEARCH_ONLY_TIMEOUT}s")
            return {
                "success": False,
                "error": f"Research timed out after {RESEARCH_ONLY_TIMEOUT} seconds. "
                "The agent may be stuck in a loop. Try a more specific topic or increase timeout.",
                "latency_ms": latency_ms,
                "timed_out": True,
            }
        except Exception as e:
            logger.error(f"Agent invocation failed: {e}", exc_info=True)
            raise RuntimeError(
                f"Research failed: {e}. "
                "This may indicate an issue with the agent, MCP tools, or model. "
                "Check logs for details and verify MCP servers are running."
            ) from e

        # Extract final message
        final_message = result["messages"][-1]
        content = (
            final_message.content
            if hasattr(final_message, "content")
            else str(final_message)
        )

        # Measure latency
        latency_ms = (time.perf_counter() - start_time) * 1000
        span.set_attribute("sota_researcher.latency_ms", latency_ms)

        return {
            "success": True,
            "results": {
                "agent_response": content,
                "messages": [str(msg) for msg in result["messages"]],
            },
            "latency_ms": latency_ms,
        }


# Create FastMCP server
if MCP_AVAILABLE:
    mcp = FastMCP("sota_researcher_v2", json_response=True)

    # Store references to underlying functions
    _research_and_plan_impl = research_and_plan
    _research_only_impl = research_only

    # Note: Using Optional[...] instead of | None for FastMCP compatibility
    # FastMCP's type validation fails with union types using | None syntax
    # The normalization code handles type conversion, but FastMCP validates before function execution
    @mcp.tool()
    async def research_and_plan(
        topic: str,
        research_questions: list[str] | None = None,  # noqa: UP007  # FastMCP requires Optional, not | None
        output_path: str | None = None,  # noqa: UP007  # FastMCP requires Optional, not | None
    ) -> dict[str, Any]:
        """Conduct SOTA research and create a plan.

        Args:
            topic: Research topic (required). The main subject to research.
            research_questions: Optional list of specific research questions (list of strings).
                - If None or not provided: No specific questions, general research will be conducted.
                - If a list: Each item should be a string question (e.g., ["Question 1", "Question 2"]).
                - If a single string: Will be normalized to a list with one question.
                - The function automatically normalizes various input formats.
            output_path: Optional path to save research results (string or None).

        Returns:
            dict with research results and plan containing:
            - success: bool - Whether research succeeded
            - research_results: dict - Research findings (agent-generated content)
            - plan: dict - Generated plan (agent-created)
            - latency_ms: float - Research latency in milliseconds

        Example:
            # Basic usage
            research_and_plan(topic="Vector search optimization")

            # With specific questions
            research_and_plan(
                topic="LanceDB best practices",
                research_questions=["What are best practices?", "How to optimize performance?"]
            )
        """
        # Normalize research_questions for FastMCP compatibility
        # Use comprehensive normalization function to handle all edge cases
        normalized_questions = _normalize_research_questions(research_questions)

        return await _research_and_plan_impl(topic, normalized_questions, output_path)

    @mcp.tool()
    async def research_only(
        topic: str,
        max_results: int = 10,
    ) -> dict[str, Any]:
        """Conduct research only (no planning).

        Args:
            topic: Research topic
            max_results: Maximum number of research results

        Returns:
            dict with research results
        """
        return await _research_only_impl(topic, max_results)

    # MCP Prompts - These expose as slash commands in Gemini CLI
    # Usage: /research "your topic" or /deep_plan "topic" "questions"

    @mcp.prompt()
    def research(topic: str) -> list[dict[str, Any]]:
        """Quick research on a topic.

        Usage: /research "LanceDB best practices"

        Args:
            topic: The topic to research

        Returns:
            A prompt message for the model to execute research
        """
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Use the research_only tool to research the following topic and provide a concise summary:

**Topic:** {topic}

After getting the research results, synthesize the key findings into actionable insights.""",
                },
            }
        ]

    @mcp.prompt()
    def deep_plan(topic: str, questions: str = "") -> list[dict[str, Any]]:
        """Deep research with implementation plan.

        Usage: /deep_plan "Authentication system" "What are best practices? How to implement OAuth?"

        Args:
            topic: The main topic to research
            questions: Optional semicolon-separated research questions

        Returns:
            A prompt message for comprehensive research and planning
        """
        prompt_text = f"""Use the research_and_plan tool to conduct comprehensive SOTA research and create an implementation plan.

**Topic:** {topic}
"""
        if questions:
            # Split questions by semicolon and format as list
            question_list = [q.strip() for q in questions.split(";") if q.strip()]
            if question_list:
                prompt_text += "\n**Research Questions:**\n"
                for q in question_list:
                    prompt_text += f"- {q}\n"

        prompt_text += """
After getting the research results:
1. Summarize the key findings
2. Identify actionable next steps
3. Create a prioritized implementation plan"""

        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": prompt_text,
                },
            }
        ]

else:
    mcp = None


if __name__ == "__main__":
    if MCP_AVAILABLE and mcp:
        mcp.run(transport="stdio")
    else:
        print("MCP not available")
