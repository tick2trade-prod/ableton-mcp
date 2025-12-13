#!/usr/bin/env python3
"""MCP server for Research MCP.

FastMCP protocol setup and tool exposure with:
- Web search via Tavily
- Result caching
- Summarization via Ollama
- Slash commands via MCP prompts
"""

import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Initialize logger
logger = logging.getLogger("research-mcp")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Strict import: FastMCP required
try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise ImportError(f"FastMCP is required: {e}. Install with: uv add mcp") from e

from scripts.research_mcp.core import get_core
from scripts.research_mcp.settings import get_settings

# Initialize FastMCP server
mcp = FastMCP("research_mcp", json_response=True)


@mcp.tool()
async def search_web(
    query: str,
    max_results: int = 10,
) -> dict[str, Any]:
    """Search the web using Tavily API.

    Args:
        query: Search query (required)
        max_results: Maximum results to return (1-50, default: 10)

    Returns:
        dict with search results containing:
        - success: bool
        - query: str
        - results: list of {title, url, content, score}
        - result_count: int
        - latency_ms: float

    Example:
        search_web("Python async best practices")
    """
    core = get_core()
    return await core.search_web(query, max_results)


@mcp.tool()
async def research(
    topic: str,
    questions: list[str] | None = None,
    max_results: int = 10,
    summarize: bool = True,
) -> dict[str, Any]:
    """Research a topic comprehensively.

    Searches the web for the topic and optional specific questions,
    deduplicates results, and optionally summarizes findings.

    Args:
        topic: Main research topic (required)
        questions: Optional list of specific research questions
        max_results: Maximum results per search (1-50, default: 10)
        summarize: Whether to summarize results (default: True)

    Returns:
        dict with research results containing:
        - success: bool
        - topic: str
        - results: list of {title, url, content, score}
        - result_count: int
        - summary: str (if summarize=True and Ollama available)
        - latency_ms: float

    Example:
        research("LLM fine-tuning", questions=["Best practices?", "Common pitfalls?"])
    """
    core = get_core()
    return await core.research_topic(topic, questions, max_results, summarize)


@mcp.tool()
async def summarize_text(
    content: str,
    style: str = "concise",
    max_length: int = 500,
) -> dict[str, Any]:
    """Summarize text content using Ollama.

    Args:
        content: Text content to summarize (required)
        style: Summary style - "concise", "detailed", or "bullet_points" (default: concise)
        max_length: Maximum summary length in words (default: 500)

    Returns:
        dict with summary containing:
        - success: bool
        - summary: str
        - style: str
        - model: str
        - latency_ms: float

    Example:
        summarize_text("Long article text here...", style="bullet_points")
    """
    core = get_core()
    return await core.summarize(content, style, max_length)


@mcp.tool()
async def get_research_status() -> dict[str, Any]:
    """Get Research MCP status and configuration.

    Returns:
        dict with status information:
        - tavily_configured: bool
        - ollama_enabled: bool
        - ollama_model: str
        - cache_enabled: bool (redis or disk)
        - max_results: int

    Example:
        get_research_status()
    """
    settings = get_settings()
    core = get_core()

    return {
        "success": True,
        "tavily_configured": bool(settings.tavily_api_key),
        "ollama_enabled": settings.use_ollama,
        "ollama_model": settings.ollama_model,
        "ollama_url": settings.ollama_base_url,
        "redis_enabled": settings.use_redis,
        "cache_dir": str(settings.cache_dir),
        "max_results": settings.max_results,
        "timeout_seconds": settings.timeout_seconds,
    }


# MCP Prompts - Slash commands for Gemini CLI
# Usage: /research_topic "topic" or /quick_search "query"


@mcp.prompt()
def research_topic(topic: str, questions: str = "") -> list[dict[str, Any]]:
    """Research a topic using web search.

    Usage: /research_topic "Python async patterns" "Best practices; Common mistakes"

    Args:
        topic: The topic to research
        questions: Optional semicolon-separated research questions

    Returns:
        Prompt for the model to execute research
    """
    question_list = []
    if questions:
        question_list = [q.strip() for q in questions.split(";") if q.strip()]

    prompt_text = f"""Use the research tool to investigate the following topic:

**Topic:** {topic}
"""
    if question_list:
        prompt_text += "\n**Research Questions:**\n"
        for q in question_list:
            prompt_text += f"- {q}\n"

    prompt_text += """
After getting the research results, provide:
1. Key findings summary
2. Actionable insights
3. Recommended next steps"""

    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": prompt_text,
            },
        }
    ]


@mcp.prompt()
def quick_search(query: str) -> list[dict[str, Any]]:
    """Quick web search.

    Usage: /quick_search "how to implement OAuth2 in Python"

    Args:
        query: The search query

    Returns:
        Prompt for quick search
    """
    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"""Use the search_web tool to search for: "{query}"

Summarize the top results and extract the most relevant information.""",
            },
        }
    ]


if __name__ == "__main__":
    logger.info("Starting Research MCP server...")
    mcp.run(transport="stdio")
