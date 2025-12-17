---
description: Research best practices for a topic using SOTA researcher
---

# Research Workflow

Use the SOTA Researcher MCP to gather information before implementing features.

## Quick Research

For simple questions, use the `/research` slash command:

```
/research "pytest-asyncio best practices"
```

This performs quick research and returns a concise summary.

## Deep Research with Plan

For complex features requiring implementation planning:

```
/deep_plan "Authentication system" "Best practices for OAuth2; Security considerations"
```

This conducts comprehensive research and creates an actionable plan.

## Direct Tool Usage

You can also use the tools directly in your prompts:

- **`research_only(topic, max_results=10)`** - Quick research
- **`research_and_plan(topic, research_questions, output_path)`** - Comprehensive research + plan

## Token Saving Tips

1. **Research BEFORE implementation** - Avoid back-and-forth by researching first
2. **Use specific topics** - More specific = faster, more relevant results
3. **Limit max_results** - Use `max_results=5` for focused research
4. **Save to files** - Use `output_path` to save results for later reference

## Verify MCP is Running

// turbo
```bash
/mcp list
```

Look for `sota_researcher_v2` with status `CONNECTED`.
