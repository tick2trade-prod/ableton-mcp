# Claude MCP Integration

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Claude supports the Model Context Protocol (MCP) for extending its capabilities with external tools and data sources.

## MCP in Claude

### Configuration

MCP servers are configured in Claude's settings:

```json
{
  "mcpServers": {
    "your-server": {
      "command": "python",
      "args": ["-m", "your_mcp_server"],
      "env": {}
    }
  }
}
```

### Server Types

1. **Stdio Transport**: Local process communication
2. **HTTP Transport**: Remote server communication

## ableton-mcp Integration

### Configured Servers

```json
{
  "mcpServers": {
    "ableton_codegen": {
      "command": "python",
      "args": ["-m", "mcp_servers.ableton_codegen.server"]
    },
    "research_mcp": {
      "command": "python",
      "args": ["-m", "mcp_servers.research_mcp.server"]
    },
    "sota_researcher_v2": {
      "command": "python",
      "args": ["-m", "mcp_servers.sota_researcher_v2.server"]
    }
  }
}
```

### Tool Usage

Claude can call MCP tools directly:

```
USER: Search the Ableton docs for sidechain compression
CLAUDE: I'll use the search_ableton_docs tool...
[Calls MCP tool]
[Returns results]
```

## Building MCP Servers for Claude

### Basic Structure

```python
from mcp import Server

server = Server("your-server")

@server.tool()
async def your_tool(param: str) -> dict:
    """Tool description that Claude will see."""
    return {"result": "success"}

if __name__ == "__main__":
    server.run()
```

### Best Practices

1. **Clear Documentation**: Write detailed docstrings
2. **Type Hints**: Use proper type annotations
3. **Error Handling**: Return structured errors
4. **Idempotency**: Make tools safe to retry

## Ollama + Claude + MCP

Combine Claude's capabilities with local Ollama:

```python
@server.tool()
async def summarize_locally(text: str) -> dict:
    """Summarize using local Ollama for privacy."""
    result = await query_ollama(text)
    return {"summary": result}
```

## Related Pages

- [Tool Use](tool-use.md) - General tool usage
- [Permissions](permissions.md) - Tool permissions
- [Configuration](configuration.md) - MCP config details
