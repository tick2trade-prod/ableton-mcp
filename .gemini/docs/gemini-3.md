# Gemini 3 Pro

> Source: [https://geminicli.com/docs/get-started/gemini-3](https://geminicli.com/docs/get-started/gemini-3)

## Overview

Gemini 3 Pro is Google's most advanced model, offering enhanced reasoning, coding, and multimodal capabilities.

## Enabling Gemini 3

### Via Configuration

```json
{
  "model": "gemini-3-pro"
}
```

### Via Command Line

```bash
gemini --model gemini-3-pro
```

### Via Slash Command

```
/model gemini-3-pro
```

## Features

### Enhanced Reasoning
- Complex multi-step problem solving
- Better code understanding
- Improved context retention

### Multimodal Capabilities
- Image understanding
- Code screenshot analysis
- Diagram interpretation

### Larger Context Window
- Up to 1M tokens
- Better long-form reasoning

## When to Use Gemini 3

| Use Case | Recommended |
|----------|-------------|
| Complex refactoring | ✓ Gemini 3 Pro |
| Simple edits | Gemini 2.5 Flash |
| Research + planning | ✓ Gemini 3 Pro |
| Quick queries | Gemini 2.5 Flash |

## ableton-mcp Usage

For this project, Gemini 3 Pro excels at:
- Analyzing complex track scripts
- Multi-step MCP tool development
- Research synthesis with planning

```bash
# Complex task
gemini --model gemini-3-pro "Analyze the track scripts and suggest improvements"
```

## Related Pages

- [Model Selection](model-selection.md) - All available models
- [Configuration](configuration.md) - Settings
