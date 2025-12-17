# Editor

> Source: [https://antigravity.google/docs/editor](https://antigravity.google/docs/editor)

## Overview

The Antigravity Editor provides a powerful code editing experience with AI integration.

## Editor Features

### Syntax Highlighting
Full language support including Python, Markdown, TOML, YAML.

### IntelliSense
- Code completion
- Type hints
- Documentation on hover

### AI-Powered Features
- Inline suggestions
- Code actions
- Refactoring

### File Navigation
- Go to definition
- Find references
- Symbol search

## Key Shortcuts for ableton-mcp

| Shortcut | Action |
|----------|--------|
| `Cmd+L` | Open agent chat |
| `Cmd+K` | Inline edit |
| `Cmd+P` | Quick file open |
| `Cmd+Shift+F` | Search across files |
| `Cmd+.` | Code actions |

## Project File Types

### Python (`.py`)
- MCP server code
- Test files
- Track scripts

### Markdown (`.md`)
- Documentation
- GEMINI.md
- Workflow files

### TOML (`.toml`)
- `pyproject.toml`
- Configuration

### JSON (`.json`)
- MCP configuration
- Settings

## AI-Assisted Editing

### Inline Edit (Cmd+K)
Select code and request changes:
```
Selected: def create_track(...):
Request: "Add retry logic with exponential backoff"
```

### Code Actions
Click lightbulb or `Cmd+.`:
- Extract function
- Add type hints
- Generate tests

### Documentation
Generate docstrings:
```
Request: "Add docstring to this function"
```

## Related Pages

- [Tab](tab.md) - Tab completion
- [Command](command.md) - Command interface
- [Agent Side Panel](agent-side-panel.md) - Agent UI
