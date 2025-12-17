# Claude API Usage

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Direct API Access

### Python Client
```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
print(response.content[0].text)
```

### Installation
```bash
pip install anthropic
```

## API vs CLI

| Feature | API | CLI |
|---------|-----|-----|
| Integration | Custom apps | Terminal |
| Tool use | Manual | Built-in |
| File context | Manual | Automatic |
| Best for | Automation | Development |

## Tool Use via API

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[{
        "name": "search_ableton_docs",
        "description": "Search Ableton documentation",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            }
        }
    }],
    messages=[
        {"role": "user", "content": "Search for sidechain compression"}
    ]
)
```

## ableton-mcp Integration

For this project, prefer:
- **CLI** for interactive development
- **API** for automation scripts
- **MCP** for tool integration

## Related Pages

- [Commands](commands.md) - CLI usage
- [Tool Use](tool-use.md) - Function calling
- [MCP](mcp.md) - MCP integration
