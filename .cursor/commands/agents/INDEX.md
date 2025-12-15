# Agent Commands (WHO Layer)

Commands for creating and managing specialized agents.

## Available Agents

### Core Agents
- **create-planner-agent.md** - Create planner agent for task breakdown and planning
- **create-coder-agent.md** - Create coder agent for implementation
- **create-critic-agent.md** - Create critic agent for QA and review
- **create-custom-agent.md** - Create custom agent with specific tools

### Specialized Agents
- **agent-factory.md** - Agent factory for dynamic agent creation
- **coder-agent.md** - Specialized coder agent configuration
- **critic-agent.md** - Advanced critic agent with QA scoring
- **planner-agent.md** - Planner agent with GAM + package validation
- **router-agent.md** - Model routing agent for optimal LLM selection
- **structured-agent.md** - Agent for structured JSON responses

### Execution
- **execute-agent.md** - Execute any agent by configuration

## Usage Pattern

```bash
/create-planner-agent task="Design authentication system"
/create-coder-agent task="Implement JWT middleware" language="python"
/create-critic-agent target="review plan"
```

## Agent Types

1. **Planner** - Research, planning, architecture design
2. **Coder** - Code generation, refactoring, implementation
3. **Critic** - QA validation, code review, security audit
4. **Router** - Model selection and routing
5. **Structured** - Structured output generation

## Related

- Skills (WHAT): `/skills/INDEX.md`
- Tools (HOW): `/tools/INDEX.md`
- Registry: `/registry/1000_INDEX_AGENTS.md`
