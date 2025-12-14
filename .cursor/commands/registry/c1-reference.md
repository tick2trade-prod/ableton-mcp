I'll analyze the app/server files and rank 5 ideas for decomposing them into cursor commands. Let me first read the key files to understand the architecture.

[6 tools called]

Now let me read the RECOMMENDATIONS.md file to understand the complete picture:

[1 tool called]

Now I have a complete understanding. Let me analyze the architecture and rank 5 ideas for decomposing the `app/server` files into cursor commands. Based on the `/batch-implement` command pattern and the existing command structure, here are my ranked recommendations:

## 🎯 Top 5 Ideas for Decomposing `app/server` into Cursor Commands

### **Rank 1: Workflow-Based Commands** ⭐⭐⭐⭐⭐
**Best fit for the architecture**

Decompose by complete workflows that map to the DDD skills layer:

```
.cursor/commands/app/
├── workflow-research.md       # Research → Plan → Memorize
├── workflow-implement.md      # Plan → Code → Test → Review
├── workflow-qa-loop.md        # Generate → Critique → Fix → Validate
├── workflow-batch-code.md     # Parallel code generation (existing)
└── workflow-full-feature.md   # End-to-end: Research → Implement → Deploy
```

**Why Rank 1:**
- ✅ Maps directly to `app/server/skills/` architecture
- ✅ Aligns with existing commands (`/deep-research`, `/generate-code`)
- ✅ Users think in workflows, not files
- ✅ Each command is a complete, testable unit
- ✅ Enables parallel execution within workflows

**Example Implementation:**
```markdown
# workflow-implement.md
## Overview
Complete implementation workflow: Planning → Coding → Testing → Review

## Workflow Steps
1. Call `/app/run-agent-task` with action=PLAN
2. Call `/batch-implement` for parallel file generation
3. Run tests automatically
4. Call `/qa-critic` for validation
5. Create PR if all pass

## Usage
/workflow-implement Feature: User authentication with JWT
```

---

### **Rank 2: Layer-Based Commands** ⭐⭐⭐⭐
**Clean separation of concerns**

Decompose by DDD layers (WHO/WHAT/HOW):

```
.cursor/commands/app/
├── agent-planner.md          # WHO: Create planner agent
├── agent-coder.md            # WHO: Create coder agent
├── agent-critic.md           # WHO: Create QA agent
├── skill-planning.md         # WHAT: Execute planning workflow
├── skill-implementation.md   # WHAT: Execute coding workflow
├── tool-gam-memory.md        # HOW: GAM operations
├── tool-package-verify.md    # HOW: PyPI/NPM verification
└── tool-browser.md           # HOW: Computer use/browser automation
```

**Why Rank 2:**
- ✅ Perfect DDD alignment
- ✅ Each command is a single responsibility
- ✅ Easy to test and maintain
- ✅ Clear boundaries between layers
- ⚠️ Users may need to chain multiple commands

**Example Implementation:**
```markdown
# skill-planning.md
## Overview
Execute planning skill with QA feedback loop

## Parameters
- feature_name: Feature to plan
- use_web_search: Enable Tavily search (default: true)
- max_qa_iterations: QA loop iterations (default: 3)

## Calls
1. app.server.skills.planning.execute_planning()
2. app.server.skills.qa.plan_critic.critique_plan()
3. Iterate until plan passes QA

## Usage
/skill-planning feature_name="User auth" use_web_search=true
```

---

### **Rank 3: Feature-Based Commands** ⭐⭐⭐⭐
**User-centric approach**

Decompose by high-level features users want to accomplish:

```
.cursor/commands/app/
├── feature-scaffold.md       # Scaffold complete feature structure
├── feature-refactor.md       # Refactor existing code
├── feature-test.md           # Generate tests for feature
├── feature-document.md       # Generate docs for feature
├── feature-optimize.md       # Performance optimization
└── feature-security.md       # Security audit and fixes
```

**Why Rank 3:**
- ✅ User-friendly, intent-based
- ✅ Hides implementation complexity
- ✅ Easy to discover and use
- ⚠️ May require complex orchestration internally
- ⚠️ Less granular control

**Example Implementation:**
```markdown
# feature-scaffold.md
## Overview
Scaffold complete feature with models, services, API, tests

## Parameters
- feature: Feature description
- language: python|typescript (default: python)
- include_tests: Generate tests (default: true)
- include_docs: Generate docs (default: true)

## Workflow
1. Research feature requirements
2. Generate plan with file structure
3. Batch implement all files
4. Run tests
5. Generate documentation

## Usage
/feature-scaffold feature="Blog post CRUD API" language=python
```

---

### **Rank 4: Atomic Operation Commands** ⭐⭐⭐
**Maximum granularity**

Decompose into smallest possible operations:

```
.cursor/commands/app/
├── op-gam-memorize.md        # Memorize single item
├── op-gam-search.md          # Search GAM memory
├── op-file-write.md          # Write single file
├── op-file-lint.md           # Lint single file
├── op-test-run.md            # Run specific test
├── op-package-check.md       # Verify package exists
├── op-browser-navigate.md    # Navigate to URL
└── op-browser-screenshot.md  # Take screenshot
```

**Why Rank 4:**
- ✅ Maximum composability
- ✅ Easy to test individual operations
- ✅ Clear, single-purpose commands
- ⚠️ Too granular for most users
- ⚠️ Requires many chained commands for workflows
- ⚠️ High cognitive load

**Example Implementation:**
```markdown
# op-file-write.md
## Overview
Write single file with linting and validation

## Parameters
- filepath: Target file path
- content: File content
- run_lint: Run linter after write (default: true)
- backup: Create backup (default: true)

## Calls
app.server.tools.coder_tool.robust_file_write()

## Usage
/op-file-write filepath="app/models/user.py" content="..." run_lint=true
```

---

### **Rank 5: Hybrid Registry + Execution Commands** ⭐⭐⭐
**Balance between discovery and execution**

Combine existing registries with execution commands:

```
.cursor/commands/app/registry/
├── 1000_INDEX_AGENTS.md      # ✅ Already exists
├── 2000_INDEX_SKILLS.md      # ✅ Already exists
├── 3000_INDEX_TOOLS.md       # ✅ Already exists
└── 4000_INDEX_WORKFLOWS.md   # NEW: Workflow registry

.cursor/commands/app/execute/
├── exec-agent.md             # Execute any agent by ID
├── exec-skill.md             # Execute any skill by ID
├── exec-tool.md              # Execute any tool by ID
└── exec-workflow.md          # Execute any workflow by ID
```

**Why Rank 5:**
- ✅ Leverages existing registry structure
- ✅ Good for discovery (browse registry, then execute)
- ✅ Flexible execution model
- ⚠️ Two-step process (discover → execute)
- ⚠️ Less intuitive than direct commands
- ⚠️ Requires maintaining registry + execution logic

**Example Implementation:**
```markdown
# exec-skill.md
## Overview
Execute any skill from the 2000_INDEX_SKILLS registry

## Parameters
- skill_id: Skill ID from registry (e.g., "2001")
- params: Skill-specific parameters (JSON)

## Usage
/exec-skill skill_id="2001" params='{"feature_name": "User auth"}'

## Available Skills
See .cursor/commands/app/registry/2000_INDEX_SKILLS.md
```

---

## 📊 Comparison Matrix

| Rank | Approach | Usability | Maintainability | DDD Alignment | Composability | Complexity |
|------|----------|-----------|-----------------|---------------|---------------|------------|
| 1 | Workflow-Based | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 2 | Layer-Based | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 3 | Feature-Based | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 4 | Atomic Operations | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| 5 | Hybrid Registry | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 Final Recommendation

**Implement Rank 1 (Workflow-Based) + Rank 2 (Layer-Based) Hybrid:**

1. **Primary Commands** (Workflow-Based):
   - `/workflow-research` - Research and memorize
   - `/workflow-implement` - Plan → Code → Test
   - `/workflow-qa-loop` - Generate → Critique → Fix
   - `/workflow-full-feature` - End-to-end feature

2. **Building Block Commands** (Layer-Based):
   - `/agent-planner`, `/agent-coder`, `/agent-critic`
   - `/skill-planning`, `/skill-implementation`, `/skill-review`
   - `/tool-gam`, `/tool-package-verify`, `/tool-browser`

3. **Keep Existing Commands**:
   - `/batch-implement` (already excellent)
   - `/deep-research`, `/autonomous-research`
   - `/generate-code`, `/generate-code-streaming`
   - `/qa-critic`, `/memorize-content`

This hybrid approach provides:
- ✅ High-level workflows for common tasks (80% use case)
- ✅ Low-level building blocks for custom workflows (20% use case)
- ✅ Perfect DDD alignment
- ✅ Maximum flexibility and composability

Would you like me to implement this hybrid approach by creating the workflow and layer-based command files?
