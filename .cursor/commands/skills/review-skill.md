# Skill: Review

## Overview

Create PR and validate changes. This command invokes the review skill from `app/server/skills/review.py` to perform comprehensive code review, create pull requests, and validate implementations.

> **Layer**: WHAT (Skill Orchestration)

## Usage

Type `/skill-review` followed by the review scope.

## Parameters

- `scope`: What to review (current_changes, branch, files) (default: "current_changes")
- `create_pr`: Create pull request (default: true)
- `pr_title`: PR title (optional, auto-generated)
- `pr_description`: PR description (optional, auto-generated)
- `run_qa`: Run QA/Critic validation (default: true)
- `min_qa_score`: Minimum QA score (default: 75)
- `check_tests`: Verify tests pass (default: true)

## Example Usage

### Review Current Changes

```
/skill-review
Scope: current_changes
Create PR: true
Run QA: true
Min QA Score: 80
```

### Review Specific Branch

```
/skill-review
Scope: branch
Branch Name: feature/auth-jwt
Create PR: true
PR Title: Add JWT authentication
```

### Review Files Only (No PR)

```
/skill-review
Scope: files
Files: app/auth/*.py
Create PR: false
Run QA: true
```

## Workflow

1. **Scope Detection**:
   - Identify changed files
   - Detect git branch
   - Gather file diffs

2. **QA Validation** (if enabled):
   - Run Critic agent on changes
   - Check for security issues
   - Validate architecture patterns
   - Verify test coverage

3. **Test Verification** (if enabled):
   - Run test suite
   - Check coverage metrics
   - Identify failing tests

4. **PR Creation** (if enabled):
   - Generate PR title/description
   - Create pull request
   - Add labels and assignees
   - Link to related issues

5. **Summary Report**:
   - List all changes
   - Show QA results
   - Display test results
   - Provide PR link

## Output Format

```json
{
  "scope": "current_changes",
  "files_reviewed": [
    "app/middleware/auth.py",
    "app/models/user.py",
    "tests/test_auth.py"
  ],
  "qa_report": {
    "score": 88,
    "critical_issues": [],
    "warnings": [
      {
        "file": "app/middleware/auth.py",
        "line": 42,
        "issue": "Consider adding rate limiting"
      }
    ],
    "suggestions": [
      "Add more edge case tests"
    ]
  },
  "test_results": {
    "passed": 15,
    "failed": 0,
    "coverage": "92%"
  },
  "pr_created": {
    "url": "https://github.com/user/repo/pull/123",
    "title": "Add JWT authentication middleware",
    "number": 123
  }
}
```

## Best Practices

- Always run QA before creating PR
- Set appropriate min_qa_score for production
- Ensure tests pass before PR creation
- Review QA warnings carefully
- Add descriptive PR titles/descriptions
- Link PRs to related issues

## Integration

- Follows `/skill-implementation` in workflow
- Uses `/agent-critic` for QA validation
- Invokes `/tool-gam` for context
- Creates GitHub PR via API

## Related Commands

- `/skill-planning` - Plan before implementation
- `/skill-implementation` - Implement before review
- `/qa-critic` - Direct QA validation
- `/validate-architecture` - Architecture validation

## Source

- **File**: `app/server/skills/review.py`
- **Function**: `create_pr_and_validate()`
- **Layer**: Skills (WHAT)
