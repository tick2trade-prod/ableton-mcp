# QA Validation

## Overview

Run quality assurance checks on plans or code using the critic agent (Senior Architect). Provides multi-dimensional validation including architecture, package verification, syntax checking, and security scanning.

## Usage

Type `/qa-validation` followed by your validation request.

## Parameters

- `target`: What to validate (required)
  - `plan`: Validate implementation plan
  - `code`: Validate code files
  - `architecture`: Validate system architecture
- `content`: Content to validate (required)
  - File path: `@app/server/orchestrator.py`
  - Inline content: Direct text/code
- `dimensions`: QA dimensions to check (default: all)
  - `architecture`: System design and patterns
  - `packages`: Package existence and compatibility
  - `syntax`: Code syntax and linting
  - `security`: Security vulnerabilities
  - `performance`: Performance issues
  - `testing`: Test coverage and quality
- `auto_fix`: Attempt auto-fix on failures (default: false)
- `max_retries`: Maximum fix attempts (default: 2)

## Example Usage

### Validate Code File

```
/qa-validation
Target: code
Content: @app/server/orchestrator.py
Dimensions: [syntax, security, architecture]
Auto Fix: true
```

### Validate Implementation Plan

```
/qa-validation
Target: plan
Content: @plan.md
Dimensions: [architecture, packages]
Auto Fix: false
```

### Quick Syntax Check

```
/qa-validation
Target: code
Content: @app/core/gam_memory.py
Dimensions: [syntax]
```

### Full Architecture Review

```
/qa-validation
Target: architecture
Content: @app/server/
Dimensions: all
Auto Fix: false
```

## Workflow

1. **Dimension Selection**:
   - Parse dimensions parameter
   - Map target to appropriate QA dimensions:
     - `plan` → [architecture, packages]
     - `code` → [syntax, security, performance]
     - `architecture` → [architecture, patterns, scalability]

2. **Critic Agent Creation**:
   - Create critic agent: `/agent-factory agent_type=critic temperature=0.1`
   - Load validation prompts from `app/server/agents/prompts.py::CRITIC_SYSTEM_PROMPT`
   - Attach tools: `package_tool`, `gam_tool`, `search_tool`

3. **Package Verification** (if packages dimension):
   - Extract package imports from code/plan
   - Verify each package:
     - Python: Check PyPI with `package_tool.verify_python_package()`
     - Node: Check npm with `package_tool.verify_npm_package()`
   - Flag hallucinated or deprecated packages
   - Suggest alternatives for missing packages

4. **Syntax Validation** (if syntax dimension):
   - Run linting: `coder_tool.lint_code(content, language)`
   - Check type hints: `mypy --check-untyped-defs`
   - Validate imports and dependencies
   - Report syntax errors with line numbers

5. **Security Scan** (if security dimension):
   - Check for common vulnerabilities:
     - SQL injection patterns
     - XSS vulnerabilities
     - Hardcoded secrets
     - Insecure dependencies
   - Use `bandit` for Python security checks
   - Report security issues with severity levels

6. **Architecture Review** (if architecture dimension):
   - Validate DDD compliance:
     - Layer separation (Domain vs Infrastructure)
     - Dependency direction (Infrastructure → Domain, not reverse)
     - Protocol definitions (Pydantic models)
   - Check design patterns
   - Verify SOLID principles
   - Assess scalability and maintainability

7. **Feedback Generation**:
   - Create structured critique report:
     ```python
     QAReport(
         target=target,
         dimensions_checked=dimensions,
         issues=[
             CritiqueIssue(
                 dimension="packages",
                 severity="high",
                 message="Package 'nonexistent-lib' not found on PyPI",
                 location="line 15",
                 suggestion="Use 'requests' instead"
             )
         ],
         passed=False,
         score=0.75
     )
     ```

8. **Auto-Fix** (if enabled):
   - Attempt fixes for each issue:
     - Replace hallucinated packages
     - Fix syntax errors
     - Remove security vulnerabilities
   - Re-run validation after fixes
   - Max retries: 2 attempts
   - Report fix success/failure

## QA Dimensions

### Architecture

- **Checks**: DDD compliance, layer separation, design patterns
- **Tools**: Critic agent, GAM memory lookup
- **Output**: Architecture score (0-1), design recommendations

### Packages

- **Checks**: Package existence, version compatibility, deprecation
- **Tools**: `package_tool`, PyPI/npm APIs
- **Output**: List of valid/invalid packages, alternatives

### Syntax

- **Checks**: Linting, type hints, import validation
- **Tools**: `ruff`, `mypy`, `coder_tool`
- **Output**: Syntax errors with line numbers, fix suggestions

### Security

- **Checks**: Vulnerabilities, secrets, insecure patterns
- **Tools**: `bandit`, security scanners
- **Output**: Security issues with severity, remediation steps

### Performance

- **Checks**: Inefficient algorithms, memory leaks, N+1 queries
- **Tools**: Critic agent analysis
- **Output**: Performance bottlenecks, optimization suggestions

### Testing

- **Checks**: Test coverage, test quality, missing tests
- **Tools**: `pytest --cov`, critic agent
- **Output**: Coverage report, missing test cases

## Validation Report Format

```json
{
    "target": "code",
    "file": "app/server/orchestrator.py",
    "dimensions_checked": ["syntax", "security", "architecture"],
    "passed": false,
    "score": 0.75,
    "issues": [
        {
            "dimension": "security",
            "severity": "high",
            "message": "Hardcoded password found",
            "location": "line 42",
            "code_snippet": "password = 'admin123'",
            "suggestion": "Use environment variable: os.getenv('PASSWORD')"
        },
        {
            "dimension": "syntax",
            "severity": "medium",
            "message": "Missing type hint for return value",
            "location": "line 67",
            "suggestion": "Add return type: -> dict[str, Any]"
        }
    ],
    "auto_fix_applied": true,
    "fixes": [
        {
            "issue": "Hardcoded password",
            "action": "Replaced with environment variable",
            "success": true
        }
    ],
    "validation_time_ms": 3420
}
```

## Best Practices

- Run QA validation before committing code
- Use `auto_fix=true` for quick fixes
- Validate plans before implementation
- Check all dimensions for production code
- Use `architecture` dimension for design reviews
- Enable `packages` dimension to prevent hallucinations
- Run `security` dimension on sensitive code
- Combine with `/workflow-orchestration` for automatic QA loops

## Integration Points

**Calls:**
- `app/server/skills/qa/plan_critic.py::validate_plan()`
- `app/server/skills/qa/code_critic.py::validate_code()`
- `app/server/agents/critic.py::create_critic_agent()`
- `app/server/tools/package_tool.py::verify_package()`
- `app/server/tools/coder_tool.py::lint_code()`

**Used By:**
- `/workflow-orchestration` - Auto-QA after planning/implementation
- `/validate-architecture` - Architecture-specific validation
- `/generate-code-streaming` - Auto-lint after generation
- `/batch-implement` - Parallel validation

## Error Handling

### Validation Failure

```json
{
    "target": "code",
    "passed": false,
    "score": 0.45,
    "critical_issues": 3,
    "error": "Validation failed with critical issues",
    "recommendation": "Fix critical issues before proceeding"
}
```

### Auto-Fix Failure

```json
{
    "auto_fix_applied": true,
    "fixes": [
        {
            "issue": "Import error",
            "action": "Attempted to fix import",
            "success": false,
            "error": "Cannot resolve module 'nonexistent'"
        }
    ],
    "recommendation": "Manual intervention required"
}
```

## Related Commands

- `/validate-architecture` - Architecture-specific validation
- `/workflow-orchestration` - Includes automatic QA loops
- `/agent-factory` - Create critic agent
- `/generate-code-streaming` - Auto-lint after generation
