# Workflow: Automated PR Creation with Intelligent Reviewer Assignment

## Overview

Automatically create GitHub Pull Requests with intelligent reviewer assignment based on code ownership, expertise, and availability. Monitors code changes and creates PRs with optimal metadata.

## Usage

```bash
/workflow-auto-pr-create
```

## Parameters

- `feature_name`: Feature or task name (required)
- `title`: PR title (optional, auto-generated if not provided)
- `description`: PR description (optional, auto-generated from commits)
- `auto_assign_reviewers`: Automatically assign reviewers (default: true)
- `max_reviewers`: Maximum number of reviewers to assign (default: 3)
- `priority`: PR priority - low, medium, high, critical (default: medium)
- `labels`: Comma-separated labels (optional, auto-detected if not provided)
- `draft`: Create as draft PR (default: false)
- `auto_merge`: Enable auto-merge after approval (default: false)
- `ticket_id`: Issue/ticket reference (optional)
- `stream_output`: Stream results in real-time (default: true)

## Workflow Steps

### 1. Pre-Flight Analysis

```python
from app.server.skills.planning import execute_planning
from app.core.gam_memory import GAMMemoryManager

# Research similar PRs from GAM memory
gam = GAMMemoryManager()
similar_prs = gam.research(f"PRs for {feature_name}", max_iters=5)

# Analyze current changes
changes = analyze_git_changes()
```

### 2. Intelligent Reviewer Assignment

```python
from app.server.tools.search import search_codebase

# Find code owners based on CODEOWNERS file and git history
code_owners = find_code_owners(changes.files_modified)

# Query GAM for expert reviewers
expert_reviewers = gam.research(
    f"expert reviewers for {changes.technology_stack}",
    max_iters=3
)

# Check reviewer availability (GitHub API)
available_reviewers = check_reviewer_availability(
    code_owners + expert_reviewers
)

# Rank reviewers by:
# - Code ownership (40%)
# - Domain expertise (30%)
# - Review velocity (20%)
# - Current workload (10%)
reviewers = rank_and_select_reviewers(
    available_reviewers,
    max_count=max_reviewers
)
```

### 3. Auto-Generate PR Content

```python
from app.server.agents.factory import create_workflow_agent

# Create PR agent
agent = await create_workflow_agent(step="review")

# Generate title (conventional commits format)
title = generate_pr_title(
    changes=changes,
    feature_name=feature_name,
    similar_prs=similar_prs
)

# Generate description
description = await agent.generate_pr_description(
    changes=changes,
    context=similar_prs,
    template=get_pr_template(changes.pr_type)
)
```

### 4. Auto-Detect Labels

```python
# Detect labels based on:
# - File paths (backend, frontend, docs)
# - Code changes (feature, bugfix, refactor)
# - Dependencies (breaking-change, security)
# - Tests (needs-tests, test-only)

labels = detect_labels(
    changes=changes,
    description=description,
    similar_prs=similar_prs
)
```

### 5. Create PR via GitHub CLI

```python
from app.server.tools.fallback import execute_git_command

# Ensure branch is pushed
await execute_git_command("push origin HEAD")

# Create PR
pr_result = await create_github_pr(
    title=title,
    body=description,
    reviewers=reviewers,
    labels=labels,
    draft=draft,
    auto_merge=auto_merge
)

# Memorize successful PR creation
gam.memorize(f"""
PR Created: {pr_result.url}
Feature: {feature_name}
Reviewers: {', '.join(reviewers)}
Labels: {', '.join(labels)}
Success: True
""")
```

### 6. Post-Creation Actions

```python
# Link PR to ticket
if ticket_id:
    link_pr_to_ticket(pr_result.number, ticket_id)

# Notify reviewers (Slack/Discord)
notify_reviewers(
    reviewers=reviewers,
    pr_url=pr_result.url,
    priority=priority
)

# Add PR to project board
add_to_project_board(pr_result.number, status="In Review")
```

## Example Usage

### Simple Feature PR
```bash
/workflow-auto-pr-create
  feature_name="JWT authentication"
  priority="high"
```

### Hotfix with Auto-Merge
```bash
/workflow-auto-pr-create
  feature_name="Fix null pointer in user endpoint"
  priority="critical"
  auto_merge=true
  max_reviewers=1
```

### Draft PR for Early Feedback
```bash
/workflow-auto-pr-create
  feature_name="Stripe payment integration"
  draft=true
  labels="wip,needs-feedback"
```

## Integration with App Architecture

### Skills Used
```python
from app.server.skills.planning import execute_planning
from app.server.skills.review import create_pr
```

### Tools Used
```python
from app.server.tools.gam_tool import research_memory
from app.server.tools.search import search_codebase
from app.server.tools.fallback import execute_git_command
```

### Agents Used
```python
from app.server.agents.factory import create_workflow_agent
# Uses "review" agent with PR creation prompts
```

## Autonomous Agent Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. RESEARCH PHASE (Autonomous)                              │
│    - Agent queries GAM for similar PRs                      │
│    - Agent analyzes git changes                             │
│    - Agent searches codebase for context                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. PLANNING PHASE (Autonomous)                              │
│    - Agent finds code owners                                │
│    - Agent ranks reviewers by expertise                     │
│    - Agent detects optimal labels                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. GENERATION PHASE (Streaming)                             │
│    - Agent generates PR title (conventional commits)        │
│    - Agent generates PR description (streaming)             │
│    - Agent validates against template                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. EXECUTION PHASE (Autonomous)                             │
│    - Agent pushes branch                                    │
│    - Agent creates PR via GitHub CLI                        │
│    - Agent assigns reviewers                                │
│    - Agent adds labels                                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. MEMORIZATION PHASE (Learning)                            │
│    - Agent memorizes successful PR creation                 │
│    - Agent learns reviewer preferences                      │
│    - Agent updates expertise graph                          │
└─────────────────────────────────────────────────────────────┘
```

## Reviewer Ranking Algorithm

```python
def rank_reviewers(candidates, changes):
    scores = {}

    for reviewer in candidates:
        score = 0

        # Code ownership (40%)
        ownership_score = calculate_ownership(
            reviewer, changes.files_modified
        )
        score += ownership_score * 0.4

        # Domain expertise (30%)
        expertise_score = calculate_expertise(
            reviewer, changes.technology_stack
        )
        score += expertise_score * 0.3

        # Review velocity (20%)
        velocity_score = calculate_review_velocity(reviewer)
        score += velocity_score * 0.2

        # Current workload (10% - inverse)
        workload_score = 1.0 - calculate_workload(reviewer)
        score += workload_score * 0.1

        scores[reviewer] = score

    # Sort by score and return top N
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

## PR Title Generation

```python
def generate_pr_title(changes, feature_name, similar_prs):
    # Detect type
    pr_type = detect_pr_type(changes)  # feat, fix, refactor, docs, etc.

    # Detect scope
    scope = detect_scope(changes.files_modified)  # auth, api, ui, etc.

    # Generate description
    description = summarize_changes(
        feature_name=feature_name,
        changes=changes,
        similar_prs=similar_prs,
        max_length=50
    )

    # Format: type(scope): description
    return f"{pr_type}({scope}): {description}"
```

## PR Description Template

```markdown
## What
{brief_summary_of_changes}

## Why
{reason_for_changes}
{link_to_ticket_if_applicable}

## How
{technical_approach}
{key_decisions}

## Changes
- {file_1}: {description}
- {file_2}: {description}
...

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passing
- [ ] Manual testing completed

## Screenshots (if applicable)
{before_after_screenshots_for_ui_changes}

## Checklist
- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No linter errors
- [ ] No breaking changes (or documented)

## Related Issues
Closes #{ticket_id}
```

## Output

Returns:
```json
{
  "pr_url": "https://github.com/org/repo/pull/123",
  "pr_number": 123,
  "title": "feat(auth): add JWT authentication",
  "reviewers": ["alice", "bob", "charlie"],
  "labels": ["feature", "backend", "security"],
  "status": "open",
  "checks_url": "https://github.com/org/repo/pull/123/checks",
  "estimated_review_time_hours": 2.5,
  "auto_merge_enabled": false
}
```

## Error Handling

- **Uncommitted changes**: Auto-commit with generated message
- **Unpushed commits**: Auto-push branch
- **No reviewers available**: Assign team lead as fallback
- **Invalid title/description**: Regenerate with stricter constraints
- **GitHub API rate limit**: Retry with exponential backoff
- **Merge conflicts**: Notify and suggest resolution

## Performance

- **Avg execution time**: 30 seconds
- **GAM queries**: 2-3
- **GitHub API calls**: 3-5
- **Streaming**: Real-time PR description generation

## Related Workflows

- `/workflow-ai-code-review` - Review the created PR
- `/workflow-pr-summary` - Generate PR summary
- `/workflow-merge-deploy` - Merge and deploy PR
- `/workflow-fast-review` - Expedited review for hotfixes

## Best Practices

1. **Let the agent research**: Don't manually specify reviewers unless necessary
2. **Use conventional commits**: Helps with auto-title generation
3. **Enable streaming**: Watch PR description being generated
4. **Trust the ranking**: Agent learns optimal reviewer assignments over time
5. **Memorize outcomes**: Successful PRs improve future assignments

## Learning & Improvement

The workflow learns from:
- ✅ Reviewer approval times
- ✅ Code review quality
- ✅ Merge success rates
- ✅ Post-merge issues
- ✅ Team feedback

This data improves:
- 🎯 Reviewer selection accuracy
- 🎯 Label detection precision
- 🎯 Priority assignment
- 🎯 Description quality
