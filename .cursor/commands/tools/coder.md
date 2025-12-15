# Tool: Coder

## Overview

Write code with linting validation. This command provides direct access to the coder tool from `app/server/tools/coder_tool.py` for writing, editing, and validating code files with automatic linting.

## Usage

Type `/tool-coder` followed by the file operation.

## Parameters

- `operation`: Operation to perform (write, edit, delete, validate) (required)
- `file_path`: Path to file (required)
- `content`: File content (for write/edit operations)
- `changes`: Specific changes to make (for edit operation)
- `run_linting`: Enable linting after write (default: true)
- `auto_fix`: Auto-fix linting errors (default: true)
- `language`: Programming language (auto-detected from extension)

## Example Usage

### Write New File

```
/tool-coder
Operation: write
File Path: app/api/users.py
Content: |
  from fastapi import APIRouter, HTTPException
  from app.models import User

  router = APIRouter()

  @router.get("/users/{user_id}")
  async def get_user(user_id: int):
      user = await User.get(user_id)
      if not user:
          raise HTTPException(404, "User not found")
      return user
Run Linting: true
Auto Fix: true
```

### Edit Existing File

```
/tool-coder
Operation: edit
File Path: app/api/users.py
Changes: |
  Add caching decorator to get_user function
  Add rate limiting
Run Linting: true
```

### Validate File

```
/tool-coder
Operation: validate
File Path: app/api/users.py
```

### Delete File

```
/tool-coder
Operation: delete
File Path: app/api/deprecated.py
```

## Operations

### Write

Create new file with content and linting.

**Workflow**:
1. Create file with content
2. Run language-specific linter
3. Auto-fix common errors if enabled
4. Report linting results

**Returns**:
```json
{
  "operation": "write",
  "file_path": "app/api/users.py",
  "lines_written": 12,
  "linting_results": {
    "passed": true,
    "errors": 0,
    "warnings": 1,
    "fixed": 1,
    "details": [
      {
        "line": 8,
        "message": "Missing trailing comma",
        "fixed": true
      }
    ]
  },
  "success": true
}
```

### Edit

Modify existing file with changes.

**Workflow**:
1. Load existing file
2. Apply changes
3. Run linting
4. Auto-fix if enabled
5. Save file

**Returns**:
```json
{
  "operation": "edit",
  "file_path": "app/api/users.py",
  "changes_applied": [
    "Added caching decorator",
    "Added rate limiting"
  ],
  "linting_results": {
    "passed": true,
    "errors": 0,
    "warnings": 0
  },
  "success": true
}
```

### Validate

Check file for linting errors without modifying.

**Returns**:
```json
{
  "operation": "validate",
  "file_path": "app/api/users.py",
  "valid": false,
  "errors": [
    {
      "line": 15,
      "column": 20,
      "message": "Undefined variable 'db'",
      "severity": "error"
    }
  ],
  "warnings": [
    {
      "line": 8,
      "message": "Function too complex (complexity: 12)",
      "severity": "warning"
    }
  ]
}
```

### Delete

Remove file from filesystem.

**Returns**:
```json
{
  "operation": "delete",
  "file_path": "app/api/deprecated.py",
  "success": true,
  "backup_path": "/tmp/backup/deprecated.py"
}
```

## Linting Support

### Python
- **Linter**: ruff
- **Auto-fix**: Format, import sorting, common errors
- **Checks**: Syntax, style, complexity, security

### TypeScript/JavaScript
- **Linter**: eslint
- **Auto-fix**: Format, semicolons, quotes
- **Checks**: Syntax, style, best practices

### Go
- **Linter**: gofmt, golint
- **Auto-fix**: Format only
- **Checks**: Format, style

### Rust
- **Linter**: rustfmt, clippy
- **Auto-fix**: Format only
- **Checks**: Format, style, common mistakes

## Best Practices

- Always run linting for production code
- Enable auto-fix to save time
- Validate before committing
- Review linting warnings
- Use consistent code style
- Fix errors before warnings

## Integration

- Used by `/skill-implementation` internally
- Invoked by `/agent-coder` for file operations
- Provides immediate feedback loop
- Ensures code quality

## Related Commands

- `/skill-implementation` - Full implementation workflow
- `/agent-coder` - Code generation agent
- `/generate-code` - Alternative code generation
- `/optimize-imports` - Import optimization

## Source

- **File**: `app/server/tools/coder_tool.py`
- **Function**: `robust_file_write()`, `validate_code()`
- **Layer**: Tools (HOW)
