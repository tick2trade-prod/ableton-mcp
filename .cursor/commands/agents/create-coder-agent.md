# Create Coder Agent

## Overview

Create a coding agent with linting validation and best practices enforcement. The Coder agent generates clean, tested code following project conventions.

## Usage

Type `/create-coder-agent` followed by coding task and language.

## Parameters

- `task`: Coding task description (required)
- `language`: Programming language (default: python)
- `run_linting`: Enable automatic linting (default: true)
- `run_tests`: Generate tests (default: true)

## Example Usage

### Basic Code Generation

```
/create-coder-agent
Task: Create FastAPI endpoint for user registration with validation
Language: python
```

### Code with Tests

```
/create-coder-agent
Task: Implement Redis caching service with async operations
Language: python
Run Tests: true
```

### Quick Code (No Linting)

```
/create-coder-agent
Task: Add type hints to existing function
Run Linting: false
Run Tests: false
```

## Workflow

1. **Create Agent**:
   - Call `app.server.agents.factory.create_agent("coder")`
   - Inject `CODER_SYSTEM_PROMPT` with task context
   - Attach tools: `coder_tool`, `gam_tool`, `package_tool`

2. **Research Phase**:
   - Query GAM memory for similar code patterns
   - Research language-specific best practices
   - Check for existing implementations

3. **Code Generation**:
   - Generate code following project conventions
   - Include type hints and docstrings
   - Follow KISS principle

4. **Validation Phase**:
   - Run Ruff linting (if enabled)
   - Run Mypy type checking
   - Auto-fix common issues
   - Report remaining issues

5. **Testing Phase** (if enabled):
   - Generate pytest tests
   - Include unit tests for all functions
   - Add integration tests if needed

6. **Output**:
   - Write code to file using `coder_tool.robust_file_write()`
   - Return validation report
   - Save patterns to GAM memory

## Implementation

This command uses:
- **Agent Factory**: `app.server.agents.factory.create_agent()`
- **System Prompt**: `app.server.agents.prompts.CODER_SYSTEM_PROMPT`
- **GAM Integration**: `app.core.GAMMemoryManager`
- **Tools**: `coder_tool`, `gam_tool`, `package_tool`
- **Linting**: Ruff + Mypy via `coder_tool.robust_file_write()`

## Output Format

```json
{
  "code": {
    "file_path": "app/services/auth.py",
    "content": "# Generated code...",
    "lines": 150
  },
  "validation": {
    "ruff_issues": [],
    "type_issues": [],
    "success": true
  },
  "tests": {
    "file_path": "tests/unit/test_auth.py",
    "test_count": 8
  }
}
```

## Best Practices

- Always research similar patterns first
- Enable linting for production code
- Generate tests for all new code
- Use type hints consistently
- Follow project conventions
- Validate package dependencies

## Related Commands

- `/execute-implementation-skill` - Full implementation workflow
- `/lint-code` - Standalone linting tool
- `/verify-packages` - Package validation
- `/gam-research` - Research code patterns

## Requirements

- Ollama server running (for agent execution)
- Ruff installed (for linting)
- Mypy installed (for type checking)
- Pytest installed (for test generation)
