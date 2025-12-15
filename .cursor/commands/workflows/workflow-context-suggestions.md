# Workflow: Context-Aware Code Suggestions

## Overview

AI agent understands entire project structure to provide code suggestions aligned with existing architecture and coding standards.

## Usage

```bash
/workflow-context-suggestions
```

## Parameters

- `file_path`: File to analyze (required)
- `suggestion_types`: refactor, optimize, security, style (default: all)
- `max_suggestions`: Maximum suggestions (default: 10)
- `auto_apply`: Auto-apply safe suggestions (default: false)

## Suggestion Types

```python
# Refactoring
- Extract method
- Rename variable
- Simplify logic
- Remove duplication

# Optimization
- Algorithm improvement
- Database query optimization
- Caching opportunities
- Resource usage

# Security
- Input validation
- Authentication checks
- Authorization checks
- Secrets management

# Style
- Naming conventions
- Code formatting
- Documentation
- Type hints
```

## Output

```json
{
  "suggestions": [
    {
      "type": "refactor",
      "title": "Extract method",
      "description": "...",
      "confidence": 0.95,
      "auto_applicable": true
    }
  ],
  "auto_applied": 3,
  "manual_review": 2
}
```
