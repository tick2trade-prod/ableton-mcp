# Claude Vision

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Claude can understand and analyze images.

## Capabilities

- Screenshot analysis
- Diagram interpretation
- UI review
- Error screenshot debugging

## Usage

### CLI
```bash
claude "Explain this error" -i screenshot.png
```

### API
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"data": base64_image}},
            {"type": "text", "text": "Explain this error"}
        ]
    }]
)
```

## ableton-mcp Use Cases

### Ableton Screenshots
```
"Here's a screenshot of my Ableton session.
What's wrong with the routing?"
```

### Error Screenshots
```
"This error appears in Ableton. What does it mean?"
```

### Documentation
```
"Extract the parameter names from this device screenshot"
```

## Supported Formats

- PNG
- JPEG
- GIF
- WebP

## Related Pages

- [Commands](commands.md) - CLI usage
- [API](api.md) - API integration
