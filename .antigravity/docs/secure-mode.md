# Secure Mode

> Source: [https://antigravity.google/docs/secure-mode](https://antigravity.google/docs/secure-mode)

## Overview

Secure Mode restricts agent capabilities for sensitive operations or production environments.

## When to Use Secure Mode

- Production deployments
- Sensitive code handling
- Shared environments
- Compliance requirements

## Secure Mode Features

### Command Restrictions
- All commands require explicit approval
- No auto-run capabilities
- Command history logging

### File Access Control
- Read-only by default
- Write requires approval
- No access to system files

### Network Restrictions
- Limited external requests
- No browser subagent
- MCP tools require approval

## Configuration

Enable secure mode in settings:
```json
{
  "agent": {
    "secureMode": true,
    "allowedCommands": [
      "pytest",
      "git status",
      "make check-*"
    ],
    "allowedPaths": [
      "./tests/",
      "./src/"
    ]
  }
}
```

## ableton-mcp Considerations

### When to Use Secure Mode

| Scenario | Secure Mode |
|----------|-------------|
| Development | Off |
| Testing | Off |
| Live Ableton session | Consider On |
| Production scripts | On |

### Safe Operations (No Secure Mode Needed)
- Running pytest
- Viewing files
- Git status/diff

### Sensitive Operations (Consider Secure Mode)
- Modifying track scripts
- Executing in live Ableton
- Network requests

## Best Practices

### 1. Default to Open Development
For this project, secure mode is generally not needed during development.

### 2. Enable for Live Sessions
If running scripts against live Ableton projects:
```json
{
  "agent": {
    "secureMode": true,
    "confirmBefore": ["run_command"]
  }
}
```

### 3. Log All Actions
```json
{
  "logging": {
    "commands": true,
    "fileChanges": true,
    "mcpCalls": true
  }
}
```

## Related Pages

- [Agent Modes / Settings](agent-modes-settings.md) - Configuration
- [Agent](agent.md) - Agent capabilities
