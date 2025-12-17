# Review Changes + Source Control (Manager)

> Source: [https://antigravity.google/docs/review-changes-manager](https://antigravity.google/docs/review-changes-manager)

## Overview

The Agent Manager view of source control provides a high-level overview of changes across workspaces.

## Features

### Workspace Changes
- View changes per workspace
- Cross-workspace comparison

### Change History
- Recent commits
- Pending changes

### Batch Operations
- Stage all
- Commit all
- Push all

## Manager vs Editor View

| Feature | Manager View | Editor View |
|---------|--------------|-------------|
| Scope | All workspaces | Current file/workspace |
| Detail | High-level | Line-by-line |
| Actions | Batch | Individual |

## Usage in ableton-mcp

### Reviewing Agent Changes
1. Open Agent Manager
2. Go to Source Control
3. View all modified files
4. Review diffs
5. Stage and commit

### Batch Commit
After development session:
```bash
# Manager shows:
Modified files:
  ✓ tests/test_track_02_rumble.py
  ✓ live_set/.../track_02_rumble.py
  ✓ GEMINI.md

[Stage All] [Commit] [Push]
```

## Related Pages

- [Review Changes (Editor)](review-changes-editor.md) - Editor view
- [Changes Sidebar](changes-sidebar.md) - Sidebar view
- [Agent Manager](agent-manager.md) - Manager overview
