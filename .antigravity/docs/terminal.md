# Terminal

> Source: [https://antigravity.google/docs/terminal](https://antigravity.google/docs/terminal)

## Overview

The integrated terminal in Antigravity provides command execution capabilities with agent integration.

## Terminal Features

### Command Execution
- Run shell commands directly
- Agent can propose and execute commands
- View command output and status

### Background Commands
Long-running processes run in background:
- MCP servers
- Development servers
- Test suites

### Command History
All commands are tracked and referenceable.

## Key Commands for ableton-mcp

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run single test
pytest tests/test_tools.py::test_get_session_info -v

# Run with markers
pytest -m "session" -v

# Check test timeout
pytest tests/ -v --timeout=300
```

### Ableton Connection
```bash
# Check port
make check-port

# Test connection
make test-connection

# View Ableton logs
tail -f ~/Library/Preferences/Ableton/Live\ 12.3.1/Log.txt
```

### MCP Server Management
```bash
# Start Redis for MCP
docker-compose up -d redis

# Restart MCP servers
make restart-mcp

# Check MCP status
curl localhost:8080/status
```

### Ollama
```bash
# Start Ollama
ollama serve

# List models
ollama list

# Pull model
ollama pull llama3.2

# Run inference
ollama run llama3.2 "Explain sidechain compression"
```

### Development
```bash
# Sync dependencies
uv sync

# Run linter
ruff check .

# Format code
ruff format .

# Pre-commit hooks
pre-commit run --all-files
```

## Agent Terminal Integration

### Command Proposals
The agent proposes commands with approval:
```
AGENT: I'll run the test to verify the fix:
       > pytest tests/test_tools.py::test_create_track -v
       [Approve] [Reject] [Modify]
```

### Auto-Run Commands
Safe commands can auto-run:
```yaml
# In settings
autoApprovePatterns:
  - "pytest *"
  - "git status"
  - "make check-*"
```

### Background Process Monitoring
```
AGENT: Starting MCP server in background...
       Command ID: abc123
       Status: Running
       [View Output] [Stop]
```

## Terminal Best Practices

### 1. Use Make Targets
Prefer `make` commands for common tasks:
```makefile
# Makefile
test:
	pytest tests/ -v

lint:
	ruff check .
```

### 2. Handle Long-Running Commands
```bash
# Run in background
nohup python -m mcp_server &

# Or use tmux
tmux new-session -d -s mcp 'python -m mcp_server'
```

### 3. Check Exit Codes
```bash
# After command
echo $?  # 0 = success
```

### 4. Capture Output
```bash
# Save test output
pytest tests/ -v 2>&1 | tee test_output.log
```

## Related Pages

- [Agent](agent.md) - Agent command execution
- [MCP](mcp.md) - Running MCP servers
- [Rule / Workflows](rules-workflows.md) - Automated command sequences
