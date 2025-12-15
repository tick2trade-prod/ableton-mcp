I'll analyze the files you've provided and rank 5 ideas for decomposing each file in `app/` core logic into Cursor commands, following the pattern established in your command registry.

Let me first examine the key files to understand the current architecture:

[7 tools called]

Now let me read the remaining key files to complete my analysis:

[5 tools called]

Now let me examine the core directories to understand what files exist:

[8 tools called]

Perfect! Now I have a complete understanding of the architecture. Let me create a comprehensive ranking of 5 ideas for decomposing each file in `app/` core logic into Cursor commands.

# 🎯 Top 5 Ideas for Decomposing App Core Logic into Cursor Commands

Based on the DDD MCP Tools architecture and existing command patterns, here are the **ranked ideas** for decomposing each file in `app/` into reusable Cursor commands:

---

## 🥇 **Rank 1: Skill-Based Decomposition (HIGHEST VALUE)**

**Rationale**: Aligns perfectly with DDD "WHAT" layer. Each skill represents a high-level workflow that users actually want to execute.

### Commands to Create:

| Command | Source File | Purpose |
|---------|-------------|---------|
| `/app/planning` | `app/server/skills/planning.py` | Execute research & planning with QA loop |
| `/app/implementation` | `app/server/skills/implementation.py` | Generate and implement code with linting |
| `/app/review` | `app/server/skills/review.py` | Create PR and validate changes |
| `/app/research-and-plan` | `app/server/skills/planning.py` → `research_and_plan()` | Research topic + create plan |
| `/app/execute-planning` | `app/server/skills/planning.py` → `execute_planning()` | Plan feature with GAM context |

**Why Rank 1**:
- ✅ Direct mapping to user workflows
- ✅ Reusable across different projects
- ✅ Clear separation of concerns
- ✅ Already tested and working
- ✅ Matches existing command pattern (`/deep-research`, `/generate-code`)

---

## 🥈 **Rank 2: Agent-Based Decomposition (HIGH VALUE)**

**Rationale**: Exposes the "WHO" layer. Users can invoke specific agents for different tasks (planning, coding, critiquing).

### Commands to Create:

| Command | Source File | Purpose |
|---------|-------------|---------|
| `/app/agent-planner` | `app/server/agents/factory.py` + `prompts.py` | Invoke planner agent with context |
| `/app/agent-coder` | `app/server/agents/factory.py` + `prompts.py` | Invoke coder agent for implementation |
| `/app/agent-critic` | `app/server/agents/factory.py` + `prompts.py` | Invoke critic agent for QA review |
| `/app/agent-structured` | `app/server/agents/factory.py` → `generate_structured_response()` | Get structured JSON response from agent |
| `/app/agent-router` | `app/server/agents/router.py` | Route to best Ollama model for task |

**Why Rank 2**:
- ✅ Flexible agent invocation
- ✅ Supports different LLM models
- ✅ Enables agent composition
- ✅ Useful for debugging agent behavior
- ⚠️ Slightly lower-level than skills

---

## 🥉 **Rank 3: Tool-Based Decomposition (MEDIUM-HIGH VALUE)**

**Rationale**: Exposes the "HOW" layer. Useful for power users who want fine-grained control over individual tools.

### Commands to Create:

| Command | Source File | Purpose |
|---------|-------------|---------|
| `/app/tool-gam` | `app/server/tools/gam_tool.py` | GAM memory operations (memorize, recall, search) |
| `/app/tool-coder` | `app/server/tools/coder_tool.py` | Write code with linting validation |
| `/app/tool-package` | `app/server/tools/package_tool.py` | Verify package exists (PyPI/NPM) |
| `/app/tool-search` | `app/server/tools/search.py` | Search codebase or GAM memory |
| `/app/tool-computer` | `app/server/tools/computer_tool.py` | Browser automation (navigate, click, screenshot) |
| `/app/tool-thinking` | `app/server/tools/thinking_tool.py` | Explicit reasoning before action |

**Why Rank 3**:
- ✅ Fine-grained control
- ✅ Composable building blocks
- ✅ Useful for debugging
- ⚠️ More verbose for end users
- ⚠️ Requires understanding of tool layer

---

## 🏅 **Rank 4: Domain-Based Decomposition (MEDIUM VALUE)**

**Rationale**: Exposes pure domain logic from `app/core`, `app/generation`, `app/research`, `app/orchestration`. Useful for direct access to business logic.

### Commands to Create:

| Command | Source File | Purpose |
|---------|-------------|---------|
| `/app/gam-memory` | `app/core/gam_memory.py` | Direct GAM operations (no MCP wrapper) |
| `/app/code-generator` | `app/generation/code_generator.py` | Code generation with streaming |
| `/app/autonomous-research` | `app/research/autonomous_research.py` | Autonomous research workflows |
| `/app/agent-task` | `app/orchestration/agent_task.py` | Agent task management |

**Why Rank 4**:
- ✅ Pure domain logic (no infrastructure)
- ✅ Reusable across interfaces
- ⚠️ Less user-facing than skills
- ⚠️ Requires understanding of domain layer
- ⚠️ Already wrapped by tools/skills

---

## 🎖️ **Rank 5: Orchestrator-Based Decomposition (LOWER VALUE)**

**Rationale**: Exposes orchestrator functions. Useful for full workflow execution but overlaps with existing commands.

### Commands to Create:

| Command | Source File | Purpose |
|---------|-------------|---------|
| `/app/execute-task` | `app/server/orchestrator.py` → `execute_task()` | Execute task with action mode |
| `/app/execute-workflow` | `app/server/orchestrator.py` → `execute_workflow()` | Execute complete workflow |
| `/app/execute-streaming` | `app/server/orchestrator.py` → `execute_workflow_streaming()` | Execute workflow with progress updates |
| `/app/execute-background` | `app/server/orchestrator.py` → `execute_task_background()` | Queue task for background execution |

**Why Rank 5**:
- ✅ Complete workflow execution
- ⚠️ Overlaps with `/run-agent-task`
- ⚠️ Less granular than skills
- ⚠️ Already exposed via existing commands
- ⚠️ Thin routing layer (not much logic to expose)

---

## 📊 **Summary Comparison**

| Rank | Approach | User Value | Reusability | Granularity | Alignment with DDD |
|------|----------|------------|-------------|-------------|-------------------|
| 1 | Skill-Based | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium | Perfect (WHAT) |
| 2 | Agent-Based | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Medium-Low | Perfect (WHO) |
| 3 | Tool-Based | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | High | Perfect (HOW) |
| 4 | Domain-Based | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Low | Good (Domain) |
| 5 | Orchestrator-Based | ⭐⭐ | ⭐⭐⭐ | Low | Good (Router) |

---

## 🎯 **Recommended Implementation Strategy**

### Phase 1: Skill Commands (Rank 1) ✅ **DO THIS FIRST**
Create 5 skill-based commands that map directly to user workflows:
1. `/app/planning` - Research & plan with QA
2. `/app/implementation` - Generate & implement code
3. `/app/review` - Create PR & validate
4. `/app/research-and-plan` - Research topic + plan
5. `/app/execute-planning` - Plan feature with GAM

### Phase 2: Agent Commands (Rank 2)
Create 5 agent-based commands for flexible agent invocation:
1. `/app/agent-planner`
2. `/app/agent-coder`
3. `/app/agent-critic`
4. `/app/agent-structured`
5. `/app/agent-router`

### Phase 3: Tool Commands (Rank 3)
Create 6 tool-based commands for fine-grained control:
1. `/app/tool-gam`
2. `/app/tool-coder`
3. `/app/tool-package`
4. `/app/tool-search`
5. `/app/tool-computer`
6. `/app/tool-thinking`

### Phase 4: Domain Commands (Rank 4) - Optional
Only if users need direct domain access:
1. `/app/gam-memory`
2. `/app/code-generator`
3. `/app/autonomous-research`
4. `/app/agent-task`

### Phase 5: Orchestrator Commands (Rank 5) - Skip or Refactor
Likely not needed since `/run-agent-task` already exists. Consider refactoring existing commands instead.

---

## 🔍 **Key Insights**

1. **Skill-based commands provide the most value** because they map directly to user workflows and align with DDD's "WHAT" layer.

2. **Agent-based commands enable flexibility** by allowing users to invoke specific agents (planner, coder, critic) with custom prompts.

3. **Tool-based commands provide granular control** for power users who want to compose workflows from primitives.

4. **Domain commands are already wrapped** by tools/skills, so direct exposure has limited value unless users need pure domain logic.

5. **Orchestrator commands overlap** with existing `/run-agent-task` and `/execute-workflow`, so they're lower priority.

---

## ✅ **Next Steps**

Would you like me to:
1. **Implement Phase 1 (Skill Commands)** - Create 5 skill-based commands now?
2. **Create detailed command specs** for all 5 ranks?
3. **Refactor existing commands** to align with this decomposition?
4. **Update command registry** with new numbering scheme?

Let me know which direction you'd like to proceed!
