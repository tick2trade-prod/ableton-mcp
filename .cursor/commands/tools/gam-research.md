# GAM Research

## Overview

Research from GAM memory using semantic search to retrieve relevant information. Always research from memory first before web search for faster, local token usage.

> **Layer**: HOW (Execution Primitives)
> **Rank**: 4 - Atomic Operation (`/op-gam-search`)

## Usage

Type `/gam-research` followed by your research query.

## Parameters

- `query`: Research query (required)
- `limit`: Maximum results to return (default: 5)
- `min_similarity`: Minimum similarity score (default: 0.7)

## Example Usage

### Basic Research

```
/gam-research
Query: FastAPI async patterns best practices
```

### Focused Research

```
/gam-research
Query: How to use lancedb for vector search optimization
Limit: 3
Min Similarity: 0.8
```

### Code Pattern Research

```
/gam-research
Query: Python type hints patterns for FastMCP decorators
Limit: 10
```

## Workflow

1. **Query Processing**:
   - Call `app.core.GAMMemoryManager.research()`
   - Use semantic search with embeddings
   - Apply similarity threshold

2. **Result Ranking**:
   - Rank by relevance score
   - Filter by min_similarity
   - Limit to requested count

3. **Output**:
   - Return ranked results
   - Include similarity scores
   - Provide source references

## Implementation

This command uses:
- **Core GAM**: `app.core.GAMMemoryManager.research()`
- **MCP Tool**: `app.server.tools.gam_tool.research_memory()`
- **Retriever**: BM25 + semantic search

## Output Format

```json
{
  "query": "FastAPI async patterns",
  "results": [
    {
      "content": "FastAPI async best practices: Use async/await for I/O...",
      "similarity": 0.92,
      "source": "research-2024-12-01",
      "timestamp": "2024-12-01T10:30:00Z"
    },
    {
      "content": "Async database connections with SQLAlchemy...",
      "similarity": 0.85,
      "source": "code-patterns",
      "timestamp": "2024-11-28T14:20:00Z"
    }
  ],
  "result_count": 2
}
```

## Best Practices

- **ALWAYS research from memory first** (faster, local tokens)
- Use specific, descriptive queries
- Combine memory research with web search for comprehensive results
- Memorize findings after research for future use
- Adjust min_similarity based on task (0.7 for broad, 0.9 for exact)

## Related Commands

- `/gam-memorize` - Save content to GAM memory
- `/deep-research` - Memory + web research workflow
- `/research-memorize-generate` - Complete research workflow
- `/371-research-memorize` - Web search + memorize

## Requirements

- GAM memory initialized
- Ollama server running (for embeddings)
- Java/JDK installed (for BM25 retriever, optional but recommended)
