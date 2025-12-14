# Workflow Orchestration

## Overview

Execute complete workflows with streaming progress updates and checkpoint management. This is the core orchestration command that coordinates planning, implementation, and QA phases with real-time feedback.

## Usage

Type `/workflow-orchestration` followed by your workflow request.

## Parameters

- `feature_name`: Feature to implement (required)
- `workflow_id`: Optional workflow ID for resuming (default: auto-generated)
- `mode`: Execution mode (default: full)
  - `full`: Complete workflow (planning + implementation + QA)
  - `planning_only`: Only execute planning phase
  - `implementation_only`: Skip planning, go straight to implementation
- `stream`: Enable streaming progress (default: true)
- `save_checkpoints`: Save workflow state for resumability (default: true)

## Example Usage

### Full Workflow with Streaming

```
/workflow-orchestration
Feature: User authentication system with JWT tokens
Mode: full
Stream: true
```

### Resume from Checkpoint

```
/workflow-orchestration
Feature: User authentication system
Workflow ID: workflow-a3f8b2c1
Mode: implementation_only
```

### Planning Only (Fast Validation)

```
/workflow-orchestration
Feature: Add rate limiting to API endpoints
Mode: planning_only
Stream: true
```

## Workflow

1. **Context Check**:
   - Call `context_manager.get_token_count()` to verify budget
   - If usage > 80%, trigger compression before starting
   - Stream status: `"Context budget: {used}/{max} tokens ({percent}%)"`

2. **Planning Phase** (if mode = full or planning_only):
   - Stream: `"🔍 Planning phase started"`
   - Initialize GAM memory: `gam = GAMMemoryManager()`
   - Execute planning: `plan = await execute_planning(feature_name, gam_memory=gam)`
   - Create checkpoint: `WorkflowCheckpoint(step="planning", state="completed", data=plan.model_dump())`
   - Stream: `"✅ Planning completed: {len(plan.todos)} tasks identified"`
   - **QA Loop**: Auto-validate plan with critic agent
     - If validation fails, stream errors and retry (max 2 attempts)

3. **Implementation Phase** (if mode = full or implementation_only):
   - Stream: `"🔨 Implementation phase started"`
   - For each task in plan:
     - Stream: `"⚙️ Implementing task {i}/{total}: {task.title}"`
     - Call `generate_and_implement(prompt=task.description, language=task.language)`
     - Stream code chunks as they arrive
     - Create checkpoint after each task completion
   - Stream: `"✅ Implementation completed"`

4. **State Management**:
   - Save workflow state: `state_service.save_state(workflow_id, checkpoints)`
   - Enable resumability from any checkpoint
   - Stream final status: `"Workflow {workflow_id} completed in {latency_ms}ms"`

5. **Error Handling**:
   - On failure, save error checkpoint
   - Stream error details with actionable feedback
   - Provide resume command for retry

## Streaming Output Format

```
🚀 Starting workflow for 'User authentication system'
📊 Context budget: 45000/128000 tokens (35%)

🔍 Planning phase started
  ⚙️ Researching best practices...
  ⚙️ Generating architecture plan...
✅ Planning completed: 5 tasks identified

🔨 Implementation phase started
  ⚙️ Implementing task 1/5: Create User model
    [streaming code output...]
  ✅ Task 1 complete
  ⚙️ Implementing task 2/5: Add JWT authentication
    [streaming code output...]
  ✅ Task 2 complete
  ...
✅ Implementation completed

🎉 Workflow workflow-a3f8b2c1 completed in 45230ms
```

## Best Practices

- Use `full` mode for new features requiring planning
- Use `implementation_only` when you have a clear plan
- Use `planning_only` to validate architecture before coding
- Monitor streaming output for early error detection
- Save workflow_id for resuming long-running tasks
- Enable checkpoints for complex multi-step workflows

## Integration Points

**Calls:**
- `app/server/orchestrator.py::execute_workflow_streaming()`
- `app/server/skills/planning.py::execute_planning()`
- `app/server/skills/implementation.py::generate_and_implement()`
- `app/server/services/state_service.py::get_or_create_state()`
- `app/server/services/context_service.py::ContextManager`

**Used By:**
- `/run-agent-task` - Delegates to workflow orchestration
- `/batch-implement` - Parallel workflow execution
- `/research-memorize-generate` - Full research + implementation flow

## Related Commands

- `/task-execution` - Single task execution without full workflow
- `/generate-code-streaming` - Direct code generation
- `/validate-architecture` - Pre-workflow validation
- `/smart-context` - Context optimization before workflow
