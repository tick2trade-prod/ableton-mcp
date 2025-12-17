# Claude Configuration

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Configuration Files

### Project Settings
`.claude/settings.local.json`

### Global Settings
`~/.claude/settings.json`

## Key Settings

### Permissions
```json
{
  "permissions": {
    "allow": ["Bash(pytest:*)"],
    "deny": ["Bash(rm -rf:*)"]
  }
}
```

### Model Selection
```json
{
  "model": "claude-sonnet-4-20250514"
}
```

### Context
```json
{
  "context": {
    "maxFiles": 50,
    "maxTokens": 100000
  }
}
```

## Environment Variables

```bash
export ANTHROPIC_API_KEY=your_key
export CLAUDE_MODEL=claude-sonnet-4-20250514
```

## ableton-mcp Configuration

Current project settings:
```json
{
  "permissions": {
    "allow": [
      "Bash(uv pip install:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(grep:*)"
    ]
  }
}
```

## Related Pages

- [Permissions](permissions.md) - Permission details
- [Installation](installation.md) - Setup
- [Best Practices](best-practices.md) - Usage patterns
