# Agent: Structured Response

## Overview

Get structured JSON response from agent. This command invokes the `generate_structured_response()` function from `app/server/agents/factory.py` to get type-safe, validated JSON responses from any agent.

## Usage

Type `/agent-structured` followed by your request and schema.

## Parameters

- `request`: Request to send to agent (required)
- `schema`: Pydantic model class name (required)
- `agent_type`: Agent to use (planner, coder, critic) (default: "planner")
- `model`: Ollama model to use (default: auto-select)
- `max_retries`: Retry attempts for validation (default: 3)
- `context`: Additional context (optional)

## Example Usage

### Get Structured Plan

```
/agent-structured
Request: Create plan for user authentication
Schema: Plan
Agent Type: planner
```

### Get QA Report

```
/agent-structured
Request: Review this code for security issues
Schema: QAReport
Agent Type: critic
Context: <code to review>
```

### Get Task List

```
/agent-structured
Request: Break down e-commerce platform into tasks
Schema: TaskList
Agent Type: planner
```

## Available Schemas

### Plan

```python
class Plan(BaseModel):
    overview: str
    todos: list[Todo]
    dependencies: dict[str, list[str]]
    risks: list[str]
```

### QAReport

```python
class QAReport(BaseModel):
    score: int
    critical_issues: list[CritiqueIssue]
    warnings: list[CritiqueIssue]
    suggestions: list[CritiqueIssue]
    summary: str
```

### TaskList

```python
class TaskList(BaseModel):
    tasks: list[Task]
    total_estimated_time: str
    priority_order: list[int]
```

### FileChange

```python
class FileChange(BaseModel):
    path: str
    action: str  # create, modify, delete
    content: str
    reason: str
```

## Workflow

1. **Schema Validation**:
   - Load Pydantic schema
   - Validate schema exists
   - Generate JSON schema

2. **Agent Selection**:
   - Choose appropriate agent
   - Load system prompt
   - Configure parameters

3. **Request with Schema**:
   - Send request with JSON schema
   - Instruct agent to follow schema
   - Request JSON-only output

4. **Response Parsing**:
   - Parse JSON response
   - Validate against schema
   - Retry if validation fails

5. **Retry Logic**:
   - Up to max_retries attempts
   - Provide validation errors to agent
   - Request corrections

## Output Format

```json
{
  "request": "Create plan for user authentication",
  "schema": "Plan",
  "validated": true,
  "attempts": 1,
  "response": {
    "overview": "Implement JWT-based authentication system",
    "todos": [
      {
        "id": 1,
        "task": "Create User model",
        "priority": "high",
        "estimated_time": "2h",
        "dependencies": []
      },
      {
        "id": 2,
        "task": "Implement JWT token generation",
        "priority": "high",
        "estimated_time": "3h",
        "dependencies": [1]
      },
      {
        "id": 3,
        "task": "Create authentication middleware",
        "priority": "high",
        "estimated_time": "2h",
        "dependencies": [2]
      }
    ],
    "dependencies": {
      "pyjwt": [">=2.8.0"],
      "passlib": [">=1.7.4"],
      "python-multipart": [">=0.0.6"]
    },
    "risks": [
      "Token expiration handling",
      "Refresh token security",
      "Password hashing performance"
    ]
  }
}
```

## Best Practices

- Use appropriate schema for task
- Provide clear, specific requests
- Include context when needed
- Validate output programmatically
- Handle validation errors gracefully
- Save structured responses to GAM

## Integration

- Used by all skill commands internally
- Enables type-safe agent responses
- Integrates with Pydantic models
- Supports automatic retries

## Related Commands

- `/agent-planner` - Planning agent
- `/agent-coder` - Coding agent
- `/agent-critic` - QA agent
- `/skill-planning` - Uses structured Plan output

## Source

- **File**: `app/server/agents/factory.py`
- **Function**: `generate_structured_response()`
- **Layer**: Agents (WHO)
