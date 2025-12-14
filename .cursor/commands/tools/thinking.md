# Tool: Thinking

## Overview

Explicit reasoning before action. This command invokes the thinking tool from `app/server/tools/thinking_tool.py` to perform step-by-step reasoning before taking actions, improving decision quality.

## Usage

Type `/tool-thinking` followed by the problem or decision.

## Parameters

- `problem`: Problem or decision to reason about (required)
- `context`: Additional context (optional)
- `thinking_steps`: Number of reasoning steps (default: 5)
- `save_to_gam`: Save reasoning to GAM (default: true)
- `structured_output`: Request structured reasoning (default: false)

## Example Usage

### Reason About Architecture

```
/tool-thinking
Problem: Should we use microservices or monolith for this project?
Context: |
  - Team size: 5 developers
  - Expected users: 10K initially, 100K in 6 months
  - Budget: Limited
  - Timeline: 3 months to MVP
Thinking Steps: 7
```

### Debug Complex Issue

```
/tool-thinking
Problem: Why is the async function causing race conditions?
Context: |
  - Using FastAPI with async endpoints
  - Shared state between requests
  - Intermittent failures under load
```

### Plan Implementation

```
/tool-thinking
Problem: How should I implement JWT refresh tokens?
Context: |
  - Using FastAPI and Redis
  - Need to support token rotation
  - Security is critical
Thinking Steps: 5
```

## Workflow

1. **Problem Analysis**:
   - Parse problem statement
   - Identify key constraints
   - Gather relevant context

2. **Reasoning Steps**:
   - Step 1: Understand requirements
   - Step 2: Consider alternatives
   - Step 3: Evaluate tradeoffs
   - Step 4: Identify risks
   - Step 5: Recommend solution

3. **Context Integration**:
   - Query GAM for similar problems
   - Retrieve best practices
   - Consider project constraints

4. **Decision Making**:
   - Synthesize reasoning
   - Make recommendation
   - Provide justification

5. **Save to GAM** (if enabled):
   - Store reasoning process
   - Tag with problem type
   - Link to related entities

## Output Format

```json
{
  "problem": "Should we use microservices or monolith for this project?",
  "context": {
    "team_size": 5,
    "expected_users": "10K → 100K",
    "budget": "limited",
    "timeline": "3 months"
  },
  "reasoning_steps": [
    {
      "step": 1,
      "thought": "Understand requirements",
      "analysis": "Small team (5 devs), tight timeline (3 months), limited budget, need to scale 10x in 6 months. MVP is priority."
    },
    {
      "step": 2,
      "thought": "Consider alternatives",
      "analysis": "Option A: Microservices - Better scalability, more complexity. Option B: Monolith - Faster development, simpler deployment."
    },
    {
      "step": 3,
      "thought": "Evaluate tradeoffs",
      "analysis": "Microservices: +Scalability, +Flexibility, -Complexity, -Time. Monolith: +Speed, +Simplicity, -Scalability (initially), +Can refactor later."
    },
    {
      "step": 4,
      "thought": "Identify risks",
      "analysis": "Microservices risk: Won't finish MVP in 3 months. Monolith risk: May struggle to scale to 100K users."
    },
    {
      "step": 5,
      "thought": "Consider hybrid approach",
      "analysis": "Start with modular monolith. Design with clear boundaries. Extract services later if needed."
    },
    {
      "step": 6,
      "thought": "Validate against constraints",
      "analysis": "Modular monolith fits: Small team can manage, fast development, can scale to 100K with optimization, can extract services later."
    },
    {
      "step": 7,
      "thought": "Make recommendation",
      "analysis": "Recommend modular monolith with clear service boundaries. Plan for extraction if scaling requires it."
    }
  ],
  "recommendation": {
    "decision": "Use modular monolith architecture",
    "rationale": "Best balance of speed, simplicity, and future scalability given constraints",
    "implementation": [
      "Design with clear module boundaries",
      "Use dependency injection for loose coupling",
      "Implement async for I/O operations",
      "Plan database schema for future sharding",
      "Monitor performance and scale horizontally first"
    ],
    "risks": [
      "May need to extract services if scaling beyond 100K",
      "Requires discipline to maintain module boundaries"
    ],
    "mitigation": [
      "Regular architecture reviews",
      "Automated testing of module boundaries",
      "Performance monitoring and optimization"
    ]
  },
  "confidence": 0.85,
  "gam_id": "reasoning-architecture-monolith-vs-microservices"
}
```

## Thinking Patterns

### Problem-Solving Pattern

1. Understand the problem
2. Identify constraints
3. Generate alternatives
4. Evaluate options
5. Make decision

### Debugging Pattern

1. Reproduce the issue
2. Identify symptoms
3. Form hypotheses
4. Test hypotheses
5. Find root cause

### Design Pattern

1. Understand requirements
2. Consider patterns
3. Evaluate tradeoffs
4. Choose approach
5. Plan implementation

## Best Practices

- Provide clear problem statements
- Include relevant context
- Use appropriate thinking steps
- Save valuable reasoning to GAM
- Review reasoning before acting
- Iterate on complex problems

## Integration

- Used by all agent commands internally
- Improves decision quality
- Provides audit trail
- Enables learning from past decisions

## Related Commands

- `/agent-planner` - Uses thinking for planning
- `/agent-critic` - Uses thinking for review
- `/deep-research` - Uses thinking for research
- `/tool-gam` - Stores reasoning in memory

## Source

- **File**: `app/server/tools/thinking_tool.py`
- **Function**: `explicit_reasoning()`, `structured_thinking()`
- **Layer**: Tools (HOW)
