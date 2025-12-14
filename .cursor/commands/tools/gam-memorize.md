# GAM Memorize

## Overview

Save content to GAM long-term memory for future retrieval and context-aware operations. Memorized content persists across sessions and can be retrieved via semantic search.

> **Layer**: HOW (Execution Primitives)
> **Rank**: 2/4 - Layer-Based + Atomic Operation (`/op-gam-memorize`)

## Usage

Type `/gam-memorize` followed by the content to memorize.

## Parameters

- `content`: Content to memorize (required)
- `tags`: Optional tags for categorization (optional)
- `source`: Source identifier (optional)

## Example Usage

### Memorize Documentation

```
/gam-memorize
Content: FastAPI async patterns best practices: Use async/await for I/O operations, use background tasks for long-running operations, use dependency injection for database connections.
Tags: fastapi, async, best-practices
```

### Memorize Code Patterns

```
/gam-memorize
Content: Python type hints pattern: Use Optional[str] for FastMCP tool decorators, use str | None for underlying functions. Always include type hints in function signatures.
Tags: python, type-hints, fastmcp
Source: code-review-2024-12
```

### Memorize Research Findings

```
/gam-memorize
Content: Research findings on vector search optimization: Use LanceDB with LLM format for 20-30% token reduction, implement caching for 40-60% latency reduction, use batch operations for 5-20x speedup.
Tags: vector-search, optimization, lancedb
```

## Workflow

1. **Content Processing**:
   - Call `app.core.GAMMemoryManager.memorize()`
   - Generate embeddings for semantic search
   - Add metadata (tags, source, timestamp)

2. **Indexing**:
   - Store in GAM memory store
   - Index for BM25 retrieval
   - Index for semantic search

3. **Verification**:
   - Confirm successful storage
   - Return memory ID

4. **Output**:
   - Confirmation message
   - Memory ID for reference

## Implementation

This command uses:
- **Core GAM**: `app.core.GAMMemoryManager.memorize()`
- **MCP Tool**: `app.server.tools.gam_tool.memorize_content()`
- **Storage**: Persistent memory store

## Output Format

```json
{
  "success": true,
  "memory_id": "mem-abc123",
  "content_length": 256,
  "tags": ["fastapi", "async", "best-practices"],
  "timestamp": "2024-12-04T10:30:00Z",
  "message": "Content successfully memorized"
}
```

## Best Practices

- Memorize comprehensive findings (combining memory + web research)
- Include context and source information
- Use clear, structured content
- Add relevant tags for easy retrieval
- Memorize code patterns and best practices
- Update memory with new findings
- Avoid duplicate content

## Content Types to Memorize

1. **Best Practices**: Language/framework patterns
2. **Code Patterns**: Reusable code snippets
3. **Research Findings**: Web research results
4. **Lessons Learned**: Project-specific insights
5. **Documentation**: API usage, configuration
6. **Troubleshooting**: Common issues and solutions

## Related Commands

- `/gam-research` - Research from GAM memory
- `/deep-research` - Memory + web research workflow
- `/371-research-memorize` - Web search + memorize
- `/research-memorize-generate` - Complete research workflow

## Requirements

- GAM memory initialized
- Ollama server running (for embeddings)
- Sufficient storage space
