# Skill: Research and Plan

## Overview

Research topic and create comprehensive plan. This command invokes the `research_and_plan()` function from `app/server/skills/planning.py` to perform deep research and generate an actionable plan.

> **Layer**: WHAT (Skill Orchestration)

## Usage

Type `/skill-research-and-plan` followed by the topic.

## Parameters

- `topic`: Topic to research (required)
- `use_web_search`: Enable web search (default: true)
- `search_depth`: Search depth (shallow, medium, deep) (default: "medium")
- `max_sources`: Maximum sources to review (default: 10)
- `create_plan`: Generate plan after research (default: true)
- `save_to_gam`: Save results to GAM (default: true)

## Example Usage

### Deep Research with Plan

```
/skill-research-and-plan
Topic: Microservices architecture patterns
Use Web Search: true
Search Depth: deep
Max Sources: 15
Create Plan: true
```

### Quick Research (No Plan)

```
/skill-research-and-plan
Topic: Python async best practices
Search Depth: shallow
Max Sources: 5
Create Plan: false
```

### Research Existing Codebase

```
/skill-research-and-plan
Topic: Current authentication implementation
Use Web Search: false
Create Plan: true
```

## Workflow

1. **Research Phase**:
   - Query GAM for existing knowledge
   - Search web for latest information
   - Review documentation and examples
   - Gather best practices

2. **Analysis Phase**:
   - Synthesize research findings
   - Identify key patterns
   - Extract actionable insights
   - Note potential challenges

3. **Planning Phase** (if enabled):
   - Create structured plan
   - Break down into tasks
   - Identify dependencies
   - Estimate effort

4. **Save to GAM**:
   - Store research findings
   - Tag with topic keywords
   - Link related entities
   - Create knowledge graph

## Output Format

```json
{
  "topic": "Microservices architecture patterns",
  "research_summary": {
    "sources_reviewed": 12,
    "key_findings": [
      "API Gateway pattern is essential",
      "Service mesh improves observability",
      "Event-driven communication reduces coupling"
    ],
    "best_practices": [
      "Use circuit breakers",
      "Implement distributed tracing",
      "Design for failure"
    ],
    "challenges": [
      "Data consistency across services",
      "Increased operational complexity"
    ]
  },
  "plan": {
    "overview": "Implement microservices architecture...",
    "phases": [
      {
        "name": "Phase 1: API Gateway",
        "tasks": ["Setup gateway", "Configure routing"],
        "duration": "1 week"
      },
      {
        "name": "Phase 2: Service Mesh",
        "tasks": ["Deploy Istio", "Configure policies"],
        "duration": "2 weeks"
      }
    ]
  },
  "gam_id": "research-microservices-abc123"
}
```

## Best Practices

- Use deep search for unfamiliar topics
- Review multiple sources for accuracy
- Always create plan for implementation
- Save research to GAM for future reference
- Validate findings with QA/Critic
- Update research as patterns evolve

## Integration

- Chains to `/skill-planning` for detailed planning
- Uses `/tool-gam` for memory operations
- Invokes `/tool-search` for web research
- Validated by `/agent-critic`

## Related Commands

- `/skill-planning` - Detailed feature planning
- `/deep-research` - Alternative research workflow
- `/autonomous-research` - Autonomous research mode
- `/research-memory` - Query research memory

## Source

- **File**: `app/server/skills/planning.py`
- **Function**: `research_and_plan()`
- **Layer**: Skills (WHAT)
