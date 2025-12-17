# Claude Agent Mode

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Agent mode enables autonomous task completion with tool use.

## Capabilities

### Autonomous Execution
- Multi-step task completion
- Tool chaining
- Error recovery

### Tool Use
- File operations
- Shell commands
- External APIs (via MCP)

### Context Management
- Maintains conversation state
- Tracks file changes
- Remembers decisions

## Enabling Agent Mode

Agent mode is the default for Claude Code:
```bash
claude "Implement feature X and test it"
```

Claude will:
1. Plan the implementation
2. Write code
3. Run tests
4. Fix issues
5. Report results

## Agent Patterns

### Implement + Test
```
USER: Create a new MCP tool for tempo detection and add tests
[Claude implements, creates tests, runs tests, fixes issues]
```

### Research + Apply
```
USER: Research sidechain techniques and implement the best one
[Claude researches, implements, validates]
```

### Debug + Fix
```
USER: The tests are failing, debug and fix them
[Claude analyzes, diagnoses, fixes, verifies]
```

## Safety

Claude asks for confirmation on:
- File writes
- Shell commands
- API calls

Configure in [Permissions](permissions.md).

## ableton-mcp Usage

```
USER: Create a new hi-hat track following the lily_palmer patterns
[Claude analyzes existing patterns, creates track, tests]

USER: Fix the timeout in test_create_track
[Claude analyzes, increases timeout, verifies fix]
```

## Related Pages

- [Tool Use](tool-use.md) - Function calling
- [Permissions](permissions.md) - Safety controls
- [Best Practices](best-practices.md) - Effective usage
