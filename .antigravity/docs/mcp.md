# MCP (Model Context Protocol)

> Source: [https://antigravity.google/docs/mcp](https://antigravity.google/docs/mcp)

## Overview

The Model Context Protocol (MCP) is a standard that connects AI systems with external tools and data sources. Antigravity has native MCP support, allowing you to extend agent capabilities with custom servers.

## MCP in ableton-mcp

This project uses MCP extensively for Ableton Live integration:

### Configured MCP Servers

| Server | Purpose |
|--------|---------|
| `ableton_codegen` | Generate Ableton track code, search docs |
| `research_mcp` | Web research with Tavily |
| `sota_researcher_v2` | Comprehensive research + planning |
| `deepagents` | Multi-agent orchestration |

### Available Tools

#### ableton_codegen
```python
# Search Ableton documentation
search_ableton_docs("sidechain compression")

# Generate track code
generate_track_code({
    "name": "Kick",
    "type": "kick",
    "devices": [{"name": "Drum Sampler"}]
})

# Analyze existing scripts
analyze_track_script("live_set/track_01_kick.py")
```

#### research_mcp
```python
# Quick web search
search_web("techno rumble bass tutorial")

# Comprehensive research
research("sidechain compression in Ableton",
         questions=["Best ratio settings?", "Attack time for techno?"])
```

#### sota_researcher_v2
```python
# Research with automatic planning
research_and_plan(
    topic="Ableton Live MIDI routing",
    research_questions=["How to route MIDI between tracks?"],
    output_path="research/midi_routing.md"
)
```

## Creating Custom MCP Servers

### Server Structure

```
mcp_servers/
├── your_server/
│   ├── __init__.py
│   ├── server.py      # MCP server implementation
│   ├── tools.py       # Tool definitions
│   └── resources.py   # Resource definitions
```

### Basic Server Template

```python
# server.py
from mcp import Server, Tool
import asyncio

server = Server("your_server")

@server.tool()
async def your_tool(param: str) -> dict:
    """Tool description for the agent."""
    return {"result": f"Processed: {param}"}

if __name__ == "__main__":
    asyncio.run(server.run())
```

### Registration in Antigravity

Add to `.antigravity/mcp.json`:
```json
{
  "servers": {
    "your_server": {
      "command": "python",
      "args": ["-m", "mcp_servers.your_server.server"]
    }
  }
}
```

## Ollama + MCP Integration

Use Ollama for local LLM inference in MCP tools:

```python
import httpx

async def query_ollama(prompt: str, model: str = "llama3.2") -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
```

## Best Practices for ableton-mcp

### 1. Tool Design
- Keep tools focused and single-purpose
- Return structured data (dict, not strings)
- Include clear docstrings for agent understanding

### 2. Error Handling
```python
@server.tool()
async def safe_tool(param: str) -> dict:
    try:
        result = await process(param)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 3. Testing MCP Tools
```python
# tests/test_mcp_tools.py
import pytest

@pytest.mark.live
async def test_ableton_tool():
    result = await mcp_client.call("search_ableton_docs", {"query": "EQ Eight"})
    assert result["success"]
    assert len(result["results"]) > 0
```

## Related Pages

- [Agent](agent.md) - How agents use MCP tools
- [Rules / Workflows](rules-workflows.md) - Automating MCP tool usage
- [Terminal](terminal.md) - Running MCP servers locally
