# Workflow: Multi-Agent Collaborative Development

## Overview

Multiple specialized AI agents collaborate using Agile/TDD methodology to develop features. Agents take on roles (Product Manager, Developer, Tester, Architect) and work together autonomously.

## Usage

```bash
/workflow-multi-agent-dev
```

## Parameters

- `feature_name`: Feature to develop (required)
- `methodology`: Development methodology - agile, tdd, waterfall, kanban (default: agile)
- `team_size`: Number of agents (2-5) (default: 3)
- `sprint_duration`: Sprint duration in hours (default: 2)
- `roles`: Comma-separated roles (default: "pm,dev,tester")
  - Options: pm (Product Manager), dev (Developer), tester (QA), architect (Architect), reviewer (Code Reviewer)
- `stream_output`: Stream agent collaboration (default: true)
- `auto_commit`: Auto-commit after each sprint (default: true)

## Agent Roles

### Product Manager Agent
```python
from app.server.agents.factory import create_workflow_agent

pm_agent = await create_workflow_agent(
    step="planning",
    role="product_manager"
)

# Responsibilities:
# - Define user stories
# - Prioritize features
# - Accept/reject work
# - Manage backlog
```

### Developer Agent
```python
dev_agent = await create_workflow_agent(
    step="implementation",
    role="developer"
)

# Responsibilities:
# - Write code
# - Implement features
# - Fix bugs
# - Refactor code
```

### Tester Agent
```python
tester_agent = await create_workflow_agent(
    step="testing",
    role="tester"
)

# Responsibilities:
# - Write tests
# - Execute tests
# - Report bugs
# - Validate fixes
```

### Architect Agent
```python
architect_agent = await create_workflow_agent(
    step="design",
    role="architect"
)

# Responsibilities:
# - Design architecture
# - Review design decisions
# - Ensure best practices
# - Manage technical debt
```

## Workflow Steps

### 1. Sprint Planning (Autonomous)

```python
from app.core.gam_memory import GAMMemoryManager

gam = GAMMemoryManager()

# PM Agent creates user stories
user_stories = await pm_agent.create_user_stories(
    feature_name=feature_name,
    context=gam.research(f"features like {feature_name}", max_iters=5)
)

# Architect Agent designs solution
architecture = await architect_agent.design_solution(
    user_stories=user_stories,
    existing_architecture=gam.research("architecture patterns", max_iters=3)
)

# Team estimates work
estimates = await estimate_work(
    user_stories=user_stories,
    architecture=architecture,
    team_size=team_size
)
```

### 2. Sprint Execution (Collaborative)

```python
from app.server.skills.implementation import execute_implementation

for story in user_stories:
    # Developer implements
    code = await dev_agent.implement_story(
        story=story,
        architecture=architecture,
        stream=stream_output
    )

    # Tester writes tests
    tests = await tester_agent.write_tests(
        story=story,
        code=code,
        stream=stream_output
    )

    # Architect reviews
    review = await architect_agent.review_code(
        code=code,
        tests=tests,
        architecture=architecture
    )

    # PM accepts/rejects
    if await pm_agent.accept_work(story, code, tests, review):
        if auto_commit:
            commit_changes(story)
        gam.memorize(f"Story completed: {story.title}")
    else:
        # Iterate
        feedback = await pm_agent.provide_feedback(story, code, tests)
        continue
```

### 3. Sprint Review (Retrospective)

```python
# Collect metrics
metrics = {
    "stories_completed": count_completed_stories(),
    "bugs_found": count_bugs(),
    "code_quality_score": calculate_quality_score(),
    "test_coverage": calculate_coverage(),
    "velocity": calculate_velocity()
}

# Team retrospective
retrospective = await conduct_retrospective(
    agents=[pm_agent, dev_agent, tester_agent, architect_agent],
    metrics=metrics
)

# Memorize learnings
gam.memorize(f"""
Sprint Retrospective: {feature_name}
Completed: {metrics['stories_completed']} stories
Velocity: {metrics['velocity']} story points
Learnings: {retrospective.key_learnings}
""")
```

## Example Usage

### Agile 3-Agent Team
```bash
/workflow-multi-agent-dev
  feature_name="User authentication system"
  methodology="agile"
  team_size=3
  roles="pm,dev,tester"
```

### TDD 5-Agent Team
```bash
/workflow-multi-agent-dev
  feature_name="Payment processing"
  methodology="tdd"
  team_size=5
  roles="pm,dev,tester,architect,reviewer"
  sprint_duration=4
```

## Agent Communication Protocol

```python
class AgentMessage:
    sender: str  # Agent role
    recipient: str  # Target agent or "all"
    message_type: str  # question, task, review, approval
    content: str
    context: dict

# Example communication
dev_to_architect = AgentMessage(
    sender="developer",
    recipient="architect",
    message_type="question",
    content="Should I use Redis or Memcached for caching?",
    context={"feature": "session management"}
)

architect_response = await architect_agent.respond(dev_to_architect)
```

## Output

Returns:
```json
{
  "feature_name": "User authentication system",
  "methodology": "agile",
  "sprint_duration_hours": 2,
  "stories_completed": 8,
  "stories_total": 10,
  "bugs_found": 3,
  "bugs_fixed": 3,
  "test_coverage_percent": 87,
  "code_quality_score": 8.5,
  "velocity": 21,
  "agent_contributions": {
    "pm": "Created 10 stories, accepted 8",
    "dev": "Implemented 8 stories, 450 lines",
    "tester": "Wrote 32 tests, found 3 bugs"
  },
  "files_modified": ["app/auth.py", "tests/test_auth.py"],
  "commits": 8
}
```

## Performance

- **Avg execution time**: 5-10 minutes (depends on team size and sprint duration)
- **GAM queries**: 5-10 per agent
- **Streaming**: Real-time agent collaboration
- **Parallelization**: Agents work in parallel where possible

## Related Workflows

- `/workflow-agile-sprint` - Sprint planning
- `/workflow-auto-tests` - Test generation
- `/workflow-ai-code-review` - Code review
- `/batch-implement` - Parallel implementation

## Best Practices

1. **Start with 3 agents**: PM, Dev, Tester
2. **Add Architect for complex features**: Architecture decisions need expert
3. **Enable streaming**: Watch agents collaborate in real-time
4. **Use TDD for critical features**: Test-first approach reduces bugs
5. **Review retrospectives**: Learn from each sprint
