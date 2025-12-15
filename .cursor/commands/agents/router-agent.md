# Agent: Router

## Overview

Route to best Ollama model for task. This command uses the model router from `app/server/agents/router.py` to automatically select the most appropriate Ollama model based on task type, complexity, and requirements.

## Usage

Type `/agent-router` followed by your task description.

## Parameters

- `task_description`: Description of task (required)
- `task_type`: Type of task (planning, coding, review, research) (optional)
- `complexity`: Task complexity (low, medium, high) (optional)
- `language`: Programming language (optional)
- `prefer_speed`: Prioritize speed over quality (default: false)
- `require_reasoning`: Require reasoning capability (default: false)

## Example Usage

### Auto-Select for Planning

```
/agent-router
Task Description: Create architecture plan for microservices
Task Type: planning
Complexity: high
```

### Auto-Select for Coding

```
/agent-router
Task Description: Implement REST API endpoints
Task Type: coding
Language: python
Complexity: medium
```

### Speed-Optimized Selection

```
/agent-router
Task Description: Fix simple syntax error
Complexity: low
Prefer Speed: true
```

### Reasoning-Required Selection

```
/agent-router
Task Description: Debug complex async race condition
Require Reasoning: true
Complexity: high
```

## Workflow

1. **Task Analysis**:
   - Parse task description
   - Detect task type
   - Estimate complexity
   - Identify requirements

2. **Model Selection**:
   - Query available Ollama models
   - Score models by capability
   - Consider speed vs quality tradeoff
   - Check model availability

3. **Capability Matching**:
   - Code generation → qwen2.5-coder, deepseek-coder
   - Reasoning → qwen2.5, deepseek-r1
   - Speed → llama3.2, phi3
   - General → mistral, mixtral

4. **Fallback Logic**:
   - Primary model unavailable → fallback
   - Model too slow → faster alternative
   - Model insufficient → more capable option

## Model Selection Matrix

| Task Type | Complexity | Recommended Model | Fallback |
|-----------|-----------|------------------|----------|
| Planning | High | qwen2.5:32b | qwen2.5:14b |
| Planning | Medium | qwen2.5:14b | mistral:7b |
| Planning | Low | mistral:7b | llama3.2:3b |
| Coding | High | qwen2.5-coder:32b | deepseek-coder:33b |
| Coding | Medium | qwen2.5-coder:14b | qwen2.5-coder:7b |
| Coding | Low | qwen2.5-coder:7b | llama3.2:3b |
| Review | High | deepseek-r1:14b | qwen2.5:14b |
| Review | Medium | qwen2.5:14b | mistral:7b |
| Review | Low | mistral:7b | llama3.2:3b |
| Research | High | qwen2.5:32b | mixtral:8x7b |
| Research | Medium | qwen2.5:14b | mistral:7b |
| Research | Low | mistral:7b | llama3.2:3b |

## Output Format

```json
{
  "task_description": "Create architecture plan for microservices",
  "task_type": "planning",
  "complexity": "high",
  "selected_model": {
    "name": "qwen2.5:32b",
    "size": "32B parameters",
    "capabilities": ["planning", "reasoning", "architecture"],
    "speed": "slow",
    "quality": "excellent"
  },
  "fallback_models": [
    "qwen2.5:14b",
    "mistral:7b"
  ],
  "reasoning": "High complexity planning task requires strong reasoning and architecture knowledge. Qwen2.5:32b provides best quality for this use case.",
  "estimated_latency": "15-30 seconds",
  "confidence": 0.95
}
```

## Best Practices

- Let router auto-detect task type when possible
- Specify complexity for better selection
- Use prefer_speed for simple tasks
- Require reasoning for complex debugging
- Test selected model before production use
- Monitor model performance and adjust

## Integration

- Used by all agent commands internally
- Optimizes model selection automatically
- Supports fallback chains
- Integrates with Ollama API

## Related Commands

- `/agent-planner` - Uses router for planning
- `/agent-coder` - Uses router for coding
- `/agent-critic` - Uses router for review
- `/agent-structured` - Uses router for structured output

## Source

- **File**: `app/server/agents/router.py`
- **Function**: `select_model()`, `route_to_best_model()`
- **Layer**: Agents (WHO)
