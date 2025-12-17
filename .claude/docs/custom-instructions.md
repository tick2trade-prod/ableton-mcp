# Claude Custom Instructions

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## CLAUDE.md

The `CLAUDE.md` file provides persistent context and instructions.

## Location

- Project root: `./CLAUDE.md`
- Or use existing: `GEMINI.md` (shared context)

## Structure

```markdown
# Project Name

## Description
What this project does.

## Key Information
- Important facts
- Configuration values
- Common patterns

## Rules
- Coding standards
- Testing requirements
- Commit conventions

## Common Commands
- Frequently used commands
```

## Example for ableton-mcp

```markdown
# ableton-mcp

## Description
Ableton Live integration through Model Context Protocol.

## Prerequisites
- Ableton Live running
- AbletonMCP control surface enabled
- Port 9877 listening

## Testing Rules
- No mocks - use real Ableton connection
- Run individual tests first
- Verify in DAW after tests

## Conventions
- Conventional commits
- Type hints required
- pytest for testing

## Key Commands
- `make check-port` - Verify port
- `make test-connection` - Test Ableton
- `pytest tests/test_tools.py -v` - Run tests

## Log Location
~/Library/Preferences/Ableton/Live 12.3.1/Log.txt
```

## Sharing with Gemini

For this project, we use `GEMINI.md` which works for both:
- Gemini CLI reads it
- Claude can reference it
- Single source of truth

## Related Pages

- [Memory](memory.md) - Persistent context
- [Configuration](configuration.md) - Settings
- [Config Files](config-files.md) - File structure
