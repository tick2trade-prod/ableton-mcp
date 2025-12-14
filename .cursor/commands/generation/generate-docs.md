# Feature: Document

**Rank**: 3 - Feature-Based Commands

## Overview

Generate documentation for feature, API, or codebase.

## Usage

```
/feature-document target="app/api/" doc_type="api" format="openapi"
```

## Parameters

- `target`: Code to document (required)
- `doc_type`: api | code | architecture (default: "code")
- `format`: markdown | openapi | html (default: "markdown")

## Workflow

1. Analyze code structure
2. Extract docstrings/comments
3. Generate documentation
4. Validate examples
5. Publish docs

## Output

```json
{
  "docs_generated": "docs/api.md",
  "examples_validated": true
}
```
