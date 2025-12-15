# Workflow: Feature Research

**Phase**: 3 - Feature Development
**ID**: 4011

## Overview

Research feature requirements, edge cases, and best practices.

## Usage

```
/workflow-feature-research feature="Real-time notifications" use_web_search=true
```

## Parameters

- `feature`: Feature to research (required)
- `use_web_search`: Enable Tavily search (default: true)
- `memorize_results`: Store in GAM (default: true)

## Workflow Steps

1. Search GAM for similar features
2. Web search for best practices
3. Identify edge cases
4. Document requirements
5. Memorize findings

## Calls

- `/tool-gam-memory` search
- Tavily web search
- `/tool-gam-memory` memorize

## Output

```json
{
  "requirements": [...],
  "edge_cases": [...],
  "best_practices": [...],
  "memorized": true
}
```
