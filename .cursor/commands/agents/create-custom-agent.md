# Create Custom Agent

## Overview

Factory for creating custom agents with user-defined prompts and tools. Provides flexibility for specialized tasks beyond standard Planner/Coder/Critic roles.

## Usage

Type `/create-custom-agent` followed by agent configuration.

## Parameters

- `agent_name`: Custom agent name (required)
- `system_prompt`: Custom system prompt (required)
- `tools`: List of tools to attach (optional)
- `model`: Ollama model to use (default: from router)

## Example Usage

### Research Agent

```
/create-custom-agent
Agent Name: research-specialist
System Prompt: |
  You are a research specialist focused on finding and synthesizing
  information from multiple sources. Always cite sources and provide
  comprehensive summaries.
Tools: gam_tool, tavily_search
Model: llama3.2:3b
```

### Documentation Agent

```
/create-custom-agent
Agent Name: doc-writer
System Prompt: |
  You are a technical documentation writer. Create clear, comprehensive
  documentation with examples and best practices.
Tools: gam_tool, coder_tool
```

### Refactoring Agent

```
/create-custom-agent
Agent Name: refactoring-expert
System Prompt: |
  You are a refactoring expert. Identify code smells, suggest improvements,
  and maintain backward compatibility.
Tools: coder_tool, gam_tool, package_tool
Model: qwen2.5-coder:14b
```

## Workflow

1. **Validate Configuration**:
   - Check agent_name is unique
   - Validate system_prompt is provided
   - Verify tools exist

2. **Create Agent**:
   - Call `app.server.agents.factory.create_agent("custom")`
   - Inject custom system_prompt
   - Attach specified tools

3. **Model Selection**:
   - Use specified model or route via `agents.router`
   - Validate model is available in Ollama

4. **Tool Attachment**:
   - Attach requested tools from `app.server.tools/`
   - Validate tool compatibility

5. **Caching** (optional):
   - Cache agent instance in `agent_service`
   - Reuse for similar tasks

6. **Output**:
   - Return agent instance
   - Provide usage instructions

## Implementation

This command uses:
- **Agent Factory**: `app.server.agents.factory.create_agent()`
- **Model Router**: `app.server.agents.router.route_model()`
- **Agent Service**: `app.server.services.agent_service`
- **Available Tools**: All tools from `app.server.tools/`

## Available Tools

- `gam_tool` - GAM memory operations
- `coder_tool` - Code generation and validation
- `planner_tool` - Planning and task breakdown
- `package_tool` - Package verification
- `computer_tool` - Browser automation
- `task_tool` - Background task execution
- `thinking_tool` - Explicit reasoning

## Output Format

```json
{
  "agent": {
    "name": "research-specialist",
    "model": "llama3.2:3b",
    "tools": ["gam_tool", "tavily_search"],
    "cached": true
  },
  "usage": "Agent ready for task execution",
  "example": "agent.execute('Research FastAPI best practices')"
}
```

## Best Practices

- Use descriptive agent names
- Provide clear, specific system prompts
- Attach only necessary tools
- Choose appropriate model for task
- Cache agents for repeated use
- Test with simple tasks first

## Model Selection Guide

| Task Type | Recommended Model | Reason |
|-----------|------------------|--------|
| Planning | llama3.2:3b | Fast, good reasoning |
| Coding | qwen2.5-coder:14b | Code-specialized |
| Research | llama3.2:3b | Fast, comprehensive |
| QA/Critic | qwen2.5:14b | Detailed analysis |
| Custom | User choice | Task-dependent |

## Related Commands

- `/create-planner-agent` - Standard planning agent
- `/create-coder-agent` - Standard coding agent
- `/create-critic-agent` - Standard QA agent
- `/manage-agent-cache` - Agent caching service

## Requirements

- Ollama server running
- Specified model available in Ollama
- Requested tools exist in `app.server.tools/`
