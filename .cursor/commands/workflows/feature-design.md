# Workflow: Feature Design

**Phase**: 3 - Feature Development
**ID**: 4012

## Overview

Write design doc (1-pager) for feature implementation.

## Usage

```
/workflow-feature-design feature="Real-time notifications" format="markdown"
```

## Parameters

- `feature`: Feature to design (required)
- `format`: markdown | pdf (default: "markdown")
- `include_diagrams`: Include architecture diagrams (default: true)

## Workflow Steps

1. Define feature scope
2. Design architecture
3. Identify dependencies
4. Document API contracts
5. Create design doc

## Output

```json
{
  "design_doc": "docs/design/notifications.md",
  "diagrams": ["arch.png", "flow.png"],
  "status": "ready_for_review"
}
```
