# Op: File Write

**Rank**: 4 - Atomic Operation Commands

## Overview

Write single file with linting and validation.

## Usage

```
/op-file-write filepath="app/models/user.py" content="..." run_lint=true
```

## Parameters

- `filepath`: Target file path (required)
- `content`: File content (required)
- `run_lint`: Run linter after write (default: true)
- `backup`: Create backup (default: true)

## Implementation

```python
from app.server.tools.coder_tool import robust_file_write

await robust_file_write(
    filepath=filepath,
    content=content,
    run_lint=run_lint,
)
```

## Output

```json
{"filepath": "...", "status": "written", "linter": "passed"}
```
