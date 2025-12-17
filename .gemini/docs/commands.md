# Commands

> Source: [https://geminicli.com/docs/cli/commands](https://geminicli.com/docs/cli/commands)

## Available Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `gemini` | Start interactive mode |
| `gemini "prompt"` | Execute single prompt |
| `gemini -f <file>` | Include file context |
| `gemini -d <dir>` | Include directory context |

### Authentication

| Command | Description |
|---------|-------------|
| `gemini auth login` | Authenticate |
| `gemini auth logout` | Sign out |
| `gemini auth status` | Check auth status |

### Configuration

| Command | Description |
|---------|-------------|
| `gemini settings` | Open settings |
| `gemini --model <name>` | Use specific model |

## Slash Commands (Interactive Mode)

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/model` | Change model |
| `/mcp` | MCP server status |
| `/clear` | Clear conversation |
| `/save` | Save conversation |
| `/load` | Load conversation |
| `/settings` | Open settings |
| `/quit` | Exit CLI |

## Command Flags

### Input Flags
```bash
-f, --file <path>     # File context
-d, --directory <path> # Directory context
-m, --model <name>    # Model selection
```

### Output Flags
```bash
--json               # JSON output
--quiet              # Minimal output
--stream             # Stream output
```

### Mode Flags
```bash
--headless           # Non-interactive
--sandbox            # Sandboxed execution
```

## ableton-mcp Usage

### Common Commands
```bash
# Start session in project
cd ~/ableton-mcp && gemini

# Quick test analysis
gemini "Run tests and summarize" -d tests/

# With specific model
gemini --model gemini-2.5-pro "Complex task..."
```

### MCP Commands
```
/mcp                 # Show MCP server status
/mcp reconnect       # Reconnect servers
/mcp auth            # OAuth management
```

## Related Pages

- [Slash Commands](slash-commands.md) - Detailed slash commands
- [Interactive Mode](interactive-mode.md) - REPL usage
- [Headless](headless.md) - Scripting
