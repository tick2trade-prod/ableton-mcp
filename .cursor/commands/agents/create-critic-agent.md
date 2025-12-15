# Create Critic Agent

## Overview

Create a QA/Critic agent for architecture review and code validation. The Critic agent acts as a "Senior Architect" to catch issues, anti-patterns, and hallucinations before implementation.

## Usage

Type `/create-critic-agent` followed by what to review.

## Parameters

- `target`: What to review (plan, code, architecture) (required)
- `content`: Content to review (required)
- `strict_mode`: Fail on warnings (default: false)
- `min_score`: Minimum acceptable score (default: 70)

## Example Usage

### Review Architecture Plan

```
/create-critic-agent
Target: plan
Content: |
  Feature: Microservices architecture with:
  - FastAPI gateway
  - Redis for caching
  - PostgreSQL for persistence
  - RabbitMQ for messaging
Strict Mode: true
Min Score: 80
```

### Review Code

```
/create-critic-agent
Target: code
Content: |
  def process_user(user_id):
      user = db.query(User).filter(User.id == user_id).first()
      return user.email
Min Score: 70
```

### Review File

```
/create-critic-agent
Target: file
File Path: app/services/auth.py
Strict Mode: false
```

## Workflow

1. **Create Agent**:
   - Call `app.server.agents.factory.create_agent("critic")`
   - Inject `CRITIC_SYSTEM_PROMPT` with review context
   - Attach tools: `gam_tool`, `package_tool`

2. **Context Gathering**:
   - Load target content (plan, code, or file)
   - Gather related files and dependencies
   - Query GAM for known issues

3. **Analysis Phase**:
   - Check for security vulnerabilities
   - Identify performance issues
   - Detect anti-patterns
   - Find code smells
   - Validate error handling
   - Check for hallucinated dependencies

4. **Scoring**:
   - Calculate overall score (0-100)
   - Categorize issues: critical, warnings, suggestions
   - Provide specific line numbers
   - Suggest fixes

5. **Output**:
   - Return structured QAReport (Pydantic model)
   - Block if score < min_score
   - Provide actionable suggestions
   - Link to relevant documentation

## Implementation

This command uses:
- **Agent Factory**: `app.server.agents.factory.create_agent()`
- **System Prompt**: `app.server.agents.prompts.CRITIC_SYSTEM_PROMPT`
- **GAM Integration**: `app.core.GAMMemoryManager`
- **Tools**: `gam_tool`, `package_tool`
- **QA Models**: `app.server.protocols.qa_models`

## Output Format

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
  "summary": "Code is generally good but has security concerns",
  "passed": true
}
```

## QA Dimensions

The Critic agent evaluates:

1. **Architecture**: Design patterns, scalability, maintainability
2. **Security**: Vulnerabilities, input validation, authentication
3. **Performance**: Bottlenecks, inefficient queries, caching
4. **Code Quality**: Readability, complexity, documentation
5. **Dependencies**: Package validation, version conflicts
6. **Testing**: Test coverage, edge cases

## Best Practices

- Run before committing code
- Use strict_mode for production
- Set appropriate min_score thresholds
- Review all critical issues
- Address warnings when possible
- Save common issues to GAM

## Related Commands

- `/execute-qa-skill` - Full QA workflow
- `/validate-architecture` - Pre-generation validation
- `/verify-packages` - Package validation
- `/gam-research` - Research known issues

## Requirements

- Ollama server running (for agent execution)
- GAM memory initialized
- Package validation tools available
