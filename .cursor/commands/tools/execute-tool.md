# Exec: Tool

**Rank**: 5 - Hybrid Registry + Execution Commands

## Overview

Execute any tool from the 3000_INDEX_TOOLS registry by ID.

## Usage

```
/exec-tool tool_id="3001" params='{"package": "fastapi"}'
```

## Parameters

- `tool_id`: Tool ID from registry (required)
- `params`: Tool-specific parameters as JSON (required)

## Available Tools

See `.cursor/commands/app/registry/3000_INDEX_TOOLS.md`

## Implementation

```python
from app.server.tools import get_tool

tool = get_tool(tool_id)
result = await tool.execute(**params)
```

## Output

```json
{"tool_id": "3001", "result": {...}}
```
