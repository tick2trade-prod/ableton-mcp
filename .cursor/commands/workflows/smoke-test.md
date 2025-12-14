# Workflow: Smoke Test

**Phase**: 4 - Testing & Quality
**ID**: 4018

## Overview

Quick validation of critical paths after deployment.

## Usage

```
/workflow-smoke-test environment="production" critical_paths="auth,checkout"
```

## Parameters

- `environment`: Environment to test (required)
- `critical_paths`: Critical paths to test (default: "all")
- `timeout`: Test timeout in seconds (default: 60)

## Workflow Steps

1. Test health endpoints
2. Test critical user flows
3. Verify database connectivity
4. Check external services
5. Report status

## Output

```json
{
  "health_check": "passed",
  "critical_paths": "passed",
  "duration": "15s"
}
```
