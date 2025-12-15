# Workflow: Hotfix Branch

**Phase**: 2 - Bug/Hotfix Workflows
**ID**: 4008

## Overview

Create hotfix branch from main/prod for critical fixes.

## Usage

```
/workflow-hotfix-branch issue="PROD-123" description="Fix payment gateway"
```

## Parameters

- `issue`: Issue ID (required)
- `description`: Hotfix description (required)
- `base_branch`: Base branch (default: "main")

## Workflow Steps

1. Create hotfix branch from base
2. Set up environment
3. Document hotfix scope
4. Prepare rollback plan

## Implementation

```bash
git checkout $base_branch
git pull origin $base_branch
git checkout -b hotfix/$issue-$description
```

## Output

```json
{
  "branch": "hotfix/PROD-123-fix-payment",
  "base": "main",
  "status": "ready"
}
```
