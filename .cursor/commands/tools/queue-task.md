# Queue Task

## Overview

Queue a task for background execution using Dramatiq. Enables long-running operations without blocking the main thread.

## Usage

Type `/queue-task` followed by task description and parameters.

## Parameters

- `task`: Task description (required)
- `action`: Action to perform (research, plan, code, execute) (required)
- `language`: Programming language (default: python)
- `priority`: Task priority (low, normal, high) (default: normal)

## Example Usage

### Queue Code Generation

```
/queue-task
Task: Create authentication system with JWT tokens
Action: code
Language: python
Priority: high
```

### Queue Planning Task

```
/queue-task
Task: Design microservices architecture for blog platform
Action: plan
Priority: normal
```

### Queue Research

```
/queue-task
Task: Research FastAPI production deployment best practices
Action: research
Priority: low
```

## Workflow

1. **Task Creation**:
   - Create `TaskRequest` (Pydantic model)
   - Set priority and parameters
   - Generate task ID

2. **Queue Submission**:
   - Call `app.server.tools.task_tool.queue_task()`
   - Submit to Dramatiq broker (Redis)
   - Store in result backend

3. **Background Execution**:
   - Dramatiq worker picks up task
   - Executes `orchestrator.execute_task_background()`
   - Updates task status

4. **Result Storage**:
   - Store result in Redis backend
   - Update task status (queued → running → completed/failed)
   - Set TTL for result (24 hours)

5. **Output**:
   - Return task ID immediately
   - Provide status check command

## Implementation

This command uses:
- **Task Tool**: `app.server.tools.task_tool.queue_task()`
- **Orchestrator**: `app.server.orchestrator.execute_task_background()`
- **Dramatiq**: Task queue with Redis broker
- **Protocol Models**: `app.server.protocols.task_models.TaskRequest`

## Output Format

```json
{
  "task_id": "task-abc123",
  "status": "queued",
  "task": "Create authentication system",
  "action": "code",
  "priority": "high",
  "queued_at": "2024-12-04T10:30:00Z",
  "estimated_duration": "5-10 minutes",
  "check_status": "/check-task-status task-abc123"
}
```

## Task Priorities

- **HIGH**: Executed first, max 3 retries, 1 hour timeout
- **NORMAL**: Standard priority, max 3 retries, 1 hour timeout
- **LOW**: Executed last, max 2 retries, 30 min timeout

## Task States

1. **queued**: Waiting for worker
2. **running**: Currently executing
3. **completed**: Successfully finished
4. **failed**: Execution failed
5. **cancelled**: Manually cancelled

## Best Practices

- Use for tasks > 30 seconds
- Set appropriate priority
- Monitor task status
- Handle failures gracefully
- Set reasonable timeouts
- Clean up old results

## Related Commands

- `/check-task-status` - Check task status and result
- `/execute-task-background` - Direct background execution
- `/execute-workflow` - Synchronous workflow execution

## Requirements

- Redis running (from docker-compose.yml)
- Dramatiq worker running: `uv run dramatiq app.server.orchestrator`
- Task service configured
