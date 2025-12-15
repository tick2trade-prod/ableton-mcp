# Workflow: AI-Enhanced Sprint Planning

## Overview

Assist in sprint planning by estimating capacity, assigning work, and tracking velocity across iterations.

## Usage

```bash
/workflow-sprint-planning
```

## Parameters

- `sprint_name`: Sprint identifier (required)
- `team_capacity_hours`: Available hours (required)
- `backlog_items`: Comma-separated ticket IDs (required)
- `auto_assign`: Auto-assign tasks (default: true)
- `optimize_for`: velocity, quality, learning (default: velocity)

## Planning Steps

```python
# 1. Capacity Planning
- Calculate available hours
- Account for meetings/overhead
- Consider time off

# 2. Backlog Refinement
- Estimate story points
- Identify dependencies
- Prioritize items

# 3. Sprint Goal
- Define sprint objective
- Align with roadmap
- Set success criteria

# 4. Task Assignment
- Match skills to tasks
- Balance workload
- Consider learning opportunities

# 5. Velocity Tracking
- Historical velocity
- Predicted velocity
- Confidence interval
```

## Output

```json
{
  "sprint_name": "Sprint 24",
  "capacity_hours": 80,
  "stories_planned": 12,
  "story_points_planned": 45,
  "predicted_velocity": 42,
  "confidence": 0.85,
  "sprint_goal": "Complete user authentication"
}
```
