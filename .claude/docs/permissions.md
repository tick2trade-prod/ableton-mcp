# Claude Permissions

> Configuration for safe command execution in Claude Code.

## Overview

Permissions control what commands Claude can execute in your environment.

## Configuration File

Permissions are set in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [...],
    "deny": [...],
    "confirm": [...]
  }
}
```

## Permission Levels

### Allow
Commands that run without confirmation:
```json
{
  "allow": [
    "Bash(pytest:*)",
    "Bash(git status)",
    "Bash(grep:*)"
  ]
}
```

### Deny
Commands that are blocked entirely:
```json
{
  "deny": [
    "Bash(rm -rf:*)",
    "Bash(sudo:*)"
  ]
}
```

### Confirm
Commands that require user approval:
```json
{
  "confirm": [
    "Bash(git push:*)",
    "Bash(make deploy:*)"
  ]
}
```

## ableton-mcp Configuration

### Current Settings
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

### Recommended Additions

```json
{
  "permissions": {
    "allow": [
      // Existing
      "Bash(uv pip install:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(grep:*)",

      // Testing
      "Bash(pytest:*)",
      "Bash(make test:*)",
      "Bash(make check-*)",

      // Git read-only
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",

      // Code quality
      "Bash(ruff:*)",
      "Bash(pre-commit:*)"
    ],
    "confirm": [
      // Git write
      "Bash(git commit:*)",
      "Bash(git push:*)",

      // Build
      "Bash(make build-*)",

      // MCP servers
      "Bash(docker:*)"
    ],
    "deny": [
      // Dangerous
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Bash(chmod 777:*)"
    ]
  }
}
```

## Pattern Matching

### Wildcards
- `*` matches any arguments
- `Bash(command:*)` allows command with any args

### Specific Commands
- `Bash(git status)` allows only that exact command
- More specific rules take precedence

## Best Practices

### 1. Start Restrictive
Add permissions as needed, not all at once.

### 2. Use Confirm for Write Operations
```json
{
  "confirm": [
    "Bash(git commit:*)",
    "Bash(make deploy:*)"
  ]
}
```

### 3. Review Regularly
Audit permissions as project evolves.

### 4. Workspace-Specific
Use `settings.local.json` for project-specific rules.

## Related Pages

- [Configuration](configuration.md) - All settings
- [Security](security.md) - Security considerations
- [Best Practices](best-practices.md) - Usage patterns
