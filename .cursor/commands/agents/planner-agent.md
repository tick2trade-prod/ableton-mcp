# Agent: Planner

## Overview

Invoke planner agent with context. This command directly invokes the Planner agent from `app/server/agents/factory.py` with the PLANNER_SYSTEM_PROMPT to create plans, break down tasks, and provide strategic guidance.

> **Layer**: WHO (Agent Factory)
> **Rank**: 2 - Layer-Based Command

## Usage

Type `/agent-planner` followed by your planning request.

## Parameters

- `request`: Planning request (required)
- `context`: Additional context (optional)
- `model`: Ollama model to use (default: auto-select)
- `temperature`: Response creativity (0.0-1.0) (default: 0.7)
- `structured_output`: Request JSON output (default: false)
- `output_schema`: Pydantic schema for structured output (optional)

## Example Usage

### Basic Planning Request

```
/agent-planner
Request: How should I structure a FastAPI microservices project?
Context: Using PostgreSQL, Redis, and RabbitMQ
```

### Structured Planning Output

```
/agent-planner
Request: Create implementation plan for user authentication
Structured Output: true
Output Schema: Plan
```

### Custom Model Selection

```
/agent-planner
Request: Design database schema for e-commerce platform
Model: qwen2.5-coder:32b
Temperature: 0.5
```

## Implementation

```python
from app.server.agents.factory import create_agent
from app.server.agents.prompts import PLANNER_SYSTEM_PROMPT

agent = create_agent(
    role="planner",
    model=model,
    system_prompt=PLANNER_SYSTEM_PROMPT,
    tools=["gam_memory", "web_search", "package_verify"],
)

plan = await agent.run(
    feature_description=request,
    context=context,
    structured_output=structured_output,
    output_schema=output_schema,
)
```

## Workflow

1. **Agent Creation**:
   - Load PLANNER_SYSTEM_PROMPT
   - Select appropriate Ollama model
   - Configure temperature and parameters

2. **Context Enhancement**:
   - Query GAM for relevant patterns
   - Load project conventions
   - Gather related examples

3. **Agent Invocation**:
   - Send request with context
   - Stream response if supported
   - Parse structured output if requested

4. **Response Processing**:
   - Validate output format
   - Extract actionable items
   - Save to GAM if valuable

## Output Format

### Text Output

```
Planning Recommendation:

For a FastAPI microservices project, I recommend:

1. Project Structure:
   - api-gateway/: Entry point for all requests
   - services/: Individual microservices
   - shared/: Common models and utilities
   - infrastructure/: Docker, K8s configs

2. Communication:
   - REST APIs for synchronous calls
   - RabbitMQ for async events
   - Redis for caching and sessions

3. Data Management:
   - PostgreSQL per service (if needed)
   - Shared database for user management
   - Event sourcing for audit logs
```

### Structured Output

```json
{
  "plan": {
    "overview": "FastAPI microservices architecture",
    "components": [
      {
        "name": "API Gateway",
        "technology": "FastAPI",
        "responsibilities": ["Routing", "Authentication", "Rate limiting"]
      },
      {
        "name": "User Service",
        "technology": "FastAPI + PostgreSQL",
        "responsibilities": ["User CRUD", "Profile management"]
      }
    ],
    "dependencies": {
      "fastapi": ">=0.104.0",
      "sqlalchemy": ">=2.0.0",
      "redis": ">=5.0.0",
      "pika": ">=1.3.0"
    }
  }
}
```

## Best Practices

- Provide clear, specific requests
- Include relevant context
- Use structured output for implementation
- Save valuable plans to GAM
- Validate recommendations with QA/Critic
- Iterate on plans based on feedback

## Integration

- Used by `/skill-planning` internally
- Chains to `/agent-coder` for implementation
- Validated by `/agent-critic`
- Saves output via `/tool-gam`

## Related Commands

- `/skill-planning` - Full planning workflow
- `/agent-coder` - Implementation agent
- `/agent-critic` - QA validation agent
- `/agent-structured` - Structured response helper

## Source

- **File**: `app/server/agents/factory.py`
- **Prompt**: `app/server/agents/prompts.py` → `PLANNER_SYSTEM_PROMPT`
- **Layer**: Agents (WHO)
