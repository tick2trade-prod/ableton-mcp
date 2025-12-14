# Workflow: PR Create

## Overview

Create a GitHub Pull Request with proper formatting, context, and metadata. Used by all workflows as the final step before review.

## Usage

Type `/workflow-pr-create` after completing implementation and testing.

## Parameters

- `title`: PR title (required) - Should follow conventional commits format
- `description`: PR description (optional) - Auto-generated from commits if not provided
- `ticket_id`: Issue/ticket reference (optional) - e.g., "JIRA-123"
- `pr_type`: Type of PR (default: "feature") - Options: feature, bugfix, hotfix, refactor, docs, chore
- `reviewers`: Comma-separated list of reviewers (optional)
- `labels`: Comma-separated list of labels (optional)
- `draft`: Create as draft PR (default: false)
- `auto_merge`: Enable auto-merge after approval (default: false)

## Workflow Steps

### 1. Pre-Flight Checks
```bash
# Ensure working directory is clean
git status --porcelain

# Ensure all changes are committed
git diff --exit-code

# Ensure branch is pushed
git push origin HEAD
```

### 2. Generate PR Content

**Title Format** (Conventional Commits):
```
<type>(<scope>): <description>

Examples:
- feat(auth): add JWT authentication
- fix(api): resolve null pointer in user endpoint
- refactor(db): migrate to connection pooling
- docs(readme): update installation instructions
```

**Description Template**:
```markdown
## What
Brief description of changes

## Why
Reason for changes (link to ticket if applicable)

## How
Technical approach and key decisions

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passing
- [ ] Manual testing completed

## Screenshots (if applicable)
Before/After screenshots for UI changes

## Checklist
- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No linter errors
- [ ] No breaking changes (or documented)

## Related Issues
Closes #123
Refs #456
```

### 3. Create PR via GitHub CLI

```bash
# Create PR with gh CLI
gh pr create \
  --title "$TITLE" \
  --body "$DESCRIPTION" \
  --base main \
  --head $(git branch --show-current) \
  --reviewer "$REVIEWERS" \
  --label "$LABELS" \
  $([ "$DRAFT" = "true" ] && echo "--draft")

# Enable auto-merge if requested
if [ "$AUTO_MERGE" = "true" ]; then
  gh pr merge --auto --squash
fi
```

### 4. Post-Creation Actions

```bash
# Add PR link to ticket (if ticket_id provided)
# Update PR with CI/CD status checks
# Notify team in Slack/Discord
```

## Example Usage

### Simple Feature PR
```
/workflow-pr-create
title: "feat(auth): add JWT authentication"
description: "Implements JWT-based authentication for API endpoints"
ticket_id: "JIRA-123"
reviewers: "alice,bob"
labels: "feature,backend"
```

### Hotfix PR (Auto-merge)
```
/workflow-pr-create
title: "fix(api): resolve null pointer in user endpoint"
pr_type: "hotfix"
reviewers: "alice"
labels: "hotfix,critical"
draft: false
auto_merge: true
```

### Draft PR for Early Feedback
```
/workflow-pr-create
title: "feat(payments): integrate Stripe API"
description: "WIP: Stripe integration, need feedback on error handling"
draft: true
reviewers: "alice,bob"
labels: "feature,wip"
```

## Integration with Other Workflows

### Called By
- `/workflow-implement` - After code generation
- `/workflow-quick-fix` - After bug fix
- `/workflow-refactor-execute` - After refactoring
- `/workflow-emergency-fix` - After hotfix
- All workflows that produce code changes

### Calls
- `gh pr create` - GitHub CLI
- `git push` - Push branch
- Slack/Discord notification (optional)

## Best Practices

1. **Title**: Use conventional commits format for consistency
2. **Description**: Include context, testing, and checklist
3. **Reviewers**: Assign appropriate reviewers based on code ownership
4. **Labels**: Use labels for filtering and automation
5. **Draft**: Use draft PRs for early feedback
6. **Auto-merge**: Only for hotfixes or trivial changes

## CI/CD Integration

The PR creation triggers:
- ✅ Linting checks (Ruff, Mypy)
- ✅ Unit tests (pytest)
- ✅ Integration tests
- ✅ Security scans
- ✅ Build verification

## Related Commands

- `/workflow-code-review` - Review PR
- `/workflow-merge-deploy` - Merge and deploy PR
- `/workflow-fast-review` - Expedited review for hotfixes
- `/workflow-design-review` - Visual/UX review

## Output

Returns:
```json
{
  "pr_url": "https://github.com/org/repo/pull/123",
  "pr_number": 123,
  "status": "open",
  "checks_url": "https://github.com/org/repo/pull/123/checks",
  "reviewers": ["alice", "bob"],
  "labels": ["feature", "backend"]
}
```

## Error Handling

- **Uncommitted changes**: Prompt to commit or stash
- **Unpushed commits**: Auto-push branch
- **No GitHub CLI**: Install gh CLI
- **Invalid reviewers**: Warn and proceed without reviewers
- **Rate limit**: Retry with exponential backoff
