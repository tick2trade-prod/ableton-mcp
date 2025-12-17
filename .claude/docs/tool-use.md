# Tool Use in Claude

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Claude can use tools (functions) to interact with external systems and data sources.

## How Tool Use Works

1. **Define tools** with schemas
2. **Claude decides** when to use tools
3. **Execute** tool with provided arguments
4. **Process** tool results

## Tool Definition

### Schema Structure

```json
{
  "name": "search_ableton_docs",
  "description": "Search Ableton Live documentation for a topic",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query"
      },
      "top_k": {
        "type": "integer",
        "description": "Number of results to return",
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

### Good Descriptions

```
# Good - Specific and actionable
"Search Ableton Live documentation for a topic. Returns relevant passages with page numbers."

# Poor - Vague
"Search docs"
```

## MCP Tools

MCP servers provide tools automatically:

```python
@server.tool()
async def get_session_info() -> dict:
    """Get current Ableton Live session information.

    Returns:
        dict with tempo, time_signature, and track_count
    """
    # Implementation
```

## Tool Use Patterns

### Research Pattern

```
USER: What's the best way to set up sidechain compression?

CLAUDE: I'll search the documentation...
[Uses search_ableton_docs tool]
[Returns structured information]
```

### Multi-Tool Pattern

```
USER: Create a new track with appropriate effects

CLAUDE: I'll need to:
1. [Uses search_ableton_docs for best practices]
2. [Uses create_track to make the track]
3. [Uses load_device for each effect]
```

### Verification Pattern

```
USER: Create a kick track

CLAUDE:
1. [Uses create_track]
2. [Uses get_session_info to verify]
Result: Track created successfully at index 0
```

## Error Handling

### Tool Failures

```python
@server.tool()
async def create_track(name: str) -> dict:
    try:
        result = await ableton_client.create_track(name)
        return {"success": True, "track_index": result}
    except ConnectionError as e:
        return {"success": False, "error": str(e)}
```

### Graceful Degradation

Claude handles tool failures gracefully:
- Reports errors to user
- Suggests alternatives
- Doesn't crash on failures

## Best Practices

### 1. Return Structured Data

```python
# Good
return {
    "success": True,
    "data": {...},
    "message": "Track created"
}

# Poor
return "Track created successfully"
```

### 2. Include Context

```python
return {
    "tempo": 120,
    "source": "Ableton Live session",
    "timestamp": datetime.now().isoformat()
}
```

### 3. Handle Edge Cases

```python
if not track_name:
    return {"error": "Track name is required"}
```

### 4. Document Expected Behavior

Include examples in docstrings:
```python
"""
Get track device chain.

Example:
    >>> get_device_chain(0)
    {"devices": ["EQ Eight", "Compressor"]}
"""
```

## Related Pages

- [MCP Integration](mcp.md) - MCP-based tools
- [Best Practices](best-practices.md) - Usage patterns
- [Error Handling](error-handling.md) - Handling failures
