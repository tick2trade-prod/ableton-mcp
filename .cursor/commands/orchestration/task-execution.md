# Task Execution

## Overview

Execute tasks with specific action modes (research, plan, code, execute). This command provides flexible task routing with optional background execution using Dramatiq task queue.

## Usage

Type `/task-execution` followed by your task request.

## Parameters

- `task`: Task description (required)
- `action`: Action mode (default: execute)
  - `research`: Research and memorize findings
  - `plan`: Generate implementation plan
  - `code`: Generate code only
  - `execute`: Full workflow execution
- `language`: Programming language (default: python)
- `background`: Queue for background execution (default: false)
- `priority`: Task priority for background queue (default: normal)
  - `low`: Low priority
  - `normal`: Normal priority
  - `high`: High priority

## Example Usage

### Research Mode

```
/task-execution
Task: Research best practices for FastAPI authentication
Action: research
```

### Planning Mode

```
/task-execution
Task: Create user authentication system
Action: plan
Language: python
```

### Code Generation Mode

```
/task-execution
Task: Implement JWT token validation
Action: code
Language: python
```

### Background Execution

```
/task-execution
Task: Refactor entire database layer
Action: execute
Background: true
Priority: high
```

## Workflow

1. **Action Routing**:
   - Parse action parameter to determine execution path
   - Map to appropriate skill:
     - `research` → `research_and_plan(use_web_search=True)`
     - `plan` → `execute_planning(gam_memory=gam)`
     - `code` → `generate_and_implement(prompt, language)`
     - `execute` → `execute_workflow(task)`

2. **Research Mode** (action=research):
   - Initialize GAM memory manager
   - Perform web search using Tavily
   - Memorize findings: `gam.memorize(content, metadata)`
   - Return research summary with sources
   - **Latency**: ~5-10 seconds

3. **Plan Mode** (action=plan):
   - Create GAM memory instance
   - Execute planning skill: `plan = await execute_planning(feature_name=task, gam_memory=gam)`
   - Run QA validation on plan
   - Return structured plan with todos
   - **Latency**: ~10-20 seconds

4. **Code Mode** (action=code):
   - Quick GAM memory lookup for context
   - Generate code: `result = await generate_and_implement(prompt=task, language=language)`
   - Auto-lint with `coder_tool.robust_file_write()`
   - Return generated code with file changes
   - **Latency**: ~15-30 seconds

5. **Execute Mode** (action=execute):
   - Delegate to full workflow: `await execute_workflow(task)`
   - Includes planning + implementation + QA
   - **Latency**: ~60-120 seconds

6. **Background Execution** (background=true):
   - Queue task with Dramatiq: `execute_task_background.send(task, action, language)`
   - Return task_id immediately
   - Check status: `/task-status task_id={task_id}`
   - **Latency**: <1 second (queuing only)

## Background Task Management

### Queue Task

```python
# Queues task and returns immediately
response = {
    "task_id": "task-a3f8b2c1",
    "status": "queued",
    "task": "Refactor database layer",
    "action": "execute",
    "priority": "high"
}
```

### Check Status

```
/task-status
Task ID: task-a3f8b2c1
```

### Response

```json
{
    "task_id": "task-a3f8b2c1",
    "status": "in_progress",
    "progress": "Implementation phase: 3/5 tasks complete",
    "started_at": "2025-12-04T10:30:00Z",
    "estimated_completion": "2025-12-04T10:32:00Z"
}
```

## Performance Tracking

All executions include latency measurement:

```json
{
    "task": "Create REST API endpoint",
    "action": "code",
    "result": { ... },
    "latency_ms": 18432,
    "tokens_used": 2500
}
```

## Best Practices

- Use `research` for gathering information before implementation
- Use `plan` to validate architecture before coding
- Use `code` for direct implementation with context
- Use `execute` for complete feature implementation
- Use `background=true` for long-running tasks (>60s)
- Set `priority=high` for urgent background tasks
- Monitor latency for performance optimization

## Integration Points

**Calls:**
- `app/server/orchestrator.py::execute_task()`
- `app/server/orchestrator.py::execute_task_background()` (Dramatiq actor)
- `app/server/skills/planning.py::research_and_plan()`
- `app/server/skills/planning.py::execute_planning()`
- `app/server/skills/implementation.py::generate_and_implement()`
- `app/server/services/task_service.py` (Redis broker)

**Used By:**
- `/generate-code-streaming` - Uses code mode
- `/deep-research` - Uses research mode
- `/autonomous-research` - Uses research + plan modes
- `/batch-implement` - Parallel task execution

## Error Handling

### Synchronous Errors

```json
{
    "task": "Invalid task",
    "action": "code",
    "error": "Syntax validation failed",
    "details": "Missing required parameter: language",
    "latency_ms": 120
}
```

### Background Task Errors

```json
{
    "task_id": "task-a3f8b2c1",
    "status": "failed",
    "error": "Package not found: nonexistent-library",
    "retry_count": 3,
    "failed_at": "2025-12-04T10:31:45Z"
}
```

## Related Commands

- `/workflow-orchestration` - Full workflow with streaming
- `/generate-code-streaming` - Streaming code generation
- `/deep-research` - Deep research with memorization
- `/batch-implement` - Parallel task execution
- `/task-status` - Check background task status
