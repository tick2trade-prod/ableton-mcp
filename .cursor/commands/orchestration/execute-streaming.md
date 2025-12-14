# Orchestrator: Execute Workflow Streaming

## Overview

Execute workflow with progress updates. This command invokes the `execute_workflow_streaming()` function from `app/server/orchestrator.py` to execute workflows with real-time streaming progress updates.

## Usage

Type `/orchestrator-execute-streaming` followed by the feature name.

## Parameters

- `feature_name`: Name of feature to implement (required)
- `workflow_id`: Optional workflow ID (auto-generated if not provided)
- `stream_type`: Stream type (progress, code, all) (default: "all")
- `include_thinking`: Include thinking steps (default: true)

## Example Usage

### Stream Full Workflow

```
/orchestrator-execute-streaming
Feature Name: User authentication with JWT
Stream Type: all
Include Thinking: true
```

### Stream Progress Only

```
/orchestrator-execute-streaming
Feature Name: Payment processing
Stream Type: progress
```

### Resume with Streaming

```
/orchestrator-execute-streaming
Feature Name: User authentication
Workflow ID: workflow-abc123
```

## Stream Types

### Progress Stream

Real-time progress updates.

```json
{
    "type": "progress",
    "content": "Planning phase started",
    "metadata": {
        "step": "planning",
        "state": "in_progress",
        "percent_complete": 10
    },
    "timestamp": "2025-12-04T10:30:00Z"
}
```

### Code Stream

Generated code chunks.

```json
{
    "type": "code",
    "content": "from fastapi import APIRouter\n",
    "metadata": {
        "file": "app/api/auth.py",
        "language": "python",
        "chunk_index": 0
    },
    "timestamp": "2025-12-04T10:32:15Z"
}
```

### Thinking Stream

Reasoning and decision-making.

```json
{
    "type": "thinking",
    "content": "Considering JWT vs session-based authentication...",
    "metadata": {
        "step": "planning",
        "thinking_step": 2
    },
    "timestamp": "2025-12-04T10:30:30Z"
}
```

### Error Stream

Errors and warnings.

```json
{
    "type": "error",
    "content": "Linting warning: Missing type hint on line 42",
    "metadata": {
        "severity": "warning",
        "file": "app/api/auth.py",
        "line": 42
    },
    "timestamp": "2025-12-04T10:33:00Z"
}
```

### Done Stream

Workflow completion.

```json
{
    "type": "done",
    "content": "Workflow completed successfully",
    "metadata": {
        "success": true,
        "latency_ms": 45678,
        "files_created": 5,
        "tests_passed": 12
    },
    "timestamp": "2025-12-04T10:40:00Z"
}
```

## Streaming Workflow

### Async Generator

```python
from app.server.orchestrator import execute_workflow_streaming

# Stream workflow
async for chunk in execute_workflow_streaming(
    feature_name="User authentication with JWT"
):
    if chunk.type == "progress":
        print(f"Progress: {chunk.content}")
    elif chunk.type == "code":
        print(chunk.content, end="", flush=True)
    elif chunk.type == "thinking":
        print(f"Thinking: {chunk.content}")
    elif chunk.type == "error":
        print(f"Error: {chunk.content}")
    elif chunk.type == "done":
        print(f"Done: {chunk.metadata}")
```

## Workflow Phases with Streaming

### Phase 1: Planning

```
Stream: progress | "Starting workflow for 'User authentication'"
Stream: thinking | "Understanding requirements..."
Stream: thinking | "Querying GAM for authentication patterns..."
Stream: progress | "Planning phase started"
Stream: thinking | "Creating implementation plan..."
Stream: progress | "Planning completed: 5 tasks identified"
```

### Phase 2: Implementation

```
Stream: progress | "Implementation phase started"
Stream: code | "from fastapi import APIRouter\n"
Stream: code | "from pydantic import BaseModel\n"
Stream: code | "...\n"
Stream: progress | "Generated app/api/auth.py (45 lines)"
Stream: progress | "Running linting..."
Stream: progress | "Linting passed"
Stream: progress | "Implementation completed"
```

### Phase 3: Review

```
Stream: progress | "Review phase started"
Stream: thinking | "Running QA validation..."
Stream: progress | "QA score: 85/100"
Stream: progress | "Creating pull request..."
Stream: progress | "PR created: #123"
Stream: done | "Workflow completed successfully"
```

## Output Format

### Complete Stream

```python
[
    {
        "type": "progress",
        "content": "Starting workflow for 'User authentication'",
        "metadata": {"workflow_id": "workflow-abc123", "step": "start"}
    },
    {
        "type": "thinking",
        "content": "Understanding requirements...",
        "metadata": {"step": "planning", "thinking_step": 1}
    },
    # ... more chunks ...
    {
        "type": "done",
        "content": '{"workflow_id": "workflow-abc123", "success": true, ...}',
        "metadata": {"success": true, "latency_ms": 45678}
    }
]
```

## Best Practices

- Stream all types for full visibility
- Display progress to user
- Handle errors gracefully
- Show thinking for transparency
- Buffer code chunks for display
- Parse done chunk for final result

## Integration

- Uses OpenTelemetry for tracing
- Streams via async generators
- Integrates with all skills
- Provides real-time feedback

## Related Commands

- `/execute-workflow` - Non-streaming workflow
- `/execute-task` - Single task execution
- `/generate-code-streaming` - Streaming code generation
- `/skill-planning` - Planning phase
- `/skill-implementation` - Implementation phase

## Source

- **File**: `app/server/orchestrator.py`
- **Function**: `execute_workflow_streaming()`
- **Layer**: Orchestrator (Router)
