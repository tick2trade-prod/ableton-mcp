# Create Planner Agent

## Overview

Create a planning agent with research capabilities and QA feedback loop. The Planner agent analyzes features, researches best practices from GAM memory, and generates structured implementation plans.

## Usage

Type `/create-planner-agent` followed by feature description and tech stack.

## Parameters

- `feature`: Feature description (required)
- `tech_stack`: Technologies to use (optional)
- `use_qa`: Enable QA feedback loop (default: true)
- `max_iterations`: Maximum QA iterations (default: 3)

## Example Usage

### Basic Planning

```
/create-planner-agent
Feature: User authentication system with JWT tokens
Tech Stack: FastAPI, PostgreSQL, Redis
```

### Planning with QA Loop

```
/create-planner-agent
Feature: Blog post management API with CRUD operations
Tech Stack: FastAPI, SQLAlchemy, PostgreSQL
Use QA: true
Max Iterations: 3
```

### Quick Planning (No QA)

```
/create-planner-agent
Feature: Add logging to existing endpoints
Use QA: false
```

## Workflow

1. **Create Agent**:
   - Call `app.server.agents.factory.create_agent("planner")`
   - Inject `PLANNER_SYSTEM_PROMPT` with feature context
   - Attach tools: `gam_tool`, `planner_tool`, `package_tool`

2. **Research Phase**:
   - Query GAM memory for relevant patterns
   - Research tech stack best practices
   - Identify potential issues

3. **Planning Phase**:
   - Generate structured Plan (Pydantic model)
   - Break down into actionable tasks
   - Identify dependencies

4. **QA Loop** (if enabled):
   - Call Critic agent for validation
   - Check architecture, packages, security
   - Iterate if QA score < 80
   - Maximum iterations: 3

5. **Output**:
   - Return Plan with todos, dependencies, tech_stack
   - Save to GAM memory for future reference
   - Include QAReport if QA was enabled

## Implementation

This command uses:
- **Agent Factory**: `app.server.agents.factory.create_agent()`
- **System Prompt**: `app.server.agents.prompts.PLANNER_SYSTEM_PROMPT`
- **GAM Integration**: `app.core.GAMMemoryManager`
- **Tools**: `gam_tool`, `planner_tool`, `package_tool`

## Output Format

```json
{
  "plan": {
    "feature_name": "User authentication system",
    "description": "JWT-based authentication with refresh tokens",
    "todos": [
      {"task": "Create User model", "priority": "high"},
      {"task": "Implement JWT token generation", "priority": "high"},
      {"task": "Create login endpoint", "priority": "medium"}
    ],
    "dependencies": ["fastapi", "pyjwt", "passlib"],
    "tech_stack": ["FastAPI", "PostgreSQL", "Redis"]
  },
  "qa_report": {
    "score": 85,
    "issues": [],
    "warnings": ["Consider rate limiting for login endpoint"]
  }
}
```

## Best Practices

- Always research from GAM memory first
- Enable QA for production features
- Validate all package dependencies
- Include security considerations
- Document assumptions in plan

## Related Commands

- `/execute-planning-skill` - Full planning workflow with orchestration
- `/create-critic-agent` - QA validation agent
- `/verify-packages` - Package validation tool
- `/gam-research` - Research from GAM memory

## Requirements

- Ollama server running (for agent execution)
- GAM memory initialized
- Java/JDK installed (for BM25 retriever, optional)
