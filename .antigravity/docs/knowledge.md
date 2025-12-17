# Knowledge

> Source: [https://antigravity.google/docs/knowledge](https://antigravity.google/docs/knowledge)

## Overview

Knowledge in Antigravity refers to persistent information that informs agent behavior and responses.

## Types of Knowledge

### Project Knowledge
- `GEMINI.md` - Project-specific rules and context
- `README.md` - Project overview
- `pyproject.toml` - Dependencies and configuration

### Embedded Knowledge
- Indexed documentation
- Research results
- Conversation history

### External Knowledge
- Web search results
- MCP tool outputs
- API documentation

## Knowledge in ableton-mcp

### Project Context (GEMINI.md)

```markdown
# Key project knowledge the agent uses:

## Primary Objective
Write pytest integration tests for Ableton MCP tools

## Key Principles
- No mocks - All tests run against real Ableton Live
- Incremental testing - Test one tool at a time
- Live verification - Confirm changes in DAW

## Conventions
- Conventional Commits
- Branch naming patterns
```

### Embedded Documentation

Using the Ableton Codegen MCP:
```python
# Embed Ableton Live manual
embed_ableton_docs("docs/live12-manual-en.pdf")

# Search embedded knowledge
search_ableton_docs("sidechain compression")
```

### Research Knowledge

Store research results for reuse:
```python
# Conduct research
results = research_and_plan(
    topic="techno rumble techniques",
    output_path="knowledge/rumble_research.md"
)
```

## Knowledge Management

### Adding Knowledge

```bash
# Add to GEMINI.md
echo "## New Section\nContent" >> GEMINI.md

# Create knowledge file
mkdir -p docs/knowledge
echo "# Research on X" > docs/knowledge/topic.md
```

### Updating Knowledge

```
USER: Update our knowledge about EQ Eight with this new technique
AGENT: [Updates knowledge file or GEMINI.md]
```

### Querying Knowledge

```
USER: What do we know about sidechain compression in this project?
AGENT: [Searches project files, embedded docs, research]
```

## Knowledge Sources for This Project

| Source | Content |
|--------|---------|
| GEMINI.md | Project rules, conventions |
| pyproject.toml | Dependencies, config |
| docs/ | Project documentation |
| .antigravity/docs/ | IDE documentation |
| Redis (via MCP) | Embedded Ableton manual |
| Research outputs | Web research results |

## Best Practices

### 1. Keep GEMINI.md Updated
Add new conventions and learnings.

### 2. Store Research Results
Save valuable research for future reference.

### 3. Version Control Knowledge
```bash
git add GEMINI.md docs/knowledge/
git commit -m "docs: update project knowledge"
```

### 4. Use MCP for Large Documents
Embed large documents in Redis for efficient search:
```python
embed_ableton_docs()  # Once
search_ableton_docs("query")  # Fast retrieval
```

## Related Pages

- [Agent](agent.md) - How agent uses knowledge
- [MCP](mcp.md) - Knowledge through tools
- [Artifacts](artifacts.md) - Generated knowledge
