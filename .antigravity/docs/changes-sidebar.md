# Changes Sidebar

> Source: [https://antigravity.google/docs/changes-sidebar](https://antigravity.google/docs/changes-sidebar)

## Overview

The Changes Sidebar provides quick access to source control status in the file explorer.

## Features

### File Status Indicators
- `M` - Modified
- `A` - Added
- `D` - Deleted
- `U` - Untracked

### Quick Actions
- Stage file
- Discard changes
- View diff

### Git Status
- Current branch
- Sync status
- Pending changes count

## Sidebar in ableton-mcp

### Common Patterns
```
ableton-mcp/
├── M tests/test_tools.py
├── A tests/test_track_02_rumble.py
├── M live_set/.../track_02_rumble.py
└── M GEMINI.md
```

### Status Colors
- Green: Staged for commit
- Yellow: Modified, not staged
- Red: Conflict or deleted
- Gray: Ignored

## Quick Actions

### Right-Click Menu
- Stage Changes
- Discard Changes
- Compare with HEAD
- Open Timeline

### Keyboard Shortcuts
- Stage: Select + Enter
- Discard: Select + Backspace

## Related Pages

- [Review Changes (Editor)](review-changes-editor.md) - Detailed view
- [Files](files.md) - File explorer
