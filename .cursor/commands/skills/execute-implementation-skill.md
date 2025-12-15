# Execute Implementation Skill

## Overview

Execute the complete implementation workflow: Code generation + testing + validation. Orchestrates Coder agents to implement validated plans with automatic quality checks.

## Usage

Type `/execute-implementation-skill` followed by implementation task.

## Parameters

- `prompt`: Implementation task or plan (required)
- `language`: Programming language (default: python)
- `context_query`: Context for GAM research (optional)
- `run_tests`: Generate tests (default: true)
- `run_linting`: Enable linting (default: true)

## Example Usage

### Implement from Plan

```
/execute-implementation-skill
Prompt: Implement User authentication system based on validated plan
Language: python
Context Query: FastAPI JWT authentication patterns
Run Tests: true
```

### Quick Implementation

```
/execute-implementation-skill
Prompt: Add logging to auth endpoints
Run Tests: false
Run Linting: true
```

### Multi-file Implementation

```
/execute-implementation-skill
Prompt: |
  Create authentication system with:
  1. User model (SQLAlchemy)
  2. JWT service
  3. Auth endpoints (FastAPI)
  4. Tests (pytest)
Language: python
```

## Workflow

1. **Context Gathering**:
   - Call `/gam-research` with context_query
   - Retrieve relevant code patterns
   - Load project conventions
   - Gather dependencies

2. **Code Generation**:
   - Call `/create-coder-agent`
   - Generate code following best practices
   - Include type hints and docstrings
   - Follow KISS principle

3. **Validation Phase**:
   - Call `/lint-code` (if enabled)
   - Run Ruff linting with auto-fix
   - Run Mypy type checking
   - Report issues

4. **File Writing**:
   - Use `coder_tool.robust_file_write()`
   - Write code to filesystem
   - Apply auto-fixes
   - Verify write success

5. **Test Generation** (if enabled):
   - Generate pytest tests
   - Include unit tests for all functions
   - Add integration tests if needed
   - Write test files

6. **Final Validation**:
   - Run tests (if generated)
   - Verify all files created
   - Check import statements
   - Validate package dependencies

7. **Output**:
   - Return implementation result
   - Include file paths and metrics
   - Save patterns to GAM memory

## Implementation

This command uses:
- **Implementation Skill**: `app.server.skills.implementation.generate_and_implement()`
- **Coder Agent**: `app.server.agents.factory.create_agent("coder")`
- **GAM Integration**: `app.core.GAMMemoryManager`
- **Code Tool**: `app.server.tools.coder_tool`

## Output Format

```json
{
  "success": true,
  "files_created": [
    {
      "path": "app/models/user.py",
      "lines": 85,
      "validation": {
        "ruff_issues": 0,
        "type_issues": 0,
        "success": true
      }
    },
    {
      "path": "app/services/jwt_service.py",
      "lines": 120,
      "validation": {
        "ruff_issues": 0,
        "type_issues": 0,
        "success": true
      }
    },
    {
      "path": "app/api/auth.py",
      "lines": 95,
      "validation": {
        "ruff_issues": 0,
        "type_issues": 0,
        "success": true
      }
    }
  ],
  "tests_created": [
    {
      "path": "tests/unit/test_user.py",
      "test_count": 8
    },
    {
      "path": "tests/unit/test_jwt_service.py",
      "test_count": 12
    },
    {
      "path": "tests/integration/test_auth_api.py",
      "test_count": 6
    }
  ],
  "test_results": {
    "passed": 26,
    "failed": 0,
    "total": 26
  },
  "metrics": {
    "latency_ms": 8750,
    "generation_time_ms": 6200,
    "validation_time_ms": 1350,
    "test_time_ms": 1200
  }
}
```

## Best Practices

- Research patterns from GAM first
- Enable linting for production code
- Generate tests for all new code
- Use type hints consistently
- Follow project conventions
- Validate package dependencies
- Run tests before committing

## Error Handling

### Linting Failures

```
⚠️  Linting Issues Detected

File: app/services/auth.py
- Line 42: E501 Line too long (105 > 100) [AUTO-FIXED]
- Line 15: Missing type annotation [MANUAL FIX REQUIRED]

Action: Auto-fixed 1 issue, 1 requires manual fix
```

### Test Failures

```
❌ Tests Failed

tests/unit/test_auth.py::test_login_invalid_credentials FAILED

Error: AssertionError: Expected 401, got 500

Action: Review implementation and fix error handling
```

## Related Commands

- `/create-coder-agent` - Standalone coding agent
- `/lint-code` - Standalone linting
- `/execute-planning-skill` - Previous step (planning)
- `/execute-review-skill` - Next step (review)
- `/batch-implement` - Parallel implementation

## Requirements

- Ollama server running
- Ruff installed (for linting)
- Mypy installed (for type checking)
- Pytest installed (for test generation)
- GAM memory initialized
