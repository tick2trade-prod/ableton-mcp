# Debug Assistant

## Overview

AI-powered debugging assistant that analyzes errors, suggests fixes, and applies solutions. Uses GAM memory to learn from past bugs.

## Usage

Type `/debug-assistant` when encountering an error.

## Parameters

- `error`: Error message or stack trace (optional, auto-detected)
- `context`: Additional context (optional)
- `auto_fix`: Automatically apply suggested fix (default: false)
- `search_gam`: Search for similar past issues (default: true)

## Example Usage

### Auto-Detect Error

```
/debug-assistant
```

### With Error Message

```
/debug-assistant
Error: |
  AttributeError: 'NoneType' object has no attribute 'email'
  File "app/services/user.py", line 42, in get_user_email
Context: Occurs when user not found in database
```

### Auto-Fix Mode

```
/debug-assistant
Auto Fix: true
Search GAM: true
```

## Workflow

1. **Error Detection**:
   - Auto-detect from terminal output
   - Parse stack trace
   - Identify error type and location
   - Extract relevant code context

2. **Root Cause Analysis**:
   - Analyze error message
   - Examine surrounding code
   - Check variable states
   - Identify logical issues

3. **GAM Memory Search**:
   - Search for similar past errors
   - Find previously successful fixes
   - Learn from team knowledge
   - Avoid repeated mistakes

4. **Solution Generation**:
   - Propose 2-3 potential fixes
   - Rank by likelihood of success
   - Explain reasoning for each
   - Provide code examples

5. **Apply Fix (if enabled)**:
   - Apply highest-ranked solution
   - Run tests to verify fix
   - If tests fail, try next solution
   - Save successful fix to GAM

## Error Categories

### Common Errors Handled

- **AttributeError**: None checks, object validation
- **KeyError**: Dictionary access, default values
- **TypeError**: Type validation, conversion
- **ValueError**: Input validation, parsing
- **ImportError**: Missing dependencies, circular imports
- **SQLAlchemyError**: Query issues, connection problems
- **ValidationError**: Pydantic validation, data issues
- **HTTPException**: API errors, status codes

## Debug Report Format

```markdown
# Debug Report

## Error Summary
AttributeError: 'NoneType' object has no attribute 'email'

## Location
File: app/services/user.py
Line: 42
Function: get_user_email

## Root Cause
User object is None when user_id doesn't exist in database.
No null check before accessing .email attribute.

## Similar Past Issues
Found 2 similar issues in GAM:
1. Fixed on 2024-11-15: Added null check with proper error handling
2. Fixed on 2024-10-20: Used Optional[User] type hint

## Suggested Fixes (Ranked)

### Fix #1: Add Null Check (Confidence: 95%)
```python
def get_user_email(user_id: int) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError(f"User {user_id} not found")
    return user.email
```

### Fix #2: Use Optional Return Type (Confidence: 85%)
```python
def get_user_email(user_id: int) -> Optional[str]:
    user = db.query(User).filter(User.id == user_id).first()
    return user.email if user else None
```

## Recommended Action
Apply Fix #1 - Most robust and explicit error handling
```

## Best Practices

- Let assistant auto-detect errors when possible
- Provide context for complex issues
- Review suggested fixes before applying
- Use auto_fix for simple, well-understood errors
- Save successful fixes to GAM for team learning
- Run tests after applying fixes

## Integration

### Terminal Integration
Automatically detects errors from:
- Python tracebacks
- pytest failures
- Linter errors
- Runtime exceptions

### IDE Integration
- Inline error suggestions
- Quick fix actions
- Test execution validation

## Related Commands

- `/qa-critic` - Prevent bugs before they occur
- `/test-generator` - Add tests for fixed bugs
- `/deep-research` - Research unfamiliar errors
