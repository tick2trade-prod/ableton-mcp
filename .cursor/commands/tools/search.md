# Tool: Search

## Overview

Search codebase or GAM memory. This command provides unified search across codebase files and GAM memory from `app/server/tools/search.py` for finding relevant code, documentation, and knowledge.

## Usage

Type `/tool-search` followed by the search query and scope.

## Parameters

- `query`: Search query (required)
- `scope`: Search scope (codebase, gam, both) (default: "both")
- `file_pattern`: File pattern filter (optional, e.g., "*.py")
- `max_results`: Maximum results (default: 20)
- `include_content`: Include file content in results (default: false)
- `case_sensitive`: Case-sensitive search (default: false)

## Example Usage

### Search Codebase

```
/tool-search
Query: authentication middleware
Scope: codebase
File Pattern: *.py
Max Results: 10
```

### Search GAM Memory

```
/tool-search
Query: FastAPI best practices
Scope: gam
Max Results: 5
```

### Search Both

```
/tool-search
Query: JWT token validation
Scope: both
Include Content: true
```

### Search Specific Files

```
/tool-search
Query: async def
Scope: codebase
File Pattern: app/api/*.py
```

## Search Scopes

### Codebase Search

Search through project files using ripgrep.

**Features**:
- Fast full-text search
- Regex support
- File pattern filtering
- Context lines
- Ignore patterns (.gitignore)

**Returns**:
```json
{
  "scope": "codebase",
  "query": "authentication middleware",
  "results": [
    {
      "file": "app/middleware/auth.py",
      "line": 15,
      "column": 10,
      "match": "async def authentication_middleware(request: Request):",
      "context_before": [
        "from fastapi import Request, HTTPException",
        ""
      ],
      "context_after": [
        "    token = request.headers.get('Authorization')",
        "    if not token:"
      ]
    },
    {
      "file": "app/main.py",
      "line": 42,
      "match": "app.middleware('http')(authentication_middleware)",
      "context_before": ["# Add middleware"],
      "context_after": [""]
    }
  ],
  "total_results": 2,
  "search_time_ms": 45
}
```

### GAM Memory Search

Search through stored knowledge and entities.

**Features**:
- Semantic search
- Tag filtering
- Entity type filtering
- Relevance scoring

**Returns**:
```json
{
  "scope": "gam",
  "query": "FastAPI best practices",
  "results": [
    {
      "entity_name": "fastapi-best-practices",
      "entity_type": "knowledge",
      "relevance": 0.95,
      "content": "FastAPI best practices: Use dependency injection...",
      "tags": ["fastapi", "best-practices", "python"],
      "created_at": "2025-12-04T10:30:00Z"
    },
    {
      "entity_name": "fastapi-middleware-patterns",
      "entity_type": "pattern",
      "relevance": 0.87,
      "content": "Middleware patterns in FastAPI...",
      "tags": ["fastapi", "middleware", "patterns"],
      "created_at": "2025-12-03T15:20:00Z"
    }
  ],
  "total_results": 2,
  "search_time_ms": 120
}
```

### Combined Search

Search both codebase and GAM memory.

**Returns**:
```json
{
  "scope": "both",
  "query": "JWT token validation",
  "codebase_results": [
    {
      "file": "app/auth/jwt.py",
      "line": 28,
      "match": "def validate_jwt_token(token: str) -> dict:"
    }
  ],
  "gam_results": [
    {
      "entity_name": "jwt-validation-patterns",
      "relevance": 0.92,
      "content": "JWT validation best practices..."
    }
  ],
  "total_results": 2,
  "search_time_ms": 165
}
```

## Advanced Search

### Regex Search

```
/tool-search
Query: "async def \w+_middleware"
Scope: codebase
File Pattern: *.py
```

### Tag-Based GAM Search

```
/tool-search
Query: tags:authentication AND tags:security
Scope: gam
```

### Multi-File Pattern

```
/tool-search
Query: import fastapi
Scope: codebase
File Pattern: {app,tests}/**/*.py
```

## Best Practices

- Use specific queries for better results
- Filter by file patterns to narrow scope
- Search GAM for patterns and best practices
- Search codebase for implementation examples
- Use regex for complex patterns
- Include context for better understanding

## Integration

- Used by all skill and agent commands
- Provides context for code generation
- Enables knowledge discovery
- Supports research workflows

## Related Commands

- `/smart-context` - Context-aware search
- `/research-memory` - Research-focused search
- `/tool-gam` - Direct GAM operations
- `/deep-research` - Deep research workflow

## Source

- **File**: `app/server/tools/search.py`
- **Functions**: `search_codebase()`, `search_gam()`, `unified_search()`
- **Layer**: Tools (HOW)
