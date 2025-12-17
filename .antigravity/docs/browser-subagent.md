# Browser Subagent

> Source: [https://antigravity.google/docs/browser-subagent](https://antigravity.google/docs/browser-subagent)

## Overview

The Browser Subagent enables automated web browsing for research, testing, and data collection.

## Capabilities

- **Navigate**: Open URLs and follow links
- **Interact**: Click buttons, fill forms
- **Extract**: Read page content
- **Record**: Capture browser sessions as video

## Usage in ableton-mcp

### Research Tasks

```python
# Example: Research production techniques
browser_subagent(
    TaskName="Research Sidechain Compression",
    Task="""
    1. Navigate to musicradar.com
    2. Search for "Ableton sidechain compression tutorial"
    3. Read the top 3 results
    4. Extract key techniques and settings
    5. Return when you have documented 5 techniques
    """,
    RecordingName="sidechain_research"
)
```

### Documentation Lookup

```python
# Example: Find Ableton device documentation
browser_subagent(
    TaskName="Roar Device Documentation",
    Task="""
    1. Navigate to ableton.com/manual
    2. Search for "Roar" device
    3. Extract parameter descriptions
    4. Document multiband saturation settings
    """,
    RecordingName="roar_docs"
)
```

### Tutorial Extraction

```python
# Example: Extract tutorial steps
browser_subagent(
    TaskName="Extract Tutorial",
    Task="""
    1. Navigate to the given tutorial URL
    2. Read through the step-by-step guide
    3. Extract settings and parameter values
    4. Summarize the technique
    5. Return when complete
    """,
    RecordingName="tutorial_extraction"
)
```

## Recording Browser Sessions

All browser subagent actions are recorded:

```
.antigravity/
└── recordings/
    ├── sidechain_research.webp
    ├── roar_docs.webp
    └── tutorial_extraction.webp
```

### Viewing Recordings
Recordings can be reviewed for:
- Debugging failed tasks
- Training documentation
- Verification of extracted data

## Integration with MCP Research

The browser subagent complements MCP research tools:

| Tool | Use Case |
|------|----------|
| `search_web` (MCP) | Quick text search |
| `browser_subagent` | Interactive browsing |
| `research` (MCP) | Comprehensive research |

### Workflow Example

```markdown
## Research Workflow

1. Use `search_web` to find relevant URLs
2. Use `browser_subagent` for detailed extraction
3. Use Ollama to summarize findings locally
4. Store results in project knowledge base
```

## Best Practices

### 1. Clear Task Descriptions
```python
Task="""
Specific action 1
Specific action 2
Clear return condition
"""
```

### 2. Set Return Conditions
```python
Task="... Return when you have extracted the device chain settings"
```

### 3. Handle Dynamic Content
```python
Task="""
Wait for the page to load
Scroll to find the settings section
Extract visible parameters
"""
```

### 4. Limit Scope
Focus on specific, achievable tasks rather than broad browsing.

## Related Pages

- [Browser](browser.md) - Browser overview
- [Browser Subagent View](browser-subagent-view.md) - UI for subagent
- [MCP](mcp.md) - Complementary research tools
