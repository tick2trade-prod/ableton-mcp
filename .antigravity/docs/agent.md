# Agent

> Source: [https://antigravity.google/docs/agent](https://antigravity.google/docs/agent)

## Overview

The Antigravity Agent is an AI-powered coding assistant that can understand your codebase, execute commands, and interact with external tools through MCP.

## Agent Capabilities

### Code Understanding
- Analyzes project structure and dependencies
- Understands code context across files
- Recognizes patterns and best practices

### Code Generation
- Writes new code based on specifications
- Refactors existing code
- Generates tests following TDD patterns

### Tool Usage
- Runs terminal commands
- Interacts with MCP servers
- Browses documentation and web resources

## Using Agents in ableton-mcp

### Conversation Patterns

#### For Testing
```
USER: Run the test for get_session_info
AGENT: [Executes pytest, analyzes results, suggests fixes]

USER: The test fails with timeout - what's wrong?
AGENT: [Checks Ableton connection, reviews socket handling]
```

#### For Research
```
USER: /research techno sidechain compression techniques
AGENT: [Uses research_mcp to find tutorials, summarizes techniques]

USER: How do I implement that in this project?
AGENT: [Generates code using ableton_codegen patterns]
```

#### For Code Generation
```
USER: Create a new MCP tool for tempo detection
AGENT: [Analyzes existing tools, generates new tool following patterns]
```

### Agent Context

The agent has access to:

1. **Project Files**: All source code in the workspace
2. **GEMINI.md**: Your custom instructions
3. **MCP Servers**: External tools configured in `.antigravity/mcp.json`
4. **Conversation History**: Previous interactions

### Best Practices

#### Be Specific
```
# Good
"Fix the timeout error in test_create_track by increasing the socket timeout to 30 seconds"

# Less effective
"Fix the error"
```

#### Provide Context
```
# Good
"Looking at tests/test_tools.py line 45, the assertion fails because..."

# Less effective
"The test doesn't work"
```

#### Use Workflows
```
# Invoke predefined workflows
/research sidechain compression
/code-quality tests/test_tools.py
```

## Agent for Agentic Workflows

### Multi-Step Tasks

The agent can handle complex workflows:

1. **Research Phase**: Gather information using MCP research tools
2. **Planning Phase**: Create implementation plans
3. **Execution Phase**: Write code, run tests
4. **Iteration Phase**: Fix issues, refactor

### Example: Creating a New Track Script

```
USER: Create a new rumble track following the lily_palmer style

AGENT:
1. Analyzes existing track scripts in live_set/lily_palmer/
2. Researches rumble bass techniques using search_ableton_docs
3. Generates track_02_rumble.py following patterns
4. Creates corresponding test file
5. Runs tests and iterates until passing
```

## Integration with Ollama

For local LLM tasks within agent workflows:

```python
# The agent can use Ollama through MCP tools
# Example: Local summarization of research results

@server.tool()
async def summarize_with_ollama(content: str) -> dict:
    """Summarize content using local Ollama model."""
    summary = await query_ollama(
        f"Summarize for a music producer: {content}",
        model="llama3.2"
    )
    return {"summary": summary}
```

## Related Pages

- [Models](models.md) - Available AI models
- [Agent Modes / Settings](agent-modes-settings.md) - Configuration
- [MCP](mcp.md) - External tool integration
