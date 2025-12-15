# Domain: Code Generator

## Overview

Code generation with streaming. This command provides direct access to the pure domain logic in `app/generation/code_generator.py` (`CodeGenerator`) for generating code with streaming support.

## Usage

Type `/domain-code-generator` followed by the generation request.

## Parameters

- `prompt`: Code generation prompt (required)
- `language`: Programming language (default: "python")
- `context`: Additional context (optional)
- `streaming`: Enable streaming output (default: true)
- `include_tests`: Generate tests (default: true)
- `include_docs`: Generate documentation (default: true)

## Example Usage

### Generate Python Code

```
/domain-code-generator
Prompt: Create FastAPI endpoint for user registration
Language: python
Context: Using SQLAlchemy and Pydantic
Streaming: true
Include Tests: true
```

### Generate TypeScript Code

```
/domain-code-generator
Prompt: Create React component for login form
Language: typescript
Context: Using React Hook Form and Zod validation
Include Tests: true
```

### Generate with Streaming

```
/domain-code-generator
Prompt: Implement binary search algorithm
Language: python
Streaming: true
```

## Domain Logic

### CodeGenerator

Pure domain class for code generation.

```python
from app.generation.code_generator import CodeGenerator

# Initialize
generator = CodeGenerator(
    language="python",
    include_tests=True,
    include_docs=True
)

# Generate code (streaming)
async for chunk in generator.generate_streaming(
    prompt="Create FastAPI endpoint for user registration",
    context="Using SQLAlchemy and Pydantic"
):
    print(chunk.content, end="", flush=True)

# Generate code (non-streaming)
result = await generator.generate(
    prompt="Create FastAPI endpoint",
    context="Using SQLAlchemy"
)
```

## Output Format

### Streaming Output

```python
# Chunk 1
{
    "type": "code",
    "content": "from fastapi import APIRouter, HTTPException\n",
    "language": "python",
    "chunk_index": 0
}

# Chunk 2
{
    "type": "code",
    "content": "from pydantic import BaseModel, EmailStr\n",
    "language": "python",
    "chunk_index": 1
}

# ... more chunks ...

# Final chunk
{
    "type": "done",
    "total_chunks": 45,
    "total_lines": 67,
    "files_generated": ["app/api/users.py", "tests/test_users.py"]
}
```

### Complete Output

```python
{
    "prompt": "Create FastAPI endpoint for user registration",
    "language": "python",
    "code": {
        "implementation": """
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.models import User
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db=Depends(get_db)):
    # Implementation...
    pass
""",
        "tests": """
import pytest
from fastapi.testclient import TestClient

def test_register_user_success():
    # Test implementation...
    pass

def test_register_duplicate_email():
    # Test implementation...
    pass
""",
        "docs": """
# User Registration API

## Endpoint
POST /api/users/register

## Request Body
- email: Valid email address
- password: Secure password
- full_name: User's full name

## Response
201 Created with user data
"""
    },
    "metadata": {
        "lines_of_code": 67,
        "test_count": 2,
        "generation_time_ms": 2345
    }
}
```

## Features

### Language Support

- **Python**: FastAPI, Django, Flask
- **TypeScript**: React, Node.js, Express
- **Go**: Standard library, Gin, Echo
- **Rust**: Actix, Rocket, Axum

### Code Quality

- Type hints and annotations
- Error handling
- Input validation
- Documentation strings
- Best practices

### Test Generation

- Unit tests
- Integration tests
- Edge cases
- Mock data

### Documentation

- API documentation
- Usage examples
- Parameter descriptions
- Return value docs

## Best Practices

- Provide clear, specific prompts
- Include relevant context
- Enable streaming for better UX
- Always generate tests
- Review generated code
- Validate with linting

## Integration

- Used by `/skill-implementation` internally
- Wrapped by `/tool-coder` for file operations
- Invoked by `/agent-coder`
- Pure domain logic, no infrastructure

## Related Commands

- `/skill-implementation` - Full implementation workflow
- `/agent-coder` - Coding agent
- `/tool-coder` - Coder tool with file operations
- `/generate-code` - Alternative generation command

## Source

- **File**: `app/generation/code_generator.py`
- **Class**: `CodeGenerator`
- **Layer**: Domain (Generation)
