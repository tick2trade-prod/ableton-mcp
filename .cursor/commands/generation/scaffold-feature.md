# Feature: Scaffold

**Rank**: 3 - Feature-Based Commands

## Overview

Scaffold complete feature with models, services, API, tests, and documentation.

## Usage

```
/feature-scaffold feature="Blog post CRUD API" language=python include_tests=true
```

## Parameters

- `feature`: Feature description (required)
- `language`: python | typescript (default: "python")
- `include_tests`: Generate tests (default: true)
- `include_docs`: Generate docs (default: true)

## Workflow

1. Research feature requirements
2. Generate plan with file structure
3. Batch implement all files
4. Run tests
5. Generate documentation

## Implementation

```python
# 1. Research
await research_and_plan(topic=feature)

# 2. Plan
plan = await execute_planning(feature_name=feature)

# 3. Implement
await batch_execution.execute_parallel_tasks(plan.todos)

# 4. Test
await run_tests()

# 5. Document
await generate_docs()
```

## Output

```json
{
  "files_created": 12,
  "tests_passed": true,
  "docs_generated": true
}
```
