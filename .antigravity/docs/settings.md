# Settings

> Source: [https://antigravity.google/docs/settings](https://antigravity.google/docs/settings)

## Overview

Configure Antigravity behavior through settings.

## Settings Categories

### Agent Settings
- Mode selection
- Model preferences
- Command approval

### Editor Settings
- Theme
- Font size
- Tab size

### MCP Settings
- Server configuration
- Tool enablement
- Timeout values

### Browser Settings
- Profile selection
- Allowlist/denylist
- Recording options

## Key Settings for ableton-mcp

### Agent Configuration
```json
{
  "agent": {
    "mode": "agentic",
    "autoApproveCommands": false,
    "defaultModel": "gemini-2.5-pro",
    "contextWindowSize": "large"
  }
}
```

### MCP Configuration
```json
{
  "mcp": {
    "timeout": 30000,
    "retries": 3,
    "servers": {
      "ableton_codegen": {"enabled": true},
      "research_mcp": {"enabled": true}
    }
  }
}
```

### Terminal Configuration
```json
{
  "terminal": {
    "shell": "/bin/zsh",
    "defaultCwd": "/Users/alexzh/ableton-mcp",
    "fontSize": 14
  }
}
```

### Ollama Configuration
```json
{
  "ollama": {
    "baseUrl": "http://localhost:11434",
    "model": "llama3.2",
    "timeout": 60000
  }
}
```

## Accessing Settings

- `Cmd+,` - Open settings
- Command palette → "Settings"

## Settings Files

### User Settings
Global settings across all workspaces.

### Workspace Settings
Project-specific settings in `.antigravity/settings.json`.

## Related Pages

- [Agent Modes / Settings](agent-modes-settings.md) - Agent config
- [MCP](mcp.md) - MCP configuration
- [Plans](plans.md) - Available features
