# Models

> Source: [https://antigravity.google/docs/models](https://antigravity.google/docs/models)

## Overview

Antigravity supports multiple AI models for different use cases. Understanding which model to use helps optimize your workflow.

## Available Models

### Gemini 2.5 Pro
- **Best for**: Complex reasoning, large context
- **Context window**: 1M+ tokens
- **Use case in ableton-mcp**: Analyzing entire codebase, complex refactoring

### Gemini 2.5 Flash
- **Best for**: Fast responses, standard tasks
- **Context window**: Large
- **Use case in ableton-mcp**: Quick code edits, simple queries

### Gemini 2.0 Flash
- **Best for**: Balanced speed and capability
- **Use case in ableton-mcp**: General development tasks

## Model Selection for ableton-mcp

| Task | Recommended Model |
|------|-------------------|
| Writing new MCP tools | Gemini 2.5 Pro |
| Quick test fixes | Gemini 2.5 Flash |
| Research + Planning | Gemini 2.5 Pro |
| Simple refactoring | Gemini 2.0 Flash |

## Ollama for Local Inference

For tasks requiring local LLM inference:

### Recommended Models

```bash
# Fast, efficient
ollama pull llama3.2

# More capable
ollama pull llama3.1:70b

# Code-focused
ollama pull codellama
```

### Use Cases in Project

1. **Summarization**: Summarize research results locally
2. **Classification**: Categorize Ableton devices
3. **Embeddings**: Generate embeddings for semantic search

### Configuration

```python
# In MCP tools
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
```

## Model Context for This Project

When working with large context:

```markdown
# Project files typically loaded:
- pyproject.toml (112 lines)
- GEMINI.md (60 lines)
- Current working files
- Test files
- MCP server code
```

### Tips for Efficient Context Use

1. **Reference files explicitly**: `@[path/to/file.py]`
2. **Use file outlines first**: Let agent scan structure
3. **Split large tasks**: Break into smaller conversations

## Related Pages

- [Agent](agent.md) - How models power the agent
- [Agent Modes / Settings](agent-modes-settings.md) - Model configuration
