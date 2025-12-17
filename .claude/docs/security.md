# Claude Security

> Source: [Anthropic Documentation](https://www.anthropic.com/engineering/claude-code-best-practices)

## Overview

Security considerations when using Claude Code.

## API Key Security

### Environment Variables
```bash
# Good: Use environment variables
export ANTHROPIC_API_KEY=sk-ant-...

# Bad: Hardcoded in code
api_key = "sk-ant-..."
```

### .gitignore
```gitignore
.env
*.key
**/secrets.*
.anthropic/
```

### Key Rotation
Rotate API keys periodically (every 90 days).

## Command Permissions

### Allowlist Pattern
```json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(git status)"
    ]
  }
}
```

### Denylist Pattern
```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Bash(curl *:*)"
    ]
  }
}
```

## Code Review

### Review Generated Code
Always review:
- File modifications
- Shell commands
- API calls
- External dependencies

### Check for Secrets
Claude shouldn't generate secrets:
```python
# Review these patterns
API_KEY = "..."
password = "..."
secret_token = "..."
```

## Network Security

### MCP Server Isolation
- Run in controlled environment
- Limit network access
- Monitor connections

### External APIs
Review before allowing:
- What data is sent
- Who receives it
- Is it necessary

## ableton-mcp Considerations

### Safe Commands
```json
{
  "allow": [
    "Bash(pytest:*)",
    "Bash(make check-*)",
    "Bash(git status)",
    "Bash(git diff:*)"
  ]
}
```

### Sensitive Operations
Require confirmation for:
- Git push
- File deletion
- Docker operations

## Related Pages

- [Permissions](permissions.md) - Permission configuration
- [Best Practices](best-practices.md) - Safe usage
- [Configuration](configuration.md) - Security settings
