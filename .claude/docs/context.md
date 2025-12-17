# Claude Context Management

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Context management determines what information Claude sees.

## Context Sources

### Conversation History
Previous messages in current session.

### File References
Files explicitly mentioned:
```
@tests/test_tools.py
```

### Project Context
CLAUDE.md and project files.

### Tool Results
Outputs from tool calls.

## Context Limits

| Model | Context Window |
|-------|----------------|
| Claude 3.5 Sonnet | 200K tokens |
| Claude 3 Opus | 100K tokens |

## Managing Context

### File References
Be explicit about needed files:
```
@src/client.py @tests/test_client.py
Explain how these work together
```

### New Conversations
Start fresh for unrelated topics:
```bash
claude --new "Different topic"
```

### Focus Context
```
Focus only on the MCP server code:
@mcp_servers/ableton_codegen/
```

## Best Practices

### Be Specific
```
# Good
@tests/test_tools.py::test_create_track explain the timeout issue

# Less Good
Explain the test issues
```

### Remove Noise
Don't include files not relevant to the task.

### Summarize Long Outputs
Ask Claude to summarize lengthy results.

## ableton-mcp Context

Commonly referenced:
```
@GEMINI.md            # Project rules
@tests/test_tools.py  # Test file
@pyproject.toml       # Dependencies
@mcp_servers/         # MCP code
```

## Related Pages

- [Agent Mode](agent-mode.md) - Autonomous execution
- [Memory](memory.md) - Persistent context
- [Best Practices](best-practices.md) - Usage patterns
