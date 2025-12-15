# Context Optimization

## Overview

Manage token budgets and compress conversation history to prevent context overflow. Uses intelligent compression with GAM summarization and sliding window to maintain conversation coherence while staying within token limits.

## Usage

Type `/context-optimization` followed by your optimization request.

## Parameters

- `max_tokens`: Maximum token budget (default: 128000)
  - Claude: 200000
  - GPT-4: 128000
  - Ollama: 8192-32768 (model dependent)
- `compression_threshold`: Trigger compression at % usage (default: 80)
- `preserve_messages`: Number of recent messages to keep (default: 10)
- `summarize`: Use GAM to summarize compressed history (default: true)
- `mode`: Optimization mode (default: auto)
  - `auto`: Automatic compression when threshold reached
  - `aggressive`: Compress immediately
  - `conservative`: Only compress at 95% usage
  - `manual`: Manual compression only

## Example Usage

### Auto Optimization

```
/context-optimization
Max Tokens: 128000
Compression Threshold: 80
Preserve Messages: 10
Summarize: true
```

### Aggressive Compression

```
/context-optimization
Mode: aggressive
Max Tokens: 32768
Preserve Messages: 5
```

### Check Current Usage

```
/context-optimization
Mode: check
```

### Manual Compression

```
/context-optimization
Mode: manual
Preserve Messages: 15
Summarize: true
```

## Workflow

1. **Token Counting**:
   - Count current context usage with `tiktoken`:
     ```python
     encoding = tiktoken.get_encoding("cl100k_base")
     token_count = len(encoding.encode(conversation_history))
     ```
   - Track tokens by message type:
     - System prompts: ~500-1000 tokens
     - User messages: Variable
     - Assistant messages: Variable
     - Tool outputs: Variable

2. **Budget Check**:
   - Calculate usage percentage: `(current_tokens / max_tokens) * 100`
   - Alert levels:
     - **Green** (<60%): No action needed
     - **Yellow** (60-80%): Warning, consider compression
     - **Orange** (80-95%): Compression recommended
     - **Red** (>95%): Immediate compression required
   - Stream status: `"⚠️ Context usage: {current}/{max} tokens ({percent}%)"`

3. **Compression Trigger**:
   - Auto-trigger when threshold exceeded
   - Modes:
     - `auto`: Trigger at 80%
     - `aggressive`: Trigger at 60%
     - `conservative`: Trigger at 95%
     - `manual`: Never auto-trigger

4. **Sliding Window**:
   - Preserve critical messages:
     - System prompt (always keep)
     - Last N user messages (default: 10)
     - Last N assistant messages (default: 10)
     - Recent tool outputs (default: 5)
   - Compress older messages:
     - Group by conversation topic
     - Summarize each group
     - Store summaries in GAM

5. **GAM Summarization** (if enabled):
   - Summarize compressed messages:
     ```python
     summary = gam.summarize(
         messages=older_messages,
         max_length=500,
         preserve_context=True
     )
     ```
   - Store summary in GAM memory:
     ```python
     gam.memorize(
         content=summary,
         metadata={
             "type": "conversation_summary",
             "original_tokens": compressed_token_count,
             "summary_tokens": summary_token_count,
             "compression_ratio": ratio
         }
     )
     ```
   - Replace compressed messages with summary reference

6. **Compression Report**:
   - Generate compression report:
     ```json
     {
         "before_tokens": 105000,
         "after_tokens": 42000,
         "compression_ratio": 0.60,
         "messages_compressed": 45,
         "messages_preserved": 20,
         "summary_stored": true,
         "gam_memory_id": "summary-a3f8b2c1"
     }
     ```

## Token Budget Tracking

### Real-Time Monitoring

```json
{
    "current_tokens": 85000,
    "max_tokens": 128000,
    "usage_percent": 66.4,
    "status": "yellow",
    "recommendation": "Consider compression soon",
    "estimated_messages_remaining": 15
}
```

### Token Breakdown

```json
{
    "system_prompt": 512,
    "user_messages": 35000,
    "assistant_messages": 42000,
    "tool_outputs": 7500,
    "total": 85012
}
```

## Compression Strategies

### Conservative (Default)

- Preserve: Last 10 messages
- Compress: Messages older than 10
- Summarize: Group by topic
- Compression ratio: ~0.60-0.70

### Aggressive

- Preserve: Last 5 messages
- Compress: Messages older than 5
- Summarize: Aggressive summarization
- Compression ratio: ~0.40-0.50

### Smart (Context-Aware)

- Preserve: Important context messages
- Compress: Redundant or low-value messages
- Summarize: Intelligent grouping
- Compression ratio: ~0.50-0.60

## Best Practices

- Enable auto-optimization for long conversations
- Use `aggressive` mode for large refactoring tasks
- Preserve more messages for complex debugging
- Enable GAM summarization for context retention
- Monitor token usage before starting workflows
- Set lower max_tokens for Ollama models
- Use `check` mode to audit current usage
- Combine with `/workflow-orchestration` for automatic optimization

## Integration Points

**Calls:**
- `app/server/services/context_service.py::ContextManager`
- `app/core/gam_memory.py::GAMMemoryManager.summarize()`
- `tiktoken` library for token counting
- `app/server/services/state_service.py` for state persistence

**Used By:**
- `/workflow-orchestration` - Pre-workflow context check
- `/generate-code-streaming` - Auto-compression during generation
- `/deep-research` - Context management for long research
- `/smart-context` - Enhanced context management

## Performance Metrics

```json
{
    "operation": "compression",
    "before_tokens": 105000,
    "after_tokens": 42000,
    "compression_time_ms": 1250,
    "messages_processed": 65,
    "gam_operations": 3,
    "compression_ratio": 0.60
}
```

## Error Handling

### Compression Failure

```json
{
    "error": "Compression failed",
    "reason": "Unable to summarize messages",
    "current_tokens": 105000,
    "max_tokens": 128000,
    "recommendation": "Try manual compression or reduce preserve_messages"
}
```

### Token Overflow

```json
{
    "error": "Token limit exceeded",
    "current_tokens": 130000,
    "max_tokens": 128000,
    "overflow": 2000,
    "action": "Emergency compression triggered",
    "result": "Compressed to 45000 tokens"
}
```

## Optimization Report

```
🔍 Context Optimization Report

📊 Before Compression:
  - Total tokens: 105,000
  - System prompt: 512 tokens
  - User messages: 35,000 tokens (45 messages)
  - Assistant messages: 42,000 tokens (45 messages)
  - Tool outputs: 7,500 tokens (20 outputs)
  - Usage: 82% (⚠️ Orange)

🗜️ Compression Applied:
  - Strategy: Conservative
  - Messages compressed: 45
  - Messages preserved: 20
  - Summaries created: 3
  - GAM memory stored: Yes

✅ After Compression:
  - Total tokens: 42,000
  - Compression ratio: 60%
  - Tokens saved: 63,000
  - Usage: 33% (✅ Green)
  - Estimated messages remaining: 40+

💾 GAM Summary:
  - Summary ID: summary-a3f8b2c1
  - Summary tokens: 500
  - Original tokens: 63,000
  - Compression: 99.2%
```

## Related Commands

- `/smart-context` - Enhanced context management
- `/workflow-orchestration` - Includes automatic context checks
- `/generate-code-streaming` - Auto-compression during generation
- `/deep-research` - Long-running tasks with context management
