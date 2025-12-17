# Gemini CLI Configuration

> Source: [https://geminicli.com/docs/get-started/configuration](https://geminicli.com/docs/get-started/configuration)

## Configuration Files

### Global Settings
`~/.gemini/settings.json`

### Project Settings
`.gemini/settings.json` in project root

## Key Settings

### Model Selection

```json
{
  "model": "gemini-2.5-pro"
}
```

Available models:
- `gemini-2.5-pro` - Most capable
- `gemini-2.5-flash` - Fast responses
- `gemini-2.0-flash` - Balanced

### MCP Servers

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["-m", "my_server"],
      "env": {},
      "trust": false
    }
  }
}
```

### Theme

```json
{
  "theme": "dark"
}
```

### Telemetry

```json
{
  "telemetry": false
}
```

## ableton-mcp Configuration

### Recommended Settings

```json
{
  "model": "gemini-2.5-pro",
  "theme": "dark",
  "mcpServers": {
    "ableton_codegen": {
      "command": "python",
      "args": ["-m", "mcp_servers.ableton_codegen.server"],
      "env": {
        "REDIS_URL": "redis://localhost:6379"
      }
    },
    "research_mcp": {
      "command": "python",
      "args": ["-m", "mcp_servers.research_mcp.server"],
      "env": {
        "TAVILY_API_KEY": "$TAVILY_API_KEY"
      }
    },
    "sota_researcher_v2": {
      "command": "python",
      "args": ["-m", "mcp_servers.sota_researcher_v2.server"]
    }
  },
  "mcp": {
    "allowed": ["ableton_codegen", "research_mcp", "sota_researcher_v2"]
  }
}
```

### Environment Variables

```bash
# .env or ~/.bashrc
export GOOGLE_API_KEY=your_api_key
export REDIS_URL=redis://localhost:6379
export TAVILY_API_KEY=your_tavily_key
export OLLAMA_BASE_URL=http://localhost:11434
```

## Configuration Hierarchy

1. **Command line flags** (highest priority)
2. **Project settings** (`.gemini/settings.json`)
3. **Global settings** (`~/.gemini/settings.json`)
4. **Environment variables**
5. **Defaults**

## Common Configurations

### Development

```json
{
  "model": "gemini-2.5-pro",
  "confirmToolCalls": true,
  "telemetry": false
}
```

### Automation

```json
{
  "model": "gemini-2.5-flash",
  "confirmToolCalls": false,
  "headless": true
}
```

### Secure

```json
{
  "model": "gemini-2.5-pro",
  "confirmToolCalls": true,
  "sandbox": true
}
```

## Related Pages

- [Installation](installation.md) - Installation options
- [MCP](mcp.md) - MCP configuration details
- [Settings](settings.md) - All settings reference
