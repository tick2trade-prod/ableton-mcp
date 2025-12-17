# Gemini CLI Get Started

> Source: [https://geminicli.com/docs/get-started](https://geminicli.com/docs/get-started)

## Quick Start

### Installation

```bash
# Install via npm
npm install -g @anthropic-ai/gemini-cli

# Or via Homebrew
brew install gemini-cli
```

### Authentication

```bash
# Login with Google account
gemini auth login

# Or use API key
export GOOGLE_API_KEY=your_api_key
```

### First Run

```bash
# Start interactive mode
gemini

# Or run single command
gemini "Explain this code" -f main.py
```

## Basic Usage

### Interactive Mode (REPL)

```bash
$ gemini
> What files are in this directory?
[Lists files using built-in tools]

> Create a Python function to add two numbers
[Generates code]
```

### Single Commands

```bash
# Quick question
gemini "How do I configure pytest?"

# With file context
gemini "Explain this code" -f tests/test_tools.py

# With directory context
gemini "Summarize this project" -d ./
```

## Project Setup for ableton-mcp

### Configuration

Create `~/.gemini/settings.json`:

```json
{
  "model": "gemini-2.5-pro",
  "mcpServers": {
    "ableton_codegen": {
      "command": "python",
      "args": ["-m", "mcp_servers.ableton_codegen.server"]
    }
  }
}
```

### Working Directory

```bash
cd ~/ableton-mcp
gemini
```

### Common Commands

```bash
# Run tests
> Run pytest for test_tools.py

# Research
> Search Ableton docs for sidechain compression

# Generate code
> Create a new MCP tool for tempo detection
```

## Next Steps

- [Configuration](configuration.md) - Detailed settings
- [MCP Servers](mcp.md) - Add MCP tools
- [Commands](commands.md) - All CLI commands

## Related Pages

- [Installation](installation.md) - Detailed installation
- [Authentication](authentication.md) - Auth options
- [Examples](examples.md) - Usage examples
