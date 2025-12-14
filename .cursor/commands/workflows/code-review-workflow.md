# Workflow: Code Review

## Overview

Comprehensive code review process with automated checks, human review, and feedback loops. Ensures code quality, security, and maintainability.

## Usage

Type `/workflow-code-review` after PR is created to initiate review process.

## Parameters

- `pr_number`: PR number to review (required)
- `review_type`: Type of review (default: "standard") - Options: standard, fast-track, security, architecture
- `auto_assign_reviewers`: Auto-assign based on code ownership (default: true)
- `require_approvals`: Number of approvals required (default: 2)
- `run_automated_checks`: Run automated review tools (default: true)
- `block_on_comments`: Block merge if unresolved comments (default: true)

## Workflow Steps

### 1. Automated Pre-Review Checks

```bash
# Linting
uv run ruff check . --fix
uv run ruff format .

# Type checking
uv run mypy app/ --ignore-missing-imports

# Security scanning
uv run bandit -r app/ -ll

# Test coverage
uv run pytest --cov=app --cov-report=term --cov-report=html

# Dependency vulnerabilities
uv run safety check

# Code complexity
uv run radon cc app/ -a -nb
```

### 2. AI-Assisted Review

```bash
# Use QA/Critic agent for automated review
/qa-critic pr_number=$PR_NUMBER

# Check for:
# - Code smells
# - Security vulnerabilities
# - Performance issues
# - Best practice violations
# - Missing tests
# - Incomplete documentation
```

### 3. Assign Reviewers

```bash
# Auto-assign based on CODEOWNERS
gh pr edit $PR_NUMBER --add-reviewer $(gh api repos/:owner/:repo/codeowners)

# Or manual assignment
gh pr edit $PR_NUMBER --add-reviewer alice,bob

# Request specific expertise
# - Security review: @security-team
# - Architecture review: @architects
# - Performance review: @performance-team
```

### 4. Review Checklist

**Code Quality**:
- [ ] Code follows project style guide
- [ ] No code smells or anti-patterns
- [ ] Appropriate abstractions and DRY
- [ ] Clear variable/function names
- [ ] Adequate comments for complex logic

**Testing**:
- [ ] Unit tests added/updated
- [ ] Integration tests if needed
- [ ] Edge cases covered
- [ ] Test coverage >= 80%
- [ ] Tests are readable and maintainable

**Security**:
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Authentication/authorization checked

**Performance**:
- [ ] No N+1 queries
- [ ] Appropriate indexing
- [ ] Efficient algorithms
- [ ] No memory leaks
- [ ] Caching where appropriate

**Documentation**:
- [ ] README updated if needed
- [ ] API docs updated
- [ ] Inline comments for complex logic
- [ ] Migration guide if breaking changes

**Architecture**:
- [ ] Follows DDD principles
- [ ] Proper layer separation
- [ ] No circular dependencies
- [ ] Scalable design

### 5. Review Types

#### Standard Review (2 approvals)
```
- Code owner review
- Peer review
- Automated checks
- Estimated time: 1-2 days
```

#### Fast-Track Review (1 approval)
```
- For: Bug fixes, typos, minor changes
- Single reviewer
- Automated checks only
- Estimated time: 1-4 hours
```

#### Security Review (Security team + 1)
```
- For: Authentication, authorization, data handling
- Security team mandatory
- Additional peer review
- Security scanning required
- Estimated time: 2-3 days
```

#### Architecture Review (Architect + 2)
```
- For: Major refactors, new services, schema changes
- Architect mandatory
- Two peer reviews
- Design doc required
- Estimated time: 3-5 days
```

### 6. Feedback Loop

```bash
# Author addresses feedback
git commit -m "fix: address review comments"
git push

# Request re-review
gh pr review $PR_NUMBER --comment -b "Addressed all feedback, PTAL"

# Reviewers re-review
gh pr review $PR_NUMBER --approve

# Resolve conversations
gh pr review $PR_NUMBER --comment -b "LGTM" --resolve
```

### 7. Approval & Merge

```bash
# Check approval status
gh pr view $PR_NUMBER --json reviewDecision

# If approved, merge
if [ "$REVIEW_DECISION" = "APPROVED" ]; then
  /workflow-merge-deploy pr_number=$PR_NUMBER
fi
```

## Example Usage

### Standard Feature Review
```
/workflow-code-review
pr_number: 123
review_type: standard
require_approvals: 2
auto_assign_reviewers: true
```

### Fast-Track Bug Fix
```
/workflow-code-review
pr_number: 456
review_type: fast-track
require_approvals: 1
run_automated_checks: true
```

### Security-Critical Change
```
/workflow-code-review
pr_number: 789
review_type: security
require_approvals: 2
block_on_comments: true
```

### Architecture Refactor
```
/workflow-code-review
pr_number: 321
review_type: architecture
require_approvals: 3
run_automated_checks: true
```

## Integration with Other Workflows

### Called By
- `/workflow-pr-create` - After PR creation
- `/workflow-implement` - After implementation
- `/workflow-refactor-execute` - After refactoring

### Calls
- `/qa-critic` - AI-assisted review
- `gh pr review` - GitHub review API
- `uv run pytest` - Run tests
- `uv run ruff` - Linting
- `/workflow-merge-deploy` - After approval

## Review Guidelines

### For Reviewers

**DO**:
- ✅ Be constructive and respectful
- ✅ Explain the "why" behind feedback
- ✅ Suggest concrete improvements
- ✅ Approve if no blocking issues
- ✅ Respond within 24 hours

**DON'T**:
- ❌ Nitpick on style (let linters handle it)
- ❌ Request changes without explanation
- ❌ Block on personal preferences
- ❌ Leave reviews incomplete
- ❌ Ignore automated check failures

### For Authors

**DO**:
- ✅ Keep PRs small and focused
- ✅ Respond to feedback promptly
- ✅ Ask questions if unclear
- ✅ Update tests with code changes
- ✅ Resolve conversations after addressing

**DON'T**:
- ❌ Submit PRs with failing tests
- ❌ Ignore review feedback
- ❌ Force-push after review starts
- ❌ Merge without required approvals
- ❌ Submit PRs with linter errors

## Automated Review Tools

### Linting & Formatting
```bash
# Ruff (Python)
uv run ruff check . --fix
uv run ruff format .

# ESLint (JavaScript/TypeScript)
npm run lint
npm run format
```

### Security Scanning
```bash
# Bandit (Python)
uv run bandit -r app/ -ll

# npm audit (Node.js)
npm audit

# Trivy (Container images)
trivy image myapp:latest
```

### Code Quality
```bash
# Complexity analysis
uv run radon cc app/ -a -nb

# Maintainability index
uv run radon mi app/ -nb

# Code duplication
uv run pylint app/ --disable=all --enable=duplicate-code
```

### Test Coverage
```bash
# Python
uv run pytest --cov=app --cov-report=html

# JavaScript
npm run test:coverage
```

## Best Practices

1. **PR Size**: Keep PRs under 400 lines of code
2. **Review Time**: Respond within 24 hours
3. **Approval Threshold**: 2 approvals for features, 1 for fixes
4. **Automated Checks**: Must pass before human review
5. **Unresolved Comments**: Block merge until resolved
6. **Re-review**: Required after significant changes

## Related Commands

- `/workflow-pr-create` - Create PR
- `/workflow-merge-deploy` - Merge after approval
- `/qa-critic` - AI-assisted review
- `/workflow-fast-review` - Expedited review
- `/workflow-design-review` - Visual/UX review

## Output

Returns:
```json
{
  "pr_number": 123,
  "review_status": "approved",
  "approvals": 2,
  "required_approvals": 2,
  "reviewers": ["alice", "bob"],
  "automated_checks": "passed",
  "unresolved_comments": 0,
  "ready_to_merge": true,
  "review_duration_hours": 18
}
```

## Error Handling

- **Failed automated checks**: Block review until fixed
- **No reviewers assigned**: Auto-assign from CODEOWNERS
- **Stale reviews**: Request re-review after force-push
- **Unresolved comments**: Block merge
- **Insufficient approvals**: Request additional reviewers
