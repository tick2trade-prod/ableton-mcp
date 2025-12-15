I'll analyze the app/server core logic files and rank 5 ideas for decomposing them into Cursor commands, using the streaming code generation workflow.

[6 tools called]

Now I'll analyze the app/server core logic and rank 5 ideas for decomposing each file into Cursor commands, using the streaming code generation workflow as the template.

## 🎯 Top 5 Ideas for Decomposing `app/server/` Core Logic into Cursor Commands

Based on analyzing the architecture and existing commands, here are the ranked ideas:

---

### **Rank 1: `/workflow-orchestration` - Workflow Execution Command** ⭐⭐⭐⭐⭐

**Decompose:** `orchestrator.py` → Cursor command for executing complete workflows

**Why #1:**
- **High Impact**: Core orchestration logic used by all other features
- **Streaming Native**: Already has `execute_workflow_streaming()` - perfect fit
- **Reusable**: Every feature needs workflow orchestration
- **Low Latency**: Streaming progress updates reduce perceived wait time

**Command Structure:**
```markdown
# Workflow Orchestration

## Overview
Execute complete workflows with streaming progress updates and checkpoint management.

## Parameters
- `feature_name`: Feature to implement (required)
- `workflow_id`: Optional workflow ID for resuming
- `mode`: Execution mode (full, planning_only, implementation_only)
- `stream`: Enable streaming progress (default: true)

## Workflow
1. **Context Check**: Verify token budget before starting
2. **Planning Phase**: Stream planning progress with GAM memory lookup
3. **Implementation Phase**: Stream code generation with checkpoints
4. **QA Loop**: Auto-validate with critic agent
5. **State Management**: Save checkpoints for resumability

## Example
/workflow-orchestration
Feature: User authentication system
Mode: full
Stream: true
```

**Extracted from:**
- `orchestrator.py` lines 220-369 (`execute_workflow_streaming`)
- `orchestrator.py` lines 117-218 (`execute_workflow`)

---

### **Rank 2: `/task-execution` - Action-Based Task Router** ⭐⭐⭐⭐

**Decompose:** `orchestrator.py::execute_task()` → Command for routing tasks by action type

**Why #2:**
- **Clear Routing**: Maps ActionStep enum to appropriate skills
- **Background Support**: Already has Dramatiq integration
- **Flexible**: Supports research, plan, code, execute modes
- **Performance Tracking**: Built-in latency measurement

**Command Structure:**
```markdown
# Task Execution

## Overview
Execute tasks with specific action modes (research, plan, code, execute).

## Parameters
- `task`: Task description (required)
- `action`: Action mode (research, plan, code, execute)
- `language`: Programming language (default: python)
- `background`: Queue for background execution (default: false)

## Workflow
1. **Action Routing**: Route to appropriate skill based on action
2. **Research Mode**: Use `research_and_plan` skill with web search
3. **Plan Mode**: Use `execute_planning` skill with GAM memory
4. **Code Mode**: Use `generate_and_implement` skill
5. **Execute Mode**: Full workflow execution

## Example
/task-execution
Task: Create REST API endpoint
Action: code
Language: python
Background: false
```

**Extracted from:**
- `orchestrator.py` lines 51-115 (`execute_task`)
- `orchestrator.py` lines 31-48 (`execute_task_background`)

---

### **Rank 3: `/agent-factory` - Dynamic Agent Creation** ⭐⭐⭐⭐

**Decompose:** `agents/factory.py` + `agents/router.py` → Command for creating specialized agents

**Why #3:**
- **Agent Specialization**: Creates planner, coder, critic agents
- **Model Routing**: Intelligent Ollama model selection
- **Prompt Management**: Centralized system prompts
- **Caching**: Agent service caching for performance

**Command Structure:**
```markdown
# Agent Factory

## Overview
Create specialized agents (planner, coder, critic) with appropriate prompts and tools.

## Parameters
- `agent_type`: Agent type (planner, coder, critic, researcher)
- `model`: Optional model override (default: auto-select)
- `temperature`: Creativity level (0.0-1.0)
- `tools`: Additional tools to provide

## Workflow
1. **Agent Selection**: Choose agent type based on task
2. **Model Routing**: Select best Ollama model for agent
3. **Prompt Loading**: Load system prompts from templates
4. **Tool Binding**: Attach appropriate tools (GAM, coder, planner)
5. **Caching**: Cache agent instance for reuse

## Example
/agent-factory
Agent Type: coder
Model: qwen2.5-coder:32b
Temperature: 0.2
Tools: [coder_tool, gam_tool, package_tool]
```

**Extracted from:**
- `agents/factory.py` (agent creation logic)
- `agents/router.py` (model routing)
- `agents/prompts.py` (system prompts)

---

### **Rank 4: `/qa-validation` - Quality Assurance Loop** ⭐⭐⭐

**Decompose:** `skills/qa/` → Command for running QA validation on plans/code

**Why #4:**
- **Quality Control**: Critical for preventing hallucinations
- **Multi-Dimensional**: Architecture, package, syntax, security checks
- **Critic Agent**: Uses "Senior Architect" agent for validation
- **Feedback Loop**: Auto-retry with fixes

**Command Structure:**
```markdown
# QA Validation

## Overview
Run quality assurance checks on plans or code using critic agent.

## Parameters
- `target`: What to validate (plan, code, architecture)
- `content`: Content to validate (file path or inline)
- `dimensions`: QA dimensions to check (default: all)
- `auto_fix`: Attempt auto-fix on failures (default: false)

## Workflow
1. **Dimension Selection**: Choose QA dimensions based on target
2. **Critic Agent**: Create critic agent with validation prompts
3. **Package Verification**: Check for hallucinated libraries
4. **Syntax Validation**: Run linting/type checking
5. **Security Scan**: Check for security issues
6. **Feedback Generation**: Generate actionable critique

## Example
/qa-validation
Target: code
Content: @app/server/orchestrator.py
Dimensions: [syntax, security, architecture]
Auto Fix: true
```

**Extracted from:**
- `skills/qa/plan_critic.py` (architecture validation)
- `skills/qa/code_critic.py` (syntax/security validation)
- `agents/critic.py` (critic agent)

---

### **Rank 5: `/context-optimization` - Token Budget Management** ⭐⭐⭐

**Decompose:** `services/context_service.py` → Command for managing context windows

**Why #5:**
- **Token Awareness**: Prevents context overflow crashes
- **Compression**: Automatic history compression using GAM
- **Sliding Window**: Preserves system + recent messages
- **Budget Tracking**: Real-time token counting with tiktoken

**Command Structure:**
```markdown
# Context Optimization

## Overview
Manage token budgets and compress conversation history to prevent context overflow.

## Parameters
- `max_tokens`: Maximum token budget (default: 128000)
- `compression_threshold`: Trigger compression at % usage (default: 80)
- `preserve_messages`: Number of recent messages to keep (default: 10)
- `summarize`: Use GAM to summarize compressed history (default: true)

## Workflow
1. **Token Counting**: Count current context usage with tiktoken
2. **Budget Check**: Alert if approaching limit (>80%)
3. **Compression Trigger**: Auto-compress when threshold exceeded
4. **Sliding Window**: Keep system prompt + recent messages
5. **GAM Summarization**: Summarize compressed history to GAM

## Example
/context-optimization
Max Tokens: 128000
Compression Threshold: 80
Preserve Messages: 10
Summarize: true
```

**Extracted from:**
- `services/context_service.py` (token budgeting, compression)
- `app/core/gam_memory.py` (summarization)

---

## 📊 Comparison Matrix

| Rank | Command | Impact | Reusability | Complexity | Streaming | DDD Alignment |
|------|---------|--------|-------------|------------|-----------|---------------|
| 1 | `/workflow-orchestration` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Native | ✅ Perfect |
| 2 | `/task-execution` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⚠️ Partial | ✅ Good |
| 3 | `/agent-factory` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ No | ✅ Perfect |
| 4 | `/qa-validation` | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⚠️ Partial | ✅ Good |
| 5 | `/context-optimization` | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ No | ✅ Good |

---

## 🎯 Implementation Priority

**Phase 1 (Immediate):**
1. `/workflow-orchestration` - Core workflow execution
2. `/task-execution` - Task routing

**Phase 2 (Short-term):**
3. `/agent-factory` - Agent specialization
4. `/qa-validation` - Quality control

**Phase 3 (Enhancement):**
5. `/context-optimization` - Token management

---

## 🔗 Integration with Existing Commands

These new commands complement existing ones:

- `/generate-code-streaming` → Uses `/task-execution` (action=code)
- `/deep-research` → Uses `/task-execution` (action=research)
- `/run-agent-task` → Uses `/workflow-orchestration`
- `/validate-architecture` → Uses `/qa-validation`
- `/smart-context` → Uses `/context-optimization`

This decomposition creates a **composable command library** where complex workflows are built from simpler primitives, following the DDD MCP Tools architecture! 🚀
