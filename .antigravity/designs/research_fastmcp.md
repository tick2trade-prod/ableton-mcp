# FastMCP Research Summary

> Research conducted: 2025-12-16
> Source: https://gofastmcp.com

## What is FastMCP?

FastMCP is the fast, Pythonic way to build MCP (Model Context Protocol) servers. It provides decorators and patterns that simplify MCP server creation.

## Core Patterns

### 1. Server Creation
```python
from fastmcp import FastMCP
mcp = FastMCP("My MCP Server")
```

### 2. Tool Definition
```python
@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### 3. Resource Templates
```python
@mcp.resource("weather://{city}/current")
def get_weather(city: str) -> dict:
    """Provides weather information for a specific city."""
    return {"city": city, "temperature": 22}
```

### 4. Running the Server
```python
if __name__ == "__main__":
    mcp.run()
```

## Key Differences from Current ableton-mcp

| Current Approach | FastMCP Approach |
|------------------|------------------|
| Manual socket communication | Decorator-based tools |
| Custom protocol handling | Standard MCP protocol |
| Complex error handling | Built-in error handling |
| Manual JSON serialization | Automatic serialization |

## Resources vs Tools

| Concept | Purpose | Example |
|---------|---------|---------|
| **Tools** | Actions that modify state | `separate_stems()`, `create_track()` |
| **Resources** | Read-only data access | `stems://{song}/drums`, `track://{index}/info` |

## Recommended Project Structure for ableton-fastmcp

```
ableton-fastmcp/
├── src/
│   ├── __init__.py
│   ├── server.py           # FastMCP server entry point
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── session.py      # Session tools
│   │   ├── tracks.py       # Track manipulation
│   │   ├── devices.py      # Device loading
│   │   └── stems.py        # NEW: Stem separation
│   └── resources/
│       ├── __init__.py
│       ├── stems.py        # Stem file access
│       └── tracks.py       # Track info resources
├── agents/                  # Ollama-based agents
├── tests/
├── pyproject.toml
└── GEMINI.md
```

## Integration Points for Existing Agents

The current agents in `dearpygui_controller/agents/` use:
- `BaseAgent` with `ollama_model` parameter
- `get_mcp_client()` method for MCP access
- Async `execute()` pattern

These can integrate with FastMCP by:
1. Using FastMCP tools instead of direct socket calls
2. Keeping Ollama for reasoning/suggestions
3. Using FastMCP resources for stem file access

## Next Steps for Research

1. [ ] Review FastMCP authentication patterns
2. [ ] Check FastMCP streaming support for long operations
3. [ ] Investigate FastMCP Cloud for potential deployment
4. [ ] Review FastMCP context manager patterns
