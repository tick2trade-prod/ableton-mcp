# Workflow: Complete PR Workflow Automation

## Overview

Automate entire PR workflow including tagging, labeling, branch protection, CI/CD triggers, and team notifications.

## Usage

```bash
/workflow-pr-automation
```

## Parameters

- `pr_number`: PR to automate (required)
- `auto_tag`: Auto-tag relevant team members (default: true)
- `auto_label`: Auto-apply labels (default: true)
- `enforce_branch_protection`: Enforce protection rules (default: true)
- `notify_channels`: Slack/Discord channels (optional)

## Automation Steps

```python
# 1. Auto-Tagging
- Tag code owners
- Tag reviewers
- Tag stakeholders

# 2. Auto-Labeling
- Detect PR type
- Detect affected areas
- Detect priority

# 3. Branch Protection
- Require reviews
- Require CI/CD pass
- Require up-to-date branch

# 4. Notifications
- Slack/Discord notifications
- Email notifications
- GitHub notifications
```

## Output

```json
{
  "tags_applied": ["@alice", "@bob"],
  "labels_applied": ["feature", "backend"],
  "branch_protection_enforced": true,
  "notifications_sent": 3
}
```
