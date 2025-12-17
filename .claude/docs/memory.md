# Claude Memory

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Memory enables persistent information across sessions.

## Types of Memory

### Session Memory
Within conversation:
- Recent messages
- Tool results
- File context

### Project Memory (CLAUDE.md)
Persistent project context:
```markdown
# Project: ableton-mcp
This project integrates Ableton Live with MCP.
```

## Using Memory

### Remember Information
```
USER: Remember that our kick track is at 120 BPM
[Claude notes for session]
```

### Project Memory
Add to CLAUDE.md:
```markdown
## Key Information
- Tempo: 120 BPM
- Key: A minor
- DAW: Ableton Live 12
```

## ableton-mcp Memories

Recommended CLAUDE.md content:
```markdown
# ableton-mcp

## Project Context
Ableton Live integration through Model Context Protocol.

## Key Rules
- No mocks in tests - use real Ableton
- Conventional commits
- pytest for testing

## Frequently Used
- Tempo: 120 BPM
- Rumble chain: Hybrid Reverb → Roar → EQ Eight → Compressor
- Test command: pytest tests/test_tools.py -v
```

## Related Pages

- [Context](context.md) - Context management
- [Configuration](configuration.md) - Settings
