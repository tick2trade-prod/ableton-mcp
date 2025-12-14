#!/usr/bin/env python3
"""MCP server for Ableton Code Generation.

FastMCP protocol with tools for:
- Embedding Ableton documentation into Redis
- Searching embedded docs and web guides
- AST-based code generation for track creation
"""

import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Initialize logger
logger = logging.getLogger("ableton-codegen-mcp")
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

from scripts.ableton_cache_ast_codegen_mcp.code_generator import AbletonCodeGenerator
from scripts.ableton_cache_ast_codegen_mcp.pdf_embeddings import AbletonDocEmbeddings
from scripts.ableton_cache_ast_codegen_mcp.settings import get_settings
from scripts.ableton_cache_ast_codegen_mcp.web_search import AbletonWebSearch

# Initialize FastMCP server
mcp = FastMCP("ableton_codegen", json_response=True)

# Lazy-initialized components
_embeddings: AbletonDocEmbeddings | None = None
_web_search: AbletonWebSearch | None = None
_code_generator: AbletonCodeGenerator | None = None


def _get_embeddings() -> AbletonDocEmbeddings:
    """Get or create embeddings instance."""
    global _embeddings
    if _embeddings is None:
        settings = get_settings()
        _embeddings = AbletonDocEmbeddings(
            pdf_path=settings.pdf_path,
            redis_url=settings.redis_url,
            index_name=settings.redis_index_name,
            embedding_model=settings.embedding_model,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
    return _embeddings


def _get_web_search() -> AbletonWebSearch:
    """Get or create web search instance."""
    global _web_search
    if _web_search is None:
        settings = get_settings()
        _web_search = AbletonWebSearch(
            tavily_api_key=settings.tavily_api_key,
            max_results=settings.max_search_results,
        )
    return _web_search


def _get_code_generator() -> AbletonCodeGenerator:
    """Get or create code generator instance."""
    global _code_generator
    if _code_generator is None:
        settings = get_settings()
        _code_generator = AbletonCodeGenerator(
            scripts_dir=settings.track_scripts_dir,
            mcp_server_path=settings.mcp_server_path,
        )
    return _code_generator


# ============================================================================
# PDF Embedding Tools
# ============================================================================


@mcp.tool()
async def embed_ableton_docs(
    pdf_path: str | None = None,
) -> dict[str, Any]:
    """Embed Ableton Live manual into Redis vector store.

    Extracts text from the PDF, chunks it, generates embeddings,
    and stores in Redis for semantic search.

    Args:
        pdf_path: Optional custom PDF path (default: docs/live12-manual-en.pdf)

    Returns:
        dict with embedding stats:
        - success: bool
        - chunks_stored: int
        - total_pages: int
        - total_elapsed_seconds: float

    Example:
        embed_ableton_docs()
    """
    embeddings = _get_embeddings()

    if pdf_path:
        embeddings.pdf_path = Path(pdf_path)

    try:
        result = await embeddings.embed_document()
        return result
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def search_ableton_docs(
    query: str,
    top_k: int = 5,
) -> dict[str, Any]:
    """Search embedded Ableton documentation.

    Args:
        query: Search query (e.g., "how to use Roar device")
        top_k: Number of results to return (default: 5)

    Returns:
        dict with search results:
        - success: bool
        - results: list of {text, page_num, section, similarity}
        - latency_ms: float

    Example:
        search_ableton_docs("sidechain compression setup")
    """
    embeddings = _get_embeddings()
    return await embeddings.search_docs(query, top_k)


@mcp.tool()
async def get_docs_index_stats() -> dict[str, Any]:
    """Get statistics about the embedded documentation index.

    Returns:
        dict with index stats:
        - total_chunks: int
        - embedding_model: str
        - pdf_path: str
        - indexed_at: timestamp

    Example:
        get_docs_index_stats()
    """
    embeddings = _get_embeddings()
    return embeddings.get_index_stats()


# ============================================================================
# Web Search Tools
# ============================================================================


@mcp.tool()
async def search_ableton_guides(
    query: str,
    max_results: int = 10,
) -> dict[str, Any]:
    """Search for Ableton engineering guides and tutorials.

    Prioritizes results from ableton.com, musicradar, studiobrootle.

    Args:
        query: Search query (e.g., "techno rumble kick")
        max_results: Maximum results (default: 10)

    Returns:
        dict with search results:
        - success: bool
        - results: list of {title, url, content, score}
        - latency_ms: float

    Example:
        search_ableton_guides("Roar multiband saturation tutorial")
    """
    web_search = _get_web_search()
    return await web_search.search_ableton_guides(query, max_results)


@mcp.tool()
async def search_device_docs(
    device_name: str,
    aspect: str = "",
) -> dict[str, Any]:
    """Search for specific Ableton device documentation.

    Args:
        device_name: Device name (Roar, Meld, Drift, etc.)
        aspect: Optional specific aspect (modulation, filters, etc.)

    Returns:
        dict with device-specific results

    Example:
        search_device_docs("Roar", "multiband saturation")
    """
    web_search = _get_web_search()
    return await web_search.search_device_documentation(device_name, aspect)


@mcp.tool()
async def search_production_technique(
    technique: str,
    genre: str = "techno",
) -> dict[str, Any]:
    """Search for production technique tutorials.

    Args:
        technique: Technique name (e.g., "sidechain compression")
        genre: Genre context (default: "techno")

    Returns:
        dict with technique-focused results

    Example:
        search_production_technique("rumble kick", "techno")
    """
    web_search = _get_web_search()
    return await web_search.search_production_technique(technique, genre)


# ============================================================================
# Code Generation Tools
# ============================================================================


@mcp.tool()
async def analyze_track_script(
    script_path: str,
) -> dict[str, Any]:
    """Analyze a track creation script and extract MCP tool patterns.

    Args:
        script_path: Path to Python script to analyze

    Returns:
        dict with pattern info:
        - track_type: str
        - track_name: str
        - tool_calls: list of {tool_name, args, line_number}

    Example:
        analyze_track_script("live_set/lily_palmer/i_am_machine/track_01_kick.py")
    """
    generator = _get_code_generator()
    try:
        pattern = await generator.analyze_script(script_path)
        return {
            "success": True,
            **pattern.to_dict(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def analyze_all_track_scripts() -> dict[str, Any]:
    """Analyze all track scripts in the configured directory.

    Returns:
        dict with analysis results:
        - patterns: list of pattern dicts
        - total_scripts: int
        - total_tool_calls: int

    Example:
        analyze_all_track_scripts()
    """
    generator = _get_code_generator()
    patterns = await generator.analyze_all_scripts()

    total_tool_calls = sum(len(p.tool_calls) for p in patterns)

    return {
        "success": True,
        "patterns": [p.to_dict() for p in patterns],
        "total_scripts": len(patterns),
        "total_tool_calls": total_tool_calls,
    }


@mcp.tool()
async def generate_track_code(
    track_spec: dict[str, Any],
) -> dict[str, Any]:
    """Generate Python code for creating an Ableton track.

    Args:
        track_spec: Track specification with:
            - name: Track name
            - type: Track type (kick, snare, bass, etc.)
            - index: Track index (-1 for end)
            - devices: List of devices to load
            - notes: Optional note data

    Returns:
        dict with generated code:
        - success: bool
        - code: str
        - validation: dict

    Example:
        generate_track_code({
            "name": "Kick",
            "type": "kick",
            "index": 0,
            "devices": [{"name": "Drum Sampler"}]
        })
    """
    generator = _get_code_generator()

    # Find similar patterns if possible
    patterns = await generator.analyze_all_scripts()
    track_type = track_spec.get("type", "unknown")
    similar = generator.find_similar_patterns(track_type, patterns)

    reference = similar[0] if similar else None

    # Generate code
    code = generator.generate_track_code(track_spec, reference)

    # Validate
    validation = await generator.validate_code(code)

    return {
        "success": validation["valid"],
        "code": code,
        "validation": validation,
        "reference_pattern": reference.source_file if reference else None,
    }


@mcp.tool()
async def validate_track_code(
    code: str,
) -> dict[str, Any]:
    """Validate generated track creation code.

    Args:
        code: Python code string to validate

    Returns:
        dict with validation results:
        - valid: bool
        - errors: list of error messages
        - warnings: list of warnings
        - tool_calls_count: int

    Example:
        validate_track_code("async def create_track(): ...")
    """
    generator = _get_code_generator()
    return await generator.validate_code(code)


# ============================================================================
# Status Tool
# ============================================================================


@mcp.tool()
async def get_codegen_status() -> dict[str, Any]:
    """Get Ableton Code Generation MCP status.

    Returns:
        dict with status info:
        - pdf_configured: bool
        - redis_available: bool
        - tavily_configured: bool
        - scripts_dir_exists: bool

    Example:
        get_codegen_status()
    """
    settings = get_settings()

    return {
        "success": True,
        "pdf_path": str(settings.pdf_path),
        "pdf_exists": settings.pdf_path.exists(),
        "redis_url": settings.redis_url,
        "tavily_configured": bool(settings.tavily_api_key),
        "scripts_dir": str(settings.track_scripts_dir),
        "scripts_dir_exists": settings.track_scripts_dir.exists(),
        "embedding_model": settings.embedding_model,
        "ollama_enabled": settings.use_ollama,
    }


# ============================================================================
# MCP Prompts (Slash Commands)
# ============================================================================


@mcp.prompt()
def ableton_research(topic: str) -> list[dict[str, Any]]:
    """Research Ableton production topic.

    Usage: /ableton_research "rumble kick creation"
    """
    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"""Research the following Ableton production topic:

**Topic:** {topic}

Use these tools in order:
1. search_ableton_docs("{topic}") - Check embedded manual
2. search_ableton_guides("{topic}") - Find online tutorials
3. Synthesize findings into actionable steps""",
            },
        }
    ]


@mcp.prompt()
def generate_track(track_type: str, track_name: str) -> list[dict[str, Any]]:
    """Generate code for an Ableton track.

    Usage: /generate_track "kick" "Main Kick"
    """
    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"""Generate Ableton track creation code:

**Track Type:** {track_type}
**Track Name:** {track_name}

Use these tools:
1. analyze_all_track_scripts() - Find reference patterns
2. search_ableton_docs("{track_type}") - Get device recommendations
3. generate_track_code() - Create the code""",
            },
        }
    ]


if __name__ == "__main__":
    logger.info("Starting Ableton Code Generation MCP server...")
    mcp.run(transport="stdio")
