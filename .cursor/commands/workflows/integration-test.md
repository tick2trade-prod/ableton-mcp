# Workflow: Integration Test

**Phase**: 4 - Testing & Quality
**ID**: 4016

## Overview

Run integration tests for component interactions.

## Usage

```
/workflow-integration-test target="app/api/" services="redis,postgres"
```

## Parameters

- `target`: Test target (required)
- `services`: Required services (default: "all")
- `parallel`: Run in parallel (default: true)

## Workflow Steps

1. Start required services
2. Run integration tests
3. Collect results
4. Stop services
5. Generate report

## Implementation

```bash
docker-compose up -d $services
uv run pytest tests/integration/ -v
docker-compose down
```

## Output

```json
{
  "tests_run": 45,
  "passed": 43,
  "failed": 2,
  "duration": "2.5m"
}
```
