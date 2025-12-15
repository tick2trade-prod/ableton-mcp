# Agent Handoff Logs

This directory contains handoff logs when switching between AI agents mid-task.

## Naming Convention
`YYYY-MM-DD-task-name.md`

Example: `2025-12-13-beat-generator.md`

## Template

```markdown
## Handoff: [Source Agent] → [Target Agent]
**Date:** YYYY-MM-DD HH:MM
**Task:** [Task name]
**Status:** [Architecture complete | Implementation in progress | Testing needed]

### Completed Steps
1. [What was done]
2. [What was completed]

### Next Steps
1. [What needs to be done next]
2. [Specific implementation tasks]
3. [Testing requirements]

### Context Files
- [Relevant spec files]
- [Reference implementations]
- [Related documentation]

### Important Notes
- [Critical information for next agent]
- [Constraints or requirements]
- [Known issues or blockers]

### Files Modified
- `path/to/file1.py` - [What was changed]
- `path/to/file2.py` - [What was changed]

### Dependencies
- [External libraries needed]
- [Services that must be running]
- [Environment variables required]
```

## Usage

### When to Create a Handoff
- Switching agents mid-task (e.g., Claude designed architecture, Ollama will implement)
- Task requires multiple agent specializations
- Long-running task spanning multiple work sessions
- Complex task with clear phase boundaries

### When NOT to Create a Handoff
- Simple, single-step tasks
- Same agent continuing work
- Quick fixes or minor edits

## Examples

Good handoff scenario:
```
Claude designs MCP tool architecture →
Handoff log created →
Ollama implements the tool →
Handoff log updated →
Claude reviews and refines
```

No handoff needed:
```
Codex generates utility function → Complete (single agent, single task)
```
