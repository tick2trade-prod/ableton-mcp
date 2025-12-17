# Todo Tool

> Source: [https://geminicli.com/docs/tools/todos](https://geminicli.com/docs/tools/todos)

## Overview

Manage task lists with the todo tool.

## write_todos

```
> Add todo: Implement tempo detection MCP tool
[Adds to todo list]
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | string | add, complete, list |
| `content` | string | Todo content |
| `id` | string | Todo ID (for updates) |

## Management

```
/todos               # List all todos
/todos add "task"    # Add todo
/todos done 1        # Complete todo
/todos clear         # Clear completed
```

## ableton-mcp Tasks

```
> Add todo: Fix socket timeout in test_create_track
> Add todo: Create hi-hat track script
> Add todo: Add MCP tool for audio analysis
> Add todo: Update documentation
```

## Integration

Todos sync with conversation:
```
> What are my current todos?
[Lists pending tasks]

> I finished the timeout fix
[Marks as complete]
```

## Related Pages

- [Memory Tool](memory.md) - Persistent context
- [Tools](tools.md) - All tools
