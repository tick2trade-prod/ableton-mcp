# Claude IDE Integration

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Use Claude within your IDE for enhanced development experience.

## Supported IDEs

### VS Code
- Claude extension available
- Inline suggestions
- Chat panel

### JetBrains
- Plugin available
- Tool window integration

### Terminal Integration
Use Claude CLI in any IDE's integrated terminal.

## Antigravity IDE

For this project, we use **Antigravity IDE** which has native Claude support:
- Built-in agent (uses Claude or Gemini)
- MCP integration
- File context management

See [Antigravity Documentation](../.antigravity/docs/README.md).

## VS Code Setup

1. Install Claude extension
2. Configure API key
3. Use Cmd+Shift+P → "Claude: Open Chat"

## Terminal Integration

Works in any IDE:
```bash
cd ~/ableton-mcp
claude "Explain the tests"
```

## Related Pages

- [Installation](installation.md) - CLI setup
- [Commands](commands.md) - CLI usage
