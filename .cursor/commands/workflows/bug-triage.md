# Workflow: Bug Triage

**Phase**: 2 - Bug/Hotfix Workflows
**ID**: 4006

## Overview

Reproduce bug, identify root cause, and assess severity.

## Usage

```
/workflow-bug-triage issue="API returns 500 on user login"
```

## Parameters

- `issue`: Bug description (required)
- `reproduce_steps`: Steps to reproduce (optional)
- `priority`: low | medium | high | critical (default: "medium")

## Workflow Steps

1. Reproduce bug locally
2. Check logs and stack traces
3. Identify root cause
4. Assess severity and impact
5. Create bug report

## Calls

- Browser automation for reproduction
- Log analysis
- GAM search for similar issues

## Output

```json
{
  "root_cause": "Null pointer in auth service",
  "severity": "high",
  "affected_users": "~1000",
  "recommended_fix": "Add null check"
}
```
