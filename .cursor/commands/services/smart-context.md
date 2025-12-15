# Smart Context Optimization

## Overview

Manually optimize the context window before large refactors. Compresses history and injects relevant knowledge to save tokens.

## Usage

Type `/smart-context` to analyze and optimize current context.

## Parameters

- `action`: Action to perform (analyze, compress, inject, reset) (default: analyze)
- `compression_ratio`: Percentage of history to compress (default: 50)
- `knowledge_limit`: Max GAM snippets to inject (default: 3)

## Example Usage

### Analyze Context

```
/smart-context
Action: analyze
```

### Compress History

```
/smart-context
Action: compress
Compression Ratio: 50
```

### Inject Knowledge

```
/smart-context
Action: inject
Knowledge Limit: 5
```

### Full Optimization

```
/smart-context
Action: compress
Compression Ratio: 60
Knowledge Limit: 3
```

## Workflow

1. **Analyze Usage**:
   - Call `context_manager.get_context_window()`
   - Report current token count and percentage of limit
   - Display breakdown: system, user, assistant, tools

2. **Summarize History**:
   - If requested, execute `context_manager.compress_middle_history()`
   - Replace middle X% of conversation with concise summary
   - Preserve recent context and initial instructions

3. **Knowledge Injection**:
   - Fetch *only* most relevant N snippets from GAM for active file
   - Inject as fresh "System Note" at end of context
   - Avoid duplicate information

4. **Reset**:
   - Clear stale tool outputs or error logs from context
   - Remove redundant file reads
   - Optimize for next operation

## Best Practices

- Run before large refactors or batch operations
- Compress when context usage > 70%
- Inject knowledge for complex tasks
- Reset after completing major features
- Monitor token usage regularly

## Context Limits

- **Standard**: ~200K tokens
- **Extended**: ~1M tokens
- **Warning Threshold**: 80% usage
- **Auto-compress**: 90% usage

## Related Commands

- `/generate-code-streaming` - Uses optimized context
- `/batch-implement` - Benefits from compression
- `/deep-research` - Injects knowledge automatically
