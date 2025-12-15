# C3 Command Index

## Overview

This directory contains **24 commands** decomposed from `app/` core logic following the DDD MCP Tools architecture. Commands are organized by architectural layer and ranked by user value.

**Based on**: Analysis in `c3.md`
**Architecture**: Domain-Driven Design (DDD) with WHO-WHAT-HOW separation
**Created**: December 4, 2025

---

## Command Categories

| Rank | Category | Commands | User Value | Layer |
|------|----------|----------|------------|-------|
| 1 | Skills | 5 | ⭐⭐⭐⭐⭐ | WHAT |
| 2 | Agents | 5 | ⭐⭐⭐⭐ | WHO |
| 3 | Tools | 6 | ⭐⭐⭐ | HOW |
| 4 | Domain | 4 | ⭐⭐⭐ | Core |
| 5 | Orchestrator | 4 | ⭐⭐ | Router |

**Total**: 24 commands

---

## Phase 1: Skills (Rank 1) - WHAT Layer

**Rationale**: Direct mapping to user workflows. Highest value commands.

| # | Command | Source | Purpose |
|---|---------|--------|---------|
| 1 | `/skill-planning` | `skills/planning.py` | Execute research & planning with QA loop |
| 2 | `/skill-implementation` | `skills/implementation.py` | Generate and implement code with linting |
| 3 | `/skill-review` | `skills/review.py` | Create PR and validate changes |
| 4 | `/skill-research-and-plan` | `skills/planning.py` → `research_and_plan()` | Research topic + create plan |
| 5 | `/skill-execute-planning` | `skills/planning.py` → `execute_planning()` | Plan feature with GAM context |

**Files**:
- `skill-planning.md`
- `skill-implementation.md`
- `skill-review.md`
- `skill-research-and-plan.md`
- `skill-execute-planning.md`

---

## Phase 2: Agents (Rank 2) - WHO Layer

**Rationale**: Flexible agent invocation. Enables agent composition.

| # | Command | Source | Purpose |
|---|---------|--------|---------|
| 6 | `/agent-planner` | `agents/factory.py` + `prompts.py` | Invoke planner agent with context |
| 7 | `/agent-coder` | `agents/factory.py` + `prompts.py` | Invoke coder agent for implementation |
| 8 | `/agent-critic` | `agents/factory.py` + `prompts.py` | Invoke critic agent for QA review |
| 9 | `/agent-structured` | `agents/factory.py` → `generate_structured_response()` | Get structured JSON response from agent |
| 10 | `/agent-router` | `agents/router.py` | Route to best Ollama model for task |

**Files**:
- `agent-planner.md`
- `agent-coder.md`
- `agent-critic.md`
- `agent-structured.md`
- `agent-router.md`

---

## Phase 3: Tools (Rank 3) - HOW Layer

**Rationale**: Fine-grained control for power users. Composable primitives.

| # | Command | Source | Purpose |
|---|---------|--------|---------|
| 11 | `/tool-gam` | `tools/gam_tool.py` | GAM memory operations (memorize, recall, search) |
| 12 | `/tool-coder` | `tools/coder_tool.py` | Write code with linting validation |
| 13 | `/tool-package` | `tools/package_tool.py` | Verify package exists (PyPI/NPM) |
| 14 | `/tool-search` | `tools/search.py` | Search codebase or GAM memory |
| 15 | `/tool-computer` | `tools/computer_tool.py` | Browser automation (navigate, click, screenshot) |
| 16 | `/tool-thinking` | `tools/thinking_tool.py` | Explicit reasoning before action |

**Files**:
- `tool-gam.md`
- `tool-coder.md`
- `tool-package.md`
- `tool-search.md`
- `tool-computer.md`
- `tool-thinking.md`

---

## Phase 4: Domain (Rank 4) - Core Layer

**Rationale**: Pure domain logic. Reusable across interfaces.

| # | Command | Source | Purpose |
|---|---------|--------|---------|
| 17 | `/domain-gam-memory` | `core/gam_memory.py` | Direct GAM operations (no MCP wrapper) |
| 18 | `/domain-code-generator` | `generation/code_generator.py` | Code generation with streaming |
| 19 | `/domain-autonomous-research` | `research/autonomous_research.py` | Autonomous research workflows |
| 20 | `/domain-agent-task` | `orchestration/agent_task.py` | Agent task management |

**Files**:
- `domain-gam-memory.md`
- `domain-code-generator.md`
- `domain-autonomous-research.md`
- `domain-agent-task.md`

---

## Phase 5: Orchestrator (Rank 5) - Router Layer

**Rationale**: Full workflow execution. Thin routing layer.

| # | Command | Source | Purpose |
|---|---------|--------|---------|
| 21 | `/orchestrator-execute-task` | `orchestrator.py` → `execute_task()` | Execute task with action mode |
| 22 | `/orchestrator-execute-workflow` | `orchestrator.py` → `execute_workflow()` | Execute complete workflow |
| 23 | `/orchestrator-execute-streaming` | `orchestrator.py` → `execute_workflow_streaming()` | Execute workflow with progress updates |
| 24 | `/orchestrator-execute-background` | `orchestrator.py` → `execute_task_background()` | Queue task for background execution |

**Files**:
- `orchestrator-execute-task.md`
- `orchestrator-execute-workflow.md`
- `orchestrator-execute-streaming.md`
- `orchestrator-execute-background.md`

---

## Architecture Alignment

### DDD Layers

```
┌─────────────────────────────────────────────┐
│  Orchestrator (Router)                      │
│  - execute_task                             │
│  - execute_workflow                         │
│  - execute_streaming                        │
│  - execute_background                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Skills (WHAT) - Workflows                  │
│  - planning                                 │
│  - implementation                           │
│  - review                                   │
│  - research-and-plan                        │
│  - execute-planning                         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Agents (WHO) - Agent Invocation            │
│  - planner                                  │
│  - coder                                    │
│  - critic                                   │
│  - structured                               │
│  - router                                   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Tools (HOW) - Execution Primitives         │
│  - gam                                      │
│  - coder                                    │
│  - package                                  │
│  - search                                   │
│  - computer                                 │
│  - thinking                                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Domain (Core) - Pure Business Logic        │
│  - gam-memory                               │
│  - code-generator                           │
│  - autonomous-research                      │
│  - agent-task                               │
└─────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Dependencies | Examples |
|-------|---------------|--------------|----------|
| **Orchestrator** | Route requests, manage state | Skills, Services | execute_task, execute_workflow |
| **Skills** | High-level workflows | Agents, Tools, Domain | planning, implementation, review |
| **Agents** | LLM invocation, prompts | Tools, Domain | planner, coder, critic |
| **Tools** | Execution primitives | Domain, External APIs | gam, coder, search |
| **Domain** | Pure business logic | None (no infrastructure) | GAMMemoryManager, CodeGenerator |

---

## Usage Patterns

### Pattern 1: Full Workflow

```
User → /orchestrator-execute-workflow
     → /skill-planning
     → /skill-implementation
     → /skill-review
```

### Pattern 2: Skill Composition

```
User → /skill-research-and-plan
     → /skill-implementation
     → /skill-review
```

### Pattern 3: Agent Direct

```
User → /agent-planner (get plan)
     → /agent-coder (generate code)
     → /agent-critic (review code)
```

### Pattern 4: Tool Granular

```
User → /tool-gam (search context)
     → /tool-coder (write file)
     → /tool-package (verify deps)
```

### Pattern 5: Domain Pure

```
User → /domain-gam-memory (create entity)
     → /domain-code-generator (generate code)
     → /domain-autonomous-research (research)
```

---

## Command Relationships

### Skill Commands Use

- **Agents**: All skill commands invoke agents internally
- **Tools**: All skill commands use tools for execution
- **Domain**: Skills delegate to domain logic

### Agent Commands Use

- **Tools**: Agents use tools for operations
- **Domain**: Agents query domain for context
- **Router**: Agent router selects best model

### Tool Commands Use

- **Domain**: Tools wrap domain logic
- **External**: Tools integrate external services
- **MCP**: Tools provide MCP interface

### Domain Commands

- **Pure**: No infrastructure dependencies
- **Reusable**: Used by all layers above
- **Testable**: Easy to unit test

---

## Quick Reference

### By Use Case

| Use Case | Recommended Command | Alternative |
|----------|-------------------|-------------|
| Plan feature | `/skill-planning` | `/skill-execute-planning` |
| Implement code | `/skill-implementation` | `/agent-coder` |
| Review code | `/skill-review` | `/agent-critic` |
| Research topic | `/skill-research-and-plan` | `/domain-autonomous-research` |
| Full workflow | `/orchestrator-execute-workflow` | `/orchestrator-execute-streaming` |
| Background task | `/orchestrator-execute-background` | `/orchestrator-execute-task` |
| Memory operations | `/tool-gam` | `/domain-gam-memory` |
| Code generation | `/agent-coder` | `/domain-code-generator` |
| QA validation | `/agent-critic` | `/qa-critic` |
| Package check | `/tool-package` | N/A |

### By Layer

| Layer | Start Here | Then Try |
|-------|-----------|----------|
| **Skills** | `/skill-planning` | `/skill-implementation`, `/skill-review` |
| **Agents** | `/agent-planner` | `/agent-coder`, `/agent-critic` |
| **Tools** | `/tool-gam` | `/tool-search`, `/tool-coder` |
| **Domain** | `/domain-gam-memory` | `/domain-code-generator` |
| **Orchestrator** | `/orchestrator-execute-task` | `/orchestrator-execute-workflow` |

---

## Best Practices

### For Users

1. **Start with Skills** - Highest value, most complete workflows
2. **Use Agents for flexibility** - When you need custom agent behavior
3. **Use Tools for granular control** - When you need specific operations
4. **Use Domain for pure logic** - When you need infrastructure-free operations
5. **Use Orchestrator for full workflows** - When you need complete feature implementation

### For Developers

1. **Skills compose Agents and Tools** - Don't duplicate logic
2. **Agents invoke Tools** - Keep agents focused on LLM interaction
3. **Tools wrap Domain** - Provide MCP interface to pure logic
4. **Domain has no dependencies** - Keep it pure and testable
5. **Orchestrator routes only** - Thin layer, no business logic

---

## Integration with Existing Commands

### Existing Commands

| Existing | New Equivalent | Notes |
|----------|---------------|-------|
| `/deep-research` | `/skill-research-and-plan` | Similar research workflow |
| `/generate-code` | `/skill-implementation` | More complete implementation |
| `/qa-critic` | `/agent-critic` | Direct agent access |
| `/autonomous-research` | `/domain-autonomous-research` | Pure domain version |
| `/run-agent-task` | `/orchestrator-execute-task` | Similar task execution |
| `/memorize-content` | `/tool-gam` | Simplified GAM operations |
| `/research-memory` | `/tool-gam` + `/tool-search` | Combined search |

### Migration Path

1. **Phase 1**: Use new skill commands alongside existing
2. **Phase 2**: Migrate workflows to new commands
3. **Phase 3**: Deprecate overlapping existing commands
4. **Phase 4**: Consolidate command registry

---

## Testing

### Test Coverage

- ✅ All commands have documentation
- ✅ All commands map to source files
- ✅ All commands follow DDD architecture
- ⏳ Integration tests needed
- ⏳ End-to-end workflow tests needed

### Test Commands

```bash
# Test skill commands
/skill-planning Feature Name: Test feature
/skill-implementation Prompt: Create test endpoint

# Test agent commands
/agent-planner Request: Plan test architecture
/agent-coder Request: Generate test code

# Test tool commands
/tool-gam Operation: search Query: test patterns
/tool-coder Operation: validate File Path: app/test.py

# Test domain commands
/domain-gam-memory Operation: create_entity Entity Name: test-entity
/domain-code-generator Prompt: Generate test function

# Test orchestrator commands
/orchestrator-execute-task Task: Test task Action: plan
/orchestrator-execute-workflow Feature Name: Test feature
```

---

## Maintenance

### Adding New Commands

1. Identify layer (Skills, Agents, Tools, Domain, Orchestrator)
2. Create command file following template
3. Update this INDEX.md
4. Add to appropriate category
5. Document relationships
6. Add tests

### Deprecating Commands

1. Mark as deprecated in documentation
2. Provide migration path
3. Update INDEX.md
4. Remove after grace period

### Updating Commands

1. Update command file
2. Update INDEX.md if relationships change
3. Update tests
4. Document breaking changes

---

## Related Files

- **Analysis**: `c3.md` - Original decomposition analysis
- **Architecture**: `app/server/AGENTS.md` - DDD architecture documentation
- **Implementation**: `app/server/IMPLEMENTATION_SUMMARY.md` - Implementation details
- **Recommendations**: `app/server/RECOMMENDATIONS.md` - Architecture recommendations

---

## Statistics

- **Total Commands**: 24
- **Skills**: 5 (21%)
- **Agents**: 5 (21%)
- **Tools**: 6 (25%)
- **Domain**: 4 (17%)
- **Orchestrator**: 4 (17%)

**Coverage**:
- ✅ Planning workflows: 3 commands
- ✅ Implementation workflows: 2 commands
- ✅ Review workflows: 1 command
- ✅ Research workflows: 3 commands
- ✅ Agent invocation: 5 commands
- ✅ Tool operations: 6 commands
- ✅ Domain logic: 4 commands
- ✅ Orchestration: 4 commands

---

## Changelog

### 2025-12-04 - Initial Release

- Created 24 commands across 5 phases
- Documented all commands
- Created INDEX.md
- Aligned with DDD architecture

---

## Future Enhancements

### Planned

1. Add integration tests for all commands
2. Create command composition examples
3. Add performance benchmarks
4. Create video tutorials
5. Add command aliases

### Considered

1. Auto-generate commands from source code
2. Command validation tool
3. Command dependency graph
4. Command usage analytics
5. Command recommendation system

---

**Last Updated**: December 4, 2025
**Maintainer**: AI Agent
**Status**: ✅ Complete
