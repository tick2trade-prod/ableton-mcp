# C6 Commands Index

## Overview

C6 (Command Set 6) contains advanced development workflow commands optimized for low latency, token efficiency, and programmatic tool calling.

## Commands

### Core Generation Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `generate-code-streaming.md` | Real-time code generation | Streaming output, context-aware, auto-retry |
| `generate-code-batch.md` | Parallel multi-task generation | 5-20x speedup, batch processing |
| `batch-implement.md` | Multi-file scaffolding | Parallel file creation, integration tests |

### Quality & Validation Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `validate-architecture.md` | Pre-generation validation | Package verification, anti-pattern detection |
| `qa-critic.md` | Code quality review | Structured QA reports, severity ratings |
| `code-review.md` | Comprehensive code review | Multi-aspect analysis, scoring, feedback |
| `optimize-imports.md` | Import validation & cleanup | Hallucination detection, auto-fix |

### Refactoring & Maintenance Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `refactor-batch.md` | Parallel refactoring | Pattern migration, backup/rollback |
| `test-generator.md` | Automated test generation | Unit/integration/e2e, coverage analysis |
| `dependency-analyzer.md` | Dependency management | Security audit, license check, optimization |

### Research & Context Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `deep-research.md` | Think-first research | Parallel search, GAM integration, reports |
| `smart-context.md` | Context optimization | History compression, knowledge injection |

### Debugging & Performance Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `debug-assistant.md` | AI-powered debugging | Auto-detect errors, GAM learning, auto-fix |
| `performance-profiler.md` | Performance analysis | CPU/memory/I/O profiling, flame graphs |

## Command Categories

### 🚀 Speed & Efficiency
- `generate-code-streaming.md` - Instant feedback
- `generate-code-batch.md` - Parallel execution
- `batch-implement.md` - Multi-file generation
- `smart-context.md` - Token optimization

### 🛡️ Quality & Safety
- `validate-architecture.md` - Pre-flight checks
- `qa-critic.md` - Quality gates
- `code-review.md` - Comprehensive review
- `optimize-imports.md` - Import safety

### 🔧 Maintenance & Refactoring
- `refactor-batch.md` - Large-scale refactoring
- `test-generator.md` - Test coverage
- `dependency-analyzer.md` - Dependency health

### 🔍 Research & Debug
- `deep-research.md` - Knowledge gathering
- `debug-assistant.md` - Error resolution
- `performance-profiler.md` - Bottleneck analysis

## Usage Patterns

### New Feature Development
1. `/deep-research` - Research the topic
2. `/validate-architecture` - Validate approach
3. `/batch-implement` - Generate code in parallel
4. `/test-generator` - Create test suite
5. `/code-review` - Review before commit

### Bug Fixing
1. `/debug-assistant` - Analyze error
2. `/deep-research` - Research solution (if needed)
3. `/generate-code-streaming` - Apply fix
4. `/test-generator` - Add regression test

### Refactoring
1. `/code-review` - Identify issues
2. `/performance-profiler` - Find bottlenecks (if needed)
3. `/refactor-batch` - Apply changes in parallel
4. `/qa-critic` - Validate refactoring

### Maintenance
1. `/dependency-analyzer` - Check dependencies
2. `/optimize-imports` - Clean up imports
3. `/test-generator` - Improve coverage
4. `/code-review` - Quality check

## Best Practices

### Performance
- Use streaming for real-time feedback
- Leverage parallel execution for multiple files
- Optimize context before large operations
- Save findings to GAM for reuse

### Quality
- Validate before generating
- Review after generating
- Run tests after changes
- Use strict mode for production

### Safety
- Enable dry-run for refactoring
- Create backups before changes
- Use auto-fix cautiously
- Review AI suggestions

### Learning
- Save successful patterns to GAM
- Learn from past errors
- Document common issues
- Share team knowledge

## Integration

### Pre-commit Hooks
```yaml
- id: optimize-imports
  entry: /optimize-imports --fix
- id: qa-critic
  entry: /qa-critic --strict
```

### CI/CD Pipeline
```yaml
- name: Code Review
  run: /code-review --target pr
- name: Dependency Audit
  run: /dependency-analyzer --action audit
- name: Performance Check
  run: /performance-profiler --compare-baseline
```

### IDE Integration
- Inline error detection → `/debug-assistant`
- Quick fix actions → `/generate-code-streaming`
- Refactoring suggestions → `/refactor-batch`

## Related Documentation

- `DEVELOPER.md` - Developer guide for C6 commands
- `../README.md` - Overall commands documentation
- `../../rules/109-development-workflow.mdc` - Development workflow rules

## Version History

- **v1.0** (2024-12-04): Initial C6 command set
  - 7 core commands from original design
  - 6 additional advanced commands
  - Comprehensive documentation

## Future Enhancements

- Real-time collaboration commands
- Multi-language support (TypeScript, Go, Rust)
- Visual debugging tools
- Performance benchmarking suite
- Team analytics dashboard
