# Workflow: API Design

**Phase**: 3 - Feature Development
**ID**: 4013

## Overview

Design API contract using OpenAPI specification.

## Usage

```
/workflow-api-design feature="User management API" version="v1"
```

## Parameters

- `feature`: API feature (required)
- `version`: API version (default: "v1")
- `format`: openapi | swagger (default: "openapi")

## Workflow Steps

1. Define endpoints
2. Specify request/response schemas
3. Document authentication
4. Add examples
5. Generate OpenAPI spec

## Output

```json
{
  "openapi_spec": "docs/api/users-v1.yaml",
  "endpoints": 8,
  "status": "ready_for_review"
}
```
