# Workflow: Quick Fix

**Phase**: 2 - Bug/Hotfix Workflows
**ID**: 4007

## Overview

Write minimal fix with test for simple bugs.

## Usage

```
/workflow-quick-fix issue="Typo in error message" file="app/api/users.py"
```

## Parameters

- `issue`: Bug description (required)
- `file`: File to fix (optional)
- `run_tests`: Run tests after fix (default: true)

## Workflow Steps

1. Identify fix location
2. Write minimal fix
3. Add/update test
4. Run tests
5. Create PR

## Calls

- `/agent-coder` for fix generation
- `/workflow-test-suite-full` for validation
- `/workflow-pr-create` for PR

## Output

```json
{
  "files_modified": 1,
  "tests_added": 1,
  "tests_passed": true,
  "pr_number": 123
}
```
