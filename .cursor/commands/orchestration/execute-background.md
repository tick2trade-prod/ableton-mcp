# Orchestrator: Execute Task Background

## Overview

Queue task for background execution. This command invokes the `execute_task_background()` Dramatiq actor from `app/server/orchestrator.py` to queue tasks for asynchronous background processing.

## Usage

Type `/orchestrator-execute-background` followed by the task details.

## Parameters

- `task`: Task description (required)
- `action`: Action mode (research, plan, code, execute) (required)
- `language`: Programming language (default: "python")
- `priority`: Task priority (low, normal, high) (default: "normal")
- `max_retries`: Maximum retry attempts (default: 3)
- `timeout`: Task timeout in seconds (default: 3600)

## Example Usage

### Queue Coding Task

```
/orchestrator-execute-background
Task: Implement user authentication
Action: code
Language: python
Priority: high
```

### Queue Research Task

```
/orchestrator-execute-background
Task: Microservices architecture patterns
Action: research
Priority: normal
```

### Queue Planning Task

```
/orchestrator-execute-background
Task: Design payment processing system
Action: plan
Priority: high
Max Retries: 5
```

## Background Processing

### Dramatiq Actor

```python
from app.server.orchestrator import execute_task_background

# Queue task
task_id = execute_task_background.send(
    task="Implement user authentication",
    action="code",
    language="python"
)

print(f"Task queued: {task_id}")
```

### Task Queue

- **Broker**: Redis
- **Queue**: default
- **Workers**: Configurable
- **Retry**: Exponential backoff
- **Timeout**: 3600 seconds default

## Task Status

### Check Status

```python
from app.server.services.task_service import get_task_status

# Check task status
status = await get_task_status(task_id)
print(f"Status: {status.state}")
```

### Status States

- `pending`: Task queued, not started
- `started`: Task picked up by worker
- `success`: Task completed successfully
- `failure`: Task failed
- `retry`: Task being retried

## Output Format

### Task Queued

```json
{
    "task_id": "task-abc123",
    "task": "Implement user authentication",
    "action": "code",
    "language": "python",
    "priority": "high",
    "status": "pending",
    "queued_at": "2025-12-04T10:30:00Z",
    "estimated_start": "2025-12-04T10:30:05Z"
}
```

### Task Started

```json
{
    "task_id": "task-abc123",
    "status": "started",
    "started_at": "2025-12-04T10:30:05Z",
    "worker_id": "worker-1",
    "progress": {
        "current_step": "code_generation",
        "percent_complete": 25
    }
}
```

### Task Completed

```json
{
    "task_id": "task-abc123",
    "status": "success",
    "started_at": "2025-12-04T10:30:05Z",
    "completed_at": "2025-12-04T10:45:00Z",
    "duration_ms": 895000,
    "result": {
        "files_created": ["app/auth/jwt.py", "tests/test_jwt.py"],
        "files_modified": ["app/main.py"],
        "linting_passed": true,
        "tests_passed": 15
    }
}
```

### Task Failed

```json
{
    "task_id": "task-abc123",
    "status": "failure",
    "started_at": "2025-12-04T10:30:05Z",
    "failed_at": "2025-12-04T10:32:00Z",
    "error": {
        "type": "ValidationError",
        "message": "Package 'nonexistent-lib' not found",
        "traceback": "..."
    },
    "retry_count": 1,
    "max_retries": 3,
    "next_retry_at": "2025-12-04T10:32:30Z"
}
```

## Worker Management

### Start Worker

```bash
# Start Dramatiq worker
uv run dramatiq app.server.orchestrator

# Start with multiple workers
uv run dramatiq app.server.orchestrator --processes 4 --threads 8
```

### Monitor Workers

```bash
# Check worker status
dramatiq-status

# Monitor queue depth
redis-cli LLEN dramatiq:default.DQ
```

## Retry Logic

### Automatic Retry

- Max retries: 3 (configurable)
- Backoff: Exponential (1s, 2s, 4s, 8s)
- Retry on: Transient failures
- No retry on: Validation errors

### Manual Retry

```python
from app.server.services.task_service import retry_task

# Retry failed task
result = await retry_task(task_id)
```

## Best Practices

- Use background tasks for long-running operations
- Set appropriate priorities
- Configure timeouts based on task complexity
- Monitor queue depth
- Handle failures gracefully
- Use retries for transient failures only
- Check task status periodically

## Integration

- Uses Dramatiq for task queue
- Redis as message broker
- Result backend for status
- Integrates with all skills

## Related Commands

- `/execute-task` - Synchronous task execution
- `/execute-workflow` - Full workflow execution
- `/run-agent-task` - Alternative task execution
- `/skill-planning` - Planning tasks
- `/skill-implementation` - Coding tasks

## Source

- **File**: `app/server/orchestrator.py`
- **Function**: `execute_task_background()` (Dramatiq actor)
- **Technology**: Dramatiq + Redis
- **Layer**: Orchestrator (Router)
