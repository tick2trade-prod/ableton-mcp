# Check Task Status

## Overview

Check the status and result of a background task queued via Dramatiq. Retrieves task state, progress, and final result.

## Usage

Type `/check-task-status` followed by task ID.

## Parameters

- `task_id`: Task ID to check (required)
- `include_result`: Include full result (default: true)

## Example Usage

### Check Task Status

```
/check-task-status
Task ID: task-abc123
```

### Check Without Result

```
/check-task-status
Task ID: task-abc123
Include Result: false
```

## Workflow

1. **Task Lookup**:
   - Call `app.server.tools.task_tool.get_task_status()`
   - Query Redis result backend
   - Retrieve task metadata

2. **Status Check**:
   - Get current state (queued, running, completed, failed)
   - Get progress information
   - Get error details (if failed)

3. **Result Retrieval** (if completed):
   - Fetch result from backend
   - Parse result data
   - Include latency metrics

4. **Output**:
   - Return task status
   - Include result if available
   - Provide next steps

## Implementation

This command uses:
- **Task Tool**: `app.server.tools.task_tool.get_task_status()`
- **Redis Backend**: Dramatiq result backend
- **Protocol Models**: `app.server.protocols.task_models.TaskResponse`

## Output Format

### Queued Task

```json
{
  "task_id": "task-abc123",
  "status": "queued",
  "task": "Create authentication system",
  "action": "code",
  "queued_at": "2024-12-04T10:30:00Z",
  "position_in_queue": 3,
  "estimated_start": "2024-12-04T10:32:00Z"
}
```

### Running Task

```json
{
  "task_id": "task-abc123",
  "status": "running",
  "task": "Create authentication system",
  "action": "code",
  "started_at": "2024-12-04T10:31:00Z",
  "progress": "Planning phase completed, starting implementation",
  "estimated_completion": "2024-12-04T10:36:00Z"
}
```

### Completed Task

```json
{
  "task_id": "task-abc123",
  "status": "completed",
  "task": "Create authentication system",
  "action": "code",
  "completed_at": "2024-12-04T10:35:00Z",
  "latency_ms": 240000,
  "result": {
    "files_created": 5,
    "tests_passed": 12,
    "success": true
  }
}
```

### Failed Task

```json
{
  "task_id": "task-abc123",
  "status": "failed",
  "task": "Create authentication system",
  "action": "code",
  "failed_at": "2024-12-04T10:33:00Z",
  "error": "Package 'fake-jwt' not found in PyPI",
  "retry_count": 3,
  "suggestion": "Verify package names and retry"
}
```

## Task Lifecycle

```
queued → running → completed
                 ↘ failed
```

## Best Practices

- Check status periodically for long tasks
- Handle all status states
- Retry failed tasks with fixes
- Clean up completed task results
- Set result TTL appropriately
- Log task metrics for monitoring

## Polling Strategy

For long-running tasks:

```python
# Exponential backoff
intervals = [1, 2, 5, 10, 30, 60]  # seconds

for interval in intervals:
    status = check_task_status(task_id)
    if status in ["completed", "failed"]:
        break
    time.sleep(interval)
```

## Related Commands

- `/queue-task` - Queue background task
- `/execute-task-background` - Direct background execution
- `/execute-workflow` - Synchronous workflow

## Requirements

- Redis running (from docker-compose.yml)
- Dramatiq worker running
- Task result backend configured
- Valid task ID
