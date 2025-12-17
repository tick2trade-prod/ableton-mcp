# Shell Tool

> Source: [https://geminicli.com/docs/tools/shell](https://geminicli.com/docs/tools/shell)

## Overview

The shell tool executes commands in the system shell.

## Usage

```
> Run pytest on test_tools.py
[Executes: pytest tests/test_tools.py -v]
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | Command to execute |
| `cwd` | string | Working directory |
| `timeout` | number | Timeout in ms |

## Confirmation

Shell commands require confirmation by default:
```
Command: pytest tests/ -v
[Approve] [Deny] [Always Allow]
```

## Trusted Commands

Configure trusted patterns:
```json
{
  "trustedCommands": [
    "pytest *",
    "git status",
    "make check-*"
  ]
}
```

## ableton-mcp Commands

Common trusted commands:
```json
{
  "trustedCommands": [
    "pytest tests/*",
    "make check-port",
    "make test-connection",
    "ruff check .",
    "git status"
  ]
}
```

## Related Pages

- [Tools](tools.md) - All tools
- [Trusted Folders](trusted-folders.md) - Trust settings
- [Policy Engine](policy-engine.md) - Command control
