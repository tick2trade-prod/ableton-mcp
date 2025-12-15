# Tool Execution Commands Registry

**Index Range**: 3000-3999
**Category**: Tools (THE "HOW")
**Purpose**: Atomic operations and execution primitives

---

## Overview

Tool execution commands provide low-level primitives for agents and skills. Each tool performs a specific, well-defined operation with clear inputs and outputs.

---

## Tool Commands

### 3001: GAM Research

**Command**: `/gam-research`
**File**: `.cursor/commands/app/tools/gam-research.md`
**Purpose**: Research from GAM memory using semantic search
**Status**: ✅ Active

**Key Features**:
- Semantic search with embeddings
- BM25 + vector search
- Similarity scoring
- Fast, local token usage

**Implementation**: `app.core.GAMMemoryManager.research()`

**Related**: `/gam-memorize`, `/deep-research`

---

### 3002: GAM Memorize

**Command**: `/gam-memorize`
**File**: `.cursor/commands/app/tools/gam-memorize.md`
**Purpose**: Save content to GAM long-term memory
**Status**: ✅ Active

**Key Features**:
- Persistent storage
- Semantic indexing
- Tag-based categorization
- Cross-session persistence

**Implementation**: `app.core.GAMMemoryManager.memorize()`

**Related**: `/gam-research`, `/371-research-memorize`

---

### 3003: Verify Packages

**Command**: `/verify-packages`
**File**: `.cursor/commands/app/tools/verify-packages.md`
**Purpose**: Verify package dependencies (PyPI/NPM)
**Status**: ✅ Active

**Key Features**:
- PyPI JSON API integration
- NPM Registry integration
- Hallucination detection
- Version validation
- Alternative suggestions

**Implementation**: `app.server.tools.package_tool.validate_dependencies()`

**Related**: `/validate-architecture`, `/create-critic-agent`

---

### 3004: Lint Code

**Command**: `/lint-code`
**File**: `.cursor/commands/app/tools/lint-code.md`
**Purpose**: Run Ruff linting + Mypy type checking
**Status**: ✅ Active

**Key Features**:
- Ruff linting (10-100x faster)
- Mypy type checking
- Auto-fix support
- Line-specific issues
- Comprehensive rules

**Implementation**: `app.server.tools.coder_tool.robust_file_write()`

**Related**: `/create-coder-agent`, `/optimize-imports`

---

### 3005: Browser Action

**Command**: `/browser-action`
**File**: `.cursor/commands/app/tools/browser-action.md`
**Purpose**: Browser automation with Playwright
**Status**: ✅ Active

**Key Features**:
- Navigate, click, type, screenshot, scroll
- Headless Chromium
- Element interaction
- Screenshot capture
- Computer Use capability

**Implementation**: `app.server.tools.computer_tool.browser_action()`

**Related**: `/deep-research`, `/execute-qa-skill`

---

### 3006: Queue Task

**Command**: `/queue-task`
**File**: `.cursor/commands/app/tools/queue-task.md`
**Purpose**: Queue background task with Dramatiq
**Status**: ✅ Active

**Key Features**:
- Dramatiq + Redis integration
- Priority-based queuing
- Async execution
- Result storage
- Retry logic

**Implementation**: `app.server.tools.task_tool.queue_task()`

**Related**: `/check-task-status`, `/execute-task-background`

---

### 3007: Check Task Status

**Command**: `/check-task-status`
**File**: `.cursor/commands/app/tools/check-task-status.md`
**Purpose**: Check background task status and result
**Status**: ✅ Active

**Key Features**:
- Redis result backend
- Status tracking (queued, running, completed, failed)
- Progress monitoring
- Result retrieval
- Error details

**Implementation**: `app.server.tools.task_tool.get_task_status()`

**Related**: `/queue-task`, `/execute-workflow`

---

## Tool Architecture

### Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **Memory** | gam-research, gam-memorize | GAM operations |
| **Validation** | verify-packages, lint-code | Quality checks |
| **Automation** | browser-action | Computer Use |
| **Async** | queue-task, check-task-status | Background execution |

### Tool Integration

```python
# app/server/tools/ structure
tools/
├── gam_tool.py          # GAM memory operations
├── package_tool.py      # Package verification
├── coder_tool.py        # Code generation + linting
├── computer_tool.py     # Browser automation
├── task_tool.py         # Background tasks
├── planner_tool.py      # Planning workflows
├── workflow_tool.py     # Workflow execution
├── mcp_client.py        # MCP client
├── fallback.py          # Local fallback tools
└── search.py            # Codebase search
```

### MCP Integration

Tools are exposed via FastMCP:
- `app.mcp_server` - Main MCP server
- `@mcp.tool` decorator - Tool registration
- Pydantic models - Type safety

---

## Implementation Details

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| GAM Tool | `app/server/tools/gam_tool.py` | Memory operations |
| Package Tool | `app/server/tools/package_tool.py` | Package validation |
| Coder Tool | `app/server/tools/coder_tool.py` | Code generation |
| Computer Tool | `app/server/tools/computer_tool.py` | Browser automation |
| Task Tool | `app/server/tools/task_tool.py` | Background tasks |

### Protocol Models

Located in `app/server/protocols/`:
- `tool_models.py` - Browser automation models
- `task_models.py` - Background task models
- `models.py` - Core workflow models

---

## Usage Patterns

### Tool Composition

```python
# Skills compose multiple tools
async def execute_planning_skill():
    # 1. Research from memory
    context = await gam_research(query)

    # 2. Verify packages
    validation = await verify_packages(deps)

    # 3. Generate plan
    plan = await create_plan(context)

    return plan
```

### Tool Chaining

```
/gam-research → /verify-packages → /create-planner-agent → /lint-code
```

---

## Best Practices

1. **Memory First**: Always use `/gam-research` before web search
2. **Validate Early**: Run `/verify-packages` before implementation
3. **Lint Often**: Use `/lint-code` during development
4. **Background Long Tasks**: Use `/queue-task` for > 30s operations
5. **Browser Wisely**: Use `/browser-action` for dynamic content only
6. **Check Status**: Monitor `/check-task-status` for queued tasks

---

## Performance Characteristics

| Tool | Latency | Throughput | Use Case |
|------|---------|------------|----------|
| gam-research | <100ms | High | Memory lookup |
| gam-memorize | <200ms | Medium | Memory storage |
| verify-packages | <500ms | Medium | API queries |
| lint-code | <100ms | High | Ruff linting |
| browser-action | 1-5s | Low | Web automation |
| queue-task | <50ms | Very High | Task queuing |
| check-task-status | <50ms | Very High | Status check |

---

## Related Registries

- **1000: Agents Registry** - Agents that use these tools
- **2000: Skills Registry** - Skills that compose tools
- **300: Main Command Index** - All commands

---

## Next Steps

- [ ] Add tool performance metrics
- [ ] Implement tool caching
- [ ] Add tool composition patterns
- [ ] Create tool templates
- [ ] Add tool error handling

---

**Last Updated**: 2024-12-04
**Total Commands**: 7
**Status**: Phase 1 Complete ✅
