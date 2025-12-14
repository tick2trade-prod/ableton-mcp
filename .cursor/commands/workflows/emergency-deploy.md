# Workflow: Emergency Deploy

**Phase**: 2 - Bug/Hotfix Workflows
**ID**: 4010

## Overview

Deploy hotfix to production with rollback plan.

## Usage

```
/workflow-emergency-deploy pr_number=456 notify_team=true
```

## Parameters

- `pr_number`: PR to deploy (required)
- `notify_team`: Send alerts (default: true)
- `auto_rollback`: Enable auto-rollback (default: true)

## Workflow Steps

1. Verify PR approved
2. Run smoke tests
3. Deploy with monitoring
4. Verify deployment
5. Notify team

## Calls

- `/workflow-smoke-test` for validation
- `/workflow-merge-deploy` with emergency mode
- Slack/PagerDuty notifications

## Output

```json
{
  "deployed": true,
  "environment": "production",
  "rollback_available": true,
  "team_notified": true
}
```
