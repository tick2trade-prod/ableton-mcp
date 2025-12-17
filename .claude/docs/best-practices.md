# Claude Code Best Practices

> Source: [Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-best-practices)

## Overview

Best practices for using Claude Code effectively in development workflows.

## Project Setup

### CLAUDE.md File

Create a `CLAUDE.md` in your project root:

```markdown
# Project: ableton-mcp

## Context
Ableton Live integration through Model Context Protocol.

## Key Principles
- No mocks in tests - use real Ableton connection
- Incremental testing - one tool at a time
- Live verification in DAW

## Conventions
- Conventional commits
- Type hints for all functions
- pytest for testing

## Important Files
- GEMINI.md - Project rules (shared with Gemini)
- pyproject.toml - Dependencies
- tests/ - Integration tests
```

### Settings Configuration

```json
// .claude/settings.local.json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(make:*)",
      "Bash(python:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)"
    ]
  }
}
```

## Effective Prompting

### Be Specific

```
# Good
"Add a retry mechanism with exponential backoff to the socket connection in src/ableton_mcp/client.py, starting at 100ms and maxing at 5 seconds"

# Less Effective
"Make the connection more reliable"
```

### Provide Context

```
# Good
"Looking at tests/test_tools.py, the test_create_track test times out after 30 seconds. The socket timeout is currently 10 seconds. Increase it to 30 seconds."

# Less Effective
"Fix the timeout"
```

### Use File References

```
@tests/test_tools.py
@src/ableton_mcp/client.py

These files need to work together for the connection retry logic.
```

## Multi-Turn Patterns

### Iterative Development

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

## Error Handling

### When Things Go Wrong

1. **Provide error context**: Share the full error message
2. **Show recent changes**: What was just modified
3. **Describe expected behavior**: What should happen

```
The test fails with:
```
ConnectionError: Socket timeout after 10 seconds
```

I expected the track to be created within 5 seconds. The Ableton connection is working (verified with make check-port).
```

## Tool Usage Patterns

### Safe Commands

```json
{
  "allow": [
    "Bash(pytest:*)",          // Testing
    "Bash(make check-*)",       // Verification
    "Bash(git status)",         // Read-only git
    "Bash(git diff)",           // Read-only git
    "Bash(grep:*)"              // Search
  ]
}
```

### Require Confirmation

```json
{
  "confirm": [
    "Bash(git commit:*)",       // Write operations
    "Bash(make build-*)",       // Build operations
    "Bash(python -m mcp_*)"     // Server operations
  ]
}
```

## Performance Tips

### Context Management

1. **Start fresh for new topics**: Don't carry unrelated context
2. **Use @ references**: Focused file context
3. **Be concise**: Less noise = better responses

### Token Efficiency

1. **Research before implementing**: Gather info first
2. **Batch related changes**: Multiple edits in one turn
3. **Use summaries**: Ask for summaries of long outputs

## Security Considerations

### Sensitive Data

- Don't include API keys in prompts
- Use environment variables
- Review generated code for secrets

### Command Permissions

- Start restrictive, expand as needed
- Log all executed commands
- Review before sensitive operations

## Related Pages

- [Permissions](permissions.md) - Permission configuration
- [CLAUDE.md Guide](claude-md.md) - Project context file
- [MCP Integration](mcp.md) - Tool development
