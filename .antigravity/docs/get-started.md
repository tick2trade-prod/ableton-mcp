# Getting Started

> Source: [https://antigravity.google/docs/get-started](https://antigravity.google/docs/get-started)

## Quick Start for ableton-mcp

### Prerequisites

1. **Antigravity IDE** installed and authenticated
2. **Ableton Live** running with AbletonMCP control surface
3. **Python 3.12+** with project dependencies installed

### Project Setup

```bash
# Clone and setup
cd ~/ableton-mcp
uv sync

# Verify Ableton connection
make check-port  # Port 9877 should be listening
make test-connection
```

### First Steps with Antigravity

#### 1. Open the Project
Open the `ableton-mcp` folder in Antigravity IDE.

#### 2. Configure MCP Servers
The project includes these MCP servers in `.antigravity/mcp.json`:
- `ableton_codegen` - Ableton code generation
- `research_mcp` - Web research capabilities
- `sota_researcher_v2` - State-of-the-art research
- `deepagents` - Multi-agent orchestration

#### 3. Run Your First Test
```bash
pytest tests/test_tools.py::test_get_session_info -v
```

### Using AI Assistance

#### Chat with Agent
- Press `Cmd+L` to open agent chat
- Ask about Ableton API, MCP tools, or project structure

#### Run Workflows
- Type `/research` for quick research
- Use `/code-quality` for code analysis

### Ollama Integration

For local LLM inference:
```bash
# Start Ollama
ollama serve

# Pull a model
ollama pull llama3.2

# Configure in project
export OLLAMA_MODEL=llama3.2
```

## Next Steps

- [Agent Features](agent.md) - Learn about AI capabilities
- [MCP Integration](mcp.md) - Configure custom MCP servers
- [Workflows](rules-workflows.md) - Automate repetitive tasks
