# Artifacts

> Source: [https://antigravity.google/docs/artifacts](https://antigravity.google/docs/artifacts)

## Overview

Artifacts are generated content that the agent produces during conversations. They can include code, documentation, images, and other files.

## Types of Artifacts

### Implementation Plans
Structured plans for complex tasks:
```markdown
## Implementation Plan: New MCP Tool

### Phase 1: Design
- [ ] Define API
- [ ] Research existing patterns

### Phase 2: Implementation
- [ ] Create tool file
- [ ] Add tests

### Phase 3: Integration
- [ ] Register in MCP config
- [ ] Documentation
```

### Walkthroughs
Step-by-step guides for processes:
```markdown
## Walkthrough: Testing Ableton Connection

1. Start Ableton Live
2. Enable AbletonMCP control surface
3. Run: `make check-port`
4. Verify: Port 9877 is listening
```

### Tasks
Individual actionable items:
```markdown
## Task: Fix timeout in test_create_track

**Status**: In Progress
**Priority**: High

### Steps
1. Increase socket timeout
2. Add retry logic
3. Run test to verify
```

### Other
- Code snippets
- Configuration files
- Research summaries
- Screenshots and recordings

## Artifact Management in ableton-mcp

### Storage Location
Artifacts are stored in the project directory:
```
.antigravity/
├── artifacts/
│   ├── implementation_plans/
│   ├── walkthroughs/
│   ├── tasks/
│   └── screenshots/
```

### Creating Artifacts

The agent creates artifacts when:
1. Generating implementation plans
2. Creating step-by-step guides
3. Breaking down complex tasks
4. Capturing screenshots

### Using Artifacts

Reference artifacts in conversations:
```
USER: Continue with the implementation plan for the rumble track
AGENT: [Reads artifact, continues from last completed step]
```

## Project-Specific Artifacts

### Track Creation Plans
```markdown
## Track: Rumble Bass

### Devices
1. Hybrid Reverb
2. Roar (saturation)
3. EQ Eight
4. Compressor (sidechain)

### Audio Routing
- Input: Resampling
- Output: Master
- Sidechain: From Kick
```

### Test Improvement Plans
```markdown
## Test Improvement: test_tools.py

### Week 1 Goals
- Achieve 70% pass rate
- Add AAA comments
- Include TDD markers

### Current Status
- 15/27 tests passing
- 5 tests need timeout fixes
```

## Best Practices

### 1. Reference Artifacts
Keep artifacts updated as you progress.

### 2. Version Control
Commit artifacts with related code:
```bash
git add .antigravity/artifacts/
git commit -m "docs: update implementation plan for track creation"
```

### 3. Review Before Execution
Let agent summarize artifact before continuing:
```
USER: Summarize the current state of the implementation plan
AGENT: [Reviews artifact, highlights completed/remaining items]
```

## Related Pages

- [Task List](task-list.md) - Managing tasks
- [Implementation Plan](implementation-plan.md) - Planning features
- [Walkthrough](walkthrough.md) - Guide creation
