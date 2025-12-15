# Verify Packages

## Overview

Verify package dependencies exist in PyPI or NPM to prevent hallucinated libraries. Critical for catching non-existent packages before implementation.

> **Layer**: HOW (Execution Primitives)
> **Rank**: 2 - Layer-Based Command (`/tool-package-verify`)

## Usage

Type `/verify-packages` followed by package list.

## Parameters

- `packages`: List of packages to verify (required)
- `ecosystem`: Package ecosystem (pypi, npm) (default: pypi)
- `strict`: Fail on any invalid package (default: true)

## Example Usage

### Verify Python Packages

```
/verify-packages
Packages: fastapi, sqlalchemy, redis, fake-package
Ecosystem: pypi
```

### Verify NPM Packages

```
/verify-packages
Packages: react, typescript, express, nonexistent-lib
Ecosystem: npm
Strict: true
```

### Quick Validation

```
/verify-packages
Packages: pydantic, fastmcp, deepagents
```

## Workflow

1. **Package Parsing**:
   - Parse package names from list
   - Handle version specs (>=, ==, <)
   - Extract package name only

2. **API Query**:
   - Call `app.server.tools.package_tool.validate_dependencies()`
   - Query PyPI JSON API: `https://pypi.org/pypi/{package}/json`
   - Query NPM Registry: `https://registry.npmjs.org/{package}`

3. **Validation**:
   - Check HTTP 200 response
   - Extract package metadata
   - Identify invalid packages

4. **Reporting**:
   - List valid packages with versions
   - List invalid packages with errors
   - Suggest alternatives if available

5. **Action**:
   - **HALT** if any package is hallucinated (strict mode)
   - Provide fix suggestions

## Implementation

This command uses:
- **Package Tool**: `app.server.tools.package_tool`
- **PyPI API**: `https://pypi.org/pypi/{package}/json`
- **NPM Registry**: `https://registry.npmjs.org/{package}`
- **HTTP Client**: `requests` or `httpx`

## Output Format

```json
{
  "total": 4,
  "valid": 3,
  "invalid": [
    {
      "name": "fake-package",
      "exists": false,
      "error": "Package not found (HTTP 404)",
      "suggestion": "Did you mean: faker?"
    }
  ],
  "all_valid": false,
  "packages": [
    {
      "name": "fastapi",
      "exists": true,
      "latest_version": "0.109.0",
      "description": "FastAPI framework"
    },
    {
      "name": "sqlalchemy",
      "exists": true,
      "latest_version": "2.0.25",
      "description": "SQL toolkit"
    },
    {
      "name": "redis",
      "exists": true,
      "latest_version": "5.0.1",
      "description": "Redis client"
    }
  ]
}
```

## Error Handling

### Hallucinated Package Detected

```
❌ HALLUCINATION DETECTED

Package 'fake-package' does not exist in PyPI.

Suggestions:
- Did you mean: faker, fake-factory?
- Search PyPI: https://pypi.org/search/?q=fake-package
- Use /gam-research to find alternative packages

Action: HALT - Fix package names before proceeding.
```

## Best Practices

- **Always validate before implementation**
- Run before `/create-planner-agent`
- Use strict mode for production
- Verify all dependencies in plan
- Check for typos in package names
- Research alternatives for invalid packages
- Update pyproject.toml after validation

## Integration Points

### With Planning

```
1. /create-planner-agent → generates plan with dependencies
2. /verify-packages → validates all packages
3. If valid → proceed to implementation
4. If invalid → revise plan with Critic agent
```

### With QA

```
1. /create-critic-agent → reviews architecture
2. /verify-packages → validates dependencies
3. Critic includes package validation in QAReport
```

## Related Commands

- `/validate-architecture` - Pre-generation validation (includes package check)
- `/create-critic-agent` - QA validation with package check
- `/create-planner-agent` - Planning with dependency validation
- `/optimize-imports` - Import validation and cleanup

## Requirements

- Internet connection (for API queries)
- `requests` or `httpx` library
- PyPI/NPM API access (no auth required)
