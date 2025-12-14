# Research from Memory

## Overview

Research from GAM memory using semantic search to retrieve relevant information before starting new tasks.

## Usage

Type `/research-memory` followed by your research query.

## Parameters

- `query`: Research query (required)

## Example Usage

### Research Best Practices

```
/research-memory
Query: FastAPI async patterns best practices
```

### Research Code Patterns

```
/research-memory
Query: Python type hints patterns for FastMCP
```

### Research Package Usage

```
/research-memory
Query: How to use lancedb for vector search optimization
```

## Workflow

1. Query is processed using GAM ResearchAgent (via `app.core.GAMMemoryManager`)
2. Semantic search retrieves relevant memories
3. Results are ranked by relevance
4. Retrieved information can be used for tasks

## Implementation

This command uses the `app.core.GAMMemoryManager` class from the refactored `app/` structure:
- Core GAM integration: `app.core.GAMMemoryManager.research()`
- Memory state: `app.core.GAMMemoryManager.get_memory_state()`

## Best Practices

- ALWAYS research from memory first (faster, local tokens)
- Use specific, descriptive queries
- Combine memory research with web search for comprehensive results
- Memorize findings after research for future use
