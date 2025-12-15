# QA Commands Index

Quality assurance commands for code review, testing, and dependency management.

---

## Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `code-review.md` | Comprehensive code review | Security, performance, quality checks |
| `test-generator.md` | Generate test suites | Unit, integration, e2e tests |
| `dependency-analyzer.md` | Analyze dependencies | Security audit, outdated packages, licenses |

---

## Usage Patterns

### Code Review Before Commit
```
/code-review
Target: current
Focus: all
Strictness: standard
```

### Generate Tests for New Code
```
/test-generator
Target: app/services/new_feature.py
Test Type: all
Coverage Goal: 90
```

### Security Audit
```
/dependency-analyzer
Action: audit
Severity: high
```

---

## Integration

These commands work together:
1. **Code Review** → Identifies issues
2. **Test Generator** → Creates tests for uncovered code
3. **Dependency Analyzer** → Ensures secure dependencies

---

## Related Directories

- `/workflows/` - End-to-end workflows that may include QA
- `/analysis/` - Debugging and performance analysis
- `/operations/` - Code generation and refactoring
