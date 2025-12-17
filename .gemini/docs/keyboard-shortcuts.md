# Keyboard Shortcuts

> Source: [https://geminicli.com/docs/cli/keyboard-shortcuts](https://geminicli.com/docs/cli/keyboard-shortcuts)

## Navigation

| Shortcut | Action |
|----------|--------|
| `↑` / `↓` | History navigation |
| `Ctrl+A` | Beginning of line |
| `Ctrl+E` | End of line |
| `Ctrl+←` | Previous word |
| `Ctrl+→` | Next word |

## Editing

| Shortcut | Action |
|----------|--------|
| `Ctrl+U` | Clear line |
| `Ctrl+K` | Delete to end |
| `Ctrl+W` | Delete word |
| `Ctrl+L` | Clear screen |
| `Tab` | Autocomplete |

## Session Control

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current |
| `Ctrl+D` | Exit (EOF) |
| `Ctrl+Z` | Suspend |

## Multi-line Input

| Shortcut | Action |
|----------|--------|
| `Shift+Enter` | New line |
| `Enter` | Submit |
| `Ctrl+Enter` | Force submit |

## Tool Interaction

| Shortcut | Action |
|----------|--------|
| `y` / `Enter` | Approve tool |
| `n` | Deny tool |
| `a` | Always allow |
| `s` | Always allow server |

## Quick Commands

| Shortcut | Action |
|----------|--------|
| `/` + `Tab` | List commands |
| `@` + `Tab` | File/resource completion |

## Customization

Configure in settings:
```json
{
  "keyBindings": {
    "submit": "Enter",
    "newLine": "Shift+Enter"
  }
}
```

## Related Pages

- [Interactive Mode](interactive-mode.md) - REPL usage
- [Settings](settings.md) - Customization
