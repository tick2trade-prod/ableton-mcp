# Execute Batch Skill

## Overview

Execute multiple tasks in parallel for 5-20x speedup. Perfect for scaffolding complete features with multiple independent files simultaneously.

## Usage

Type `/execute-batch-skill` followed by task list.

## Parameters

- `tasks`: List of independent tasks (required)
- `language`: Programming language (default: python)
- `max_concurrent`: Maximum parallel tasks (default: 5)
- `run_tests`: Run tests after generation (default: true)

## Example Usage

### Feature Scaffolding

```
/execute-batch-skill
Tasks:
1. Create User model (Pydantic)
2. Create UserService (business logic)
3. Create auth endpoints (FastAPI)
4. Create tests (pytest)
Language: python
Max Concurrent: 4
```

### Full Stack Feature

```
/execute-batch-skill
Tasks:
1. Backend: User model (app/models/user.py)
2. Backend: Auth service (app/services/auth.py)
3. Backend: API endpoints (app/api/auth.py)
4. Frontend: Login component (frontend/components/Login.tsx)
5. Frontend: Register component (frontend/components/Register.tsx)
6. Tests: Backend tests (tests/test_auth.py)
Max Concurrent: 5
```

### Quick Scaffold

```
/execute-batch-skill
Tasks:
1. Create CRUD endpoints for Product model
2. Create Product service layer
3. Create Product tests
Language: python
```

## Workflow

1. **Task Decomposition**:
   - Parse task list
   - Identify dependencies
   - Group independent tasks
   - Validate task count (max 10)

2. **Parallel Planning**:
   - Use small model (llama3.2:3b) for decomposition
   - Generate file specifications
   - Validate no circular dependencies
   - Estimate completion time

3. **Parallel Execution**:
   - Call `app.server.skills.batch_execution.execute_parallel_tasks()`
   - Use `asyncio.gather` for concurrency
   - Execute up to `max_concurrent` tasks simultaneously
   - Monitor progress

4. **Programmatic Write**:
   - As each task finishes, use `coder_tool.write_file()` directly
   - **Do not** paste code into chat
   - Write directly to filesystem
   - Apply linting automatically

5. **Integration Test**:
   - Once all files written, trigger pytest
   - Run on new directory
   - Report pass/fail status only
   - Calculate coverage

6. **Output**:
   - Return batch result
   - Include per-task metrics
   - Report overall success rate

## Implementation

This command uses:
- **Batch Skill**: `app.server.skills.batch_execution.execute_parallel_tasks()`
- **Coder Agents**: Multiple instances in parallel
- **Task Service**: `app.server.services.task_service` (Dramatiq)
- **Async Execution**: `asyncio.gather()`

## Output Format

```json
{
  "success": true,
  "total_tasks": 5,
  "completed": 5,
  "failed": 0,
  "tasks": [
    {
      "task": "Create User model",
      "file": "app/models/user.py",
      "status": "completed",
      "latency_ms": 3200,
      "lines": 85
    },
    {
      "task": "Create UserService",
      "file": "app/services/user_service.py",
      "status": "completed",
      "latency_ms": 4100,
      "lines": 120
    },
    {
      "task": "Create auth endpoints",
      "file": "app/api/auth.py",
      "status": "completed",
      "latency_ms": 3800,
      "lines": 95
    },
    {
      "task": "Create tests",
      "file": "tests/unit/test_auth.py",
      "status": "completed",
      "latency_ms": 3500,
      "lines": 142
    },
    {
      "task": "Create integration tests",
      "file": "tests/integration/test_auth_flow.py",
      "status": "completed",
      "latency_ms": 3900,
      "lines": 98
    }
  ],
  "metrics": {
    "total_latency_ms": 4100,
    "sequential_estimate_ms": 18500,
    "speedup": "4.5x",
    "test_results": {
      "passed": 26,
      "failed": 0,
      "total": 26
    }
  }
}
```

## Performance

| Tasks | Sequential | Parallel (5 concurrent) | Speedup |
|-------|-----------|------------------------|---------|
| 1 | 3-5 min | 3-5 min | 1x |
| 3 | 9-15 min | 3-5 min | 3x |
| 5 | 15-25 min | 3-5 min | 5x |
| 10 | 30-50 min | 6-10 min | 5-10x |

## Best Practices

- Group related, independent tasks together
- Use appropriate max_concurrent (default: 5)
- Leverage parallelization for maximum speedup
- Review generated files for consistency
- Run integration tests after batch completion
- Use for complete feature sets, not single files
- Ensure tasks have no dependencies

## Task Independence

✅ **Good (Independent)**:
```
1. Create User model
2. Create Product model
3. Create Order model
```

❌ **Bad (Dependent)**:
```
1. Create User model
2. Create UserService (depends on User model)
3. Create auth endpoints (depends on UserService)
```

## Related Commands

- `/batch-implement` - Alternative batch generation command
- `/execute-implementation-skill` - Single file implementation
- `/generate-code-streaming` - Streaming single file generation
- `/validate-architecture` - Pre-batch validation

## Requirements

- Ollama server running
- Sufficient system resources (5 concurrent LLM calls)
- Tasks must be independent
- Max 10 tasks per batch
