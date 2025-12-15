# Workflow: Human-Quality Release Notes Generation

## Overview

Generate human-readable release notes from merged PRs and issues, summarizing changes for stakeholders.

## Usage

```bash
/workflow-release-notes
```

## Parameters

- `version`: Release version (required)
- `since_version`: Previous version (optional, auto-detected)
- `format`: markdown, html, plain (default: markdown)
- `audience`: technical, non-technical, executive (default: technical)
- `include_contributors`: Include contributor list (default: true)

## Release Notes Sections

```markdown
# Release v2.0.0

## 🎉 Highlights
- Major feature additions
- Performance improvements
- Breaking changes

## ✨ New Features
- Feature 1
- Feature 2

## 🐛 Bug Fixes
- Fix 1
- Fix 2

## 🔧 Improvements
- Improvement 1
- Improvement 2

## ⚠️ Breaking Changes
- Breaking change 1

## 👥 Contributors
- @alice
- @bob
```

## Output

```json
{
  "release_notes_url": "https://github.com/org/repo/releases/v2.0.0",
  "prs_included": 45,
  "contributors": 8,
  "breaking_changes": 2
}
```
