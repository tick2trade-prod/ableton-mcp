# Playground

> Source: [https://antigravity.google/docs/playground](https://antigravity.google/docs/playground)

## Overview

The Playground provides a sandbox environment for experimentation without affecting your main workspace.

## Features

### Isolated Environment
- Temporary files
- No Git tracking
- Quick experiments

### AI Exploration
- Test prompts
- Try new MCP tools
- Prototype code

### Quick Prototyping
- Create snippets
- Test ideas
- Validate concepts

## Using Playground for ableton-mcp

### Experiment with MCP Tools
```python
# Try new MCP tool calls
result = await search_ableton_docs("Roar device")
print(result)

# Test code generation
code = await generate_track_code({
    "name": "Test",
    "type": "bass"
})
```

### Prototype Track Scripts
```python
# Quick test without creating files
async def test_device_chain():
    await create_track("Test", 0)
    await load_device(0, "Roar")
    await set_device_parameter(0, 0, "Drive", 0.5)
```

### Test Ollama Prompts
```python
# Experiment with prompts
prompt = "Explain multiband saturation for techno bass"
result = await query_ollama(prompt)
print(result)
```

## Playground vs Workspace

| Feature | Playground | Workspace |
|---------|------------|-----------|
| Persistence | Temporary | Permanent |
| Git | No | Yes |
| MCP Access | Yes | Yes |
| File Saving | Optional | Automatic |

## Best Practices

### 1. Validate Before Moving
Test in playground, then move to workspace.

### 2. Save Useful Snippets
Export useful code to project.

### 3. Experiment Freely
No consequences for failure.

## Related Pages

- [Workspaces](workspaces.md) - Production workspace
- [Agent](agent.md) - Agent features in playground
