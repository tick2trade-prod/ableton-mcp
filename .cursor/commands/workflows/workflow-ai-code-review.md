# Workflow: AI-Powered Context-Aware Code Review

## Overview

Autonomous AI agent performs deep, context-aware code reviews analyzing code quality, security vulnerabilities, performance issues, and adherence to coding standards. Provides actionable feedback with improvement suggestions.

## Usage

```bash
/workflow-ai-code-review
```

## Parameters

- `pr_number`: PR number to review (required if not in PR context)
- `focus`: Review focus areas - comma-separated (default: "all")
  - Options: security, performance, maintainability, testing, documentation, architecture
- `depth`: Review depth - shallow, standard, deep (default: standard)
- `auto_comment`: Automatically post review comments (default: true)
- `auto_approve`: Auto-approve if no issues found (default: false)
- `block_on_critical`: Block merge on critical issues (default: true)
- `suggest_fixes`: Generate fix suggestions (default: true)
- `stream_output`: Stream review in real-time (default: true)

## Workflow Steps

### 1. Context Gathering (Autonomous)

```python
from app.core.gam_memory import GAMMemoryManager
from app.server.tools.search import search_codebase

gam = GAMMemoryManager()

# Fetch PR details
pr_details = fetch_pr_details(pr_number)

# Research similar code reviews from GAM
similar_reviews = gam.research(
    f"code reviews for {pr_details.technology_stack}",
    max_iters=5
)

# Search codebase for related code
related_code = await search_codebase(
    query=pr_details.feature_description,
    file_types=pr_details.file_extensions
)

# Fetch project conventions
conventions = load_project_conventions()
```

### 2. Multi-Dimensional Analysis (Streaming)

```python
from app.server.agents.critic import create_critic_agent

# Create specialized critic agent
critic = await create_critic_agent(focus_areas=focus.split(','))

# Analyze each dimension
review_dimensions = {
    "security": await critic.analyze_security(pr_details.diff),
    "performance": await critic.analyze_performance(pr_details.diff),
    "maintainability": await critic.analyze_maintainability(pr_details.diff),
    "testing": await critic.analyze_testing(pr_details.diff),
    "documentation": await critic.analyze_documentation(pr_details.diff),
    "architecture": await critic.analyze_architecture(pr_details.diff),
}
```

### 3. Issue Detection & Categorization

```python
from app.server.protocols.qa_models import CritiqueIssue, QAReport

issues = []

for dimension, analysis in review_dimensions.items():
    for finding in analysis.findings:
        issue = CritiqueIssue(
            dimension=dimension,
            severity=finding.severity,  # critical, high, medium, low, info
            title=finding.title,
            description=finding.description,
            file_path=finding.file_path,
            line_number=finding.line_number,
            suggestion=finding.suggestion if suggest_fixes else None,
            code_snippet=finding.code_snippet,
            references=finding.references
        )
        issues.append(issue)

# Sort by severity
issues.sort(key=lambda x: severity_rank(x.severity), reverse=True)
```

### 4. Generate Fix Suggestions (Autonomous)

```python
from app.server.tools.coder_tool import generate_code

if suggest_fixes:
    for issue in issues:
        if issue.severity in ["critical", "high"]:
            # Agent generates fix
            fix = await generate_code(
                prompt=f"""
                Fix this {issue.severity} issue:
                {issue.description}

                Current code:
                {issue.code_snippet}

                Context:
                {related_code}
                """,
                language=detect_language(issue.file_path),
                context=similar_reviews
            )

            issue.suggested_fix = fix
```

### 5. Create Review Report

```python
report = QAReport(
    pr_number=pr_number,
    reviewer="AI Code Reviewer",
    timestamp=datetime.now(),
    overall_score=calculate_overall_score(issues),
    issues=issues,
    summary=generate_summary(issues),
    recommendation=determine_recommendation(issues),
    estimated_fix_time=estimate_fix_time(issues)
)

# Memorize review for learning
gam.memorize(f"""
Code Review: PR #{pr_number}
Feature: {pr_details.title}
Issues Found: {len(issues)}
Critical: {count_by_severity(issues, 'critical')}
High: {count_by_severity(issues, 'high')}
Recommendation: {report.recommendation}
""")
```

### 6. Post Review Comments (Autonomous)

```python
from app.server.tools.fallback import execute_git_command

if auto_comment:
    # Post inline comments
    for issue in issues:
        post_review_comment(
            pr_number=pr_number,
            file_path=issue.file_path,
            line_number=issue.line_number,
            body=format_comment(issue)
        )

    # Post summary comment
    post_review_summary(
        pr_number=pr_number,
        body=format_summary(report)
    )

    # Approve or request changes
    if report.recommendation == "approve" and auto_approve:
        approve_pr(pr_number)
    elif report.recommendation == "reject" and block_on_critical:
        request_changes(pr_number, reason=report.summary)
```

## Example Usage

### Standard Review
```bash
/workflow-ai-code-review
  pr_number=123
  focus="all"
  depth="standard"
```

### Security-Focused Review
```bash
/workflow-ai-code-review
  pr_number=456
  focus="security,performance"
  depth="deep"
  block_on_critical=true
```

### Quick Review for Hotfix
```bash
/workflow-ai-code-review
  pr_number=789
  focus="security"
  depth="shallow"
  auto_approve=true
```

## Integration with App Architecture

### Skills Used
```python
from app.server.skills.review import execute_review
from app.server.skills.planning import research_and_plan
```

### Tools Used
```python
from app.server.tools.gam_tool import research_memory
from app.server.tools.search import search_codebase
from app.server.tools.coder_tool import generate_code
```

### Agents Used
```python
from app.server.agents.critic import create_critic_agent
# Uses specialized "Senior Architect" critic agent
```

## Autonomous Agent Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CONTEXT PHASE (Autonomous)                               │
│    - Agent fetches PR details                               │
│    - Agent researches similar reviews from GAM              │
│    - Agent searches codebase for related code               │
│    - Agent loads project conventions                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. ANALYSIS PHASE (Streaming)                               │
│    - Agent analyzes security (streaming)                    │
│    - Agent analyzes performance (streaming)                 │
│    - Agent analyzes maintainability (streaming)             │
│    - Agent analyzes testing (streaming)                     │
│    - Agent analyzes documentation (streaming)               │
│    - Agent analyzes architecture (streaming)                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. DETECTION PHASE (Autonomous)                             │
│    - Agent categorizes issues by severity                   │
│    - Agent prioritizes critical issues                      │
│    - Agent generates fix suggestions                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. REPORTING PHASE (Streaming)                              │
│    - Agent generates review report (streaming)              │
│    - Agent calculates overall score                         │
│    - Agent provides recommendation                          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. ACTION PHASE (Autonomous)                                │
│    - Agent posts inline comments                            │
│    - Agent posts summary comment                            │
│    - Agent approves or requests changes                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. LEARNING PHASE (Memorization)                            │
│    - Agent memorizes review patterns                        │
│    - Agent learns from developer responses                  │
│    - Agent improves detection accuracy                      │
└─────────────────────────────────────────────────────────────┘
```

## Review Dimensions

### 1. Security Analysis
```python
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Secrets in code
- Insecure dependencies
- CSRF vulnerabilities
- Input validation issues
```

### 2. Performance Analysis
```python
- N+1 query problems
- Inefficient algorithms
- Memory leaks
- Unnecessary database calls
- Missing indexes
- Blocking operations
- Resource exhaustion risks
```

### 3. Maintainability Analysis
```python
- Code complexity (cyclomatic)
- Code duplication
- Naming conventions
- Function length
- Class cohesion
- Coupling issues
- SOLID principles violations
```

### 4. Testing Analysis
```python
- Test coverage
- Missing edge cases
- Flaky tests
- Test quality
- Integration test gaps
- Mock usage
```

### 5. Documentation Analysis
```python
- Missing docstrings
- Outdated comments
- API documentation
- README updates
- Changelog entries
```

### 6. Architecture Analysis
```python
- Design pattern violations
- Layering violations
- Dependency direction
- Circular dependencies
- Interface segregation
```

## Comment Format

```markdown
### 🔴 Critical: SQL Injection Vulnerability

**File**: `app/api/users.py`
**Line**: 42

**Issue**:
User input is directly interpolated into SQL query without sanitization.

**Current Code**:
```python
query = f"SELECT * FROM users WHERE email = '{email}'"
```

**Suggested Fix**:
```python
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

**References**:
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- Similar fix in PR #456

**Estimated Fix Time**: 5 minutes
```

## Review Report Format

```markdown
# AI Code Review Report

**PR**: #123 - Add user authentication
**Reviewer**: AI Code Reviewer
**Date**: 2024-12-04 10:30:00
**Overall Score**: 7.5/10

## Summary

Reviewed 12 files with 450 lines changed. Found 8 issues across 6 dimensions.

## Issues by Severity

- 🔴 **Critical**: 1
- 🟠 **High**: 2
- 🟡 **Medium**: 3
- 🔵 **Low**: 2
- ⚪ **Info**: 0

## Detailed Findings

### Security (2 issues)
1. 🔴 SQL Injection in user query (Line 42)
2. 🟠 Weak password hashing (Line 78)

### Performance (1 issue)
1. 🟡 N+1 query in user list (Line 120)

### Maintainability (3 issues)
1. 🟠 High cyclomatic complexity (Line 150)
2. 🟡 Code duplication (Lines 200-220)
3. 🔵 Long function (Line 250)

### Testing (2 issues)
1. 🟡 Missing edge case tests
2. 🔵 Low test coverage (65%)

## Recommendation

**Request Changes** - Critical security issue must be fixed before merge.

## Estimated Fix Time

- Critical issues: 30 minutes
- High priority issues: 1 hour
- Medium priority issues: 2 hours
- **Total**: 3.5 hours

## Next Steps

1. Fix SQL injection vulnerability (Critical)
2. Improve password hashing (High)
3. Reduce cyclomatic complexity (High)
4. Address remaining issues (Medium/Low)

## Learning Notes

This PR follows similar patterns to PR #456. Consider creating a reusable authentication module.
```

## Output

Returns:
```json
{
  "pr_number": 123,
  "overall_score": 7.5,
  "recommendation": "request_changes",
  "issues_count": {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 2,
    "info": 0
  },
  "estimated_fix_time_hours": 3.5,
  "review_url": "https://github.com/org/repo/pull/123#pullrequestreview-123456",
  "dimensions_analyzed": [
    "security",
    "performance",
    "maintainability",
    "testing",
    "documentation",
    "architecture"
  ],
  "auto_approved": false,
  "changes_requested": true
}
```

## Error Handling

- **PR not found**: Verify PR number and retry
- **Insufficient permissions**: Request GitHub token with review permissions
- **Rate limit exceeded**: Queue review for later
- **Analysis timeout**: Fall back to shallow review
- **Invalid diff format**: Request re-push

## Performance

- **Avg execution time**: 45 seconds (standard), 2-3 minutes (deep)
- **GAM queries**: 3-5
- **GitHub API calls**: 5-10
- **Streaming**: Real-time analysis output

## Related Workflows

- `/workflow-auto-pr-create` - Create PR before review
- `/workflow-security-scan` - Deep security analysis
- `/workflow-context-suggestions` - Code improvement suggestions
- `/workflow-merge-deploy` - Merge after approval

## Best Practices

1. **Start with standard depth**: Use deep only for critical PRs
2. **Focus on relevant dimensions**: Don't analyze everything for small PRs
3. **Enable streaming**: Watch analysis in real-time
4. **Trust the agent**: It learns from past reviews
5. **Review the suggestions**: Agent-generated fixes are high quality

## Learning & Improvement

The workflow learns from:
- ✅ Developer acceptance of suggestions
- ✅ Post-merge issues
- ✅ False positive rates
- ✅ Review quality feedback
- ✅ Fix implementation patterns

This data improves:
- 🎯 Issue detection accuracy
- 🎯 Severity classification
- 🎯 Fix suggestion quality
- 🎯 False positive reduction
