# Claude Streaming

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Streaming provides real-time response output.

## CLI Streaming

Enabled by default in interactive mode:
```bash
claude
> Generate a long explanation
[Response streams in real-time]
```

## API Streaming

```python
from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Explain MCP in detail"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Benefits

- **Responsive**: See output immediately
- **Cancelable**: Stop generation early
- **Progressive**: Process as received

## Use Cases

### Long responses
Stream to avoid waiting.

### Interactive development
See Claude's thinking process.

### UI integration
Update display progressively.

## Related Pages

- [API](api.md) - API usage
- [Commands](commands.md) - CLI usage
