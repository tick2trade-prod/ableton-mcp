# Workflow Commands Registry

**Index Range**: 5000-5999
**Category**: Workflow Commands
**Purpose**: End-to-end workflows for PR completion in startup environments

---

## Overview

Workflow commands orchestrate multiple agents, skills, and tools to complete complex software engineering tasks. All workflows integrate with the autonomous agent architecture in `@app`.

---

## Workflow Categories

### 🤖 C5: Autonomous PR Workflows (5100-5119)

**Location**: `.cursor/commands/app/c5/`
**Purpose**: 20 production-ready workflows for GitHub PR completion
**Status**: ✅ Complete

#### Automation & Intelligence (5100-5104)

| ID | Command | File | Purpose | Complexity |
|----|---------|------|---------|------------|
| 5100 | `/workflow-auto-pr-create` | `c5/workflow-auto-pr-create.md` | Automated PR creation with intelligent reviewer assignment | Low |
| 5101 | `/workflow-ai-code-review` | `c5/workflow-ai-code-review.md` | Context-aware code review with improvement suggestions | Medium |
| 5102 | `/workflow-multi-agent-dev` | `c5/workflow-multi-agent-dev.md` | Multi-agent collaborative development (Agile/TDD) | High |
| 5103 | `/workflow-security-scan` | `c5/workflow-security-scan.md` | Security-enhanced code generation with vulnerability detection | Medium |
| 5104 | `/workflow-agile-sprint` | `c5/workflow-agile-sprint.md` | Agile methodology integration with AI role assignment | Medium |

#### Standards & Documentation (5105-5109)

| ID | Command | File | Purpose | Complexity |
|----|---------|------|---------|------------|
| 5105 | `/workflow-pr-templates` | `c5/workflow-pr-templates.md` | Standardized PR templates enforcement | Low |
| 5106 | `/workflow-pr-summary` | `c5/workflow-pr-summary.md` | Automated PR summarization for quick review | Low |
| 5107 | `/workflow-code-scan` | `c5/workflow-code-scan.md` | Real-time code scanning for vulnerabilities | Medium |
| 5108 | `/workflow-context-suggestions` | `c5/workflow-context-suggestions.md` | Context-aware code suggestions aligned with architecture | Medium |
| 5109 | `/workflow-auto-tests` | `c5/workflow-auto-tests.md` | Automated test case generation from specifications | Medium |

#### Workflow Automation (5110-5114)

| ID | Command | File | Purpose | Complexity |
|----|---------|------|---------|------------|
| 5110 | `/workflow-pr-automation` | `c5/workflow-pr-automation.md` | Complete PR workflow automation (tagging, labels, rules) | Low |
| 5111 | `/workflow-docs-sync` | `c5/workflow-docs-sync.md` | Automated documentation updates with code changes | Medium |
| 5112 | `/workflow-release-notes` | `c5/workflow-release-notes.md` | Human-quality release notes generation | Low |
| 5113 | `/workflow-infra-mgmt` | `c5/workflow-infra-mgmt.md` | Intelligent infrastructure management and scaling | High |
| 5114 | `/workflow-incident-mgmt` | `c5/workflow-incident-mgmt.md` | AI-driven incident management and resolution | High |

#### Quality & Compliance (5115-5119)

| ID | Command | File | Purpose | Complexity |
|----|---------|------|---------|------------|
| 5115 | `/workflow-compliance-check` | `c5/workflow-compliance-check.md` | Automated compliance checks and fix PRs | Medium |
| 5116 | `/workflow-onboarding` | `c5/workflow-onboarding.md` | AI-powered onboarding with personalized learning paths | Medium |
| 5117 | `/workflow-dependency-mgmt` | `c5/workflow-dependency-mgmt.md` | Automated dependency updates with risk analysis | Medium |
| 5118 | `/workflow-sprint-planning` | `c5/workflow-sprint-planning.md` | AI-enhanced sprint planning and capacity estimation | Medium |
| 5119 | `/workflow-anomaly-detect` | `c5/workflow-anomaly-detect.md` | Proactive anomaly detection and mitigation | Medium |

---

### 📋 Core Workflows (5000-5019)

**Location**: `.cursor/commands/app/`
**Purpose**: Foundational workflows for common tasks
**Status**: ✅ Active

| ID | Command | File | Purpose |
|----|---------|------|---------|
| 5000 | `/workflow-research` | `workflow-research.md` | Research → Plan → Memorize |
| 5001 | `/workflow-implement` | `workflow-implement.md` | Plan → Code → Test → Review |
| 5002 | `/workflow-qa-loop` | `workflow-qa-loop.md` | Generate → Critique → Fix → Validate |
| 5003 | `/batch-implement` | `batch-implement.md` | Parallel code generation |
| 5004 | `/workflow-full-feature` | `workflow-full-feature.md` | End-to-end: Research → Implement → Deploy |
| 5005 | `/workflow-feature-breakdown` | `workflow-feature-breakdown.md` | Break down large features into tasks |
| 5006 | `/workflow-pr-create` | `workflow-pr-create.md` | Basic PR creation |
| 5007 | `/workflow-code-review` | `workflow-code-review.md` | Code review process |
| 5008 | `/workflow-merge-deploy` | `workflow-merge-deploy.md` | Merge and deployment |
| 5009 | `/workflow-test-suite-full` | `workflow-test-suite-full.md` | Full test suite execution |

---

## Architecture Integration

All workflows integrate with:

```
app/
├── core/
│   └── gam_memory.py          # Persistent memory for learning
├── server/
│   ├── orchestrator.py        # Workflow routing
│   ├── agents/                # Agent factories (WHO)
│   │   ├── factory.py
│   │   ├── critic.py
│   │   └── prompts.py
│   ├── skills/                # Workflow capabilities (WHAT)
│   │   ├── planning.py
│   │   ├── implementation.py
│   │   └── review.py
│   └── tools/                 # Execution primitives (HOW)
│       ├── gam_tool.py
│       ├── coder_tool.py
│       └── search.py
```

---

## Usage Patterns

### Sequential Workflow
```bash
# Research → Plan → Implement → Review → PR
/workflow-research topic="User authentication"
/workflow-implement feature="User authentication"
/workflow-auto-pr-create feature_name="User authentication"
/workflow-ai-code-review pr_number=123
```

### Parallel Workflow
```bash
# Break down → Implement in parallel → Test → PR
/workflow-feature-breakdown feature="E-commerce checkout"
/batch-implement tasks="task1,task2,task3,task4,task5"
/workflow-auto-tests feature_name="E-commerce checkout"
/workflow-auto-pr-create feature_name="E-commerce checkout"
```

### Security-Critical Workflow
```bash
# Security scan → Multi-agent dev → Deep review → Compliance
/workflow-security-scan feature_name="Payment processing"
/workflow-multi-agent-dev feature_name="Payment processing" methodology="tdd"
/workflow-ai-code-review pr_number=123 focus="security,performance" depth="deep"
/workflow-compliance-check compliance_standards="pci-dss,owasp"
```

### Sprint Workflow
```bash
# Sprint planning → Agile execution → Release notes
/workflow-sprint-planning sprint_name="Sprint 24" backlog_items="JIRA-123,JIRA-124"
/workflow-agile-sprint sprint_name="Sprint 24"
/workflow-release-notes version="v2.0.0"
```

---

## Performance Characteristics

| Complexity | Avg Time | GAM Queries | Agents | Streaming | Parallelizable |
|------------|----------|-------------|--------|-----------|----------------|
| Low | 15-30s | 1-2 | 1 | ✅ | ✅ |
| Medium | 30s-2min | 2-5 | 1-2 | ✅ | ✅ |
| High | 2-10min | 5-10 | 3-5 | ✅ | Partial |

---

## Key Features

### 1. Autonomous Agents
- Agents research from GAM memory
- Agents generate code with streaming
- Agents execute tools/skills without human intervention
- Agents learn from past executions

### 2. Streaming Output
- Real-time code generation
- Live tool execution feedback
- Immediate error surfacing

### 3. Memory-Augmented
- Search GAM for similar past work
- Memorize successful patterns
- Learn from failures
- Improve over time

### 4. Composable
- Workflows call other workflows
- Chain workflows together
- Run workflows in parallel
- Share context via GAM

---

## Best Practices

1. **Start with Research**: Always research before implementing
   ```bash
   /workflow-research topic="$FEATURE"
   ```

2. **Break Down Large Features**: Use feature breakdown for 4+ files
   ```bash
   /workflow-feature-breakdown feature="$LARGE_FEATURE"
   ```

3. **Enable Streaming**: Watch agents work in real-time
   ```bash
   /workflow-multi-agent-dev feature="$FEATURE" stream_output=true
   ```

4. **Leverage GAM Memory**: Let agents learn from history
   ```bash
   /workflow-context-suggestions feature="$FEATURE" gam_memory=true
   ```

5. **Use QA Loops**: Enable quality assurance for production code
   ```bash
   /workflow-qa-loop feature="$FEATURE" max_iterations=3
   ```

---

## Related Registries

- **1000: Agents Registry** - Agent factories used by workflows
- **2000: Skills Registry** - Skills orchestrated by workflows
- **3000: Tools Registry** - Tools used by workflows
- **300: Main Command Index** - All commands

---

## Documentation

- **C5 README**: `.cursor/commands/app/c5/README.md`
- **C5 INDEX**: `.cursor/commands/app/c5/INDEX.md`
- **App Architecture**: `app/ARCHITECTURE.md`
- **Implementation Summary**: `app/IMPLEMENTATION_SUMMARY.md`
- **Quick Reference**: `app/QUICK_REFERENCE.md`

---

## Contributing

To add a new workflow:

1. Create workflow file in appropriate category
2. Follow existing workflow structure
3. Integrate with `app/server/skills/`
4. Add tests in `tests/integration/test_workflows.py`
5. Update this registry

---

## Next Steps

- [ ] Add workflow performance metrics
- [ ] Implement workflow chaining DSL
- [ ] Add workflow templates
- [ ] Create workflow composition patterns
- [ ] Add multi-workflow orchestration

---

**Last Updated**: 2024-12-04
**Total Workflows**: 30 (10 core + 20 C5)
**Status**: Phase 1 Complete ✅

**C5 Workflows**: 20 autonomous PR workflows for startups
**C5 Status**: ✅ Complete - All 20 workflows implemented
