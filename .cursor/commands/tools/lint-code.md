# Lint Code

## Overview

Run Ruff linting and Mypy type checking for immediate feedback and validation. Provides fast, comprehensive code quality checks.

> **Layer**: HOW (Execution Primitives)
> **Rank**: 4 - Atomic Operation (`/op-file-lint`)

## Usage

Type `/lint-code` to check current file or specify target.

## Parameters

- `target`: File or directory to lint (default: current file)
- `auto_fix`: Auto-fix issues (default: true)
- `strict`: Fail on any issues (default: false)
- `check_types`: Run Mypy type checking (default: true)

## Example Usage

### Lint Current File

```
/lint-code
```

### Lint with Auto-fix

```
/lint-code
Target: app/services/auth.py
Auto Fix: true
```

### Lint Directory

```
/lint-code
Target: app/server/
Auto Fix: false
Strict: true
```

### Quick Lint (No Type Check)

```
/lint-code
Target: app/utils/helpers.py
Check Types: false
```

## Workflow

1. **Ruff Linting**:
   - Run `ruff check --fix {target}` (if auto_fix)
   - Run `ruff check {target}` (if no auto_fix)
   - Capture output and errors
   - Parse issues by line number

2. **Mypy Type Checking** (if enabled):
   - Run `mypy {target}`
   - Capture type errors
   - Parse issues by line number

3. **Reporting**:
   - Group issues by severity
   - Provide line numbers
   - Suggest fixes
   - Show auto-fixed issues

4. **Action**:
   - Return validation report
   - Fail if strict mode and issues found
   - Provide fix commands

## Implementation

This command uses:
- **Coder Tool**: `app.server.tools.coder_tool.robust_file_write()`
- **Ruff**: Blazingly fast Python linter (Rust-based)
- **Mypy**: Static type checker
- **Subprocess**: Command execution

## Output Format

```json
{
  "target": "app/services/auth.py",
  "ruff": {
    "issues": [
      {
        "line": 42,
        "column": 10,
        "code": "E501",
        "message": "Line too long (105 > 100)",
        "severity": "warning",
        "auto_fixed": true
      }
    ],
    "auto_fixed_count": 1,
    "remaining_count": 0
  },
  "mypy": {
    "issues": [
      {
        "line": 15,
        "message": "Missing type annotation for 'user'",
        "severity": "error"
      }
    ],
    "error_count": 1
  },
  "success": false,
  "summary": "1 auto-fixed, 1 type error remaining"
}
```

## Ruff Rules

Default rules enabled:
- **E**: pycodestyle errors
- **F**: Pyflakes
- **I**: isort (import sorting)
- **N**: pep8-naming
- **W**: pycodestyle warnings
- **UP**: pyupgrade
- **ASYNC**: async best practices
- **S**: bandit security checks

## Best Practices

- Run before committing code
- Enable auto_fix for quick cleanup
- Use strict mode for production
- Fix type errors manually
- Run on entire directory periodically
- Integrate with pre-commit hooks
- Keep pyproject.toml config updated

## Performance

- **Ruff**: 10-100x faster than Pylint/Flake8
- **Mypy**: Moderate speed, thorough checking
- **Typical File**: <100ms for Ruff, <1s for Mypy
- **Large Directory**: <5s for Ruff, <30s for Mypy

## Related Commands

- `/create-coder-agent` - Code generation with auto-linting
- `/optimize-imports` - Import-specific validation
- `/qa-critic` - Comprehensive code review
- `/generate-code-streaming` - Generation with validation

## Requirements

- Ruff installed: `uv add ruff`
- Mypy installed: `uv add --dev mypy`
- Python 3.12+ for best results
