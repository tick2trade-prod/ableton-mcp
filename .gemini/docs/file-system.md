# File System Tools

> Source: [https://geminicli.com/docs/tools/file-system](https://geminicli.com/docs/tools/file-system)

## Overview

File system tools enable reading and writing files.

## read_file

Read file contents:
```
> Read the contents of pyproject.toml
[Returns file contents]
```

### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | File path |
| `encoding` | string | Optional encoding |

## write_file

Write or create files:
```
> Create a new file config.json with database settings
[Creates file]
```

### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | File path |
| `content` | string | File contents |
| `mode` | string | "write" or "append" |

## File References

Use `@` syntax for context:
```
> Explain @tests/test_tools.py
[Reads and explains file]
```

## ableton-mcp Usage

```
> Read @live_set/lily_palmer/i_am_machine/track_01_kick.py

> Create live_set/new/track_02_rumble.py with rumble bass pattern
```

## Related Pages

- [Tools](tools.md) - All tools
- [Shell Tool](shell.md) - Command execution
