# Skill: Implementation

## Overview

Generate and implement code with linting validation. This command invokes the implementation skill from `app/server/skills/implementation.py` to write, test, and validate code.

> **Layer**: WHAT (Skill Orchestration)
> **Rank**: 2 - Layer-Based Command

## Usage

Type `/skill-implementation` followed by the implementation details.

## Parameters

- `prompt`: Implementation instructions (required)
- `language`: Programming language (default: "python")
- `context_query`: Query for GAM context (optional)
- `run_linting`: Enable linting after generation (default: true)
- `run_tests`: Run tests after implementation (default: true)
- `auto_fix`: Auto-fix linting errors (default: true)

## Example Usage

### Implement Feature

```
/skill-implementation
Prompt: Implement JWT authentication middleware
Language: python
Context Query: authentication patterns
Run Linting: true
Run Tests: true
```

### Quick Implementation (No Tests)

```
/skill-implementation
Prompt: Add logging to existing function
Language: python
Run Tests: false
```

### TypeScript Implementation

```
/skill-implementation
Prompt: Create React component for user profile
Language: typescript
Context Query: React best practices
```

## Workflow

1. **Context Gathering**:
   - Query GAM for relevant patterns
   - Load related files from codebase
   - Retrieve implementation examples

2. **Code Generation**:
   - Invoke Coder agent with context
   - Generate implementation code
   - Apply project conventions

3. **Linting Phase** (if enabled):
   - Run language-specific linter
   - Identify syntax errors
   - Check style violations

4. **Auto-Fix Phase** (if enabled):
   - Fix common linting errors
   - Format code properly
   - Re-run linter to verify

5. **Testing Phase** (if enabled):
   - Run relevant test suite
   - Report test results
   - Identify failing tests

6. **Save Results**:
   - Write code to files
   - Save to GAM memory
   - Generate summary report

## Output Format

```json
{
  "prompt": "Implement JWT authentication middleware",
  "language": "python",
  "files_created": [
    {
      "path": "app/middleware/auth.py",
      "lines": 45,
      "functions": ["verify_token", "require_auth"]
    }
  ],
  "files_modified": [
    {
      "path": "app/main.py",
      "changes": "Added auth middleware registration"
    }
  ],
  "linting_results": {
    "passed": true,
    "errors": 0,
    "warnings": 2,
    "fixed": 2
  },
  "test_results": {
    "passed": 8,
    "failed": 0,
    "skipped": 1
  },
  "gam_id": "impl-auth-middleware-xyz789"
}
```

## Best Practices

- Provide clear, specific prompts
- Include context queries for better results
- Always run linting for production code
- Enable auto-fix to save time
- Run tests to catch regressions
- Review generated code before committing

## Integration

- Follows `/skill-planning` in workflow
- Uses `/tool-coder` for code generation
- Invokes `/tool-gam` for context
- Chains to `/skill-review` for validation

## Related Commands

- `/skill-planning` - Create implementation plan
- `/skill-review` - Review implementation
- `/generate-code` - Alternative code generation
- `/tool-coder` - Direct coder tool access

## Source

- **File**: `app/server/skills/implementation.py`
- **Function**: `generate_and_implement()`
- **Layer**: Skills (WHAT)
