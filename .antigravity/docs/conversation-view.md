# Conversation View

> Source: [https://antigravity.google/docs/conversation-view](https://antigravity.google/docs/conversation-view)

## Overview

The Conversation View provides a full-featured interface for AI agent interactions.

## Features

### Message History
- User messages
- Agent responses
- Tool calls and results

### Context Indicators
- Files in context
- MCP tools used
- Model information

### Actions
- Copy messages
- Retry responses
- Fork conversation

## Conversation Elements

### User Messages
```
USER: Create a new test for the rumble track
```

### Agent Responses
```
AGENT: I'll create a test file for the rumble track following
the existing patterns in tests/test_track_01_kick.py.

[Code block with test file]

I've created the test. Let me run it to verify:
> pytest tests/test_track_02_rumble.py -v
```

### Tool Calls
```
Tool: search_ableton_docs
Input: {"query": "Compressor sidechain"}
Result: [{...}, {...}]
```

### Approvals
```
Command: pytest tests/ -v
[Approve] [Reject] [Modify]
```

## Conversation Patterns for ableton-mcp

### Research Workflow
```
USER: /research sidechain compression techniques
AGENT: [Uses research_mcp tools]
AGENT: Here are the key techniques...
USER: Implement the first technique
AGENT: [Generates code]
```

### Development Workflow
```
USER: @[track_01_kick.py] Add Roar device to the chain
AGENT: I'll add Roar after the current device chain...
[Shows changes]
USER: Looks good, apply it
AGENT: [Applies changes]
```

### Testing Workflow
```
USER: Run the rumble track tests
AGENT: > pytest tests/test_track_02_rumble.py -v
[Approve]
...
AGENT: 3 tests passed, 1 failed. The failure is...
USER: Fix the failing test
AGENT: [Analyzes and fixes]
```

## Conversation Management

### Starting New Conversations
- `Cmd+L` → New Conversation
- Use for unrelated topics

### Continuing Conversations
- Resume from history
- Maintain context

### Forking Conversations
- Branch from a point
- Explore alternatives

## Related Pages

- [Agent Side Panel](agent-side-panel.md) - Side panel view
- [Agent](agent.md) - Agent capabilities
- [Browser Subagent View](browser-subagent-view.md) - Browser UI
