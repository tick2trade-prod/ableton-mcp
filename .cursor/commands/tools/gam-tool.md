# Tool: GAM Memory

## Overview

GAM memory operations (memorize, recall, search). This command provides direct access to GAM (General Agentic Memory) operations from `app/server/tools/gam_tool.py` for storing, retrieving, and searching knowledge.

## Usage

Type `/tool-gam` followed by the operation and parameters.

## Parameters

- `operation`: Operation to perform (memorize, recall, search, list) (required)
- `content`: Content to memorize (for memorize operation)
- `query`: Search query (for search operation)
- `entity_name`: Entity name (for recall operation)
- `tags`: Tags for categorization (optional)
- `max_results`: Maximum search results (default: 10)

## Example Usage

### Memorize Information

```
/tool-gam
Operation: memorize
Content: |
  FastAPI best practices:
  - Use dependency injection for database sessions
  - Implement proper exception handling
  - Add request validation with Pydantic
  - Use async endpoints for I/O operations
Tags: fastapi, best-practices, python
```

### Search Memory

```
/tool-gam
Operation: search
Query: authentication patterns
Max Results: 5
```

### Recall Entity

```
/tool-gam
Operation: recall
Entity Name: fastapi-best-practices
```

### List All Entities

```
/tool-gam
Operation: list
Tags: python, fastapi
```

## Operations

### Memorize

Store new information in GAM memory.

**Parameters**:
- `content`: Text content to store
- `tags`: Optional tags for categorization
- `entity_type`: Type of entity (default: "knowledge")

**Returns**:
```json
{
  "operation": "memorize",
  "entity_id": "entity-abc123",
  "entity_name": "fastapi-best-practices",
  "tags": ["fastapi", "best-practices", "python"],
  "success": true
}
```

### Recall

Retrieve specific entity from memory.

**Parameters**:
- `entity_name`: Name of entity to retrieve

**Returns**:
```json
{
  "operation": "recall",
  "entity_name": "fastapi-best-practices",
  "content": "FastAPI best practices: ...",
  "tags": ["fastapi", "best-practices"],
  "created_at": "2025-12-04T10:30:00Z",
  "observations": [
    "Use dependency injection",
    "Implement exception handling"
  ]
}
```

### Search

Search memory for relevant information.

**Parameters**:
- `query`: Search query
- `max_results`: Maximum results to return

**Returns**:
```json
{
  "operation": "search",
  "query": "authentication patterns",
  "results": [
    {
      "entity_name": "jwt-authentication",
      "relevance": 0.95,
      "content": "JWT authentication pattern...",
      "tags": ["auth", "jwt", "security"]
    },
    {
      "entity_name": "oauth2-flow",
      "relevance": 0.87,
      "content": "OAuth2 authorization flow...",
      "tags": ["auth", "oauth2", "security"]
    }
  ],
  "total_results": 2
}
```

### List

List entities by tags or type.

**Parameters**:
- `tags`: Filter by tags (optional)
- `entity_type`: Filter by type (optional)

**Returns**:
```json
{
  "operation": "list",
  "filters": {"tags": ["python", "fastapi"]},
  "entities": [
    {
      "entity_name": "fastapi-best-practices",
      "tags": ["fastapi", "best-practices", "python"],
      "created_at": "2025-12-04T10:30:00Z"
    },
    {
      "entity_name": "fastapi-middleware",
      "tags": ["fastapi", "middleware", "python"],
      "created_at": "2025-12-03T15:20:00Z"
    }
  ],
  "total_count": 2
}
```

## Best Practices

- Use descriptive entity names
- Add relevant tags for discoverability
- Store structured information
- Search before memorizing to avoid duplicates
- Update existing entities instead of creating new ones
- Use tags consistently across entities

## Integration

- Used by all skill and agent commands
- Provides persistent memory across sessions
- Enables context-aware operations
- Supports knowledge graph relationships

## Related Commands

- `/research-memory` - Research-focused memory operations
- `/memorize-content` - Simplified memorization
- `/skill-planning` - Uses GAM for context
- `/agent-planner` - Queries GAM for patterns

## Source

- **File**: `app/server/tools/gam_tool.py`
- **Domain**: `app/core/gam_memory.py` → `GAMMemoryManager`
- **Layer**: Tools (HOW)
