# Tutorials

> Source: [https://geminicli.com/docs/cli/tutorials](https://geminicli.com/docs/cli/tutorials)

## Getting Started Tutorials

### First Steps
1. [Installation](installation.md)
2. [Authentication](authentication.md)
3. [Basic Usage](get-started.md)

### Interactive Mode
1. Start with `gemini`
2. Try basic queries
3. Use file context with `@file`
4. Explore slash commands

## MCP Integration Tutorial

### Step 1: Configure Server
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"]
    }
  }
}
```

### Step 2: Verify Connection
```
/mcp
```

### Step 3: Use Tools
```
> Use my custom tool to process data
[Tool executes]
```

## ableton-mcp Tutorial

### Setup
1. Clone project
2. Install dependencies: `uv sync`
3. Configure MCP servers
4. Start Ableton with control surface

### Development Workflow
1. Start Gemini CLI in project: `cd ~/ableton-mcp && gemini`
2. Use `/mcp` to verify MCP servers
3. Create or modify track scripts
4. Run tests: `> Run pytest on test_tools.py`
5. Iterate on failures

### Track Creation Example
```
> Create a new kick track following the lily_palmer patterns
[Analyzes existing tracks]
[Generates new track script]

> Add tests for the new track
[Generates tests]

> Run the tests and fix any issues
[Runs tests, fixes issues]
```

## Advanced Tutorials

- [Headless Mode](headless.md) - Automation
- [Custom Commands](custom-commands.md) - Shortcuts
- [Hooks](hooks.md) - Customization

## Related Pages

- [Examples](examples.md) - Usage examples
- [Interactive Mode](interactive-mode.md) - REPL details
