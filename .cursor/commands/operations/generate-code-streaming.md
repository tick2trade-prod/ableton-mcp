# Generate Code with Streaming

## Overview

Real-time code generation with immediate feedback and context awareness. Optimized for low latency with streaming output.

## Usage

Type `/generate-code-streaming` followed by your code generation request.

## Parameters

- `task`: Code generation task description (required)
- `language`: Programming language (default: python)
- `agent_name`: Optional agent name
- `skip_research`: Skip web research for faster generation (default: false)

## Example Usage

### Basic Streaming Generation

```
/generate-code-streaming
Task: Create a FastAPI endpoint for user authentication
Language: python
```

### Quick Generation (No Research)

```
/generate-code-streaming
Task: Add logging to existing function
Skip Research: true
```

### With Context Check

```
/generate-code-streaming
Task: Refactor database connection logic
Language: python
Agent: coder
```

## Workflow

1. **Context Check**:
   - Call `context_manager.get_context_window()` to ensure budget is safe
   - If usage > 80%, auto-compress history before starting

2. **Research (Low Latency)**:
   - Perform quick GAM memory lookup: `gam.research_memory(query, limit=3)`
   - *Optimization:* Skip web search unless explicitly requested

3. **Thinking Phase**:
   - Use `thinking_tool.format_thinking_prompt()` to structure the request
   - Extract `<thinking>` blocks to validate approach before generation

4. **Streaming Execution**:
   - Call `execute_workflow_streaming(task, mode="code")`
   - Stream output tokens directly to editor as they arrive
   - *Key:* Do not wait for full completion to show progress

5. **QA Loop**:
   - Once generation complete, auto-trigger `coder_tool.robust_file_write()`
   - If linting fails, stream error back and auto-retry (max 1 attempt)

## Best Practices

- Use for interactive, real-time code generation
- Enable skip_research for quick edits
- Monitor streaming output for early error detection
- Leverage context compression for large refactors

## Related Commands

- `/validate-architecture` - Pre-generation validation
- `/batch-implement` - Parallel multi-file generation
- `/generate-code` - Standard non-streaming generation
