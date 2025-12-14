# Memorize Content

## Overview

Memorize content using GAM MemoryAgent for future retrieval and context-aware operations.

## Usage

Type `/memorize-content` followed by the content to memorize.

## Parameters

- `content`: Content to memorize (required)

## Example Usage

### Memorize Documentation

```
/memorize-content
Content: FastAPI async patterns best practices: Use async/await for I/O operations, use background tasks for long-running operations, use dependency injection for database connections.
```

### Memorize Code Patterns

```
/memorize-content
Content: Python type hints pattern: Use Optional[str] for FastMCP tool decorators, use str | None for underlying functions. Always include type hints in function signatures.
```

### Memorize Research Findings

```
/memorize-content
Content: Research findings on vector search optimization: Use LanceDB with LLM format for 20-30% token reduction, implement caching for 40-60% latency reduction, use batch operations for 5-20x speedup.
```

## Workflow

1. Content is memorized using GAM MemoryAgent (via `app.core.GAMMemoryManager`)
2. Content is indexed for semantic search
3. Content can be retrieved using `research_memory`
4. Content persists across sessions

## Implementation

This command uses the `app.core.GAMMemoryManager` class from the refactored `app/` structure:
- Core GAM integration: `app.core.GAMMemoryManager.memorize()`
- Memory persistence: Content stored in GAM memory store

## Best Practices

- Memorize comprehensive findings (combining memory + web research)
- Include context and source information
- Use clear, structured content
- Memorize code patterns and best practices
- Update memory with new findings

## Future Improvements (KISS)

- **Auto-Summarize Before Storing**: Add a lightweight summarization pass (LLM or rules-based) that trims redundant phrases and enforces concise bullet formatting so GAM memory stores only the most useful tokens per entry.
- **Source & TTL Metadata**: Automatically attach source URLs, timestamps, and optional TTLs when memorizing content so later retrieval can filter or expire stale knowledge without manual bookkeeping.
- **Deduplicate Similar Entries**: Compute an embedding similarity score before writing; skip (or merge) content that is >= a configurable threshold to prevent repeated storage of near-identical findings.
- **Batch Memorization Support**: Support passing multiple `content` blocks in one command, chunking them into a single transaction to reduce write latency when recording large research dumps.
- **Validation Hooks**: Provide a simple regex/quality-check hook (e.g., minimum length, banned tokens) to prevent accidental memorization of noisy logs or secrets.
