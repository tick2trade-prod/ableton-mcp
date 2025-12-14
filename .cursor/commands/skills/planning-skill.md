# Skill: Planning

## Overview

Execute research & planning workflow with QA loop. This command invokes the planning skill from `app/server/skills/planning.py` to create a comprehensive plan with quality assurance validation.

> **Layer**: WHAT (Skill Orchestration)
> **Rank**: 2 - Layer-Based Command

## Usage

Type `/skill-planning` followed by the feature name.

## Parameters

- `feature_name`: Name of feature to plan (required)
- `use_web_search`: Enable web search for research (default: true)
- `qa_enabled`: Enable QA/Critic validation (default: true)
- `min_qa_score`: Minimum QA score to accept plan (default: 70)
- `save_to_gam`: Save plan to GAM memory (default: true)

## Example Usage

### Plan New Feature

```
/skill-planning
Feature Name: User authentication with JWT
Use Web Search: true
QA Enabled: true
Min QA Score: 80
```

### Plan Without Web Search

```
/skill-planning
Feature Name: Add logging middleware
Use Web Search: false
QA Enabled: true
```

### Quick Plan (No QA)

```
/skill-planning
Feature Name: Update README
QA Enabled: false
```

## Workflow

1. **Research Phase**:
   - Query GAM memory for relevant context
   - Perform web search if enabled
   - Gather best practices and patterns

2. **Planning Phase**:
   - Create structured plan with tasks
   - Identify dependencies and risks
   - Estimate complexity and effort

3. **QA Phase** (if enabled):
   - Run Critic agent on plan
   - Validate architecture decisions
   - Check for hallucinated packages
   - Verify best practices

4. **Refinement Loop**:
   - If QA score < min_score, refine plan
   - Address critical issues
   - Re-run QA validation
   - Repeat until passing

5. **Save to GAM**:
   - Store plan in memory
   - Tag with feature name
   - Link to related entities

## Output Format

```json
{
  "feature_name": "User authentication with JWT",
  "plan": {
    "overview": "Implement JWT-based authentication...",
    "todos": [
      {
        "task": "Create User model",
        "priority": "high",
        "dependencies": []
      },
      {
        "task": "Implement JWT token generation",
        "priority": "high",
        "dependencies": ["Create User model"]
      }
    ],
    "risks": [
      "Token expiration handling",
      "Refresh token security"
    ]
  },
  "qa_report": {
    "score": 85,
    "critical_issues": [],
    "warnings": ["Consider rate limiting"],
    "suggestions": ["Add token blacklist"]
  },
  "gam_id": "plan-auth-jwt-abc123"
}
```

## Best Practices

- Enable web search for unfamiliar domains
- Set higher min_qa_score for production features
- Review QA warnings before proceeding
- Save plans to GAM for future reference
- Iterate on plans based on QA feedback

## Integration

- Chains to `/skill-implementation` for execution
- Uses `/tool-gam` for memory operations
- Invokes `/agent-planner` internally
- Validated by `/agent-critic`

## Related Commands

- `/skill-implementation` - Execute the plan
- `/skill-review` - Review implementation
- `/research-and-plan` - Alternative research workflow
- `/execute-planning` - Direct planning without research

## Source

- **File**: `app/server/skills/planning.py`
- **Function**: `execute_planning()`
- **Layer**: Skills (WHAT)
