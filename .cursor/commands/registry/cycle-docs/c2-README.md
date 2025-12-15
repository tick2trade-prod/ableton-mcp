# C2 Commands: Core Orchestration & Agent Management

## Overview

This directory contains the core commands decomposed from `app/server/` core logic files. These commands provide the foundational building blocks for workflow orchestration, task execution, agent management, quality assurance, and context optimization.

## Commands

### Phase 1: Core Workflow (Immediate Priority)

#### 1. `/workflow-orchestration` ⭐⭐⭐⭐⭐
**File**: `workflow-orchestration.md`

Execute complete workflows with streaming progress updates and checkpoint management.

**Key Features**:
- Streaming progress updates
- Checkpoint-based resumability
- Multi-phase execution (planning + implementation + QA)
- Context-aware execution
- State management

**Use Cases**:
- Full feature implementation
- Complex multi-step workflows
- Long-running tasks with resumability

**Extracted From**:
- `app/server/orchestrator.py::execute_workflow_streaming()`
- `app/server/orchestrator.py::execute_workflow()`

---

#### 2. `/task-execution` ⭐⭐⭐⭐
**File**: `task-execution.md`

Execute tasks with specific action modes (research, plan, code, execute) and optional background execution.

**Key Features**:
- Action-based routing (research, plan, code, execute)
- Background task queue with Dramatiq
- Priority-based execution
- Performance tracking
- Latency measurement

**Use Cases**:
- Single-action tasks
- Background job processing
- Quick code generation
- Research and planning

**Extracted From**:
- `app/server/orchestrator.py::execute_task()`
- `app/server/orchestrator.py::execute_task_background()`

---

### Phase 2: Agent Management (Short-term Priority)

#### 3. `/agent-factory` ⭐⭐⭐⭐
**File**: `agent-factory.md`

Create specialized agents (planner, coder, critic, researcher) with intelligent model routing and tool binding.

**Key Features**:
- Agent specialization (planner, coder, critic, researcher)
- Intelligent model routing (Ollama)
- System prompt management
- Tool binding and caching
- Performance optimization

**Use Cases**:
- Dynamic agent creation
- Model selection and routing
- Agent caching for performance
- Custom agent configuration

**Extracted From**:
- `app/server/agents/factory.py`
- `app/server/agents/router.py`
- `app/server/agents/prompts.py`

---

#### 4. `/qa-validation` ⭐⭐⭐
**File**: `qa-validation.md`

Run quality assurance checks on plans or code using the critic agent with multi-dimensional validation.

**Key Features**:
- Multi-dimensional validation (architecture, packages, syntax, security)
- Critic agent (Senior Architect)
- Package verification (prevent hallucinations)
- Auto-fix capabilities
- Structured feedback reports

**Use Cases**:
- Pre-commit validation
- Architecture review
- Security scanning
- Package verification
- Auto-fixing code issues

**Extracted From**:
- `app/server/skills/qa/plan_critic.py`
- `app/server/skills/qa/code_critic.py`
- `app/server/agents/critic.py`

---

### Phase 3: Context Management (Enhancement Priority)

#### 5. `/context-optimization` ⭐⭐⭐
**File**: `context-optimization.md`

Manage token budgets and compress conversation history to prevent context overflow.

**Key Features**:
- Token counting with tiktoken
- Automatic compression triggers
- Sliding window preservation
- GAM-based summarization
- Real-time budget tracking

**Use Cases**:
- Long conversation management
- Context overflow prevention
- Memory optimization
- Large refactoring tasks
- Token budget monitoring

**Extracted From**:
- `app/server/services/context_service.py`
- `app/core/gam_memory.py`

---

## Command Relationships

```
┌─────────────────────────────────────────────────────────┐
│                  /workflow-orchestration                │
│         (Core workflow with streaming & checkpoints)    │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│/task-execution│ │/agent-factory│ │/qa-validation│
│  (Routing)    │ │  (Agents)    │ │   (QA)       │
└──────────────┘ └──────────────┘ └──────────────┘
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
            ┌──────────────────┐
            │/context-optimization│
            │   (Token Mgmt)     │
            └──────────────────┘
```

## Integration with Existing Commands

### Commands That Use C2

- `/generate-code-streaming` → Uses `/task-execution` (action=code)
- `/deep-research` → Uses `/task-execution` (action=research)
- `/run-agent-task` → Uses `/workflow-orchestration`
- `/validate-architecture` → Uses `/qa-validation`
- `/smart-context` → Uses `/context-optimization`
- `/batch-implement` → Uses `/workflow-orchestration` (parallel)

### Commands That C2 Uses

- `/memorize-content` → Used by context optimization for summarization
- `/research-memory` → Used by task execution for context lookup
- `/optimize-imports` → Used by QA validation for syntax checks

## Comparison Matrix

| Command | Impact | Reusability | Complexity | Streaming | DDD Alignment |
|---------|--------|-------------|------------|-----------|---------------|
| `/workflow-orchestration` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Native | ✅ Perfect |
| `/task-execution` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⚠️ Partial | ✅ Good |
| `/agent-factory` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ No | ✅ Perfect |
| `/qa-validation` | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⚠️ Partial | ✅ Good |
| `/context-optimization` | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ No | ✅ Good |

## Implementation Priority

### Phase 1 (Immediate)
1. ✅ `/workflow-orchestration` - Core workflow execution
2. ✅ `/task-execution` - Task routing

### Phase 2 (Short-term)
3. ✅ `/agent-factory` - Agent specialization
4. ✅ `/qa-validation` - Quality control

### Phase 3 (Enhancement)
5. ✅ `/context-optimization` - Token management

## Architecture Alignment

All commands follow the DDD MCP Tools architecture:

```
app/server/                  # Infrastructure Layer (MCP Interface)
├── orchestrator.py          → /workflow-orchestration, /task-execution
├── agents/                  → /agent-factory
│   ├── factory.py
│   ├── router.py
│   └── prompts.py
├── skills/                  → /workflow-orchestration
│   ├── planning.py
│   ├── implementation.py
│   └── qa/                  → /qa-validation
│       ├── plan_critic.py
│       └── code_critic.py
└── services/                → /context-optimization
    ├── context_service.py
    └── agent_service.py
```

## Usage Examples

### Example 1: Full Feature Implementation

```bash
# Step 1: Create agents
/agent-factory
Agent Type: planner

/agent-factory
Agent Type: coder

# Step 2: Execute workflow
/workflow-orchestration
Feature: User authentication with JWT
Mode: full
Stream: true

# Step 3: Validate result
/qa-validation
Target: code
Content: @app/auth/
Dimensions: all
Auto Fix: true
```

### Example 2: Quick Code Generation

```bash
# Step 1: Check context
/context-optimization
Mode: check

# Step 2: Generate code
/task-execution
Task: Add logging to user service
Action: code
Language: python

# Step 3: Validate
/qa-validation
Target: code
Content: @app/services/user_service.py
Dimensions: [syntax, security]
```

### Example 3: Background Processing

```bash
# Queue long-running task
/task-execution
Task: Refactor entire database layer
Action: execute
Background: true
Priority: high

# Check status later
/task-status
Task ID: task-a3f8b2c1
```

## Best Practices

1. **Workflow Orchestration**:
   - Use for complex multi-step features
   - Enable streaming for real-time feedback
   - Save workflow_id for resumability

2. **Task Execution**:
   - Use `research` mode before implementation
   - Use `plan` mode to validate architecture
   - Use `code` mode for direct generation
   - Use `background=true` for tasks >60s

3. **Agent Factory**:
   - Let auto-selection choose models
   - Enable caching for performance
   - Use low temperature for deterministic tasks
   - Use high temperature for creative tasks

4. **QA Validation**:
   - Run before committing code
   - Enable `auto_fix` for quick fixes
   - Check all dimensions for production
   - Validate plans before implementation

5. **Context Optimization**:
   - Enable auto-optimization for long conversations
   - Use aggressive mode for large refactors
   - Monitor token usage before workflows
   - Preserve more messages for debugging

## Related Documentation

- `c2.md` - Original analysis and ranking
- `../generate-code-streaming.md` - Streaming code generation template
- `../workflow-pr-create.md` - PR creation workflow
- `../validate-architecture.md` - Architecture validation
- `../smart-context.md` - Enhanced context management

## Status

- ✅ All Phase 1, 2, and 3 commands implemented
- ✅ Following DDD MCP Tools architecture
- ✅ Streaming support where applicable
- ✅ Integration with existing commands
- ✅ Comprehensive documentation
