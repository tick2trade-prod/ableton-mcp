# Agent Side Panel

> Source: [https://antigravity.google/docs/agent-side-panel](https://antigravity.google/docs/agent-side-panel)

## Overview

The Agent Side Panel provides a dedicated space for AI interactions alongside your code.

## Features

### Conversation View
- Current conversation history
- Context indicators
- Action buttons

### Context Display
Shows what files and context the agent is using.

### Quick Actions
- New conversation
- Run workflow
- View history

## Using the Side Panel

### Opening
- Click agent icon in sidebar
- Use `Cmd+L` to open chat

### Context Indicators
The panel shows:
- Active files in context
- MCP servers connected
- Current mode

### Conversation Flow
```
[User Message]
Can you run the tests for the kick track?

[Agent Response]
I'll run the test for track_01_kick:
> pytest tests/test_track_01_kick.py -v
[Approve] [Reject]

[Result]
✓ 3 tests passed
```

## Side Panel for ableton-mcp

### Common Patterns

**Quick Test Run**
```
Side Panel → "Run tests for track 02"
Agent → Executes pytest with correct path
```

**Research Query**
```
Side Panel → "/research sidechain techniques"
Agent → Uses MCP tool, shows results
```

**Code Review**
```
Side Panel → "Review changes to track script"
Agent → Analyzes diff, provides feedback
```

### Context Management

Add context explicitly:
```
Side Panel → @[tests/test_tools.py] explain this test
```

Remove context:
```
Side Panel → Start new conversation
```

## Best Practices

### 1. Keep Context Focused
Start new conversations for unrelated tasks.

### 2. Use @ References
Explicitly reference files for clarity.

### 3. Review Context Indicators
Check what the agent is considering.

## Related Pages

- [Editor](editor.md) - Editor integration
- [Conversation View](conversation-view.md) - Full conversation UI
- [Agent](agent.md) - Agent capabilities
