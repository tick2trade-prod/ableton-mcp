# Panes

> Source: [https://antigravity.google/docs/panes](https://antigravity.google/docs/panes)

## Overview

Panes allow you to organize the Antigravity interface for your workflow.

## Pane Types

### Editor Pane
- Code editing
- File viewing
- Diff view

### Agent Pane
- Conversation view
- Side panel

### Terminal Pane
- Command execution
- Output viewing

### Browser Pane
- Browser subagent
- Web preview

### Files Pane
- File explorer
- Search results

## Pane Layouts

### Split Vertical
```
┌─────────┬─────────┐
│ Editor  │ Agent   │
│         │         │
└─────────┴─────────┘
```

### Split Horizontal
```
┌─────────────────┐
│     Editor      │
├─────────────────┤
│    Terminal     │
└─────────────────┘
```

### Three-Way Split
```
┌─────────┬─────────┐
│ Editor  │ Agent   │
├─────────┴─────────┤
│     Terminal      │
└───────────────────┘
```

## Recommended Layout for ableton-mcp

### Development Mode
```
┌─────────────┬─────────┐
│   Editor    │ Agent   │
│ (code/test) │ (chat)  │
├─────────────┴─────────┤
│      Terminal         │
│ (pytest, make)        │
└───────────────────────┘
```

### Research Mode
```
┌─────────┬─────────┐
│ Browser │ Agent   │
│         │         │
├─────────┴─────────┤
│     Editor        │
│ (notes, docs)     │
└───────────────────┘
```

## Pane Management

### Shortcuts
- `Cmd+\` - Split editor
- `Cmd+J` - Toggle terminal
- `Cmd+B` - Toggle sidebar

### Drag and Drop
- Drag tabs between panes
- Resize panes with borders

### Save Layout
Save layout as default for workspace.

## Related Pages

- [Editor](editor.md) - Editor pane
- [Terminal](terminal.md) - Terminal pane
- [Agent Side Panel](agent-side-panel.md) - Agent pane
