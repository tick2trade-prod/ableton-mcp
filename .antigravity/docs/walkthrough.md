# Walkthrough

> Source: [https://antigravity.google/docs/walkthrough](https://antigravity.google/docs/walkthrough)

## Overview

Walkthroughs are step-by-step guides for processes and procedures.

## Walkthrough Structure

```markdown
# Walkthrough: [Process Name]

## Prerequisites
- Requirement 1
- Requirement 2

## Steps

### Step 1: [Title]
Description of what to do.

```bash
# Command if applicable
```

### Step 2: [Title]
...

## Verification
How to confirm success.

## Troubleshooting
Common issues and solutions.
```

## ableton-mcp Walkthroughs

### Testing Workflow

```markdown
# Walkthrough: Running Ableton Integration Tests

## Prerequisites
- Ableton Live running
- AbletonMCP control surface enabled
- Port 9877 listening

## Steps

### Step 1: Verify Connection
```bash
make check-port
# Expected: Port 9877 is listening
```

### Step 2: Test Connection
```bash
make test-connection
# Expected: Connection successful
```

### Step 3: Run Specific Test
```bash
pytest tests/test_tools.py::test_get_session_info -v
```

### Step 4: Check Ableton State
Verify in Ableton that changes are reflected.

## Verification
- All tests pass
- No timeout errors
- Ableton state matches expected

## Troubleshooting

### Port Not Listening
1. Check Ableton is running
2. Verify control surface is enabled
3. Restart Ableton

### Timeout Errors
1. Increase socket timeout
2. Check Ableton is responsive
3. Review Ableton log
```

### MCP Development Walkthrough

```markdown
# Walkthrough: Creating a New MCP Tool

## Prerequisites
- Project dependencies installed
- Understanding of MCP protocol

## Steps

### Step 1: Define Tool API
Document what the tool will do:
```python
"""
Tool: summarize_research
Input: list of research results
Output: concise summary
"""
```

### Step 2: Create Tool File
```python
# mcp_servers/research_mcp/tools/summarize.py
async def summarize_research(results: list) -> dict:
    # Implementation
    pass
```

### Step 3: Register with Server
```python
# mcp_servers/research_mcp/server.py
from .tools.summarize import summarize_research

@server.tool()
async def summarize_research(results: list) -> dict:
    return await summarize_research(results)
```

### Step 4: Test the Tool
```bash
pytest tests/mcp/test_summarize.py -v
```

### Step 5: Update Configuration
Add to `.antigravity/mcp.json` if needed.

## Verification
- Tool appears in MCP tool list
- Returns expected output format
- Error handling works
```

### Ollama Setup Walkthrough

```markdown
# Walkthrough: Setting Up Ollama for Local Inference

## Prerequisites
- macOS or Linux
- 8GB+ RAM

## Steps

### Step 1: Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Start Ollama Server
```bash
ollama serve
```

### Step 3: Pull a Model
```bash
ollama pull llama3.2
```

### Step 4: Verify
```bash
ollama run llama3.2 "Hello, world!"
```

### Step 5: Configure Project
```bash
export OLLAMA_MODEL=llama3.2
export OLLAMA_BASE_URL=http://localhost:11434
```

## Verification
- Ollama responds to prompts
- Model loads without errors
- MCP tools can call Ollama

## Troubleshooting

### Model Not Found
```bash
ollama list  # Check available models
ollama pull model_name  # Download if missing
```

### Connection Refused
```bash
# Check if Ollama is running
pgrep ollama
# Start if not running
ollama serve
```
```

## Creating Walkthroughs

The agent can generate walkthroughs:
```
USER: Create a walkthrough for setting up the dev environment
AGENT: [Creates comprehensive walkthrough as artifact]
```

## Related Pages

- [Implementation Plan](implementation-plan.md) - Component of plans
- [Artifacts](artifacts.md) - Walkthrough storage
- [Knowledge](knowledge.md) - Reference documentation
