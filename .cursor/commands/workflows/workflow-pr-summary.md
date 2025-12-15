# Workflow: Automated PR Summarization

## Overview

Generate concise and informative PR summaries using AI, facilitating quicker understanding and review by team members.

## Usage

```bash
/workflow-pr-summary
```

## Parameters

- `pr_number`: PR to summarize (required)
- `summary_length`: short, medium, long (default: medium)
- `include_metrics`: Include code metrics (default: true)
- `audience`: technical, non-technical, executive (default: technical)

## Summary Components

```python
# 1. High-Level Overview
- What changed
- Why it changed
- Impact assessment

# 2. Technical Details
- Files modified
- Lines changed
- Key algorithms/patterns

# 3. Testing Summary
- Test coverage
- Test types
- Edge cases covered

# 4. Risk Assessment
- Breaking changes
- Performance impact
- Security implications
```

## Output

```json
{
  "summary": "Added JWT authentication...",
  "key_changes": ["auth.py", "tests/test_auth.py"],
  "impact": "medium",
  "risk_level": "low",
  "estimated_review_time_minutes": 15
}
```
