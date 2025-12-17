# Claude Commands

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## CLI Commands

### Basic Usage
```bash
# Interactive mode
claude

# Single command
claude "Write a function to calculate BPM"

# With file context
claude "Explain this" -f main.py
```

### Common Flags

| Flag | Description |
|------|-------------|
| `-f, --file` | Include file context |
| `-d, --directory` | Include directory |
| `--model` | Select model |
| `--new` | New conversation |

## Interactive Commands

### Session Control
| Command | Description |
|---------|-------------|
| `/quit` | Exit session |
| `/new` | New conversation |
| `/clear` | Clear history |

### Context
| Command | Description |
|---------|-------------|
| `/file <path>` | Add file context |
| `/dir <path>` | Add directory |

### Settings
| Command | Description |
|---------|-------------|
| `/model` | Change model |
| `/settings` | View settings |

## ableton-mcp Usage

### Common Commands
```bash
# Start in project
cd ~/ableton-mcp && claude

# With file
claude "Explain tests" -f tests/test_tools.py

# Run and fix
claude "Run pytest and fix failures" -d tests/
```

## Related Pages

- [Agent Mode](agent-mode.md) - Multi-step tasks
- [Configuration](configuration.md) - Settings
