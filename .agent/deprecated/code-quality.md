---
description: Improve code quality using DeepAgents for analysis
---

# Code Quality Workflow

Use DeepAgents to create specialized analysis agents for code review.

## Available Tools

The `deepagents` MCP server provides:

- **`create_agent(agent_type, config)`** - Create specialized agent
- **`run_agent(agent_id, task, context)`** - Execute agent task
- **`list_agents()`** - View active agents
- **`get_agent_status(agent_id)`** - Check agent status
- **`delete_agent(agent_id)`** - Cleanup agent

## Agent Types

### SOTA Researcher Agent

```
create_agent(agent_type="sota-researcher")
run_agent(agent_id, task="Research best practices for X")
```

## Workflow Example

1. **Create Agent**
   ```
   Use create_agent with agent_type="sota-researcher"
   ```

2. **Run Analysis**
   ```
   Use run_agent with task="Analyze patterns in authentication module"
   ```

3. **Cleanup**
   ```
   Use delete_agent to remove when done
   ```

## When to Use

- Before major refactoring
- After adding new features
- Preparing for code review
- Researching implementation approaches

## Token Efficiency

- Create agents once, reuse for multiple tasks
- Delete agents when done to free resources
- Use specific task descriptions for focused analysis
