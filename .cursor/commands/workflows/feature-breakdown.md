# Workflow: Feature Breakdown

## Overview

Break down a large feature into smaller, independent, parallelizable tasks. Essential for medium/large features (4+ files) to enable efficient batch implementation.

## Usage

Type `/workflow-feature-breakdown` after feature research and before implementation.

## Parameters

- `feature_description`: Feature to break down (required)
- `context`: Additional context or constraints (optional)
- `max_tasks`: Maximum number of tasks (default: 20)
- `task_size`: Target task size (default: "small") - Options: small, medium, large
- `dependencies`: Include dependency graph (default: true)
- `estimate_effort`: Estimate effort for each task (default: true)
- `assign_priority`: Assign priority to tasks (default: true)

## Workflow Steps

### 1. Feature Analysis

```bash
# Research feature requirements
/workflow-research topic="$FEATURE_DESCRIPTION"

# Query GAM memory for related context
# - Similar features implemented before
# - Existing architecture patterns
# - Technical constraints
# - Team conventions
```

### 2. Decomposition Strategy

**Vertical Slicing** (Recommended):
```
Break by user-facing functionality:
- Task 1: User can register
- Task 2: User can login
- Task 3: User can reset password
```

**Horizontal Slicing** (For infrastructure):
```
Break by technical layer:
- Task 1: Database models
- Task 2: Business logic services
- Task 3: API endpoints
- Task 4: Frontend components
- Task 5: Tests
```

**Component-Based**:
```
Break by system component:
- Task 1: Authentication service
- Task 2: User profile service
- Task 3: Notification service
```

### 3. Task Decomposition

```python
# Use AI agent to break down feature
from app.server.skills.planning import execute_planning

plan = await execute_planning(
    feature_name=feature_description,
    gam_memory=gam,
)

# Extract tasks from plan
tasks = []
for todo in plan.todos:
    task = {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "files": todo.files,
        "dependencies": todo.dependencies,
        "priority": todo.priority,
        "effort_hours": todo.effort_hours,
    }
    tasks.append(task)
```

### 4. Dependency Analysis

```python
# Build dependency graph
import networkx as nx

G = nx.DiGraph()
for task in tasks:
    G.add_node(task["id"], **task)
    for dep in task["dependencies"]:
        G.add_edge(dep, task["id"])

# Identify parallel tasks (no dependencies)
parallel_tasks = [
    task for task in tasks
    if len(list(G.predecessors(task["id"]))) == 0
]

# Identify critical path
critical_path = nx.dag_longest_path(G)

# Topological sort for execution order
execution_order = list(nx.topological_sort(G))
```

### 5. Task Specification

Each task should include:
```yaml
task_id: "task-001"
title: "Implement user registration endpoint"
description: |
  Create FastAPI endpoint for user registration with:
  - Email/password validation
  - Password hashing
  - Database persistence
  - JWT token generation
files:
  - app/api/endpoints/auth.py
  - app/models/user.py
  - app/services/auth_service.py
  - tests/test_auth_registration.py
dependencies:
  - task-000  # Database models must exist first
priority: high
effort_hours: 4
acceptance_criteria:
  - User can register with email/password
  - Password is hashed before storage
  - JWT token is returned on success
  - Validation errors are returned for invalid input
  - Tests cover happy path and edge cases
```

### 6. Effort Estimation

```python
# Estimate effort based on:
# - Number of files
# - Code complexity
# - Dependencies
# - Team velocity

def estimate_effort(task):
    base_hours = len(task["files"]) * 1.5  # 1.5 hours per file

    # Adjust for complexity
    if "database migration" in task["description"]:
        base_hours *= 1.5
    if "external API" in task["description"]:
        base_hours *= 1.3
    if "authentication" in task["description"]:
        base_hours *= 1.4

    # Adjust for dependencies
    dependency_overhead = len(task["dependencies"]) * 0.5

    return round(base_hours + dependency_overhead, 1)
```

### 7. Priority Assignment

```python
# Assign priority based on:
# - Business value
# - Dependencies (blockers are high priority)
# - Risk (high-risk tasks should be tackled early)

def assign_priority(task, dependency_graph):
    # High priority if:
    # - Blocks other tasks
    # - High business value
    # - High risk

    blocked_tasks = len(list(dependency_graph.successors(task["id"])))

    if blocked_tasks > 3:
        return "critical"
    elif blocked_tasks > 0 or "authentication" in task["description"]:
        return "high"
    elif "test" in task["title"]:
        return "medium"
    else:
        return "low"
```

### 8. Output Task List

```markdown
# Feature: User Authentication System

## Summary
- Total Tasks: 12
- Estimated Effort: 48 hours
- Parallel Tasks: 4
- Critical Path: 6 tasks (24 hours)

## Tasks

### Phase 1: Foundation (Parallel)
- [x] Task 1: Database models (2h) [HIGH]
- [x] Task 2: Password hashing utility (1h) [MEDIUM]
- [x] Task 3: JWT token service (2h) [HIGH]
- [x] Task 4: Email validation utility (1h) [LOW]

### Phase 2: Core Features (Depends on Phase 1)
- [ ] Task 5: User registration endpoint (4h) [HIGH]
  - Depends on: Task 1, Task 2, Task 3
- [ ] Task 6: User login endpoint (3h) [HIGH]
  - Depends on: Task 1, Task 3
- [ ] Task 7: Password reset endpoint (5h) [MEDIUM]
  - Depends on: Task 1, Task 4

### Phase 3: Testing (Depends on Phase 2)
- [ ] Task 8: Registration tests (2h) [HIGH]
  - Depends on: Task 5
- [ ] Task 9: Login tests (2h) [HIGH]
  - Depends on: Task 6
- [ ] Task 10: Password reset tests (2h) [MEDIUM]
  - Depends on: Task 7

### Phase 4: Integration (Depends on Phase 3)
- [ ] Task 11: E2E authentication flow test (4h) [HIGH]
  - Depends on: Task 8, Task 9, Task 10
- [ ] Task 12: API documentation (2h) [LOW]
  - Depends on: Task 5, Task 6, Task 7
```

## Example Usage

### Medium Feature
```
/workflow-feature-breakdown
feature_description: "User authentication with JWT"
task_size: small
max_tasks: 15
dependencies: true
estimate_effort: true
```

### Large Feature
```
/workflow-feature-breakdown
feature_description: "E-commerce checkout flow with payments"
context: "Use Stripe API, support multiple currencies"
task_size: medium
max_tasks: 25
assign_priority: true
```

### Refactoring
```
/workflow-feature-breakdown
feature_description: "Refactor monolith to microservices"
context: "Extract user service and payment service"
task_size: large
max_tasks: 30
dependencies: true
```

## Integration with Other Workflows

### Called By
- `/workflow-implement` - Before batch implementation
- `/workflow-full-feature` - As part of feature workflow
- `/workflow-refactor-plan` - For refactoring breakdown

### Calls
- `/workflow-research` - Research feature requirements
- `app.server.skills.planning.execute_planning` - AI-powered planning
- `app.core.gam_memory.search` - Search for related context

### Feeds Into
- `/batch-implement` - Parallel task execution
- `/workflow-implement` - Sequential task execution
- Project management tools (Jira, Linear, etc.)

## Task Size Guidelines

| Size | Files | Effort | Use Case |
|------|-------|--------|----------|
| **Small** | 1-2 | 1-3h | Single function, utility, test |
| **Medium** | 3-5 | 4-8h | API endpoint, service, component |
| **Large** | 6-10 | 9-16h | Feature module, integration |

## Best Practices

1. **Vertical Slicing**: Break by user value, not technical layers
2. **Independence**: Minimize dependencies between tasks
3. **Testability**: Each task should be testable independently
4. **Atomic**: Each task should be a complete unit of work
5. **Parallelizable**: Identify tasks that can run in parallel
6. **Clear Acceptance Criteria**: Define "done" for each task

## Dependency Patterns

### Sequential (Waterfall)
```
Task 1 → Task 2 → Task 3 → Task 4
```
**Use when**: Each task depends on previous completion

### Parallel (Independent)
```
Task 1 ─┐
Task 2 ─┼→ Task 5
Task 3 ─┤
Task 4 ─┘
```
**Use when**: Tasks are independent, can run simultaneously

### Diamond (Converge)
```
Task 1 ─┐
        ├→ Task 3
Task 2 ─┘
```
**Use when**: Multiple tasks feed into one integration task

## Related Commands

- `/workflow-research` - Research before breakdown
- `/batch-implement` - Execute tasks in parallel
- `/workflow-implement` - Execute tasks sequentially
- `/workflow-refactor-plan` - Plan refactoring breakdown
- `/workflow-tech-debt-prioritize` - Prioritize tech debt tasks

## Output

Returns:
```json
{
  "feature": "User authentication system",
  "total_tasks": 12,
  "estimated_hours": 48,
  "parallel_tasks": 4,
  "critical_path_tasks": 6,
  "critical_path_hours": 24,
  "tasks": [
    {
      "id": "task-001",
      "title": "Database models",
      "files": ["app/models/user.py"],
      "dependencies": [],
      "priority": "high",
      "effort_hours": 2,
      "phase": 1
    }
  ],
  "dependency_graph": "graph.json",
  "execution_order": ["task-001", "task-002", "..."]
}
```

## Error Handling

- **Too many tasks**: Suggest grouping related tasks
- **Circular dependencies**: Detect and break cycles
- **No parallel tasks**: Warn about potential bottleneck
- **Unbalanced effort**: Suggest splitting large tasks
- **Missing acceptance criteria**: Prompt for clarification
