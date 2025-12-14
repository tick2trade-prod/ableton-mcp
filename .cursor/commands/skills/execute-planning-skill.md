# Execute Planning Skill

## Overview

Execute the complete planning workflow: Research → Plan → QA loop. Orchestrates Planner and Critic agents to generate validated implementation plans.

## Usage

Type `/execute-planning-skill` followed by feature description.

## Parameters

- `feature`: Feature description (required)
- `feature_name`: Optional alias used when requests already include field name
- `tech_stack`: Technologies to use (optional)
- `use_qa`: Enable QA feedback loop (default: true)
- `max_iterations`: Maximum QA iterations (default: 3)
- `min_score`: Minimum QA score to pass (default: 80)
- `gam_context`: Automatically load GAM memory snippets (default: true)
- `context_query`: Specific GAM search query (optional)
- `include_docs`: Include documentation updates in plan (default: true)
- `priority`: Priority level (low, medium, high, critical) (default: "medium")

## Example Usage

### Standard Planning with QA

```
/execute-planning-skill
Feature: User authentication system with JWT tokens and refresh tokens
Tech Stack: FastAPI, PostgreSQL, Redis
Use QA: true
Max Iterations: 3
Min Score: 80
```

### Quick Planning (No QA)

```
/execute-planning-skill
Feature: Add logging to existing endpoints
Use QA: false
```

### Strict Planning

```
/execute-planning-skill
Feature: Microservices architecture for blog platform
Tech Stack: FastAPI, PostgreSQL, RabbitMQ, Redis
Use QA: true
Min Score: 90
Max Iterations: 5
Priority: critical
Include Docs: true
Context Query: microservices auth patterns
```

## Context Options

1. **GAM Context Loading**
   - When `gam_context` is true, query GAM for similar features
   - Use `context_query` to force specific lookups
   - Attach retrieved snippets to the planning prompt
2. **Documentation Planning**
   - If `include_docs` is true, add documentation tasks to the plan
   - Tag docs/tickets that must be updated
3. **Priority Handling**
   - `priority` influences task ordering and QA strictness (critical > high > medium > low)
   - Critical priorities automatically bump `min_score` to at least 85

## Workflow

1. **Research Phase**:
   - Call `/gam-research` for relevant patterns
   - Research tech stack best practices
   - Query for known issues
   - Gather context from GAM memory

2. **Planning Phase**:
   - Call `/create-planner-agent`
   - Generate structured Plan (Pydantic model)
   - Break down into actionable tasks
   - Identify dependencies
   - Estimate complexity

3. **Package Validation**:
   - Extract dependencies from plan
   - Call `/verify-packages`
   - **HALT** if hallucinated packages found
   - Suggest alternatives

4. **QA Loop** (if enabled):
   - Call `/create-critic-agent`
   - Validate architecture, security, performance
   - Calculate QA score (0-100)
   - If score < min_score:
     - Iterate with Planner agent
     - Apply suggested fixes
     - Re-validate
   - Maximum iterations: 3 (configurable)

5. **Finalization**:
   - Save validated plan to GAM memory
   - Generate implementation checklist
   - Provide next steps

6. **Output**:
   - Return Plan + QAReport
   - Include latency metrics
   - Save checkpoint to state service

## Implementation

This command uses:
- **Planning Skill**: `app.server.skills.planning.execute_planning()`
- **Planner Agent**: `app.server.agents.factory.create_agent("planner")`
- **Critic Agent**: `app.server.agents.factory.create_agent("critic")`
- **GAM Integration**: `app.core.GAMMemoryManager`
- **State Management**: `app.server.services.state_service`

## Output Format

```json
{
  "plan": {
    "feature_name": "User authentication system",
    "description": "JWT-based authentication with refresh tokens",
    "todos": [
      {
        "task": "Create User model with SQLAlchemy",
        "priority": "high",
        "estimated_time": "2h",
        "dependencies": []
      },
      {
        "task": "Implement JWT token generation and validation",
        "priority": "high",
        "estimated_time": "3h",
        "dependencies": ["User model"]
      },
      {
        "task": "Create login and refresh endpoints",
        "priority": "medium",
        "estimated_time": "2h",
        "dependencies": ["JWT implementation"]
      }
    ],
    "dependencies": ["fastapi", "pyjwt", "passlib", "sqlalchemy"],
    "tech_stack": ["FastAPI", "PostgreSQL", "Redis"],
    "complexity": "medium"
  },
  "qa_report": {
    "score": 85,
    "iterations": 2,
    "critical_issues": [],
    "warnings": [
      "Consider rate limiting for login endpoint"
    ],
    "suggestions": [
      "Add password strength validation",
      "Implement account lockout after failed attempts"
    ],
    "passed": true
  },
  "metrics": {
    "latency_ms": 5420,
    "research_time_ms": 850,
    "planning_time_ms": 3200,
    "qa_time_ms": 1370
  }
}
```

## QA Feedback Loop

```
Iteration 1: Plan → Critic → Score 65 (< 80) → Revise
Iteration 2: Plan → Critic → Score 82 (>= 80) → Pass ✓
```

## Best Practices

- Always enable QA for production features
- Set appropriate min_score (70-90)
- Research from GAM memory first
- Validate all package dependencies
- Save validated plans to memory
- Use strict mode for critical features
- Monitor iteration count

## Related Commands

- `/create-planner-agent` - Standalone planning agent
- `/create-critic-agent` - Standalone QA agent
- `/verify-packages` - Package validation
- `/gam-research` - Memory research
- `/execute-implementation-skill` - Next step after planning

## Requirements

- Ollama server running
- GAM memory initialized
- Internet connection (for package validation)
- State service configured
