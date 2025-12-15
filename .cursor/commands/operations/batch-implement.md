# Batch Implement

## Overview

High-throughput implementation of multiple files simultaneously. Perfect for scaffolding a complete feature with 5-20x speedup.

## Usage

Type `/batch-implement` followed by feature description or file list.

## Parameters

- `feature`: Feature description or list of files to create (required)
- `language`: Programming language (default: python)
- `max_concurrent`: Maximum parallel tasks (default: 5)
- `run_tests`: Run tests after generation (default: true)

## Example Usage

### Feature Scaffolding

```
/batch-implement
Feature: User authentication system with FastAPI
Files:
- models/user.py (Pydantic models)
- services/auth.py (Business logic)
- api/endpoints/auth.py (FastAPI endpoints)
- tests/test_auth.py (Pytest tests)
Language: python
Max Concurrent: 4
```

### Full Stack Feature

```
/batch-implement
Feature: Blog post management
Files:
- backend/models/post.py
- backend/services/post_service.py
- backend/api/posts.py
- frontend/components/PostList.tsx
- frontend/components/PostEditor.tsx
- tests/test_posts.py
Max Concurrent: 5
```

### Quick Scaffold

```
/batch-implement
Feature: Create CRUD endpoints for Product model
Language: python
Run Tests: true
```

## Workflow

1. **Plan Decomposition**:
   - Take user request and break into independent file tasks
   - *Optimization:* Use small model (e.g., `llama3.2:3b`) for decomposition

2. **Parallel Execution**:
   - Call `batch_execution.execute_parallel_tasks(tasks)`
   - Use `asyncio.gather` to run up to 5 concurrent generations

3. **Programmatic Write**:
   - As each task finishes, use `coder_tool.write_file()` directly
   - **Do not** paste code into chat; write directly to filesystem

4. **Integration Test**:
   - Once all files written, trigger `pytest` run on new directory
   - Report pass/fail status only

## Best Practices

- Group related, independent tasks together
- Use appropriate max_concurrent (default: 5)
- Leverage parallelization for maximum speedup
- Review generated files for consistency
- Run integration tests after batch completion
- Use for complete feature sets, not single files

## Performance

- **Sequential**: ~2-5 minutes per file
- **Parallel (5 concurrent)**: ~2-5 minutes total for 5 files
- **Speedup**: 5-20x depending on task complexity

## Related Commands

- `/validate-architecture` - Validate before batch implementation
- `/generate-code-streaming` - Single file with streaming
- `/generate-code-batch` - Alternative batch generation
