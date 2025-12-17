# Custom Commands

> Source: [https://geminicli.com/docs/cli/custom-commands](https://geminicli.com/docs/cli/custom-commands)

## Overview

Create custom commands for frequently used prompts and workflows.

## Creating Custom Commands

### Configuration

Add to `~/.gemini/settings.json`:

```json
{
  "customCommands": {
    "test": {
      "prompt": "Run pytest and analyze failures",
      "description": "Run and analyze tests"
    },
    "review": {
      "prompt": "Review this code for issues and improvements",
      "description": "Code review"
    }
  }
}
```

### Usage

```
/test
/review -f myfile.py
```

## Command Properties

| Property | Description |
|----------|-------------|
| `prompt` | The prompt to execute |
| `description` | Help text description |
| `model` | Override model for this command |
| `confirmation` | Require confirmation |

## ableton-mcp Custom Commands

### Recommended Commands

```json
{
  "customCommands": {
    "test-ableton": {
      "prompt": "Run pytest on tests/test_tools.py and analyze any failures. Check if Ableton connection is working.",
      "description": "Test Ableton MCP tools"
    },
    "new-track": {
      "prompt": "Create a new Ableton track script following the patterns in live_set/lily_palmer/i_am_machine/",
      "description": "Generate track script"
    },
    "new-mcp-tool": {
      "prompt": "Create a new MCP tool following the patterns in mcp_servers/. Include proper error handling and tests.",
      "description": "Generate MCP tool"
    },
    "research-technique": {
      "prompt": "Research production techniques for the given topic, focusing on Ableton Live implementation",
      "description": "Research production techniques"
    },
    "analyze-track": {
      "prompt": "Analyze the track script and suggest improvements for audio quality and code structure",
      "description": "Analyze track script"
    }
  }
}
```

### Usage Examples

```
/test-ableton
/new-track rumble bass
/new-mcp-tool tempo_detection
/research-technique sidechain compression
/analyze-track -f live_set/lily_palmer/i_am_machine/track_02_rumble.py
```

## Advanced Commands

### With Variables
```json
{
  "customCommands": {
    "create": {
      "prompt": "Create a {type} named {name} following project patterns"
    }
  }
}
```

### Multi-Step
```json
{
  "customCommands": {
    "full-test": {
      "prompt": "1. Run all tests\n2. Analyze failures\n3. Suggest fixes\n4. Apply fixes if approved\n5. Re-run tests"
    }
  }
}
```

## Related Pages

- [Commands](commands.md) - Built-in commands
- [Slash Commands](slash-commands.md) - Slash command details
- [Configuration](configuration.md) - Settings
