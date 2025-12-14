# Orchestrator: Execute Task

## Overview

Execute task with action mode. This command invokes the `execute_task()` function from `app/server/orchestrator.py` to execute tasks with specific action modes (research, plan, code, execute).

## Usage

Type `/orchestrator-execute-task` followed by the task and action.

## Parameters

- `task`: Task description (required)
- `action`: Action mode (research, plan, code, execute) (default: "execute")
- `language`: Programming language (default: "python")
- `context`: Additional context (optional)

## Example Usage

### Research Mode

```
/orchestrator-execute-task
Task: Microservices architecture patterns
Action: research
```

### Plan Mode

```
/orchestrator-execute-task
Task: User authentication system
Action: plan
```

### Code Mode

```
/orchestrator-execute-task
Task: Implement JWT authentication middleware
Action: code
Language: python
```

### Execute Mode (Full Workflow)

```
/orchestrator-execute-task
Task: Add user profile management
Action: execute
```

## Action Modes

### Research

Perform research and create comprehensive findings.

**Workflow**:
1. Research topic using web search
2. Query GAM for existing knowledge
3. Synthesize findings
4. Save to GAM

**Returns**:
```json
{
    "task": "Microservices architecture patterns",
    "action": "research",
    "result": {
        "key_findings": [...],
        "best_practices": [...],
        "sources": [...]
    },
    "latency_ms": 5678
}
```

### Plan

Create implementation plan with QA validation.

**Workflow**:
1. Query GAM for context
2. Create structured plan
3. Run QA/Critic validation
4. Refine if needed

**Returns**:
```json
{
    "task": "User authentication system",
    "action": "plan",
    "plan": {
        "overview": "...",
        "todos": [...],
        "dependencies": {...},
        "risks": [...]
    },
    "latency_ms": 3456
}
```

### Code

Generate and implement code with linting.

**Workflow**:
1. Load context from GAM
2. Generate code
3. Run linting
4. Auto-fix errors
5. Save files

**Returns**:
```json
{
    "task": "Implement JWT authentication middleware",
    "action": "code",
    "result": {
        "files_created": [...],
        "files_modified": [...],
        "linting_results": {...},
        "test_results": {...}
    },
    "latency_ms": 8901
}
```

### Execute

Run complete workflow (plan + implement + review).

**Workflow**:
1. Planning phase
2. Implementation phase
3. Review phase
4. Create PR

**Returns**:
```json
{
    "task": "Add user profile management",
    "action": "execute",
    "workflow_id": "workflow-abc123",
    "steps_completed": ["planning", "implementation", "review"],
    "latency_ms": 45678
}
```

## Orchestrator Logic

### Routing

```python
from app.server.orchestrator import execute_task
from app.server.protocols.actions import ActionStep

# Research mode
result = await execute_task(
    task="Microservices patterns",
    action=ActionStep.RESEARCH
)

# Plan mode
result = await execute_task(
    task="User authentication",
    action=ActionStep.PLAN
)

# Code mode
result = await execute_task(
    task="Implement JWT middleware",
    action=ActionStep.CODE,
    language="python"
)

# Execute mode (full workflow)
result = await execute_task(
    task="Add user profiles",
    action=ActionStep.EXECUTE
)
```

## Best Practices

- Use research mode for unfamiliar topics
- Use plan mode before implementation
- Use code mode for specific implementations
- Use execute mode for complete features
- Provide clear task descriptions
- Include relevant context

## Integration

- Routes to appropriate skills
- Manages workflow state
- Coordinates between layers
- Thin routing layer

## Related Commands

- `/run-agent-task` - Similar task execution
- `/execute-workflow` - Full workflow execution
- `/skill-planning` - Planning skill
- `/skill-implementation` - Implementation skill

## Source

- **File**: `app/server/orchestrator.py`
- **Function**: `execute_task()`
- **Layer**: Orchestrator (Router)
