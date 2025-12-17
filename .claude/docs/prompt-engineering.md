# Claude Prompt Engineering

> Source: [Anthropic Documentation](https://www.anthropic.com/engineering/claude-code-best-practices)

## Principles

### Be Specific
```
# Good
"Add retry logic with exponential backoff starting at 100ms to the socket connection in src/ableton_mcp/client.py"

# Too vague
"Fix the connection"
```

### Provide Context
```
# Good
"The test_create_track test times out after 30 seconds. Looking at tests/test_tools.py lines 45-60, increase the socket timeout to 60 seconds."

# Missing context
"Fix the timeout"
```

### State Expected Outcome
```
# Good
"Create a new MCP tool that returns the current tempo. It should return a dict with 'tempo' key and BPM value."

# Unclear expectations
"Make a tempo tool"
```

## Patterns

### Step-by-Step
```
1. First, analyze the existing track scripts
2. Then, create a new script following the same patterns
3. Add tests for the new script
4. Run tests and fix any issues
```

### Constraints
```
Create a new track script with these constraints:
- Must use async/await
- Must include error handling
- Must have type hints
- Must follow existing patterns in live_set/
```

### Examples
```
Create a new MCP tool similar to search_ableton_docs but for searching our track scripts.

Example usage:
>>> search_tracks("rumble")
[{"name": "track_02_rumble.py", "path": "..."}]
```

## Anti-Patterns

### Too Vague
❌ "Make it better"
✓ "Improve error handling by adding try/except blocks with specific exception types"

### Overloaded
❌ "Create the entire project with all features"
✓ Break into smaller tasks

### Ambiguous
❌ "Fix the issue"
✓ "Fix the TypeError on line 45 where we're passing a string instead of int"

## ableton-mcp Examples

### Good Prompts
```
"Add a new MCP tool in mcp_servers/ableton_codegen/ that detects BPM from an audio file using librosa"

"The test at tests/test_tools.py::test_create_track fails with timeout. Increase the socket timeout in src/ableton_mcp/client.py from 10s to 30s"

"Create a new track script for hi-hats following the pattern in live_set/lily_palmer/i_am_machine/track_01_kick.py"
```

## Related Pages

- [Best Practices](best-practices.md) - Overall practices
- [Agent Mode](agent-mode.md) - Multi-step tasks
- [Context](context.md) - Providing context
