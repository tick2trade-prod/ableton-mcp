# Settings

> Source: [https://geminicli.com/docs/cli/settings](https://geminicli.com/docs/cli/settings)

## Settings Location

- **Global**: `~/.gemini/settings.json`
- **Project**: `.gemini/settings.json`

## Opening Settings

```bash
gemini settings
```

Or in interactive mode:
```
/settings
```

## All Settings

### Model Settings
```json
{
  "model": "gemini-2.5-pro",
  "temperature": 0.7,
  "maxTokens": 8192
}
```

### MCP Settings
```json
{
  "mcpServers": {...},
  "mcp": {
    "allowed": [],
    "excluded": []
  }
}
```

### UI Settings
```json
{
  "theme": "dark",
  "colors": true,
  "markdown": true
}
```

### Tool Settings
```json
{
  "confirmToolCalls": true,
  "sandbox": false
}
```

### Telemetry
```json
{
  "telemetry": false
}
```

## ableton-mcp Settings

See [Configuration](configuration.md) for recommended project settings.

## Related Pages

- [Configuration](configuration.md) - Detailed config
- [Themes](themes.md) - Visual themes
- [Telemetry](telemetry.md) - Data collection
