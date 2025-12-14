# Agent: Critic

## Overview

Invoke critic agent for QA review. This command directly invokes the Critic agent from `app/server/agents/factory.py` with the CRITIC_SYSTEM_PROMPT to review code, plans, and architecture for quality issues.

> **Layer**: WHO (Agent Factory)
> **Rank**: 2 - Layer-Based Command

## Usage

Type `/agent-critic` followed by what to review.

## Parameters

- `target`: What to review (code, plan, architecture) (required)
- `content`: Content to review (required)
- `context`: Additional context (optional)
- `model`: Ollama model to use (default: auto-select)
- `strict_mode`: Fail on warnings (default: false)
- `min_score`: Minimum acceptable score (default: 70)
- `structured_output`: Request QAReport JSON (default: true)

## Example Usage

### Review Code

```
/agent-critic
Target: code
Content: |
  def get_user(user_id):
      user = db.query(User).filter(User.id == user_id).first()
      return user.email
Strict Mode: true
Min Score: 80
```

### Review Architecture Plan

```
/agent-critic
Target: plan
Content: |
  Microservices architecture:
  - API Gateway (FastAPI)
  - User Service (Flask)
  - Payment Service (Django)
  - Shared PostgreSQL database
```

### Review with Context

```
/agent-critic
Target: code
Content: <file contents>
Context: This is a production authentication module
Strict Mode: true
```

## Implementation

```python
from app.server.agents.factory import create_agent
from app.server.agents.prompts import CRITIC_SYSTEM_PROMPT

agent = create_agent(
    role="critic",
    model=model,
    system_prompt=CRITIC_SYSTEM_PROMPT,
    tools=["gam_memory", "package_verify"],
)

qa_report = await agent.run(
    target=target,
    content=content,
    strict_mode=strict_mode,
    min_score=min_score,
)
```

## Workflow

1. **Agent Creation**:
   - Load CRITIC_SYSTEM_PROMPT
   - Select reasoning-capable model
   - Configure for detailed analysis

2. **Context Enhancement**:
   - Load project conventions
   - Retrieve best practices
   - Gather security guidelines

3. **Analysis Phase**:
   - Check for security vulnerabilities
   - Identify performance issues
   - Detect anti-patterns
   - Verify error handling
   - Validate dependencies

4. **Scoring**:
   - Calculate overall score (0-100)
   - Categorize issues (critical, warning, suggestion)
   - Provide specific line numbers
   - Suggest fixes

5. **Report Generation**:
   - Create structured QAReport
   - Include actionable recommendations
   - Link to documentation

## Output Format

```json
{
  "target": "code",
  "score": 65,
  "passed": false,
  "critical_issues": [
    {
      "line": 2,
      "issue": "SQL injection vulnerability",
      "description": "Using string interpolation in SQL query",
      "suggestion": "Use parameterized queries with SQLAlchemy",
      "severity": "critical",
      "references": [
        "https://owasp.org/www-community/attacks/SQL_Injection"
      ]
    }
  ],
  "warnings": [
    {
      "line": 1,
      "issue": "Missing type hints",
      "description": "Function parameters lack type annotations",
      "suggestion": "Add type hints: def get_user(user_id: int) -> str:",
      "severity": "medium"
    },
    {
      "line": 3,
      "issue": "No error handling",
      "description": "Missing null check for user",
      "suggestion": "Add check: if not user: raise HTTPException(404)",
      "severity": "high"
    }
  ],
  "suggestions": [
    {
      "issue": "Return full user object",
      "description": "Returning only email is limiting",
      "suggestion": "Return User model or UserResponse schema"
    }
  ],
  "summary": "Code has critical security vulnerability (SQL injection) and lacks error handling. Must fix before production.",
  "recommendations": [
    "Use SQLAlchemy ORM properly with parameterized queries",
    "Add comprehensive error handling",
    "Include type hints for better IDE support",
    "Return structured response models"
  ]
}
```

## Best Practices

- Always review code before committing
- Use strict mode for production code
- Set appropriate min_score thresholds
- Address all critical issues immediately
- Review warnings carefully
- Save common issues to GAM for learning

## Integration

- Used by `/skill-planning` for plan validation
- Used by `/skill-review` for code review
- Chains from `/agent-planner` and `/agent-coder`
- Saves findings via `/tool-gam`

## Related Commands

- `/qa-critic` - QA workflow command
- `/skill-review` - Full review workflow
- `/validate-architecture` - Architecture validation
- `/agent-planner` - Planning agent
- `/agent-coder` - Coding agent

## Source

- **File**: `app/server/agents/factory.py`
- **Prompt**: `app/server/agents/prompts.py` → `CRITIC_SYSTEM_PROMPT`
- **Layer**: Agents (WHO)
