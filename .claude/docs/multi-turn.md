# Claude Multi-Turn Conversations

> Source: [Anthropic Documentation](https://www.anthropic.com/engineering/claude-code-best-practices)

## Overview

Multi-turn conversations enable iterative development with Claude.

## Patterns

### Iterate on Implementation
```
Turn 1: "Create a new MCP tool for tempo detection"
Turn 2: "Add input validation for the audio path"
Turn 3: "Write tests for edge cases"
Turn 4: "Run the tests and fix any failures"
```

### Research + Implement
```
Turn 1: "Search for best practices in audio BPM detection"
Turn 2: "Implement using librosa based on the research"
Turn 3: "Add error handling for edge cases mentioned"
```

### Debug Cycle
```
Turn 1: "Run the tests"
Turn 2: "The timeout test failed - analyze why"
Turn 3: "Fix the timeout issue"
Turn 4: "Re-run tests to verify"
```

## Best Practices

### Build Incrementally
Each turn should be focused:
- One concept per turn
- Review before next step
- Confirm understanding

### Maintain Focus
Stay on topic:
```
Turn 1-4: Feature implementation
Turn 5: Start NEW conversation for unrelated topic
```

### Reference Previous Work
```
Turn 3: "Now add tests for the tool you just created"
Turn 4: "Run the tests you just wrote"
```

## ableton-mcp Examples

### Track Creation Flow
```
1. "Show me the pattern used in track_01_kick.py"
2. "Create track_03_hihat.py following that pattern"
3. "Add a test for the new track"
4. "Run the test and verify it works"
```

### MCP Tool Development
```
1. "Research audio analysis libraries for Python"
2. "Create an MCP tool using librosa"
3. "Add the tool to ableton_codegen server"
4. "Test the tool with a sample audio file"
```

## Related Pages

- [Agent Mode](agent-mode.md) - Autonomous execution
- [Prompt Engineering](prompt-engineering.md) - Effective prompts
- [Context](context.md) - Maintaining context
