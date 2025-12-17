# Task Groups

> Source: [https://antigravity.google/docs/task-groups](https://antigravity.google/docs/task-groups)

## Overview

Task Groups help organize related tasks into logical units for complex projects.

## Creating Task Groups

### Structure
```markdown
## Task Group: Implement Rumble Track

### Tasks
1. [ ] Research rumble bass techniques
2. [ ] Create track script
3. [ ] Add device chain
4. [ ] Configure sidechain
5. [ ] Write tests
6. [ ] Verify in Ableton
```

### Dependencies
```markdown
## Task Group: MCP Tool Development

### Tasks
1. [ ] Design API (blocking)
2. [ ] Implement tool (requires: 1)
3. [ ] Write tests (requires: 2)
4. [ ] Documentation (requires: 2)
5. [ ] Integration testing (requires: 2, 3)
```

## Task Groups in ableton-mcp

### Example: New Track Development

```markdown
## Task Group: Create Hi-Hat Track

### Research Phase
- [ ] Search Ableton docs for hi-hat patterns
- [ ] Review existing track scripts
- [ ] Identify device requirements

### Development Phase
- [ ] Create track_04_hihat.py
- [ ] Implement device chain
- [ ] Configure MIDI patterns

### Testing Phase
- [ ] Create test_track_04_hihat.py
- [ ] Run integration tests
- [ ] Verify in live Ableton session

### Documentation Phase
- [ ] Update track index
- [ ] Document device settings
```

### Example: MCP Enhancement

```markdown
## Task Group: Add Tempo Detection Tool

### Research
- [ ] Research audio analysis libraries
- [ ] Review librosa capabilities
- [ ] Check Ableton tempo API

### Implementation
- [ ] Create tempo_detection.py tool
- [ ] Add to MCP server
- [ ] Register in mcp.json

### Testing
- [ ] Unit tests for algorithm
- [ ] Integration tests with Ableton
- [ ] Edge case testing

### Integration
- [ ] Update documentation
- [ ] Add workflow example
```

## Managing Task Groups

### Tracking Progress
```markdown
## Task Group: Q4 Milestones

### Status: 60% Complete

### Completed
- [x] Basic track creation
- [x] Test infrastructure
- [x] MCP server setup

### In Progress
- [ ] Sidechain implementation
- [ ] Research tools

### Pending
- [ ] Browser agent
- [ ] Groove templates
```

### Agent Interaction

```
USER: What's the status of the rumble track task group?
AGENT: [Reviews task group artifact, summarizes progress]

USER: Continue with the next incomplete task
AGENT: [Identifies next task, begins execution]
```

## Best Practices

### 1. Keep Groups Focused
One task group = one deliverable feature.

### 2. Define Clear Completion Criteria
```markdown
### Completion Criteria
- All tests passing
- Verified in Ableton
- Documentation updated
- Code reviewed
```

### 3. Regular Updates
Update task status after each session:
```
USER: Mark research phase as complete
AGENT: [Updates task group artifact]
```

### 4. Link to Artifacts
```markdown
### Related Artifacts
- [Implementation Plan](artifacts/plans/rumble_track.md)
- [Research Notes](artifacts/research/rumble_techniques.md)
```

## Related Pages

- [Task List](task-list.md) - Individual tasks
- [Implementation Plan](implementation-plan.md) - Detailed planning
- [Artifacts](artifacts.md) - Task documentation
