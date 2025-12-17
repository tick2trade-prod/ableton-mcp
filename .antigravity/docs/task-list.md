# Task List

> Source: [https://antigravity.google/docs/task-list](https://antigravity.google/docs/task-list)

## Overview

The Task List provides a centralized view of all tasks in your project.

## Task Structure

```markdown
## Task: [Title]

**Status**: Todo | In Progress | Done | Blocked
**Priority**: High | Medium | Low
**Assigned**: Agent | User

### Description
What needs to be accomplished.

### Steps
1. Step one
2. Step two

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## ableton-mcp Task Examples

### High Priority Tasks

```markdown
## Task: Fix Socket Timeout

**Status**: In Progress
**Priority**: High

### Description
Tests fail with timeout when Ableton is slow to respond.

### Steps
1. Increase socket timeout to 30s
2. Add retry logic with exponential backoff
3. Run affected tests

### Acceptance Criteria
- [ ] All session tests pass
- [ ] No timeout errors in CI
```

### Feature Tasks

```markdown
## Task: Add Tempo Detection MCP Tool

**Status**: Todo
**Priority**: Medium

### Description
Create an MCP tool that detects BPM from audio clips.

### Steps
1. Research librosa tempo detection
2. Create MCP tool implementation
3. Add tests
4. Document usage

### Acceptance Criteria
- [ ] Tool returns accurate BPM
- [ ] Works with various audio formats
- [ ] Integration test with Ableton clip
```

## Task Management

### Creating Tasks
```
USER: Create a task to implement sidechain compression
AGENT: [Creates task artifact with structure]
```

### Updating Tasks
```
USER: Mark the socket timeout task as done
AGENT: [Updates task status]
```

### Viewing Tasks
```
USER: Show all high priority tasks
AGENT: [Lists tasks filtered by priority]
```

## Integration with Workflows

Tasks can trigger workflows:
```markdown
## Task: Test New Track

**Workflow**: /test-track track_02_rumble

### On Completion
- [ ] Run test workflow
- [ ] Update task group status
```

## Related Pages

- [Task Groups](task-groups.md) - Organizing related tasks
- [Artifacts](artifacts.md) - Task storage
- [Implementation Plan](implementation-plan.md) - Detailed planning
