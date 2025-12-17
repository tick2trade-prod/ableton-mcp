# Review Changes + Source Control (Editor)

> Source: [https://antigravity.google/docs/review-changes-editor](https://antigravity.google/docs/review-changes-editor)

## Overview

Integrated Git support for reviewing and committing changes in the editor.

## Features

### Inline Diff
- See changes in editor gutter
- Green for additions
- Red for deletions

### Source Control Panel
- View all changed files
- Stage/unstage changes
- Commit with message

### Git Integration
- Branch management
- Push/pull
- History view

## Using Source Control in ableton-mcp

### Committing Changes

Following project conventions:
```bash
# Conventional commit format
git commit -m "feat: add tempo detection MCP tool"
git commit -m "test: add integration tests for rumble track"
git commit -m "fix: resolve socket timeout in session tests"
git commit -m "docs: update MCP documentation"
```

### Branch Workflow
```bash
# Feature branch
git checkout -b feature/tempo-detection

# After changes
git add .
git commit -m "feat: implement tempo detection"
git push -u origin feature/tempo-detection
```

### Reviewing Agent Changes

The agent modifies files which appear in source control:
1. Review diff in source control panel
2. Accept or reject changes
3. Stage approved files
4. Commit with descriptive message

## Best Practices

### 1. Review Before Commit
Always review agent-generated code changes.

### 2. Use Conventional Commits
```
feat:     New feature
fix:      Bug fix
test:     Adding tests
docs:     Documentation
refactor: Code refactoring
```

### 3. Atomic Commits
One logical change per commit.

### 4. Branch Naming
```
feature/<name>     # New features
test/<tool-name>   # Test additions
fix/<issue>        # Bug fixes
```

## Related Pages

- [Review Changes (Manager)](review-changes-manager.md) - Manager view
- [Changes Sidebar](changes-sidebar.md) - Sidebar view
