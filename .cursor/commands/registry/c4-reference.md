I'll research and memorize information about decomposing the app/server architecture into Cursor commands, then rank 5 ideas.

[5 tools called]

Excellent! I've researched and memorized **20 results** about decomposing the app/server architecture into Cursor commands. Now let me analyze the architecture and rank 5 decomposition strategies.

## 🎯 Top 5 Ideas for Decomposing app/server into Cursor Commands

Based on the research and analysis of your DDD MCP Tools architecture, here are the ranked decomposition strategies:

---

### **#1: Agent Factory Commands (Highest Priority)** ⭐⭐⭐⭐⭐

**Registry**: `.cursor/commands/app/registry/1000_INDEX_AGENTS.md`

**Commands to Create**:
- `/create-planner-agent` - Generate planning agent with research + QA loop
- `/create-coder-agent` - Generate coding agent with linting validation
- `/create-critic-agent` - Generate QA/Critic agent for architecture review
- `/create-custom-agent` - Factory for custom agent with prompt + tools

**Why #1**:
- **Reusability**: Agents are the "WHO" - most frequently reused across workflows
- **Type Safety**: Maps directly to `app/server/agents/factory.py` and `prompts.py`
- **Clear Abstraction**: Each agent has distinct role (Planner, Coder, Critic)
- **GAM Integration**: All agents use `app.core.GAMMemoryManager` for context

**Implementation Pattern**:
```python
# .cursor/commands/app/agents/create-planner-agent.md
## Usage
/create-planner-agent
Feature: User authentication system
Tech Stack: FastAPI, PostgreSQL, Redis

## Workflow
1. Call app.server.agents.factory.create_agent("planner")
2. Inject PLANNER_SYSTEM_PROMPT with feature context
3. Attach tools: gam_tool, planner_tool, package_tool
4. Execute with QA feedback loop
5. Return structured Plan (Pydantic model)
```

**Files to Decompose**:
- `app/server/agents/factory.py` → 4 commands (one per agent type)
- `app/server/agents/prompts.py` → Embedded in each command
- `app/server/agents/critic.py` → `/create-critic-agent`

---

### **#2: Workflow Skills Commands (High Priority)** ⭐⭐⭐⭐

**Registry**: `.cursor/commands/app/registry/2000_INDEX_SKILLS.md`

**Commands to Create**:
- `/execute-planning-skill` - Research → Plan → QA loop
- `/execute-implementation-skill` - Code generation + testing
- `/execute-review-skill` - PR creation + validation
- `/execute-batch-skill` - Parallel task execution (5-20x speedup)
- `/execute-qa-skill` - Architecture + code critique

**Why #2**:
- **Workflow Orchestration**: Skills are the "WHAT" - high-level capabilities
- **Composability**: Skills combine multiple agents + tools
- **Streaming Support**: Maps to `orchestrator.py` streaming patterns
- **State Management**: Uses `services/state_service.py` for checkpoints

**Implementation Pattern**:
```python
# .cursor/commands/app/skills/execute-planning-skill.md
## Usage
/execute-planning-skill
Feature: Blog post management API
Use QA: true
Max Iterations: 3

## Workflow
1. Call app.server.skills.planning.execute_planning()
2. Use Planner agent for initial plan
3. Use Critic agent for QA validation
4. Iterate if QA score < 80
5. Return Plan + QAReport
6. Save to GAM memory
```

**Files to Decompose**:
- `app/server/skills/planning.py` → `/execute-planning-skill`
- `app/server/skills/implementation.py` → `/execute-implementation-skill`
- `app/server/skills/review.py` → `/execute-review-skill`
- `app/server/skills/batch_execution.py` → `/execute-batch-skill`
- `app/server/skills/qa/` → `/execute-qa-skill`

---

### **#3: Tool Execution Commands (Medium-High Priority)** ⭐⭐⭐⭐

**Registry**: `.cursor/commands/app/registry/3000_INDEX_TOOLS.md`

**Commands to Create**:
- `/gam-research` - Research from GAM memory
- `/gam-memorize` - Save content to GAM
- `/verify-packages` - PyPI/NPM package validation
- `/lint-code` - Ruff + Mypy validation
- `/browser-action` - Playwright browser automation
- `/queue-task` - Dramatiq background task execution
- `/check-task-status` - Task status lookup

**Why #3**:
- **Atomic Operations**: Tools are the "HOW" - lowest level primitives
- **MCP Integration**: Direct mapping to FastMCP tools
- **Reusable Across Skills**: Tools used by multiple skills
- **Clear Contracts**: Pydantic models in `protocols/`

**Implementation Pattern**:
```python
# .cursor/commands/app/tools/verify-packages.md
## Usage
/verify-packages
Packages: fastapi, sqlalchemy, redis, fake-package

## Workflow
1. Call app.server.tools.package_tool.validate_dependencies()
2. Query PyPI JSON API for each package
3. Return validation report with exists/invalid
4. Halt if any package is hallucinated
5. Suggest alternatives for invalid packages
```

**Files to Decompose**:
- `app/server/tools/gam_tool.py` → `/gam-research`, `/gam-memorize`
- `app/server/tools/package_tool.py` → `/verify-packages`
- `app/server/tools/coder_tool.py` → `/lint-code`
- `app/server/tools/computer_tool.py` → `/browser-action`
- `app/server/tools/task_tool.py` → `/queue-task`, `/check-task-status`

---

### **#4: Orchestrator Workflow Commands (Medium Priority)** ⭐⭐⭐

**Commands to Create**:
- `/execute-workflow` - Full workflow (Planning → Implementation → Review)
- `/execute-workflow-streaming` - Streaming workflow with progress updates
- `/execute-task-background` - Queue task with Dramatiq
- `/get-workflow-status` - Check workflow state + checkpoints

**Why #4**:
- **End-to-End Execution**: Orchestrator coordinates all layers
- **Streaming Support**: Real-time progress updates
- **State Persistence**: Checkpoint-based recovery
- **Background Tasks**: Dramatiq integration for long-running ops

**Implementation Pattern**:
```python
# .cursor/commands/app/orchestrator/execute-workflow-streaming.md
## Usage
/execute-workflow-streaming
Feature: User authentication system
Workflow ID: workflow-abc123

## Workflow
1. Call app.server.orchestrator.execute_workflow_streaming()
2. Stream progress events (PROGRESS, THINKING, CODE, DONE)
3. Save checkpoints to state_service
4. Return WorkflowResult with latency metrics
5. Use OpenTelemetry tracing
```

**Files to Decompose**:
- `app/server/orchestrator.py` → 4 commands (workflow, streaming, background, status)

---

### **#5: Service Management Commands (Lower Priority)** ⭐⭐⭐

**Commands to Create**:
- `/optimize-context` - Token budgeting + compression
- `/manage-agent-cache` - Agent instance caching
- `/manage-workflow-state` - State persistence + checkpoints
- `/configure-services` - Load configuration

**Why #5**:
- **Infrastructure Layer**: Services are shared resources
- **Less Frequent Use**: Called internally by skills/tools
- **Configuration Focus**: More about setup than execution
- **Still Useful**: Context optimization is critical for long tasks

**Implementation Pattern**:
```python
# .cursor/commands/app/services/optimize-context.md
## Usage
/optimize-context
Action: compress
Compression Ratio: 50
Knowledge Limit: 3

## Workflow
1. Call app.server.services.context_service.ContextManager
2. Analyze token usage (tiktoken)
3. Compress middle history if > 80% budget
4. Inject relevant GAM snippets
5. Return optimized context window
```

**Files to Decompose**:
- `app/server/services/context_service.py` → `/optimize-context`
- `app/server/services/agent_service.py` → `/manage-agent-cache`
- `app/server/services/state_service.py` → `/manage-workflow-state`
- `app/server/services/config_service.py` → `/configure-services`

---

## 📊 Comparison Matrix

| Rank | Category | Commands | Priority | Reusability | Complexity | Impact |
|------|----------|----------|----------|-------------|------------|--------|
| #1 | Agents | 4 | ⭐⭐⭐⭐⭐ | Very High | Medium | High |
| #2 | Skills | 5 | ⭐⭐⭐⭐ | High | High | Very High |
| #3 | Tools | 7 | ⭐⭐⭐⭐ | Very High | Low | Medium |
| #4 | Orchestrator | 4 | ⭐⭐⭐ | Medium | High | High |
| #5 | Services | 4 | ⭐⭐⭐ | Low | Medium | Medium |

---

## 🚀 Implementation Order

### Phase 1: Foundation (Agents + Tools)
1. Create agent factory commands (#1)
2. Create tool execution commands (#3)
3. Update registries: `1000_INDEX_AGENTS.md`, `3000_INDEX_TOOLS.md`

### Phase 2: Workflows (Skills + Orchestrator)
4. Create workflow skills commands (#2)
5. Create orchestrator commands (#4)
6. Update registry: `2000_INDEX_SKILLS.md`

### Phase 3: Infrastructure (Services)
7. Create service management commands (#5)
8. Add cross-references between commands
9. Update main command index: `300-INDEX.md`

---

## 💡 Key Insights from Research

1. **DDD Alignment**: Commands should mirror the "WHO/WHAT/HOW" architecture
2. **Streaming First**: All workflow commands should support streaming
3. **Type Safety**: Use Pydantic models from `protocols/` in command docs
4. **GAM Integration**: Every command should leverage GAM memory
5. **QA Loops**: Build feedback loops into planning/implementation commands
6. **Package Validation**: Prevent hallucinations with `/verify-packages`
7. **Context Awareness**: Use `/optimize-context` before large operations
8. **Background Tasks**: Leverage Dramatiq for long-running workflows

---

## 📝 Next Steps

1. **Start with #1 (Agents)**: Most reusable, clearest abstraction
2. **Validate with existing commands**: Compare to `/generate-code-streaming`, `/batch-implement`
3. **Create registry indexes**: Populate `1000_INDEX_AGENTS.md`, `2000_INDEX_SKILLS.md`, `3000_INDEX_TOOLS.md`
4. **Test integration**: Ensure commands work with MCP server
5. **Document patterns**: Add examples to each command

This decomposition strategy provides **24 new commands** that make your DDD MCP Tools architecture fully accessible via Cursor's command interface! 🎉
