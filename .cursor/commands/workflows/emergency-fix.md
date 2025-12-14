# Workflow: Emergency Fix

**Phase**: 2 - Bug/Hotfix Workflows
**ID**: 4009

## Overview

Minimal fix for critical production issues, no refactoring.

## Usage

```
/workflow-emergency-fix issue="Production down" severity="critical"
```

## Parameters

- `issue`: Critical issue (required)
- `severity`: critical | high (default: "critical")
- `skip_tests`: Skip non-critical tests (default: false)

## Workflow Steps

1. Identify minimal fix
2. Apply fix (no refactoring)
3. Run smoke tests only
4. Prepare rollback
5. Deploy immediately

## Calls

- `/agent-coder` with minimal mode
- `/workflow-smoke-test` for validation
- `/workflow-emergency-deploy` for deployment

## Output

```json
{
  "fix_applied": true,
  "smoke_tests": "passed",
  "deployed": true,
  "rollback_ready": true
}
```
