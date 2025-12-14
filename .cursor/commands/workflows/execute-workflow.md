# Exec: Workflow

**Rank**: 5 - Hybrid Registry + Execution Commands

## Overview

Execute any workflow from the 4000_INDEX_WORKFLOWS registry by ID.

## Usage

```
/exec-workflow workflow_id="4001" params='{"feature": "User auth"}'
```

## Parameters

- `workflow_id`: Workflow ID from registry (required)
- `params`: Workflow-specific parameters as JSON (required)

## Available Workflows

See `.cursor/commands/app/registry/4000_INDEX_WORKFLOWS.md`

## Implementation

```python
from app.server.orchestrator import execute_workflow

workflow_config = get_workflow_config(workflow_id)
result = await execute_workflow(**workflow_config, **params)
```

## Output

```json
{"workflow_id": "4001", "result": {...}}
```
