# Workflow: AI-Powered Developer Onboarding

## Overview

Create personalized learning paths for new developers based on role and codebase topology, accelerating onboarding.

## Usage

```bash
/workflow-onboarding
```

## Parameters

- `developer_name`: New developer name (required)
- `role`: frontend, backend, fullstack, devops, qa (required)
- `experience_level`: junior, mid, senior (required)
- `learning_pace`: fast, normal, slow (default: normal)
- `generate_tasks`: Generate hands-on tasks (default: true)

## Onboarding Components

```python
# 1. Codebase Tour
- Architecture overview
- Key components
- Design patterns
- Code conventions

# 2. Development Setup
- Environment setup
- Tool installation
- Access provisioning
- First commit

# 3. Learning Path
- Documentation
- Code examples
- Video tutorials
- Hands-on tasks

# 4. Mentorship
- Assign mentor
- Schedule check-ins
- Track progress
- Provide feedback
```

## Output

```json
{
  "learning_path_url": "...",
  "tasks_generated": 15,
  "estimated_onboarding_days": 5,
  "mentor_assigned": "@alice",
  "first_task": "Fix bug in user service"
}
```
