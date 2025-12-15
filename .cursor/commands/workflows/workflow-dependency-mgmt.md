# Workflow: Automated Dependency Management

## Overview

Monitor dependencies, propose safe version updates, provide risk summaries, and generate migration notes.

## Usage

```bash
/workflow-dependency-mgmt
```

## Parameters

- `action`: check, update, audit (required)
- `update_type`: patch, minor, major (default: patch)
- `auto_create_pr`: Auto-create update PR (default: true)
- `run_tests`: Run tests after update (default: true)

## Dependency Operations

```python
# Check
- Scan for outdated packages
- Check for vulnerabilities
- Analyze breaking changes

# Update
- Update dependencies
- Run tests
- Create PR with changes
- Generate migration notes

# Audit
- License compliance
- Security vulnerabilities
- Dependency tree analysis
- Unused dependencies
```

## Output

```json
{
  "outdated_packages": 12,
  "security_vulnerabilities": 2,
  "updates_proposed": 10,
  "pr_created": true,
  "tests_passed": true,
  "breaking_changes": 0
}
```
