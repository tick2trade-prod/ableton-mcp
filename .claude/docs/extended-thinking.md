# Claude Extended Thinking

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Extended thinking enables deeper reasoning for complex problems.

## When to Use

- Complex algorithms
- Multi-step planning
- Debugging difficult issues
- Architecture decisions

## Enabling Extended Thinking

### API
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000
    },
    messages=[...]
)
```

### CLI
Extended thinking may be enabled automatically for complex queries.

## Thinking Process

Claude will:
1. Analyze the problem
2. Consider multiple approaches
3. Evaluate trade-offs
4. Arrive at solution

## ableton-mcp Use Cases

### Complex Debugging
```
"The tests pass locally but fail in CI. Here's the error and the code.
Think through why this might happen and how to fix it."
```

### Architecture Decisions
```
"We need to add a new feature for tempo detection. Consider the options
and recommend the best approach for our MCP architecture."
```

### Refactoring
```
"Look at the track scripts and think about how to refactor them to reduce
duplication while maintaining flexibility."
```

## Related Pages

- [Agent Mode](agent-mode.md) - Multi-step tasks
- [Prompt Engineering](prompt-engineering.md) - Effective prompts
