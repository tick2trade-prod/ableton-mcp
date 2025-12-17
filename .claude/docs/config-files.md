# Claude Configuration Files

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Directory Structure

```
project/
├── .claude/
│   ├── settings.local.json   # Project settings
│   └── docs/                  # This documentation
├── CLAUDE.md                  # Project context
└── ...
```

## settings.local.json

Project-specific permissions and settings:
```json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(python:*)"
    ],
    "deny": [],
    "confirm": []
  }
}
```

## CLAUDE.md

Project context and rules:
```markdown
# ableton-mcp

## Project Description
Ableton Live integration via MCP.

## Rules
- No mocks in tests
- Conventional commits
- Type hints required

## Common Commands
- `make check-port` - Verify Ableton
- `pytest tests/` - Run tests
```

## Global Configuration

`~/.claude/settings.json`:
```json
{
  "model": "claude-sonnet-4-20250514",
  "telemetry": false
}
```

## ableton-mcp Files

Current project configuration:
- `.claude/settings.local.json` - Permissions
- `GEMINI.md` - Project rules (also used by Claude)

## Related Pages

- [Configuration](configuration.md) - All settings
- [Permissions](permissions.md) - Command permissions
- [Memory](memory.md) - CLAUDE.md usage
