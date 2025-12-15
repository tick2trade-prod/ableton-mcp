# Agent: Coder

## Overview

Invoke coder agent for implementation. This command directly invokes the Coder agent from `app/server/agents/factory.py` with the CODER_SYSTEM_PROMPT to generate code, implement features, and write tests.

> **Layer**: WHO (Agent Factory)
> **Rank**: 2 - Layer-Based Command

## Usage

Type `/agent-coder` followed by your coding request.

## Parameters

- `request`: Coding request (required)
- `language`: Programming language (default: "python")
- `context`: Code context or examples (optional)
- `model`: Ollama model to use (default: auto-select)
- `temperature`: Response creativity (0.0-1.0) (default: 0.3)
- `include_tests`: Generate tests (default: true)
- `include_docs`: Generate docstrings (default: true)

## Example Usage

### Basic Code Generation

```
/agent-coder
Request: Create a FastAPI endpoint for user registration
Language: python
Include Tests: true
```

### TypeScript Implementation

```
/agent-coder
Request: Implement React hook for authentication
Language: typescript
Context: Using React Query and Zustand
Include Tests: true
```

### Code with Examples

```
/agent-coder
Request: Add caching decorator to existing function
Language: python
Context: |
  def get_user(user_id: int) -> User:
      return db.query(User).filter(User.id == user_id).first()
```

## Implementation

```python
from app.server.agents.factory import create_agent
from app.server.agents.prompts import CODER_SYSTEM_PROMPT

agent = create_agent(
    role="coder",
    model=model,
    system_prompt=CODER_SYSTEM_PROMPT,
    tools=["coder_tool", "package_verify", "gam_memory"],
)

code = await agent.run(
    task=request,
    language=language,
    context=context,
    include_tests=include_tests,
    include_docs=include_docs,
)
```

## Workflow

1. **Agent Creation**:
   - Load CODER_SYSTEM_PROMPT
   - Select code-optimized model
   - Configure low temperature for precision

2. **Context Enhancement**:
   - Load project structure
   - Retrieve coding conventions
   - Gather similar implementations

3. **Code Generation**:
   - Generate implementation code
   - Add type hints and annotations
   - Include error handling

4. **Test Generation** (if enabled):
   - Create unit tests
   - Add integration tests if needed
   - Include edge cases

5. **Documentation** (if enabled):
   - Add docstrings
   - Include usage examples
   - Document parameters and returns

## Output Format

```python
# Implementation
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.models import User
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    """User registration request model."""
    email: EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    """User response model."""
    id: int
    email: str
    full_name: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db=Depends(get_db)):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user information

    Raises:
        HTTPException: If email already exists
    """
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name
    )

# Tests
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user_success():
    """Test successful user registration."""
    response = client.post("/api/users/register", json={
        "email": "test@example.com",
        "password": "secure123",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_email():
    """Test registration with duplicate email fails."""
    # Register first user
    client.post("/api/users/register", json={
        "email": "duplicate@example.com",
        "password": "pass123",
        "full_name": "User One"
    })

    # Try to register again
    response = client.post("/api/users/register", json={
        "email": "duplicate@example.com",
        "password": "pass456",
        "full_name": "User Two"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
```

## Best Practices

- Provide specific, clear requests
- Include code context when available
- Always generate tests for production code
- Use low temperature for deterministic output
- Review generated code before committing
- Run linting and tests after generation

## Integration

- Used by `/skill-implementation` internally
- Chains from `/agent-planner` output
- Validated by `/agent-critic`
- Uses `/tool-coder` for file operations

## Related Commands

- `/skill-implementation` - Full implementation workflow
- `/agent-planner` - Planning agent
- `/agent-critic` - Code review agent
- `/tool-coder` - Direct coder tool

## Source

- **File**: `app/server/agents/factory.py`
- **Prompt**: `app/server/agents/prompts.py` → `CODER_SYSTEM_PROMPT`
- **Layer**: Agents (WHO)
