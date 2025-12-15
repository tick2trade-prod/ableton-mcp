# Domain: GAM Memory

## Overview

Direct GAM operations (no MCP wrapper). This command provides direct access to the pure domain logic in `app/core/gam_memory.py` (`GAMMemoryManager`) without MCP infrastructure layers.

## Usage

Type `/domain-gam-memory` followed by the operation.

## Parameters

- `operation`: Operation to perform (memorize, recall, search, create_entity, add_observation) (required)
- `content`: Content for operation (varies by operation)
- `entity_name`: Entity name (for entity operations)
- `entity_type`: Entity type (for create_entity)
- `observations`: List of observations (for add_observation)
- `query`: Search query (for search)

## Example Usage

### Create Entity

```
/domain-gam-memory
Operation: create_entity
Entity Name: fastapi-authentication
Entity Type: pattern
Observations: |
  - Use dependency injection for database sessions
  - Implement JWT token validation middleware
  - Store refresh tokens in Redis
  - Hash passwords with bcrypt
```

### Add Observation

```
/domain-gam-memory
Operation: add_observation
Entity Name: fastapi-authentication
Observations: |
  - Add rate limiting to prevent brute force
  - Implement token rotation for security
```

### Recall Entity

```
/domain-gam-memory
Operation: recall
Entity Name: fastapi-authentication
```

### Search Entities

```
/domain-gam-memory
Operation: search
Query: authentication security patterns
```

## Operations

### create_entity

Create new entity in GAM knowledge graph.

**Parameters**:
- `entity_name`: Unique entity name
- `entity_type`: Type (pattern, knowledge, example, etc.)
- `observations`: Initial observations

**Returns**:
```python
{
    "entity_name": "fastapi-authentication",
    "entity_type": "pattern",
    "observations": [
        "Use dependency injection for database sessions",
        "Implement JWT token validation middleware",
        "Store refresh tokens in Redis",
        "Hash passwords with bcrypt"
    ],
    "created_at": "2025-12-04T10:30:00Z",
    "relations": []
}
```

### add_observation

Add observations to existing entity.

**Parameters**:
- `entity_name`: Target entity
- `observations`: List of new observations

**Returns**:
```python
{
    "entity_name": "fastapi-authentication",
    "observations_added": 2,
    "total_observations": 6
}
```

### recall

Retrieve entity with all observations and relations.

**Parameters**:
- `entity_name`: Entity to retrieve

**Returns**:
```python
{
    "entity_name": "fastapi-authentication",
    "entity_type": "pattern",
    "observations": [
        "Use dependency injection for database sessions",
        "Implement JWT token validation middleware",
        "Store refresh tokens in Redis",
        "Hash passwords with bcrypt",
        "Add rate limiting to prevent brute force",
        "Implement token rotation for security"
    ],
    "relations": [
        {
            "type": "implements",
            "target": "jwt-token-pattern"
        },
        {
            "type": "uses",
            "target": "redis-caching"
        }
    ],
    "created_at": "2025-12-04T10:30:00Z",
    "updated_at": "2025-12-04T11:15:00Z"
}
```

### search

Search entities by content and relations.

**Parameters**:
- `query`: Search query
- `max_results`: Maximum results (default: 10)

**Returns**:
```python
{
    "query": "authentication security patterns",
    "results": [
        {
            "entity_name": "fastapi-authentication",
            "entity_type": "pattern",
            "relevance": 0.95,
            "matched_observations": [
                "Implement JWT token validation middleware",
                "Add rate limiting to prevent brute force"
            ]
        },
        {
            "entity_name": "oauth2-flow",
            "entity_type": "pattern",
            "relevance": 0.87,
            "matched_observations": [
                "Implement OAuth2 authorization code flow"
            ]
        }
    ]
}
```

### create_relation

Create relation between entities.

**Parameters**:
- `from_entity`: Source entity
- `relation_type`: Type of relation (implements, uses, extends, etc.)
- `to_entity`: Target entity

**Returns**:
```python
{
    "from_entity": "fastapi-authentication",
    "relation_type": "implements",
    "to_entity": "jwt-token-pattern",
    "created_at": "2025-12-04T11:20:00Z"
}
```

## Domain Logic

### GAMMemoryManager

Pure domain class with no infrastructure dependencies.

```python
from app.core.gam_memory import GAMMemoryManager

# Initialize
gam = GAMMemoryManager()

# Create entity
entity = gam.create_entity(
    name="fastapi-authentication",
    entity_type="pattern",
    observations=[
        "Use dependency injection",
        "Implement JWT validation"
    ]
)

# Add observations
gam.add_observations(
    entity_name="fastapi-authentication",
    observations=["Add rate limiting"]
)

# Search
results = gam.search(query="authentication")

# Recall
entity = gam.recall(entity_name="fastapi-authentication")
```

## Best Practices

- Use descriptive entity names
- Choose appropriate entity types
- Add observations incrementally
- Create relations between related entities
- Search before creating to avoid duplicates
- Use consistent naming conventions

## Integration

- Used by `/tool-gam` (MCP wrapper)
- Pure domain logic, no infrastructure
- Reusable across interfaces
- Foundation for all memory operations

## Related Commands

- `/tool-gam` - MCP wrapper for GAM operations
- `/research-memory` - Research-focused memory
- `/memorize-content` - Simplified memorization
- `/skill-planning` - Uses GAM for context

## Source

- **File**: `app/core/gam_memory.py`
- **Class**: `GAMMemoryManager`
- **Layer**: Domain (Core)
