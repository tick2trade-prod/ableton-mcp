# Skill Commands (WHAT Layer)

High-level skill execution commands that orchestrate multiple tools and agents.

## Available Skills (10 total)

### Core Skills
- **execute-planning-skill.md** - Execute planning workflow with QA loop
- **execute-implementation-skill.md** - Execute implementation workflow
- **execute-review-skill.md** - Execute review and validation workflow
- **execute-qa-skill.md** - Execute QA validation workflow

### Specialized Skills
- **research-and-plan.md** - Research topic and create plan
- **planning-skill.md** - Planning skill configuration
- **implementation-skill.md** - Implementation skill configuration
- **review-skill.md** - Create PRs and validate changes

### Batch Operations
- **execute-batch-skill.md** - Execute skills in batch (parallel)

### Execution
- **execute-skill.md** - Execute any skill by configuration

## Usage Pattern

```bash
/execute-planning-skill feature="User authentication" use_web_search=true
/execute-implementation-skill prompt="Implement JWT middleware" language="python"
/execute-review-skill target="code" files="src/**/*.py"
/research-and-plan topic="OAuth2 implementation patterns"
/skill-review scope="current_changes"
```

## Skill Workflow

```
Planning Skill:
  Research → Plan → Critique → Refine → Memorize

Implementation Skill:
  Context Lookup → Generate → Lint → Test → Validate

Review Skill:
  Read Code → Analyze → Critique → Generate Feedback

Batch Skill:
  Queue Tasks → Execute Parallel → Aggregate Results
```

## Skill vs Agent vs Tool

- **Tool** (HOW) - Atomic operation (e.g., memorize to GAM)
- **Agent** (WHO) - Specialized LLM with role (e.g., Planner)
- **Skill** (WHAT) - Workflow orchestrating agents + tools (e.g., Planning)

## Related

- Agents (WHO): `/agents/INDEX.md`
- Tools (HOW): `/tools/INDEX.md`
- Workflows: `/workflows/INDEX.md`
- Registry: `/registry/2000_INDEX_SKILLS.md`
