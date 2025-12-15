# Workflow: Standardized PR Templates

## Overview

Enforce standardized PR templates based on PR type (feature, bugfix, hotfix, refactor, docs, chore). Ensures consistent and comprehensive information.

## Usage

```bash
/workflow-pr-templates
```

## Parameters

- `pr_type`: Template type - feature, bugfix, hotfix, refactor, docs, chore (required)
- `auto_populate`: Auto-populate template fields (default: true)
- `enforce_checklist`: Require checklist completion (default: true)

## Templates

### Feature Template
```markdown
## What
{feature_description}

## Why
{business_justification}

## How
{technical_approach}

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] Code follows conventions
- [ ] Tests added
- [ ] Documentation updated
- [ ] No breaking changes
```

## Output

```json
{
  "template_applied": "feature",
  "fields_populated": 8,
  "checklist_items": 7,
  "checklist_completed": 5
}
```
