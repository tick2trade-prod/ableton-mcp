# C5 Workflow Index

## Overview

Complete index of 20 autonomous PR workflows for startup software engineering teams. All workflows integrate with `@app` architecture for autonomous agent execution.

## Quick Reference Table

| # | Workflow | Category | Complexity | Avg Time | Agents |
|---|----------|----------|------------|----------|--------|
| 1 | [workflow-auto-pr-create](#1-workflow-auto-pr-create) | Automation | Low | 30s | 1 |
| 2 | [workflow-ai-code-review](#2-workflow-ai-code-review) | Intelligence | Medium | 45s | 1 |
| 3 | [workflow-multi-agent-dev](#3-workflow-multi-agent-dev) | Automation | High | 5-10min | 3-5 |
| 4 | [workflow-security-scan](#4-workflow-security-scan) | Quality | Medium | 2-3min | 1 |
| 5 | [workflow-agile-sprint](#5-workflow-agile-sprint) | Automation | Medium | 1-2min | 2 |
| 6 | [workflow-pr-templates](#6-workflow-pr-templates) | Standards | Low | 15s | 1 |
| 7 | [workflow-pr-summary](#7-workflow-pr-summary) | Documentation | Low | 20s | 1 |
| 8 | [workflow-code-scan](#8-workflow-code-scan) | Quality | Medium | 1-2min | 1 |
| 9 | [workflow-context-suggestions](#9-workflow-context-suggestions) | Intelligence | Medium | 30s | 1 |
| 10 | [workflow-auto-tests](#10-workflow-auto-tests) | Automation | Medium | 1-2min | 1 |
| 11 | [workflow-pr-automation](#11-workflow-pr-automation) | Automation | Low | 25s | 1 |
| 12 | [workflow-docs-sync](#12-workflow-docs-sync) | Documentation | Medium | 1min | 1 |
| 13 | [workflow-release-notes](#13-workflow-release-notes) | Documentation | Low | 30s | 1 |
| 14 | [workflow-infra-mgmt](#14-workflow-infra-mgmt) | Automation | High | 2-5min | 1 |
| 15 | [workflow-incident-mgmt](#15-workflow-incident-mgmt) | Automation | High | 3-10min | 1 |
| 16 | [workflow-compliance-check](#16-workflow-compliance-check) | Quality | Medium | 2min | 1 |
| 17 | [workflow-onboarding](#17-workflow-onboarding) | Automation | Medium | 1-2min | 1 |
| 18 | [workflow-dependency-mgmt](#18-workflow-dependency-mgmt) | Automation | Medium | 1-2min | 1 |
| 19 | [workflow-sprint-planning](#19-workflow-sprint-planning) | Automation | Medium | 1-2min | 1 |
| 20 | [workflow-anomaly-detect](#20-workflow-anomaly-detect) | Intelligence | Medium | 30s-1min | 1 |

## Workflow Categories

### 🤖 Automation & Intelligence (1-5)
Workflows that use AI agents to automate complex development tasks with intelligent decision-making.

### 📋 Standards & Documentation (6-10)
Workflows that enforce standards and maintain documentation quality.

### 🔄 Workflow Automation (11-15)
Workflows that automate repetitive tasks and infrastructure management.

### 🛡️ Quality & Compliance (16-20)
Workflows that ensure code quality, security, and regulatory compliance.

## Detailed Workflow Descriptions

### 1. workflow-auto-pr-create
**File**: `workflow-auto-pr-create.md`
**Purpose**: Automated PR creation with intelligent reviewer assignment
**Key Features**:
- Auto-generates PR title (conventional commits)
- Intelligently assigns reviewers based on code ownership and expertise
- Auto-detects and applies labels
- Integrates with GAM memory for learning

**Use Cases**:
- Creating feature PRs
- Hotfix PRs with auto-merge
- Draft PRs for early feedback

**Integration**:
```python
from app.server.skills.review import create_pr
from app.server.tools.gam_tool import research_memory
```

---

### 2. workflow-ai-code-review
**File**: `workflow-ai-code-review.md`
**Purpose**: Context-aware code review with improvement suggestions
**Key Features**:
- Multi-dimensional analysis (security, performance, maintainability, testing, docs, architecture)
- Generates fix suggestions with code examples
- Provides severity-based issue categorization
- Auto-posts review comments

**Use Cases**:
- Standard code reviews
- Security-focused reviews
- Quick reviews for hotfixes

**Integration**:
```python
from app.server.agents.critic import create_critic_agent
from app.server.tools.coder_tool import generate_code
```

---

### 3. workflow-multi-agent-dev
**File**: `workflow-multi-agent-dev.md`
**Purpose**: Multi-agent collaborative development using Agile/TDD
**Key Features**:
- Agents take on roles (PM, Developer, Tester, Architect)
- Sprint-based development
- Agent communication protocol
- Retrospective and learning

**Use Cases**:
- Complex feature development
- TDD-driven development
- Team simulation for prototyping

**Integration**:
```python
from app.server.agents.factory import create_workflow_agent
# Multiple agents with different roles
```

---

### 4. workflow-security-scan
**File**: `workflow-security-scan.md`
**Purpose**: Security-enhanced code generation with vulnerability detection
**Key Features**:
- Static analysis (SAST)
- Dynamic analysis (DAST)
- Dependency scanning
- Fuzz testing
- Auto-fix vulnerabilities

**Use Cases**:
- Security-critical features
- Compliance requirements
- Pre-deployment security checks

**Integration**:
```python
from app.server.skills.qa.code_critic import analyze_security
```

---

### 5. workflow-agile-sprint
**File**: `workflow-agile-sprint.md`
**Purpose**: Agile methodology integration with AI role assignment
**Key Features**:
- Sprint planning
- Daily standups
- Sprint review
- Sprint retrospective
- Velocity tracking

**Use Cases**:
- Sprint planning
- Backlog management
- Team capacity planning

**Integration**:
```python
from app.server.skills.planning import execute_planning
```

---

### 6. workflow-pr-templates
**File**: `workflow-pr-templates.md`
**Purpose**: Standardized PR templates enforcement
**Key Features**:
- Template selection based on PR type
- Auto-populate template fields
- Enforce checklist completion

**Use Cases**:
- Feature PRs
- Bug fix PRs
- Refactoring PRs

---

### 7. workflow-pr-summary
**File**: `workflow-pr-summary.md`
**Purpose**: Automated PR summarization
**Key Features**:
- High-level overview
- Technical details
- Testing summary
- Risk assessment

**Use Cases**:
- Quick PR understanding
- Executive summaries
- Team updates

---

### 8. workflow-code-scan
**File**: `workflow-code-scan.md`
**Purpose**: Real-time code scanning
**Key Features**:
- Security scanning
- Quality scanning
- Compliance scanning
- Auto-fix issues

**Use Cases**:
- Pre-merge checks
- Continuous monitoring
- Compliance audits

---

### 9. workflow-context-suggestions
**File**: `workflow-context-suggestions.md`
**Purpose**: Context-aware code suggestions
**Key Features**:
- Refactoring suggestions
- Optimization suggestions
- Security suggestions
- Style suggestions

**Use Cases**:
- Code improvement
- Technical debt reduction
- Performance optimization

---

### 10. workflow-auto-tests
**File**: `workflow-auto-tests.md`
**Purpose**: Automated test case generation
**Key Features**:
- Unit test generation
- Integration test generation
- E2E test generation
- Coverage analysis

**Use Cases**:
- Improving test coverage
- TDD workflows
- Regression testing

---

### 11. workflow-pr-automation
**File**: `workflow-pr-automation.md`
**Purpose**: Complete PR workflow automation
**Key Features**:
- Auto-tagging
- Auto-labeling
- Branch protection
- Notifications

**Use Cases**:
- PR workflow standardization
- Team notifications
- Compliance enforcement

---

### 12. workflow-docs-sync
**File**: `workflow-docs-sync.md`
**Purpose**: Automated documentation updates
**Key Features**:
- README updates
- API documentation
- Changelog generation
- Code examples

**Use Cases**:
- Keeping docs in sync
- API documentation
- Release notes

---

### 13. workflow-release-notes
**File**: `workflow-release-notes.md`
**Purpose**: Human-quality release notes generation
**Key Features**:
- Highlights section
- Feature list
- Bug fixes
- Breaking changes
- Contributors

**Use Cases**:
- Version releases
- Stakeholder communication
- Public announcements

---

### 14. workflow-infra-mgmt
**File**: `workflow-infra-mgmt.md`
**Purpose**: Intelligent infrastructure management
**Key Features**:
- Resource provisioning
- Auto-scaling
- Security hardening
- Cost optimization

**Use Cases**:
- Cloud resource management
- Infrastructure as code
- Cost optimization

---

### 15. workflow-incident-mgmt
**File**: `workflow-incident-mgmt.md`
**Purpose**: AI-driven incident management
**Key Features**:
- Alert triage
- Root cause analysis
- Mitigation proposals
- Postmortem generation

**Use Cases**:
- Production incidents
- On-call support
- SRE workflows

---

### 16. workflow-compliance-check
**File**: `workflow-compliance-check.md`
**Purpose**: Automated compliance checks
**Key Features**:
- OWASP Top 10
- PCI-DSS
- HIPAA
- GDPR
- License compliance

**Use Cases**:
- Regulatory compliance
- Security audits
- License management

---

### 17. workflow-onboarding
**File**: `workflow-onboarding.md`
**Purpose**: AI-powered developer onboarding
**Key Features**:
- Personalized learning paths
- Codebase tour
- Development setup
- Mentorship assignment

**Use Cases**:
- New hire onboarding
- Team expansion
- Knowledge transfer

---

### 18. workflow-dependency-mgmt
**File**: `workflow-dependency-mgmt.md`
**Purpose**: Automated dependency management
**Key Features**:
- Dependency scanning
- Version updates
- Security audits
- License compliance

**Use Cases**:
- Dependency updates
- Security patching
- License compliance

---

### 19. workflow-sprint-planning
**File**: `workflow-sprint-planning.md`
**Purpose**: AI-enhanced sprint planning
**Key Features**:
- Capacity planning
- Backlog refinement
- Task assignment
- Velocity tracking

**Use Cases**:
- Sprint planning
- Capacity management
- Velocity tracking

---

### 20. workflow-anomaly-detect
**File**: `workflow-anomaly-detect.md`
**Purpose**: Proactive anomaly detection
**Key Features**:
- Performance anomalies
- Error anomalies
- Security anomalies
- Business anomalies

**Use Cases**:
- Production monitoring
- SRE workflows
- Performance optimization

---

## Usage Patterns

### Sequential Workflow
```bash
# 1. Research
/workflow-research topic="User authentication"

# 2. Create PR
/workflow-auto-pr-create feature_name="User authentication"

# 3. Review
/workflow-ai-code-review pr_number=123

# 4. Merge
/workflow-merge-deploy pr_number=123
```

### Parallel Workflow
```bash
# Run multiple workflows in parallel
/batch-implement tasks="task1,task2,task3"
/workflow-auto-tests feature_name="All tasks"
/workflow-docs-sync pr_number=123
```

### Conditional Workflow
```bash
# Security-critical feature
/workflow-security-scan feature_name="Payment processing"
if [[ $? -eq 0 ]]; then
  /workflow-auto-pr-create feature_name="Payment processing"
fi
```

## Integration with App Architecture

All workflows integrate with:

```
app/
├── core/
│   └── gam_memory.py          # Persistent memory
├── server/
│   ├── orchestrator.py        # Workflow routing
│   ├── agents/                # Agent factories
│   ├── skills/                # High-level capabilities
│   │   ├── planning.py
│   │   ├── implementation.py
│   │   └── review.py
│   └── tools/                 # Execution primitives
│       ├── gam_tool.py
│       ├── coder_tool.py
│       └── search.py
```

## Performance Characteristics

| Category | Avg Time | GAM Queries | Streaming | Parallelizable |
|----------|----------|-------------|-----------|----------------|
| Low Complexity | 15-30s | 1-2 | ✅ | ✅ |
| Medium Complexity | 30s-2min | 2-5 | ✅ | ✅ |
| High Complexity | 2-10min | 5-10 | ✅ | Partial |

## Best Practices

1. **Start Simple**: Begin with low-complexity workflows
2. **Enable Streaming**: Watch agents work in real-time
3. **Trust the Agents**: They learn from past executions
4. **Review Outputs**: Validate agent decisions initially
5. **Iterate**: Workflows improve with usage

## Related Documentation

- **Main README**: `c5/README.md`
- **App Architecture**: `app/ARCHITECTURE.md`
- **Implementation Summary**: `app/IMPLEMENTATION_SUMMARY.md`
- **Quick Reference**: `app/QUICK_REFERENCE.md`

## Contributing

To add a new workflow:

1. Create `workflow-{name}.md` in `c5/`
2. Follow existing workflow structure
3. Integrate with `app/server/skills/`
4. Add tests
5. Update this index

## Support

For issues or questions:
- Review workflow documentation
- Check `app/QUICK_REFERENCE.md`
- See `app/IMPLEMENTATION_SUMMARY.md`
