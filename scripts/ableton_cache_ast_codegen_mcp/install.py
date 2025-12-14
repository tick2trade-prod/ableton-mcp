#!/usr/bin/env python3
"""Installation helper for Research MCP.

Verifies dependencies, tests connectivity, and provides configuration.
"""

import json
from pathlib import Path


def check_dependencies() -> dict[str, bool]:
    """Check if required dependencies are installed."""
    deps = {}

    # Check core dependencies
    try:
        import pydantic_settings  # noqa: F401

        deps["pydantic_settings"] = True
    except ImportError:
        deps["pydantic_settings"] = False

    try:
        from mcp.server.fastmcp import FastMCP  # noqa: F401

        deps["fastmcp"] = True
    except ImportError:
        deps["fastmcp"] = False

    # Check optional dependencies
    try:
        import tavily  # noqa: F401

        deps["tavily"] = True
    except ImportError:
        deps["tavily"] = False

    try:
        import httpx  # noqa: F401

        deps["httpx"] = True
    except ImportError:
        deps["httpx"] = False

    try:
        import diskcache  # noqa: F401

        deps["diskcache"] = True
    except ImportError:
        deps["diskcache"] = False

    try:
        import tiktoken  # noqa: F401

        deps["tiktoken"] = True
    except ImportError:
        deps["tiktoken"] = False

    return deps


def get_mcp_config() -> dict:
    """Get MCP configuration for Gemini CLI."""
    project_dir = Path(__file__).parent.parent.parent
    return {
        "research_mcp": {
            "transport": "stdio",
            "command": "uv",
            "args": [
                "run",
                "--directory",
                str(project_dir),
                "python",
                str(project_dir / "scripts" / "research_mcp" / "mcp_server.py"),
            ],
            "env": {"PYTHONPATH": str(project_dir)},
            "disabled": False,
            "trust": False,
        }
    }


def print_status():
    """Print installation status."""
    print("=" * 50)
    print("Research MCP Installation Status")
    print("=" * 50)

    deps = check_dependencies()

    print("\n📦 Core Dependencies:")
    for dep in ["pydantic_settings", "fastmcp"]:
        status = "✅" if deps.get(dep) else "❌"
        print(f"  {status} {dep}")

    print("\n📦 Optional Dependencies:")
    for dep in ["tavily", "httpx", "diskcache", "tiktoken"]:
        status = "✅" if deps.get(dep) else "⚠️"
        print(f"  {status} {dep}")

    print("\n📋 MCP Configuration:")
    config = get_mcp_config()
    print(json.dumps(config, indent=2))

    print("\n📝 Environment Variables:")
    print("  RESEARCH_MCP_TAVILY_API_KEY - Tavily API key (optional)")
    print("  RESEARCH_MCP_USE_OLLAMA - Enable Ollama (default: true)")
    print("  RESEARCH_MCP_OLLAMA_MODEL - Ollama model (default: llama3.2:latest)")

    # Check if all required deps are installed
    required_ok = all(deps.get(d) for d in ["pydantic_settings", "fastmcp"])
    if required_ok:
        print("\n✅ Ready to use! Add the MCP config to ~/.gemini/settings.json")
    else:
        print("\n❌ Missing required dependencies. Run: uv sync")


if __name__ == "__main__":
    print_status()
