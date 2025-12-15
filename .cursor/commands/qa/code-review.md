# Code Review

## Overview

Comprehensive AI code review that checks quality, security, performance, and best practices. Generates actionable feedback like a senior engineer.

## Usage

Type `/code-review` to review current changes or specify target.

## Parameters

- `target`: What to review (current, file, commit, pr) (default: current)
- `file_path`: Specific file to review (optional)
- `commit_hash`: Git commit to review (optional)
- `focus`: Review focus (all, security, performance, style) (default: all)
- `strictness`: Review strictness (lenient, standard, strict) (default: standard)

## Example Usage

### Review Current Changes

```
/code-review
Target: current
```

### Review Specific File

```
/code-review
Target: file
File Path: app/services/payment.py
Focus: security
Strictness: strict
```

### Review Last Commit

```
/code-review
Target: commit
Commit Hash: HEAD
Focus: all
```

### Performance Review

```
/code-review
Target: current
Focus: performance
```

## Workflow

1. **Gather Changes**:
   - Get git diff or file contents
   - Identify modified functions
   - Extract context from surrounding code
   - Check related files

2. **Multi-Aspect Analysis**:
   - **Security**: SQL injection, XSS, secrets exposure
   - **Performance**: N+1 queries, inefficient loops, memory leaks
   - **Quality**: Code smells, complexity, maintainability
   - **Style**: PEP 8, naming conventions, documentation
   - **Testing**: Coverage, edge cases, test quality
   - **Architecture**: SOLID principles, patterns, coupling

3. **GAM Knowledge Check**:
   - Search for similar code patterns
   - Check for known anti-patterns
   - Reference team standards
   - Learn from past reviews

4. **Generate Feedback**:
   - Categorize by severity (critical, major, minor)
   - Provide specific line numbers
   - Suggest concrete improvements
   - Include code examples

5. **Scoring**:
   - Overall score (0-100)
   - Category scores
   - Comparison to team average
   - Improvement suggestions

## Review Categories

### 🔒 Security (Critical)
- SQL injection vulnerabilities
- XSS vulnerabilities
- Secrets in code
- Authentication/authorization issues
- Input validation
- CSRF protection

### ⚡ Performance (Major)
- N+1 query problems
- Inefficient algorithms
- Memory leaks
- Missing indexes
- Excessive API calls
- Blocking operations

### 🎯 Code Quality (Major)
- Code complexity (cyclomatic)
- Code duplication
- Long functions (>50 lines)
- Deep nesting (>4 levels)
- Magic numbers
- Poor naming

### 📝 Style & Documentation (Minor)
- PEP 8 compliance
- Type hints
- Docstrings
- Comments
- Naming conventions
- File organization

### 🧪 Testing (Major)
- Missing tests
- Low coverage
- Poor test quality
- Missing edge cases
- Flaky tests

### 🏗️ Architecture (Major)
- SOLID violations
- Tight coupling
- Missing abstractions
- Circular dependencies
- Poor separation of concerns

## Review Report Format

```markdown
# Code Review Report

## Summary
Reviewed: app/services/payment.py
Lines Changed: +85, -23
Overall Score: 78/100

## Critical Issues (0)
None found ✅

## Major Issues (2)

### 1. SQL Injection Vulnerability (Security)
**Line 42**: User input directly interpolated into SQL query
**Severity**: Critical
**Current Code**:
```python
query = f"SELECT * FROM users WHERE email = '{email}'"
```
**Suggested Fix**:
```python
query = select(User).where(User.email == email)
```

### 2. N+1 Query Problem (Performance)
**Line 67-72**: Loading related objects in loop
**Severity**: Major
**Impact**: 100x slower with 100 users
**Suggested Fix**: Use `selectinload()` or `joinedload()`

## Minor Issues (5)

### 1. Missing Type Hint (Style)
**Line 15**: Function lacks return type annotation
**Suggested**: Add `-> PaymentResult:`

### 2. Long Function (Quality)
**Line 30-95**: Function is 65 lines (max recommended: 50)
**Suggested**: Extract helper functions

## Positive Observations ✨
- Excellent error handling
- Good use of async/await
- Clear variable names
- Comprehensive docstrings

## Recommendations
1. Fix SQL injection immediately (security risk)
2. Optimize N+1 queries (performance impact)
3. Add type hints for better IDE support
4. Consider extracting smaller functions

## Score Breakdown
- Security: 60/100 ⚠️
- Performance: 70/100
- Quality: 85/100
- Style: 90/100
- Testing: 75/100
- Architecture: 80/100

**Overall: 78/100** (Team Average: 82/100)
```

## Strictness Levels

### Lenient
- Only critical and major issues
- Focuses on correctness
- Minimal style feedback

### Standard (Default)
- All severity levels
- Balanced feedback
- Best practices

### Strict
- Nitpicky style checks
- Enforces all conventions
- Maximum quality bar

## Best Practices

- Review before committing
- Fix critical issues immediately
- Address major issues before merge
- Use strict mode for production code
- Learn from feedback patterns
- Save common issues to GAM

## Integration

### Pre-commit Hook
```bash
uv run python -m app.tools.code_review --target current
```

### CI/CD Pipeline
```yaml
- name: Code Review
  run: uv run python -m app.tools.code_review --target pr
```

### Git Alias
```bash
git config alias.review '!uv run python -m app.tools.code_review'
```

## Related Commands

- `/qa-critic` - Quick quality check
- `/validate-architecture` - Pre-implementation review
- `/debug-assistant` - Fix issues found in review
- `/refactor-batch` - Apply review suggestions
