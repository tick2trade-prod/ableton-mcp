# Agent Factory

## Overview

Create specialized agents (planner, coder, critic, researcher) with appropriate prompts, tools, and model routing. Provides intelligent agent selection and caching for performance.

## Usage

Type `/agent-factory` followed by your agent configuration.

## Parameters

- `agent_type`: Agent type (required)
  - `planner`: Architecture and planning agent
  - `coder`: Code generation and implementation agent
  - `critic`: QA and validation agent (Senior Architect)
  - `researcher`: Research and information gathering agent
- `model`: Optional model override (default: auto-select)
  - `qwen2.5-coder:32b`: Best for coding tasks
  - `llama3.2:latest`: Best for planning/research
  - `deepseek-coder-v2:latest`: Alternative coder
- `temperature`: Creativity level 0.0-1.0 (default: auto-select per agent)
- `tools`: Additional tools to provide (default: auto-select per agent)
- `cache`: Enable agent caching (default: true)

## Example Usage

### Create Coder Agent

```
/agent-factory
Agent Type: coder
Model: qwen2.5-coder:32b
Temperature: 0.2
Tools: [coder_tool, gam_tool, package_tool]
```

### Create Critic Agent

```
/agent-factory
Agent Type: critic
Temperature: 0.1
Tools: [package_tool, gam_tool]
```

### Create Planner with Custom Model

```
/agent-factory
Agent Type: planner
Model: llama3.2:latest
Temperature: 0.7
Tools: [planner_tool, gam_tool, search_tool]
```

### Quick Agent (Auto-Config)

```
/agent-factory
Agent Type: researcher
```

## Workflow

1. **Agent Type Selection**:
   - Parse agent_type parameter
   - Load agent-specific configuration:
     - **Planner**: High-level architecture, planning prompts
     - **Coder**: Code generation, implementation prompts
     - **Critic**: QA validation, review prompts
     - **Researcher**: Information gathering, research prompts

2. **Model Routing**:
   - Auto-select best model for agent type:
     - `planner` → `llama3.2:latest` (reasoning)
     - `coder` → `qwen2.5-coder:32b` (code generation)
     - `critic` → `llama3.2:latest` (analysis)
     - `researcher` → `llama3.2:latest` (research)
   - Override with custom model if provided
   - Verify model availability: `ollama list`

3. **Prompt Loading**:
   - Load system prompts from `app/server/agents/prompts.py`:
     - `PLANNER_SYSTEM_PROMPT`: Architecture planning
     - `CODER_SYSTEM_PROMPT`: Code generation
     - `CRITIC_SYSTEM_PROMPT`: QA validation
     - `RESEARCHER_SYSTEM_PROMPT`: Research tasks
   - Include Extended Thinking blocks (`<thinking>`)
   - Add project context from GAM memory

4. **Tool Binding**:
   - Auto-attach tools based on agent type:
     - **Planner**: `planner_tool`, `gam_tool`, `search_tool`
     - **Coder**: `coder_tool`, `gam_tool`, `package_tool`, `thinking_tool`
     - **Critic**: `package_tool`, `gam_tool`, `search_tool`
     - **Researcher**: `search_tool`, `gam_tool`, `browser_tool`
   - Merge with custom tools if provided

5. **Agent Creation**:
   - Create agent instance: `agent = create_agent(agent_type, model, temperature, tools)`
   - Configure agent settings:
     - `max_tokens`: 4096 (coder), 2048 (others)
     - `top_p`: 0.9
     - `repeat_penalty`: 1.1
   - Return agent instance

6. **Caching** (if enabled):
   - Cache agent by key: `f"{agent_type}:{model}:{temperature}"`
   - TTL: 3600 seconds (1 hour)
   - Reuse cached agents for performance
   - Invalidate cache on model/prompt changes

## Agent Configurations

### Planner Agent

```python
{
    "agent_type": "planner",
    "model": "llama3.2:latest",
    "temperature": 0.7,
    "tools": ["planner_tool", "gam_tool", "search_tool"],
    "system_prompt": PLANNER_SYSTEM_PROMPT,
    "max_tokens": 2048,
    "use_thinking": True
}
```

### Coder Agent

```python
{
    "agent_type": "coder",
    "model": "qwen2.5-coder:32b",
    "temperature": 0.2,
    "tools": ["coder_tool", "gam_tool", "package_tool", "thinking_tool"],
    "system_prompt": CODER_SYSTEM_PROMPT,
    "max_tokens": 4096,
    "use_thinking": True
}
```

### Critic Agent

```python
{
    "agent_type": "critic",
    "model": "llama3.2:latest",
    "temperature": 0.1,
    "tools": ["package_tool", "gam_tool", "search_tool"],
    "system_prompt": CRITIC_SYSTEM_PROMPT,
    "max_tokens": 2048,
    "use_thinking": True
}
```

### Researcher Agent

```python
{
    "agent_type": "researcher",
    "model": "llama3.2:latest",
    "temperature": 0.5,
    "tools": ["search_tool", "gam_tool", "browser_tool"],
    "system_prompt": RESEARCHER_SYSTEM_PROMPT,
    "max_tokens": 2048,
    "use_thinking": False
}
```

## Best Practices

- Use `planner` for architecture and design decisions
- Use `coder` for implementation and code generation
- Use `critic` for QA validation and code review
- Use `researcher` for information gathering
- Enable caching for repeated agent creation
- Use low temperature (0.1-0.3) for deterministic tasks
- Use high temperature (0.6-0.8) for creative tasks
- Override model only when necessary
- Let auto-selection choose best model per agent

## Integration Points

**Calls:**
- `app/server/agents/factory.py::create_agent()`
- `app/server/agents/router.py::select_model()`
- `app/server/agents/prompts.py` (system prompts)
- `app/server/services/agent_service.py::get_or_create_agent()`
- `app/server/tools/` (tool bindings)

**Used By:**
- `/workflow-orchestration` - Creates planner + coder agents
- `/qa-validation` - Creates critic agent
- `/deep-research` - Creates researcher agent
- `/generate-code-streaming` - Creates coder agent

## Performance Metrics

```json
{
    "agent_type": "coder",
    "model": "qwen2.5-coder:32b",
    "creation_time_ms": 45,
    "cache_hit": true,
    "tools_loaded": 4,
    "prompt_tokens": 512
}
```

## Error Handling

### Model Not Available

```json
{
    "error": "Model not found",
    "model": "nonexistent-model:latest",
    "available_models": [
        "qwen2.5-coder:32b",
        "llama3.2:latest",
        "deepseek-coder-v2:latest"
    ],
    "suggestion": "Use qwen2.5-coder:32b for coding tasks"
}
```

### Invalid Agent Type

```json
{
    "error": "Invalid agent type",
    "provided": "invalid_agent",
    "valid_types": ["planner", "coder", "critic", "researcher"]
}
```

## Related Commands

- `/workflow-orchestration` - Uses planner + coder agents
- `/qa-validation` - Uses critic agent
- `/deep-research` - Uses researcher agent
- `/task-execution` - Creates agents based on action mode
