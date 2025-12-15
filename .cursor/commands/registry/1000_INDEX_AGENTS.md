# Agent Factory Commands Registry

**Index Range**: 1000-1999
**Category**: Agent Factories (THE "WHO")
**Purpose**: Create and configure agents with specific roles and capabilities

---

## Overview

Agent factory commands create specialized agents for different roles in the DDD MCP Tools architecture. Each agent has a distinct purpose, system prompt, and set of tools.

---

## Agent Commands

### 1001: Create Planner Agent

**Command**: `/create-planner-agent`
**File**: `.cursor/commands/app/agents/create-planner-agent.md`
**Purpose**: Create planning agent with research + QA loop
**Status**: ✅ Active

**Key Features**:
- Research from GAM memory
- Generate structured implementation plans
- QA feedback loop with Critic agent
- Package dependency validation
- Tech stack analysis

**Tools Used**:
- `gam_tool` - Memory operations
- `planner_tool` - Planning workflows
- `package_tool` - Package validation

**Related**: `/execute-planning-skill`, `/create-critic-agent`

---

### 1002: Create Coder Agent

**Command**: `/create-coder-agent`
**File**: `.cursor/commands/app/agents/create-coder-agent.md`
**Purpose**: Create coding agent with linting validation
**Status**: ✅ Active

**Key Features**:
- Code generation with best practices
- Automatic Ruff + Mypy validation
- Test generation (pytest)
- Type hints enforcement
- Pattern research from GAM

**Tools Used**:
- `coder_tool` - Code generation and validation
- `gam_tool` - Pattern research
- `package_tool` - Dependency verification

**Related**: `/execute-implementation-skill`, `/lint-code`

---

### 1003: Create Critic Agent

**Command**: `/create-critic-agent`
**File**: `.cursor/commands/app/agents/create-critic-agent.md`
**Purpose**: Create QA/Critic agent for architecture review
**Status**: ✅ Active

**Key Features**:
- Architecture validation
- Security vulnerability detection
- Performance issue identification
- Anti-pattern detection
- Package hallucination prevention
- Structured QAReport generation

**Tools Used**:
- `gam_tool` - Known issues research
- `package_tool` - Package validation

**Related**: `/execute-qa-skill`, `/validate-architecture`

---

### 1004: Create Custom Agent

**Command**: `/create-custom-agent`
**File**: `.cursor/commands/app/agents/create-custom-agent.md`
**Purpose**: Factory for custom agents with user-defined prompts
**Status**: ✅ Active

**Key Features**:
- Custom system prompts
- Flexible tool attachment
- Model selection (Ollama)
- Agent caching
- Specialized task support

**Tools Used**: User-configurable

**Related**: `/manage-agent-cache`, all agent commands

---

## Agent Architecture

### Agent Factory Pattern

```python
# app/server/agents/factory.py
def create_agent(agent_type: str, **kwargs) -> Agent:
    """Create agent with role-specific configuration."""
    if agent_type == "planner":
        return PlannerAgent(
            prompt=PLANNER_SYSTEM_PROMPT,
            tools=[gam_tool, planner_tool, package_tool]
        )
    # ... other agent types
```

### System Prompts

Located in `app/server/agents/prompts.py`:
- `PLANNER_SYSTEM_PROMPT` - Planning and research
- `CODER_SYSTEM_PROMPT` - Code generation
- `CRITIC_SYSTEM_PROMPT` - QA and validation

### Model Routing

Located in `app/server/agents/router.py`:
- Routes tasks to appropriate Ollama models
- Supports: llama3.2:3b, qwen2.5-coder:14b, qwen2.5:14b

---

## Implementation Details

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Agent Factory | `app/server/agents/factory.py` | Create agents |
| System Prompts | `app/server/agents/prompts.py` | Role definitions |
| Model Router | `app/server/agents/router.py` | Model selection |
| Critic Agent | `app/server/agents/critic.py` | QA specialist |

### GAM Integration

All agents use `app.core.GAMMemoryManager` for:
- Research from memory
- Pattern retrieval
- Context awareness
- Knowledge persistence

### Tool Integration

Agents access tools from `app/server/tools/`:
- `gam_tool.py` - Memory operations
- `coder_tool.py` - Code generation
- `planner_tool.py` - Planning workflows
- `package_tool.py` - Package validation

---

## Usage Patterns

### Sequential Agent Workflow

```
1. /create-planner-agent → Generate plan
2. /create-critic-agent → Validate plan
3. /create-planner-agent → Revise if needed (QA loop)
4. /create-coder-agent → Implement plan
5. /create-critic-agent → Validate code
```

### Parallel Agent Execution

```
/batch-implement uses multiple coder agents in parallel
→ 5-20x speedup for independent tasks
```

---

## Best Practices

1. **Always research first**: Use GAM memory before generation
2. **Enable QA loops**: Set `use_qa=true` for production
3. **Validate packages**: Run `/verify-packages` before implementation
4. **Choose right model**: Use router for optimal performance
5. **Cache agents**: Reuse agent instances for similar tasks
6. **Monitor metrics**: Track latency and success rates

---

## Related Registries

- **2000: Skills Registry** - Workflow orchestration using agents
- **3000: Tools Registry** - Tools available to agents
- **300: Main Command Index** - All commands

---

## Next Steps

- [ ] Add agent performance metrics
- [ ] Implement agent caching service
- [ ] Add custom agent templates
- [ ] Create agent composition patterns
- [ ] Add multi-agent orchestration

---

**Last Updated**: 2024-12-04
**Total Commands**: 4
**Status**: Phase 1 Complete ✅
