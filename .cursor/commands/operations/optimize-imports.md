# Optimize Imports

## Overview

Verify all imports are valid, remove unused imports, and detect hallucinated packages. Prevents runtime import errors.

## Usage

Type `/optimize-imports` to check current file or specify target.

## Parameters

- `target`: File or directory to check (default: current file)
- `fix`: Auto-fix issues (default: false)
- `strict`: Fail on any issues (default: false)

## Example Usage

### Check Current File

```
/optimize-imports
```

### Check and Fix

```
/optimize-imports
Target: app/services/
Fix: true
```

### Strict Validation

```
/optimize-imports
Target: app/
Strict: true
```

## Workflow

1. **Extract Imports**:
   - Parse all `import` and `from ... import` statements
   - Group by: stdlib, third-party, local

2. **Validate Packages**:
   - Call `package_tool.validate_dependencies()`
   - Check against `pyproject.toml` dependencies
   - Verify package exists on PyPI

3. **Detect Issues**:
   - Hallucinated packages (not in PyPI)
   - Missing dependencies (not in pyproject.toml)
   - Unused imports (not referenced in code)
   - Circular imports
   - Import order violations

4. **Fix (if enabled)**:
   - Remove unused imports
   - Sort imports (stdlib → third-party → local)
   - Add missing dependencies to pyproject.toml
   - Report hallucinated packages (cannot auto-fix)

## Output Format

```
Import Analysis: app/services/auth.py

✅ Valid Imports (15):
  - fastapi
  - pydantic
  - sqlalchemy

⚠️  Unused Imports (2):
  - typing.Optional (line 3)
  - datetime.timedelta (line 5)

❌ Invalid Imports (1):
  - fake_package (line 10) - Package does not exist

📦 Missing Dependencies (1):
  - redis (used but not in pyproject.toml)

Suggestions:
  - Run: uv add redis
  - Remove: fake_package import
  - Auto-fix: /optimize-imports --fix
```

## Best Practices

- Run before committing
- Use `--fix` for automatic cleanup
- Verify hallucinated packages manually
- Keep pyproject.toml in sync
- Use pre-commit hook for automation

## Integration

### Pre-commit Hook

```yaml
- id: optimize-imports
  name: Optimize Python Imports
  entry: uv run python -m app.tools.optimize_imports
  language: system
  types: [python]
```

### Makefile Target

```makefile
optimize-imports:
	uv run python -m app.tools.optimize_imports --fix app/
```

## Related Commands

- `/validate-architecture` - Includes package validation
- `/qa-critic` - Reviews import patterns
- `/generate-code-streaming` - Auto-validates imports
