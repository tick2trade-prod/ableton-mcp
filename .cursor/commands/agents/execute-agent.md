# Exec: Agent

**Rank**: 5 - Hybrid Registry + Execution Commands

## Overview

Execute any agent from the 1000_INDEX_AGENTS registry by ID.

## Usage

```
/exec-agent agent_id="1001" params='{"feature": "User auth"}'
```

## Parameters

- `agent_id`: Agent ID from registry (required)
- `params`: Agent-specific parameters as JSON (required)

## Available Agents

See `.cursor/commands/app/registry/1000_INDEX_AGENTS.md`

## Implementation

```python
from app.server.agents.factory import create_agent

agent_config = get_agent_config(agent_id)
agent = create_agent(**agent_config)
result = await agent.run(**params)
```

## Output

```json
{"agent_id": "1001", "result": {...}}
```
