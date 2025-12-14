# Run Agent Task

## Overview

Run a DeepAgent task with GAM memory integration. The agent will use memory first, then execute the task.

## Usage

Type `/run-agent-task` followed by the task description and optional agent name.

## Parameters

- `task`: Task description (required)
- `agent_name`: Optional agent name (uses default if not specified)
- `use_cache`: Use Redis cache for repeated tasks (default: true)

## Example Usage

### Basic Task Execution

```
/run-agent-task
Task: Research FastAPI async patterns from memory first, then use Tavily to find latest best practices. Memorize findings and generate example code.
```

### Task with Specific Agent

```
/run-agent-task
Agent: autonomous-researcher
Task: Research package documentation for lancedb and create a usage example with caching.
```

### Task with Cache Disabled

```
/run-agent-task
Task: Generate unique code for authentication system
Use Cache: false
```

## Workflow

1. Agent checks GAM memory for relevant information (via `app.core.GAMMemoryManager`)
2. Agent executes task using available tools (via `app.orchestration.AgentTaskOrchestrator`)
3. Results are cached (if enabled) for faster future access
4. Metrics are tracked in MLflow (if available)

## Implementation

This command uses the `app.orchestration.AgentTaskOrchestrator` class from the refactored `app/` structure:
- Task orchestration: `app.orchestration.AgentTaskOrchestrator`
- Research integration: `app.research.AutonomousResearcher`
- Code generation: `app.generation.CodeGenerator`

## Best Practices

- Always start tasks with "Research from memory first"
- Use specific, actionable task descriptions
- Leverage caching for repeated tasks
- Monitor performance via MLflow metrics
