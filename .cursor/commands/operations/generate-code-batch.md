# Generate Code Batch

## Overview

Generate multiple code features in parallel for 5-20x speedup. Perfect for creating multiple related features simultaneously.

## Usage

Type `/generate-code-batch` followed by a list of tasks.

## Parameters

- `tasks`: List of code generation task descriptions (required)
- `language`: Programming language (default: python)
- `agent_name`: Optional agent name
- `max_concurrent`: Maximum concurrent operations (default: 5)

## Example Usage

### Parallel Feature Generation

```
/generate-code-batch
Tasks:
1. Create FastAPI endpoint for user registration
2. Create FastAPI endpoint for user login
3. Create FastAPI endpoint for user profile
Language: python
Max Concurrent: 5
```

### Multiple Language Generation

```
/generate-code-batch
Tasks:
1. Create Python FastAPI endpoint
2. Create TypeScript React component
3. Create SQL migration script
Max Concurrent: 3
```

### Complete Feature Set

```
/generate-code-batch
Tasks:
1. User model (Pydantic)
2. Database schema (SQLAlchemy)
3. API endpoints (FastAPI)
4. Tests (pytest)
5. Documentation (Markdown)
Language: python
```

## Workflow

1. Tasks are processed in parallel batches
2. Each task uses GAM memory for context
3. Results are aggregated with metrics
4. Partial success is supported (some tasks may fail)

## Best Practices

- Group related tasks together
- Use appropriate max_concurrent (default: 5)
- Leverage parallelization for independent tasks
- Review results for quality and completeness
- Use for creating complete feature sets

## Future Improvements (KISS)

- **Dynamic Concurrency Adjustment**: Implement a simple heuristic to adjust `max_concurrent` based on real-time system load (CPU/memory) or task queue depth, rather than a fixed value.
- **Intelligent Batch Progress Streaming**: Provide more granular status updates or stream intermediate results for each completed task within the batch, rather than waiting for the entire batch to finish. This improves user feedback for long-running batch operations.
- **Ensure Asyncio for All I/O & Tool Calls**: Systematically audit all I/O-bound operations and tool invocations within each batch task to ensure they are fully asynchronous (`asyncio` compatible) and that independent tool calls are executed concurrently using `asyncio.gather`.
- **Tool Call Caching**: Implement a simple in-memory or Redis-backed LRU cache for idempotent tool calls (e.g., `gam.research_memory` with the same query, `coder_tool.read_file`) within each batch task to avoid redundant invocations.
- **`functools.lru_cache` for Internal Functions**: Apply `@functools.lru_cache` to frequently called, pure helper functions (e.g., parsing utilities, prompt templating logic) to minimize redundant computations within the batch generation process.
- **Semantic Chunking for Prompt Context**: When providing existing code as context to the LLM for each batch task, utilize AST to extract and prioritize semantically meaningful code chunks (functions, classes) instead of arbitrary line-based segments. This optimizes input token usage and enhances context relevance.
- **Simple Redis-backed Async Task Queue**: Decouple task submission from immediate execution. Push individual code generation tasks to a Redis queue, allowing a separate worker process to consume and execute them asynchronously. This improves CLI responsiveness and enables robust background processing for large batches.
