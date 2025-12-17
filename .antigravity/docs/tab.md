# Tab Completion

> Source: [https://antigravity.google/docs/tab](https://antigravity.google/docs/tab)

## Overview

Tab completion provides intelligent code suggestions as you type.

## Features

### Code Completion
- Variable names
- Function signatures
- Import statements
- Type annotations

### AI-Enhanced Suggestions
Machine learning-powered completions based on:
- Current context
- Project patterns
- Common idioms

## Usage in ableton-mcp

### Python Completion
```python
# Type: async def create_
# Tab shows: create_track, create_device, create_clip

# Type: await mcp_client.
# Tab shows: call, list_tools, get_resource
```

### Test Patterns
```python
# Type: @pytest.mark.
# Tab shows: live, session, device, clip, transport

# Type: async def test_
# Tab shows suggestions based on test patterns
```

### MCP Tool Names
```python
# Type: search_ab
# Tab shows: search_ableton_docs, search_ableton_guides
```

## Configuration

Enable/disable features in settings:
```json
{
  "editor": {
    "tabCompletion": true,
    "aiSuggestions": true,
    "suggestOnTriggerCharacters": true
  }
}
```

## Best Practices

### 1. Accept with Tab
Press Tab to accept the suggestion.

### 2. Cycle Options
Use arrow keys to browse alternatives.

### 3. Dismiss with Escape
Press Esc to dismiss suggestions.

## Related Pages

- [Editor](editor.md) - Editor overview
- [Command](command.md) - Command interface
