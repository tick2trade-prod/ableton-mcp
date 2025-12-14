# Workflow Skills Commands Registry

**Index Range**: 2000-2999
**Category**: Skills (THE "WHAT")
**Purpose**: High-level workflow orchestration and capabilities

---

## Overview

Workflow skills commands orchestrate multiple agents and tools to execute complex, multi-step workflows. Each skill represents a high-level capability that combines agents, tools, and business logic.

---

## Skill Commands

### 2001: Execute Planning Skill

**Command**: `/execute-planning-skill`
**File**: `.cursor/commands/app/skills/execute-planning-skill.md`
**Purpose**: Research → Plan → QA loop workflow
**Status**: ✅ Active

**Key Features**:
- GAM memory research
- Structured plan generation
- QA feedback loop (Critic agent)
- Package validation
- Iterative refinement (max 3 iterations)

**Agents Used**:
- Planner agent (planning)
- Critic agent (QA validation)

**Tools Used**:
- `gam_tool` - Memory research
- `package_tool` - Dependency validation
- `planner_tool` - Planning workflows

**Related**: `/create-planner-agent`, `/create-critic-agent`, `/execute-implementation-skill`

---

### 2002: Execute Implementation Skill

**Command**: `/execute-implementation-skill`
**File**: `.cursor/commands/app/skills/execute-implementation-skill.md`
**Purpose**: Code generation + testing + validation workflow
**Status**: ✅ Active

**Key Features**:
- Context-aware code generation
- Automatic Ruff + Mypy validation
- Test generation (pytest)
- File writing with auto-fix
- Pattern memorization

**Agents Used**:
- Coder agent (code generation)

**Tools Used**:
- `coder_tool` - Code generation and validation
- `gam_tool` - Pattern research
- `package_tool` - Dependency verification

**Related**: `/create-coder-agent`, `/lint-code`, `/execute-review-skill`

---

### 2003: Execute Review Skill

**Command**: `/execute-review-skill`
**File**: `.cursor/commands/app/skills/execute-review-skill.md`
**Purpose**: Code review + PR creation + validation workflow
**Status**: ✅ Active

**Key Features**:
- Comprehensive QA review
- Test execution
- PR creation (GitHub CLI)
- Change detection
- Quality scoring

**Agents Used**:
- Critic agent (QA review)

**Tools Used**:
- `gam_tool` - Known issues research
- Git tools - Change detection
- GitHub CLI - PR creation

**Related**: `/create-critic-agent`, `/execute-qa-skill`, `/workflow-pr-create`

---

### 2004: Execute Batch Skill

**Command**: `/execute-batch-skill`
**File**: `.cursor/commands/app/skills/execute-batch-skill.md`
**Purpose**: Parallel task execution (5-20x speedup)
**Status**: ✅ Active

**Key Features**:
- Parallel code generation
- Task decomposition
- Async execution (asyncio.gather)
- Programmatic file writing
- Integration testing

**Agents Used**:
- Multiple Coder agents (parallel)

**Tools Used**:
- `coder_tool` - Code generation
- `task_tool` - Background execution
- Dramatiq - Task queue

**Related**: `/batch-implement`, `/execute-implementation-skill`, `/queue-task`

---

### 2005: Execute QA Skill

**Command**: `/execute-qa-skill`
**File**: `.cursor/commands/app/skills/execute-qa-skill.md`
**Purpose**: Comprehensive QA validation workflow
**Status**: ✅ Active

**Key Features**:
- Architecture review
- Security validation
- Performance analysis
- Code quality check
- Package validation
- Multi-dimensional scoring

**Agents Used**:
- Critic agent (QA validation)

**Tools Used**:
- `gam_tool` - Known issues research
- `package_tool` - Dependency validation
- Plan critic - Architecture validation
- Code critic - Code validation

**Related**: `/create-critic-agent`, `/validate-architecture`, `/execute-review-skill`

---

## Skill Architecture

### Skill Composition Pattern

```python
# app/server/skills/ structure
skills/
├── planning.py          # Planning workflow
├── implementation.py    # Implementation workflow
├── review.py            # Review workflow
├── batch_execution.py   # Parallel execution
└── qa/                  # QA module
    ├── plan_critic.py   # Architecture validation
    └── code_critic.py   # Code validation
```

### Workflow Orchestration

Skills orchestrate agents and tools:

```python
# Example: Planning Skill
async def execute_planning_skill():
    # 1. Research from GAM
    context = await gam_research(query)

    # 2. Generate plan
    plan = await create_planner_agent(context)

    # 3. Validate packages
    validation = await verify_packages(plan.dependencies)

    # 4. QA loop
    for i in range(max_iterations):
        qa_report = await create_critic_agent(plan)
        if qa_report.score >= min_score:
            break
        plan = await revise_plan(plan, qa_report)

    return plan, qa_report
```

---

## Implementation Details

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Planning Skill | `app/server/skills/planning.py` | Research + Plan + QA |
| Implementation Skill | `app/server/skills/implementation.py` | Code + Tests + Validation |
| Review Skill | `app/server/skills/review.py` | QA + PR creation |
| Batch Skill | `app/server/skills/batch_execution.py` | Parallel execution |
| QA Skill | `app/server/skills/qa/` | Comprehensive validation |

### State Management

Skills use `app.server.services.state_service` for:
- Workflow checkpoints
- Progress tracking
- Error recovery
- Result caching

### Streaming Support

Skills support streaming via `orchestrator.py`:
- Real-time progress updates
- Token-by-token streaming
- Error streaming
- Completion events

---

## Usage Patterns

### Sequential Workflow

```
1. /execute-planning-skill → Generate validated plan
2. /execute-implementation-skill → Implement plan
3. /execute-review-skill → Review and create PR
```

### Parallel Workflow

```
/execute-batch-skill
  → Multiple independent tasks in parallel
  → 5-20x speedup
```

### QA Feedback Loop

```
/execute-planning-skill (use_qa=true)
  → Plan → Critic → Score 65 → Revise
  → Plan → Critic → Score 82 → Pass ✓
```

---

## Best Practices

1. **Use Skills for Complex Workflows**: Don't call agents directly for multi-step tasks
2. **Enable QA Loops**: Set `use_qa=true` for production features
3. **Validate Early**: Skills include package validation by default
4. **Monitor Progress**: Use streaming for long-running skills
5. **Save State**: Skills save checkpoints automatically
6. **Batch Independent Tasks**: Use batch skill for 5-20x speedup
7. **Review Before Merge**: Always run review skill before PR

---

## Performance Characteristics

| Skill | Latency | Complexity | Use Case |
|-------|---------|------------|----------|
| Planning | 3-5s | Medium | Feature planning |
| Implementation | 5-10s | High | Code generation |
| Review | 2-4s | Medium | QA validation |
| Batch | 3-5s | High | Parallel generation |
| QA | 2-4s | Medium | Comprehensive check |

---

## Integration Points

### With Agents (1000 Registry)

Skills use agents from agent registry:
- Planner agent (1001)
- Coder agent (1002)
- Critic agent (1003)

### With Tools (3000 Registry)

Skills use tools from tool registry:
- GAM operations (3001, 3002)
- Package validation (3003)
- Code linting (3004)
- Background tasks (3006, 3007)

### With Orchestrator

Skills are called by `app.server.orchestrator.py`:
- `execute_task()` - Synchronous execution
- `execute_workflow()` - Full workflow
- `execute_workflow_streaming()` - Streaming workflow

---

## Related Registries

- **1000: Agents Registry** - Agents used by skills
- **3000: Tools Registry** - Tools used by skills
- **300: Main Command Index** - All commands

---

## Next Steps

- [ ] Add skill performance metrics
- [ ] Implement skill caching
- [ ] Add skill composition patterns
- [ ] Create skill templates
- [ ] Add skill dependency graph

---

**Last Updated**: 2024-12-04
**Total Commands**: 5
**Status**: Phase 2 Complete ✅
