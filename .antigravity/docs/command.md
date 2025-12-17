# Command Interface

> Source: [https://antigravity.google/docs/command](https://antigravity.google/docs/command)

## Overview

The Command interface provides quick access to actions and features.

## Opening Command Palette

- **Shortcut**: `Cmd+Shift+P`
- **Quick Open**: `Cmd+P`

## Common Commands

### File Operations
- `Open File...`
- `Save All`
- `Close Editor`

### Agent Commands
- `Agent: New Conversation`
- `Agent: Run Workflow`
- `Agent: Show History`

### Git Commands
- `Git: Commit`
- `Git: Push`
- `Git: Pull`

### Terminal Commands
- `Terminal: New Terminal`
- `Terminal: Run Task`

## Project-Specific Commands

### Testing
```
> Test: Run Current File
> Test: Run Test at Cursor
> Test: Debug Test
```

### MCP
```
> MCP: Restart Servers
> MCP: View Logs
> MCP: List Tools
```

### Workflows
```
> Run Workflow: research
> Run Workflow: code-quality
> Run Workflow: configure-rumble
```

## Quick Open (Cmd+P)

Navigate quickly to files:
```
Cmd+P → test_tools      → tests/test_tools.py
Cmd+P → track_01        → live_set/.../track_01_kick.py
Cmd+P → mcp.json        → .antigravity/mcp.json
```

## Symbol Navigation

- `Cmd+Shift+O` - Go to symbol in file
- `Cmd+T` - Go to symbol in workspace

```
Cmd+Shift+O → test_create_track → Jump to function
Cmd+T → AbletonClient → Find class definition
```

## Related Pages

- [Editor](editor.md) - Editor features
- [Agent](agent.md) - Agent commands
- [Terminal](terminal.md) - Terminal commands
