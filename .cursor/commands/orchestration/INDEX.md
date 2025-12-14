# Orchestration Commands

Commands for orchestrating workflows, tasks, and background execution.

## Available Commands

### Workflow Orchestration
- **workflow-orchestration.md** - Complete workflow orchestration with streaming
- **execute-workflow.md** - Execute workflow by configuration
- **execute-streaming.md** - Execute workflow with progress streaming

### Task Execution
- **task-execution.md** - Action-based task routing (research, plan, code, execute)
- **execute-task.md** - Execute single task
- **execute-background.md** - Queue task for background execution

## Usage Pattern

```bash
/workflow-orchestration feature="User auth" mode="full" stream=true
/task-execution task="Create API endpoint" action="code" language="python"
/execute-background task="Run full test suite" queue="tests"
```

## Orchestration Flow

```
Workflow Orchestration:
  1. Context Check (token budget)
  2. Planning Phase (with streaming)
  3. Implementation Phase (with checkpoints)
  4. QA Loop (auto-validation)
  5. State Management (resumability)

Task Execution:
  1. Action Routing (by ActionStep enum)
  2. Skill Selection (research/plan/code/execute)
  3. Agent Creation (appropriate agent type)
  4. Tool Binding (required tools)
  5. Execution (with performance tracking)
```

## Action Modes

- **research** - Research and web search
- **plan** - Planning with GAM context
- **code** - Code generation
- **execute** - Full workflow execution

## Background Execution

Uses Dramatiq for:
- Long-running tasks
- Parallel batch operations
- Test suite execution
- Large-scale refactoring

## Related

- Workflows: `/workflows/INDEX.md`
- Skills: `/skills/INDEX.md`
- Services: `/services/INDEX.md`
