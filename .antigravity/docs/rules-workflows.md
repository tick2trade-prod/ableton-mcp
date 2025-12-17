# Rules / Workflows

> Source: [https://antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows)

## Overview

Rules and Workflows in Antigravity allow you to define reusable automation patterns that the agent can follow. They're defined as markdown files in `.agent/workflows/`.

## Workflow Structure

```markdown
---
description: Short description of what this workflow does
---

## Steps

1. First step
2. Second step
// turbo
3. This step auto-runs if using run_command
```

### Turbo Annotations

- `// turbo` - Auto-run the next step
- `// turbo-all` - Auto-run ALL steps in the workflow

## Project Workflows

This project includes these workflows in `.agent/workflows/`:

### /research
```bash
/research "topic"
```
Quick research using SOTA researcher with concise summaries.

### /code-quality
```bash
/code-quality path/to/file.py
```
Analyze code quality using DeepAgents.

### /configure-rumble
```bash
/configure-rumble
```
Configure Track 02 Rumble with MCP verification and debugging.

## Creating Custom Workflows

### Example: Track Creation Workflow

Create `.agent/workflows/create-track.md`:

```markdown
---
description: Create a new Ableton track with tests
---

## Create New Track

1. Research the track type using search_ableton_docs
// turbo
2. Analyze existing track patterns in live_set/
// turbo
3. Generate the track script following existing patterns
4. Create corresponding test file
// turbo
5. Run the test to verify:
   ```bash
   pytest tests/test_track_<name>.py -v
   ```
6. Fix any issues and iterate until passing
```

### Example: MCP Development Workflow

Create `.agent/workflows/new-mcp-tool.md`:

```markdown
---
description: Create a new MCP tool for Ableton integration
---

## New MCP Tool

1. Define the tool purpose and API
2. Check existing tools in mcp_servers/ for patterns
// turbo
3. Create the tool implementation
4. Add tests in tests/mcp/
// turbo
5. Register in .antigravity/mcp.json
// turbo
6. Restart MCP server and test:
   ```bash
   make restart-mcp
   ```
```

## Rules (GEMINI.md)

Rules are defined in `GEMINI.md` and apply globally:

```markdown
# From this project's GEMINI.md

## Key Principles
- **No mocks** - All tests run against real Ableton Live
- **Incremental testing** - Test one tool at a time
- **Live verification** - Confirm changes in DAW

## Conventions
- Conventional Commits: feat:, fix:, test:, docs:
- Branch Naming: feature/<name>, test/<tool>, fix/<issue>
```

## Best Practices

### 1. Keep Workflows Focused
Each workflow should do one thing well.

### 2. Use Turbo Wisely
Only auto-run safe, non-destructive commands.

### 3. Include Verification Steps
```markdown
6. Verify in Ableton:
   - [ ] Track appears in session
   - [ ] Device chain is correct
   - [ ] Audio routing works
```

### 4. Document Expected Outcomes
```markdown
## Expected Result
- New track script in live_set/
- Passing test in tests/
- No regressions in existing tests
```

## Workflow for Ollama Integration

Create `.agent/workflows/ollama-task.md`:

```markdown
---
description: Run a task using local Ollama model
---

## Ollama Task

1. Ensure Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```
// turbo
2. Define the prompt for your task
3. Use the MCP tool with Ollama backend
4. Review and refine the output
```

## Related Pages

- [Agent](agent.md) - How agents execute workflows
- [MCP](mcp.md) - Tools available in workflows
- [Task Groups](task-groups.md) - Organizing workflow tasks
