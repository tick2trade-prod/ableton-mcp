# Orchestrator: Execute Workflow

## Overview

Execute complete workflow. This command invokes the `execute_workflow()` function from `app/server/orchestrator.py` to execute a full feature implementation workflow with state management.

## Usage

Type `/orchestrator-execute-workflow` followed by the feature name.

## Parameters

- `feature_name`: Name of feature to implement (required)
- `workflow_id`: Optional workflow ID (auto-generated if not provided)
- `save_checkpoints`: Save workflow checkpoints (default: true)
- `continue_on_error`: Continue on non-critical errors (default: false)

## Example Usage

### Execute Full Workflow

```
/orchestrator-execute-workflow
Feature Name: User authentication with JWT
Save Checkpoints: true
```

### Resume Workflow

```
/orchestrator-execute-workflow
Feature Name: User authentication with JWT
Workflow ID: workflow-abc123
```

### Execute with Error Handling

```
/orchestrator-execute-workflow
Feature Name: Payment processing
Continue On Error: false
```

## Workflow Phases

### Phase 1: Planning

1. Query GAM for context
2. Create implementation plan
3. Run QA validation
4. Save checkpoint

### Phase 2: Implementation

1. Generate code
2. Run linting
3. Execute tests
4. Save checkpoint

### Phase 3: Review

1. Run QA/Critic
2. Create pull request
3. Validate changes
4. Save checkpoint

## Workflow State

### State Management

```python
from app.server.orchestrator import execute_workflow

# Execute workflow
result = await execute_workflow(
    feature_name="User authentication with JWT",
    workflow_id="workflow-abc123"
)

# Check workflow state
from app.server.services.state_service import get_state_service

state_service = get_state_service()
state = state_service.get_state("workflow-abc123")
```

### Checkpoints

```python
{
    "workflow_id": "workflow-abc123",
    "feature_name": "User authentication with JWT",
    "checkpoints": [
        {
            "step": "planning",
            "state": "completed",
            "timestamp": "2025-12-04T10:30:00Z",
            "data": {"plan": {...}}
        },
        {
            "step": "implementation",
            "state": "in_progress",
            "timestamp": "2025-12-04T10:35:00Z",
            "data": {}
        }
    ]
}
```

## Output Format

### Success

```json
{
    "workflow_id": "workflow-abc123",
    "feature_name": "User authentication with JWT",
    "success": true,
    "steps_completed": ["planning", "implementation", "review"],
    "checkpoints": [
        {
            "step": "planning",
            "state": "completed",
            "data": {"plan": {...}}
        },
        {
            "step": "implementation",
            "state": "completed",
            "data": {"files_created": [...]}
        },
        {
            "step": "review",
            "state": "completed",
            "data": {"pr_url": "..."}
        }
    ],
    "latency_ms": 45678
}
```

### Failure

```json
{
    "workflow_id": "workflow-abc123",
    "feature_name": "User authentication with JWT",
    "success": false,
    "steps_completed": ["planning"],
    "checkpoints": [
        {
            "step": "planning",
            "state": "completed",
            "data": {"plan": {...}}
        },
        {
            "step": "implementation",
            "state": "failed",
            "data": {"error": "Linting failed"}
        }
    ],
    "error": "Implementation failed: Linting errors found",
    "latency_ms": 12345
}
```

## Workflow Recovery

### Resume from Checkpoint

```python
# Resume failed workflow
result = await execute_workflow(
    feature_name="User authentication",
    workflow_id="workflow-abc123"  # Will resume from last checkpoint
)
```

### Retry Failed Step

```python
# Get state and retry
state_service = get_state_service()
state = state_service.get_state("workflow-abc123")

# Identify failed step
failed_step = next(
    cp for cp in state.checkpoints
    if cp.state == "failed"
)

# Retry from that step
# (Implementation would handle this)
```

## Best Practices

- Provide clear feature names
- Save checkpoints for long workflows
- Handle errors gracefully
- Resume from checkpoints on failure
- Monitor workflow progress
- Review checkpoints for debugging

## Integration

- Uses `/skill-planning` for planning
- Uses `/skill-implementation` for coding
- Uses `/skill-review` for review
- Manages state via `StateService`

## Related Commands

- `/execute-task` - Single task execution
- `/execute-streaming` - Streaming workflow
- `/run-agent-task` - Alternative task execution
- `/skill-planning` - Planning phase
- `/skill-implementation` - Implementation phase

## Source

- **File**: `app/server/orchestrator.py`
- **Function**: `execute_workflow()`
- **Layer**: Orchestrator (Router)
