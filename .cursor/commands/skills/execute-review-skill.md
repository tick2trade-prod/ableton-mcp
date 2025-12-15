# Execute Review Skill

## Overview

Execute the complete review workflow: Code review + PR creation + validation. Orchestrates Critic agent and Git operations for quality assurance before merge.

## Usage

Type `/execute-review-skill` followed by review scope.

## Parameters

- `target`: What to review (branch, files, commit) (required)
- `create_pr`: Create pull request (default: true)
- `run_qa`: Run Critic agent review (default: true)
- `min_score`: Minimum QA score (default: 70)
- `strict_mode`: Fail on warnings (default: false)

## Example Usage

### Review Current Branch

```
/execute-review-skill
Target: current-branch
Create PR: true
Run QA: true
Min Score: 80
```

### Review Specific Files

```
/execute-review-skill
Target: app/services/auth.py,app/api/auth.py
Run QA: true
Strict Mode: true
```

### Quick Review (No PR)

```
/execute-review-skill
Target: current-branch
Create PR: false
Run QA: true
```

## Workflow

1. **Change Detection**:
   - Detect modified files
   - Get git diff
   - Identify affected modules
   - Calculate change scope

2. **QA Review** (if enabled):
   - Call `/create-critic-agent`
   - Review each modified file
   - Check for:
     - Security vulnerabilities
     - Performance issues
     - Anti-patterns
     - Code smells
     - Missing tests
     - Hallucinated dependencies

3. **Scoring**:
   - Calculate overall QA score
   - Categorize issues (critical, warnings, suggestions)
   - Generate fix suggestions
   - Block if score < min_score

4. **Test Execution**:
   - Run affected tests
   - Run new tests
   - Calculate coverage
   - Report failures

5. **PR Creation** (if enabled):
   - Generate PR title and description
   - Include QA report
   - List modified files
   - Add test results
   - Create PR via GitHub CLI

6. **Output**:
   - Return review result
   - Include QA score and issues
   - Provide PR link (if created)

## Implementation

This command uses:
- **Review Skill**: `app.server.skills.review.execute_review()`
- **Critic Agent**: `app.server.agents.factory.create_agent("critic")`
- **Git Tools**: `app.server.tools.fallback` (Git operations)
- **GitHub CLI**: `gh pr create`

## Output Format

```json
{
  "review": {
    "files_reviewed": 5,
    "lines_changed": 342,
    "qa_score": 85,
    "critical_issues": 0,
    "warnings": 2,
    "suggestions": 5
  },
  "issues": [
    {
      "file": "app/services/auth.py",
      "line": 42,
      "severity": "warning",
      "issue": "Consider adding rate limiting",
      "suggestion": "Use Redis for rate limit tracking"
    },
    {
      "file": "app/api/auth.py",
      "line": 15,
      "severity": "warning",
      "issue": "Missing input validation",
      "suggestion": "Add Pydantic model validation"
    }
  ],
  "tests": {
    "total": 26,
    "passed": 26,
    "failed": 0,
    "coverage": "92%"
  },
  "pr": {
    "created": true,
    "url": "https://github.com/user/repo/pull/123",
    "title": "feat: Add JWT authentication system",
    "description": "Implements user authentication with JWT tokens...",
    "qa_score": 85
  },
  "passed": true
}
```

## QA Report in PR

```markdown
## QA Review Report

**Score**: 85/100 ✅

### Summary
Code quality is good with minor improvements needed.

### Critical Issues
None

### Warnings (2)
- `app/services/auth.py:42` - Consider adding rate limiting
- `app/api/auth.py:15` - Missing input validation

### Suggestions (5)
- Add password strength validation
- Implement account lockout
- Add logging for failed attempts
- Consider using Redis for session storage
- Add API documentation

### Test Results
- Total: 26
- Passed: 26 ✅
- Failed: 0
- Coverage: 92%

### Files Changed
- `app/models/user.py` (+85 lines)
- `app/services/jwt_service.py` (+120 lines)
- `app/api/auth.py` (+95 lines)
- `tests/unit/test_auth.py` (+142 lines)
```

## Best Practices

- Run before creating PR
- Use strict_mode for production
- Set appropriate min_score
- Review all critical issues
- Address warnings when possible
- Run full test suite
- Check test coverage

## Related Commands

- `/create-critic-agent` - Standalone QA agent
- `/execute-implementation-skill` - Previous step
- `/workflow-pr-create` - Alternative PR workflow
- `/qa-critic` - Standalone QA review

## Requirements

- Git repository initialized
- GitHub CLI installed (`gh`)
- GitHub authentication configured
- Ollama server running (for Critic agent)
- Pytest installed (for tests)
