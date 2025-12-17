# Agent Modes / Settings

> Source: [https://antigravity.google/docs/agent-modes-settings](https://antigravity.google/docs/agent-modes-settings)

## Overview

Configure agent behavior through modes and settings to optimize for your workflow.

## Agent Modes

### Default Mode
Standard agent behavior with balanced autonomy and safety.

### Agentic Mode
More autonomous execution:
- Runs multi-step tasks
- Makes decisions independently
- Uses MCP tools proactively

### Secure Mode
Restricted execution:
- Requires approval for commands
- Limited file access
- No network requests

## Settings for ableton-mcp

### Recommended Configuration

```json
{
  "agent": {
    "mode": "agentic",
    "autoApproveCommands": false,
    "mcpServers": ["ableton_codegen", "research_mcp", "sota_researcher_v2"],
    "workingDirectory": "/Users/alexzh/ableton-mcp"
  }
}
```

### Command Approval

For this project, consider auto-approving:
- `pytest` commands (safe, read-only tests)
- `make check-*` commands (verification)
- `git status`, `git diff` (read-only)

Keep manual approval for:
- File modifications
- `make build-*` commands
- Network requests

### Context Settings

```yaml
# Maximum files in context
maxContextFiles: 50

# File types to prioritize
priorityExtensions: [".py", ".md", ".toml"]

# Ignore patterns
ignorePatterns:
  - "*.pyc"
  - "__pycache__"
  - ".git"
  - "external/"
```

## Project-Specific Settings

### GEMINI.md Integration

Your `GEMINI.md` provides these rules:

```markdown
## Key Principles
- No mocks - All tests run against real Ableton Live
- Incremental testing - Test one tool at a time
- Live verification - Confirm changes in DAW
```

### Workflow Turbo Settings

Enable turbo for safe operations:
```markdown
// turbo-all  # In workflow files
```

### MCP Server Configuration

Located in `.antigravity/mcp.json`:
```json
{
  "servers": {
    "ableton_codegen": {
      "command": "python",
      "args": ["-m", "mcp_servers.ableton_codegen.server"],
      "env": {
        "REDIS_URL": "redis://localhost:6379"
      }
    }
  }
}
```

## Performance Optimization

### For Large Codebase
- Enable file indexing
- Use semantic search for file location
- Limit context to relevant files

### For Frequent Testing
- Create test-focused workflows
- Use turbo annotations
- Auto-run safe test commands

## Related Pages

- [Agent](agent.md) - Core agent functionality
- [Secure Mode](secure-mode.md) - Security features
- [Rules / Workflows](rules-workflows.md) - Automation settings
