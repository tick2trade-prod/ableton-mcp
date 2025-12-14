# Workflow: Agile Methodology Integration

## Overview

AI agents take on Agile roles (Product Manager, Scrum Master, Developer, Tester) to collaboratively develop software in sprints with dynamic dependency graphs.

## Usage

```bash
/workflow-agile-sprint
```

## Parameters

- `sprint_name`: Sprint identifier (required)
- `sprint_duration_days`: Sprint length (default: 2 weeks)
- `backlog_items`: Comma-separated ticket IDs (required)
- `team_capacity_hours`: Available hours (default: 80)
- `auto_assign`: Auto-assign tasks to agents (default: true)

## Agile Ceremonies

```python
# 1. Sprint Planning
- Backlog refinement
- Story point estimation
- Sprint goal definition
- Task assignment

# 2. Daily Standup
- Progress updates
- Blocker identification
- Task reallocation

# 3. Sprint Review
- Demo completed work
- Stakeholder feedback
- Acceptance criteria validation

# 4. Sprint Retrospective
- What went well
- What needs improvement
- Action items
```

## Output

```json
{
  "sprint_name": "Sprint 24",
  "stories_completed": 12,
  "story_points_completed": 45,
  "velocity": 45,
  "burndown_chart_url": "...",
  "retrospective_notes": "..."
}
```
