# C5: Autonomous PR Workflows for Startups

## Overview

Collection of 20 production-ready workflows for completing GitHub PRs in startup environments. Each workflow leverages the autonomous agent architecture in `@app` where agents stream, write, and generate their own code using tools/skills autonomously.

## Architecture Integration

All workflows integrate with:
- **`app/server/orchestrator.py`**: Thin router for task execution
- **`app/server/skills/`**: Planning, implementation, review workflows
- **`app/server/tools/`**: GAM memory, code generation, search, MCP clients
- **`app/server/agents/`**: Agent factories with specialized prompts
- **`app/core/gam_memory.py`**: Persistent memory for learning

## Workflow Categories

### 🤖 Automation & Intelligence (1-5)
1. **workflow-auto-pr-create** - Automated PR creation with intelligent reviewer assignment
2. **workflow-ai-code-review** - Context-aware code review with improvement suggestions
3. **workflow-multi-agent-dev** - Multi-agent collaborative development (Agile/TDD)
4. **workflow-security-scan** - Security-enhanced code generation with vulnerability detection
5. **workflow-agile-sprint** - Agile methodology integration with AI role assignment

### 📋 Standards & Documentation (6-10)
6. **workflow-pr-templates** - Standardized PR templates enforcement
7. **workflow-pr-summary** - Automated PR summarization for quick review
8. **workflow-code-scan** - Real-time code scanning for vulnerabilities
9. **workflow-context-suggestions** - Context-aware code suggestions aligned with architecture
10. **workflow-auto-tests** - Automated test case generation from specifications

### 🔄 Workflow Automation (11-15)
11. **workflow-pr-automation** - Complete PR workflow automation (tagging, labels, rules)
12. **workflow-docs-sync** - Automated documentation updates with code changes
13. **workflow-release-notes** - Human-quality release notes generation
14. **workflow-infra-mgmt** - Intelligent infrastructure management and scaling
15. **workflow-incident-mgmt** - AI-driven incident management and resolution

### 🛡️ Quality & Compliance (16-20)
16. **workflow-compliance-check** - Automated compliance checks and fix PRs
17. **workflow-onboarding** - AI-powered onboarding with personalized learning paths
18. **workflow-dependency-mgmt** - Automated dependency updates with risk analysis
19. **workflow-sprint-planning** - AI-enhanced sprint planning and capacity estimation
20. **workflow-anomaly-detect** - Proactive anomaly detection and mitigation

## Usage Pattern

All workflows follow a consistent pattern:

```bash
# Basic usage
/workflow-name

# With parameters
/workflow-name param1="value1" param2="value2"

# Example
/workflow-auto-pr-create
  title="feat(auth): add JWT authentication"
  reviewers="alice,bob"
  auto_assign=true
```

## Common Parameters

Most workflows support:
- `feature_name`: Name of feature/task (required for most)
- `context`: Additional context or constraints (optional)
- `gam_memory`: Use GAM memory for context (default: true)
- `stream_output`: Stream results in real-time (default: true)
- `auto_execute`: Execute without confirmation (default: false)

## Integration with Existing Workflows

### Builds On
- `/workflow-research` - Research before implementation
- `/workflow-implement` - Core implementation workflow
- `/workflow-pr-create` - Basic PR creation

### Extends
- `/batch-implement` - Parallel task execution
- `/workflow-feature-breakdown` - Task decomposition

### Feeds Into
- `/workflow-code-review` - Code review process
- `/workflow-merge-deploy` - Merge and deployment

## Architecture Benefits

### 1. Autonomous Agents
Agents autonomously:
- Research from GAM memory
- Generate code with streaming
- Execute tools/skills without human intervention
- Learn from past executions

### 2. Streaming Output
Real-time feedback:
- Code generation streams as it's written
- Tool execution shows progress
- Errors surface immediately

### 3. Memory-Augmented
Every workflow:
- Searches GAM for similar past work
- Memorizes successful patterns
- Learns from failures
- Improves over time

### 4. Composable
Workflows can:
- Call other workflows
- Chain together
- Run in parallel
- Share context via GAM

## Quick Start

### 1. Simple Feature PR
```bash
# Research → Plan → Implement → PR
/workflow-auto-pr-create
  feature="User authentication with JWT"
  auto_assign=true
```

### 2. Security-Critical Feature
```bash
# Security scan + Multi-agent review
/workflow-security-scan
  feature="Payment processing integration"
  scan_depth="deep"

/workflow-ai-code-review
  pr_number=123
  focus="security,performance"
```

### 3. Sprint Planning
```bash
# AI-enhanced sprint planning
/workflow-sprint-planning
  sprint_name="Sprint 24"
  capacity_hours=80
  backlog_items="JIRA-123,JIRA-124,JIRA-125"
```

### 4. Incident Response
```bash
# Automated incident management
/workflow-incident-mgmt
  alert_id="PROD-2024-001"
  severity="critical"
  auto_mitigate=true
```

## Best Practices

### 1. Start with Research
Always research before implementing:
```bash
/workflow-research topic="$FEATURE"
/workflow-auto-pr-create feature="$FEATURE"
```

### 2. Use Feature Breakdown for Large Tasks
Break down complex features:
```bash
/workflow-feature-breakdown feature="$LARGE_FEATURE"
/batch-implement tasks="$TASK_LIST"
```

### 3. Enable Streaming for Long-Running Tasks
Stream output for visibility:
```bash
/workflow-multi-agent-dev
  feature="$FEATURE"
  stream_output=true
```

### 4. Leverage GAM Memory
Let agents learn from history:
```bash
/workflow-context-suggestions
  feature="$FEATURE"
  gam_memory=true
  max_context_iters=10
```

## Performance Characteristics

| Workflow | Avg Time | Streaming | GAM Queries | Agents |
|----------|----------|-----------|-------------|--------|
| auto-pr-create | 30s | ✅ | 2-3 | 1 |
| ai-code-review | 45s | ✅ | 3-5 | 1 |
| multi-agent-dev | 5-10min | ✅ | 5-10 | 3-5 |
| security-scan | 2-3min | ✅ | 2-3 | 1 |
| agile-sprint | 1-2min | ✅ | 5-8 | 2 |

## Error Handling

All workflows include:
- ✅ Graceful degradation
- ✅ Retry logic with exponential backoff
- ✅ Detailed error messages
- ✅ Rollback capabilities
- ✅ GAM memory of failures for learning

## Related Documentation

- **Architecture**: `app/ARCHITECTURE.md`
- **Core GAM**: `app/core/gam_memory.py`
- **Skills**: `app/server/skills/`
- **Tools**: `app/server/tools/`
- **Existing Workflows**: `.cursor/commands/app/workflow-*.md`

## Contributing

To add a new workflow:

1. Create workflow file: `c5/workflow-{name}.md`
2. Follow the template structure
3. Integrate with `app/server/skills/`
4. Add tests in `tests/integration/test_workflows.py`
5. Update this README

## Support

For issues or questions:
- Check `app/QUICK_REFERENCE.md`
- Review `app/IMPLEMENTATION_SUMMARY.md`
- See existing workflow examples
