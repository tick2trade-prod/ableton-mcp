# Files

> Source: [https://antigravity.google/docs/files](https://antigravity.google/docs/files)

## Overview

The Files pane provides file system navigation and management.

## Features

### File Tree
- Hierarchical file view
- Expand/collapse folders
- Search files

### File Operations
- Create files/folders
- Rename
- Delete
- Move

### Preview
- Quick preview on select
- Full open on double-click

## File Tree in ableton-mcp

### Key Locations
```
ableton-mcp/
├── .agent/workflows/        # Custom workflows
├── .antigravity/
│   ├── docs/                # This documentation
│   └── mcp.json             # MCP configuration
├── docs/                    # Project docs
├── live_set/                # Ableton track scripts
│   └── lily_palmer/
│       └── i_am_machine/
│           ├── track_01_kick.py
│           ├── track_02_rumble.py
│           └── ...
├── mcp_servers/             # MCP server code
├── src/                     # Source code
├── tests/                   # Test files
├── GEMINI.md                # Project rules
└── pyproject.toml           # Config
```

### Quick Navigation
- `Cmd+P` - Open file by name
- `Cmd+Shift+E` - Focus file tree
- Arrow keys - Navigate

### Context Menu
Right-click for:
- New File
- New Folder
- Reveal in Finder
- Copy Path
- Open with Agent

## Integration with Agent

### Reference Files
```
@[path/to/file.py]  # Reference in chat
```

### Open with Agent
Right-click → Open with Agent → Start conversation about file

## Related Pages

- [Editor](editor.md) - File editing
- [Changes Sidebar](changes-sidebar.md) - Git status in tree
