# Workflow: Automated Documentation Updates

## Overview

Automatically update documentation (README, API docs, changelogs) in sync with code changes, ensuring up-to-date information.

## Usage

```bash
/workflow-docs-sync
```

## Parameters

- `pr_number`: PR with code changes (required)
- `doc_types`: readme, api, changelog, all (default: all)
- `auto_commit`: Auto-commit doc updates (default: true)
- `generate_examples`: Generate code examples (default: true)

## Documentation Types

```python
# README Updates
- Installation instructions
- Usage examples
- Feature list
- Configuration

# API Documentation
- Endpoint descriptions
- Request/response schemas
- Authentication
- Error codes

# Changelog
- Version history
- Breaking changes
- New features
- Bug fixes
```

## Output

```json
{
  "docs_updated": ["README.md", "API.md", "CHANGELOG.md"],
  "examples_generated": 5,
  "auto_committed": true
}
```
