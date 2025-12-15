# Domain: Agent Task

## Overview

Agent task management. This command provides direct access to the pure domain logic in `app/orchestration/agent_task.py` for managing agent tasks, workflows, and execution state.

## Usage

Type `/domain-agent-task` followed by the task operation.

## Parameters

- `operation`: Operation to perform (create, execute, status, cancel, retry) (required)
- `task_name`: Task name (required for create/execute)
- `task_type`: Task type (planning, coding, review, research) (required for create)
- `task_params`: Task parameters (varies by type)
- `task_id`: Task ID (for status/cancel/retry operations)
- `priority`: Task priority (low, medium, high, critical) (default: "medium")

## Example Usage

### Create Task

```
/domain-agent-task
Operation: create
Task Name: Implement user authentication
Task Type: coding
Task Params: |
  language: python
  framework: fastapi
  features: [jwt, refresh_tokens, rate_limiting]
Priority: high
```

### Execute Task

```
/domain-agent-task
Operation: execute
Task ID: task-abc123
```

### Check Status

```
/domain-agent-task
Operation: status
Task ID: task-abc123
```

### Cancel Task

```
/domain-agent-task
Operation: cancel
Task ID: task-abc123
```

### Retry Failed Task

```
/domain-agent-task
Operation: retry
Task ID: task-abc123
```

## Domain Logic

### AgentTask

Pure domain class for task management.

```python
from app.orchestration.agent_task import AgentTask, TaskType, TaskStatus

# Create task
task = AgentTask(
    name="Implement user authentication",
    task_type=TaskType.CODING,
    params={
        "language": "python",
        "framework": "fastapi",
        "features": ["jwt", "refresh_tokens"]
    },
    priority="high"
)

# Execute task
result = await task.execute()

# Check status
status = task.get_status()

# Cancel task
task.cancel()

# Retry task
task.retry()
```

## Task Types

### Planning Task

```python
task = AgentTask(
    name="Plan microservices architecture",
    task_type=TaskType.PLANNING,
    params={
        "feature": "user management",
        "use_web_search": True,
        "qa_enabled": True
    }
)
```

### Coding Task

```python
task = AgentTask(
    name="Implement REST API",
    task_type=TaskType.CODING,
    params={
        "language": "python",
        "prompt": "Create FastAPI endpoints",
        "include_tests": True
    }
)
```

### Review Task

```python
task = AgentTask(
    name="Review authentication code",
    task_type=TaskType.REVIEW,
    params={
        "scope": "current_changes",
        "run_qa": True,
        "min_qa_score": 80
    }
)
```

### Research Task

```python
task = AgentTask(
    name="Research caching strategies",
    task_type=TaskType.RESEARCH,
    params={
        "topic": "Redis caching patterns",
        "depth": "deep",
        "use_web_search": True
    }
)
```

## Task Status

### Lifecycle

```
pending → in_progress → completed
                    → failed → retrying → completed
                                       → failed
                    → cancelled
```

### Status Codes

- `pending`: Task created, not started
- `in_progress`: Task currently executing
- `completed`: Task finished successfully
- `failed`: Task failed with error
- `cancelled`: Task cancelled by user
- `retrying`: Task being retried after failure

## Output Format

### Task Creation

```python
{
    "task_id": "task-abc123",
    "task_name": "Implement user authentication",
    "task_type": "coding",
    "status": "pending",
    "priority": "high",
    "created_at": "2025-12-04T10:30:00Z",
    "params": {
        "language": "python",
        "framework": "fastapi",
        "features": ["jwt", "refresh_tokens", "rate_limiting"]
    }
}
```

### Task Execution

```python
{
    "task_id": "task-abc123",
    "status": "in_progress",
    "started_at": "2025-12-04T10:31:00Z",
    "progress": {
        "current_step": "code_generation",
        "steps_completed": 2,
        "total_steps": 5,
        "percent_complete": 40
    }
}
```

### Task Completion

```python
{
    "task_id": "task-abc123",
    "status": "completed",
    "started_at": "2025-12-04T10:31:00Z",
    "completed_at": "2025-12-04T10:45:00Z",
    "duration_ms": 840000,
    "result": {
        "files_created": ["app/auth/jwt.py", "tests/test_jwt.py"],
        "files_modified": ["app/main.py"],
        "tests_passed": 15,
        "linting_passed": True
    }
}
```

### Task Failure

```python
{
    "task_id": "task-abc123",
    "status": "failed",
    "started_at": "2025-12-04T10:31:00Z",
    "failed_at": "2025-12-04T10:35:00Z",
    "error": {
        "type": "ValidationError",
        "message": "Package 'nonexistent-lib' not found in PyPI",
        "step": "dependency_validation",
        "retryable": True
    },
    "retry_count": 0,
    "max_retries": 3
}
```

## Task Management

### Priority Queue

Tasks are executed based on priority:

1. **Critical**: Security fixes, production issues
2. **High**: Important features, blocking issues
3. **Medium**: Regular features, improvements
4. **Low**: Nice-to-haves, optimizations

### Retry Logic

- Automatic retry for transient failures
- Exponential backoff between retries
- Max 3 retries by default
- Manual retry option

### Cancellation

- Graceful cancellation when possible
- Cleanup of partial work
- Status update to cancelled
- No automatic retry after cancellation

## Best Practices

- Use appropriate task types
- Set realistic priorities
- Provide complete task params
- Monitor task status
- Handle failures gracefully
- Retry transient failures only

## Integration

- Used by `/run-agent-task` command
- Wrapped by orchestrator workflows
- Manages task lifecycle
- Pure domain logic, no infrastructure

## Related Commands

- `/run-agent-task` - Command wrapper
- `/execute-workflow` - Workflow execution
- `/skill-planning` - Planning tasks
- `/skill-implementation` - Coding tasks

## Source

- **File**: `app/orchestration/agent_task.py`
- **Class**: `AgentTask`, `TaskManager`
- **Layer**: Domain (Orchestration)
