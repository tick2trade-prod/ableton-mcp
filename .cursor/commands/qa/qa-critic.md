# QA Critic

## Overview

Run the Critic agent to review code, plans, or architecture for quality issues, anti-patterns, and potential bugs.

## Usage

Type `/qa-critic` followed by what to review.

## Parameters

- `target`: What to review (code, plan, architecture, file) (required)
- `file_path`: Path to file to review (optional)
- `strict_mode`: Fail on warnings (default: false)
- `min_score`: Minimum acceptable score (default: 70)

## Example Usage

### Review Current File

```
/qa-critic
Target: file
File Path: app/services/auth.py
Min Score: 80
```

### Review Architecture Plan

```
/qa-critic
Target: plan
Plan: |
  Create microservices architecture with:
  - FastAPI gateway
  - Redis for caching
  - PostgreSQL for persistence
  - RabbitMQ for messaging
Strict Mode: true
```

### Review Code Snippet

```
/qa-critic
Target: code
Code: |
  def process_user(user_id):
      user = db.query(User).filter(User.id == user_id).first()
      return user.email
```

## Workflow

1. **Extract Context**:
   - Load file or parse provided code/plan
   - Gather related files and dependencies
   - Check GAM for known issues

2. **Run Critic Agent**:
   - Invoke with `CRITIC_SYSTEM_PROMPT`
   - Request structured `QAReport` (JSON)
   - Analyze for:
     - Security vulnerabilities
     - Performance issues
     - Anti-patterns
     - Code smells
     - Missing error handling
     - Hallucinated dependencies

3. **Generate Report**:
   - Overall score (0-100)
   - Critical issues (must fix)
   - Warnings (should fix)
   - Suggestions (nice to have)
   - Specific line numbers for issues

4. **Action Items**:
   - If score < min_score, block and require fixes
   - Output actionable suggestions
   - Link to relevant documentation

## QA Report Format

```json
{
  "score": 85,
  "critical_issues": [],
  "warnings": [
    {
      "line": 42,
      "issue": "SQL injection vulnerability",
      "suggestion": "Use parameterized queries",
      "severity": "high"
    }
  ],
  "suggestions": [
    {
      "line": 15,
      "issue": "Missing type hints",
      "suggestion": "Add type annotations for better IDE support"
    }
  ],
  "summary": "Code is generally good but has security concerns"
}
```

## Best Practices

- Run before committing code
- Use strict_mode for production code
- Set appropriate min_score thresholds
- Review all critical issues
- Address warnings when possible
- Save common issues to GAM

## Integration

- Pre-commit hook: `uv run python -m app.tools.qa_critic --file {file}`
- CI/CD: Run on all changed files
- IDE: Integrate with linting tools

## Related Commands

- `/validate-architecture` - Pre-generation validation
- `/generate-code-streaming` - Auto-QA after generation
- `/deep-research` - Research before fixing issues
