# Execute QA Skill

## Overview

Execute comprehensive QA workflow: Architecture review + code validation + security check. Orchestrates Critic agent with package validation and best practices enforcement.

## Usage

Type `/execute-qa-skill` followed by review target.

## Parameters

- `target`: What to review (plan, code, file, architecture) (required)
- `content`: Content to review (required if not file)
- `file_path`: Path to file (required if target=file)
- `strict_mode`: Fail on warnings (default: false)
- `min_score`: Minimum acceptable score (default: 70)

## Example Usage

### Review Architecture Plan

```
/execute-qa-skill
Target: plan
Content: |
  Feature: Microservices architecture
  Components:
  - FastAPI gateway
  - Redis for caching
  - PostgreSQL for persistence
  - RabbitMQ for messaging
Strict Mode: true
Min Score: 80
```

### Review Code File

```
/execute-qa-skill
Target: file
File Path: app/services/auth.py
Min Score: 80
```

### Review Code Snippet

```
/execute-qa-skill
Target: code
Content: |
  def process_user(user_id):
      user = db.query(User).filter(User.id == user_id).first()
      return user.email
Strict Mode: true
```

## Workflow

1. **Context Gathering**:
   - Load target content (plan, code, or file)
   - Gather related files and dependencies
   - Query GAM for known issues
   - Extract dependencies

2. **Package Validation**:
   - Extract all dependencies
   - Call `/verify-packages`
   - **HALT** if hallucinated packages found
   - Report invalid packages

3. **Architecture Review**:
   - Call `/create-critic-agent`
   - Analyze architecture patterns
   - Check scalability
   - Validate design decisions
   - Identify potential bottlenecks

4. **Security Review**:
   - Check for SQL injection
   - Validate input sanitization
   - Check authentication/authorization
   - Identify exposed secrets
   - Validate HTTPS usage

5. **Performance Review**:
   - Identify N+1 queries
   - Check caching strategy
   - Validate async usage
   - Check connection pooling
   - Identify blocking operations

6. **Code Quality Review**:
   - Check readability
   - Validate complexity
   - Check documentation
   - Validate type hints
   - Check error handling

7. **Scoring**:
   - Calculate overall score (0-100)
   - Weight by severity (critical > warning > suggestion)
   - Generate detailed report
   - Provide actionable fixes

8. **Output**:
   - Return structured QAReport
   - Block if score < min_score
   - Provide fix suggestions
   - Link to documentation

## Implementation

This command uses:
- **QA Skill**: `app.server.skills.qa/`
- **Plan Critic**: `app.server.skills.qa.plan_critic`
- **Code Critic**: `app.server.skills.qa.code_critic`
- **Critic Agent**: `app.server.agents.factory.create_agent("critic")`
- **Package Tool**: `app.server.tools.package_tool`

## Output Format

```json
{
  "score": 85,
  "passed": true,
  "dimensions": {
    "architecture": 90,
    "security": 80,
    "performance": 85,
    "code_quality": 85,
    "dependencies": 90
  },
  "critical_issues": [],
  "warnings": [
    {
      "dimension": "security",
      "file": "app/services/auth.py",
      "line": 42,
      "issue": "SQL injection vulnerability",
      "suggestion": "Use parameterized queries",
      "severity": "high"
    },
    {
      "dimension": "performance",
      "file": "app/api/users.py",
      "line": 25,
      "issue": "N+1 query detected",
      "suggestion": "Use eager loading with joinedload()",
      "severity": "medium"
    }
  ],
  "suggestions": [
    {
      "dimension": "code_quality",
      "file": "app/services/auth.py",
      "line": 15,
      "issue": "Missing type hints",
      "suggestion": "Add type annotations for better IDE support"
    }
  ],
  "package_validation": {
    "total": 8,
    "valid": 8,
    "invalid": [],
    "all_valid": true
  },
  "summary": "Code is generally good but has security concerns that should be addressed"
}
```

## QA Dimensions

1. **Architecture** (Weight: 30%)
   - Design patterns
   - Scalability
   - Maintainability
   - Separation of concerns

2. **Security** (Weight: 25%)
   - Vulnerabilities
   - Input validation
   - Authentication/Authorization
   - Secret management

3. **Performance** (Weight: 20%)
   - Query optimization
   - Caching strategy
   - Async usage
   - Resource management

4. **Code Quality** (Weight: 15%)
   - Readability
   - Complexity
   - Documentation
   - Type hints

5. **Dependencies** (Weight: 10%)
   - Package validation
   - Version compatibility
   - Security advisories

## Best Practices

- Run before committing code
- Use strict_mode for production
- Set appropriate min_score thresholds
- Review all critical issues
- Address warnings when possible
- Save common issues to GAM
- Integrate with CI/CD

## Related Commands

- `/create-critic-agent` - Standalone Critic agent
- `/validate-architecture` - Pre-generation validation
- `/verify-packages` - Package validation only
- `/execute-review-skill` - Full review workflow with PR

## Requirements

- Ollama server running (for Critic agent)
- GAM memory initialized
- Internet connection (for package validation)
- Package validation tools available
