# Gemini CLI Tools

> Source: [https://geminicli.com/docs/tools](https://geminicli.com/docs/tools)

## Overview

Gemini CLI includes built-in tools for common development tasks.

## Built-in Tools

### File System Tools

#### read_file
Read contents of a file:
```
> Read the contents of pyproject.toml
[Uses read_file tool]
```

#### write_file
Write or modify files:
```
> Create a new config.json with database settings
[Uses write_file tool]
```

### Shell Tool

#### run_shell_command
Execute shell commands:
```
> Run pytest on test_tools.py
[Executes: pytest tests/test_tools.py -v]
```

### Web Tools

#### web_fetch
Fetch web page content:
```
> Get the content from ableton.com/help
[Fetches page content]
```

#### google_web_search
Search the web:
```
> Search for "techno sidechain compression tutorial"
[Returns search results]
```

### Memory Tools

#### save_memory
Store information for future reference:
```
> Remember that our kick uses 120 BPM
[Saves to memory]
```

### Todo Tool

#### write_todos
Manage task lists:
```
> Add a todo: Implement tempo detection
[Adds to todo list]
```

## MCP Tools

MCP servers add additional tools. See [MCP documentation](mcp.md).

### ableton-mcp Tools

| Tool | Description |
|------|-------------|
| `search_ableton_docs` | Search Ableton documentation |
| `generate_track_code` | Generate track scripts |
| `analyze_track_script` | Analyze existing scripts |
| `research` | Comprehensive web research |

## Tool Confirmation

### Trust Levels

1. **Built-in tools**: Generally trusted
2. **MCP tools**: Require confirmation by default
3. **Trusted servers**: Skip confirmation

### Configuration

```json
{
  "mcpServers": {
    "my-server": {
      "command": "...",
      "trust": true  // Skip confirmations
    }
  }
}
```

## Tool Usage Patterns

### Research + Action

```
> Search for best EQ settings for techno kick
[web_search]
> Apply those settings to our kick track
[MCP tools]
```

### Read + Modify

```
> Read track_01_kick.py and add error handling
[read_file → write_file]
```

### Test + Fix

```
> Run tests and fix any failures
[run_shell_command → read_file → write_file]
```

## Tool Selection

Gemini automatically selects appropriate tools:

```
Request: "What's the project structure?"
→ Uses: run_shell_command (ls/tree) or read_file

Request: "Create a new test file"
→ Uses: write_file

Request: "Search for compression tutorials"
→ Uses: google_web_search
```

## Related Pages

- [MCP](mcp.md) - MCP tool integration
- [Shell Tool](shell.md) - Shell command details
- [File System](file-system.md) - File operations
