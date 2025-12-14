# Agent Controller GUI - User Guide

**Version:** 1.0.0
**Last Updated:** 2025-12-13

---

## Overview

The **Ableton MCP Agent Controller** is a graphical interface for managing multi-agent workflows across Claude, Gemini, Ollama, and Codex. It provides an intuitive way to:

- Execute agent commands with visual feedback
- Manage context files (`.context/` directory)
- View command history and activity logs
- Monitor Ollama server logs
- Export session data for collaboration

---

## Prerequisites

1. **uv Python** - Modern Python package manager
2. **dearpygui** - Installed automatically via setup
3. **Agent CLI tools** - claude-cli, gemini-cli, codex-cli, ollama must be available in PATH

---

## Installation

```bash
cd /Users/alexzh/ableton-mcp

# Install dearpygui (if not already installed)
uv pip install dearpygui

# Make executable
chmod +x agent_gui.py
```

---

## Usage

### Starting the GUI

```bash
# From ableton-mcp directory
uv python agent_gui.py

# Or if executable
./agent_gui.py
```

### Interface Layout

The GUI is divided into two main panels:

#### Left Panel - Agent Control (700px)

1. **Agent Selection**
   - Dropdown to select agent (Claude, Gemini, Ollama, Codex)
   - Agent description displays role specialization
   - Ollama model selector appears when Ollama is selected

2. **Prompt Input**
   - Multi-line text area for entering tasks/prompts
   - Supports complex, multi-paragraph prompts

3. **Action Buttons**
   - **Send Prompt** - Execute the current prompt with selected agent
   - **Clear Output** - Clear the output display
   - **View Ollama Log** - Display last 100 lines of ollama.log
   - **Export Session** - Save session data to JSON file

4. **Output Display**
   - Shows agent responses in real-time
   - Read-only text area with scrolling
   - Displays errors and status messages

#### Right Panel - Context & Activity (470px)

1. **Context Files Viewer**
   - Dropdown to select context file
   - View/edit context files directly
   - **Refresh** - Reload selected file
   - **Save** - Write changes back to file

2. **Command History**
   - Shows last 10 commands executed
   - Format: `[timestamp] agent: prompt...`

3. **Activity Log**
   - Real-time logging of all actions
   - Timestamped entries with log levels (INFO, WARNING, ERROR, SUCCESS)
   - Auto-scrolls to latest entry

---

## Features

### 1. Multi-Agent Support

**Claude**
- Command: `claude "prompt"`
- Best for: Architecture, design, complex refactoring
- Color: Blue

**Gemini**
- Command: `gemini "prompt"`
- Best for: Research, exploration, multi-modal analysis
- Color: Red

**Ollama**
- Command: `ollama run <model> "prompt"`
- Models: deepseek-coder-v2, qwen2.5-coder, codellama, mixtral, llama3.3
- Best for: Local iteration, privacy-sensitive code
- Color: Green

**Codex**
- Command: `codex "prompt"`
- Best for: Code generation, boilerplate, tests
- Color: Yellow

### 2. Context File Management

Directly view and edit context files:
- `current-session.md` - Active work log
- `decisions.md` - Architecture Decision Records
- `research-notes.md` - Research findings
- `todos.md` - Task tracking

Changes are saved immediately to the `.context/` directory.

### 3. Ollama Integration

- **Model Selection** - Switch between different Ollama models
- **Log Viewer** - Monitor Ollama server activity
- **Path** - Reads from `../ollama_crewai_lab/ollama.log`

### 4. Session Export

Export complete session data including:
- Timestamp and active agent
- Full command history
- All context file contents

Format: `session_YYYYMMDD_HHMMSS.json`

### 5. Command History

Tracks all executed commands with:
- ISO timestamp
- Agent name
- Prompt (first 40 chars)
- Response (first 200 chars)

### 6. Activity Logging

All GUI actions are logged with levels:
- **INFO** - Normal operations
- **SUCCESS** - Completed actions
- **WARNING** - Non-critical issues
- **ERROR** - Failed operations

---

## Workflow Examples

### Example 1: Quick Ollama Iteration

1. Select **Ollama** from agent dropdown
2. Choose **deepseek-coder-v2** model
3. Enter prompt: `"Create a MIDI pattern generator for techno kicks"`
4. Click **Send Prompt**
5. View output in real-time
6. Iterate quickly without API costs

### Example 2: Architecture Design with Claude

1. Select **Claude** from dropdown
2. Enter prompt: `"Design an MCP tool for stem separation with Redis caching"`
3. Click **Send Prompt**
4. Copy output to specs/ directory
5. Update `decisions.md` in context viewer
6. Click **Save** to persist changes

### Example 3: Multi-Agent Workflow

1. **Research Phase (Gemini)**
   - Select Gemini
   - Prompt: `"What are best practices for real-time audio processing?"`
   - Copy findings to `research-notes.md`

2. **Architecture Phase (Claude)**
   - Select Claude
   - Prompt: `"Design processor based on research-notes.md"`
   - Save design to `decisions.md`

3. **Implementation Phase (Ollama)**
   - Select Ollama + deepseek-coder-v2
   - Prompt: `"Implement the processor from decisions.md"`
   - Iterate quickly

4. **Review Phase (Codex)**
   - Select Codex
   - Prompt: `"Generate tests for the processor"`

### Example 4: Context Coordination

1. Open **context_selector** dropdown
2. Select `current-session.md`
3. Review active work
4. Switch to `todos.md`
5. Add new tasks directly in editor
6. Click **Save**
7. Other agents can now read updated context

---

## Keyboard Workflow

While the GUI doesn't have custom keyboard shortcuts, you can optimize workflow:

1. **Tab** - Navigate between fields
2. **Enter** in prompt field - (Does not submit, use button)
3. **Ctrl+A** in output - Select all text for copying
4. **Mouse wheel** - Scroll output/logs

---

## Error Handling

### Common Issues

**"Agent command not found"**
- Ensure CLI tools (claude, gemini, codex, ollama) are in PATH
- Test in terminal: `which claude` should return path

**"Context file not found"**
- Ensure `.context/` directory exists
- Run from `ableton-mcp/` directory
- Click **Refresh** to reload

**"Command timed out"**
- Complex prompts may take >2 minutes
- Increase timeout in code if needed
- Use Ollama for faster iteration

**"Ollama log not found"**
- Check path: `../ollama_crewai_lab/ollama.log`
- Ensure Ollama server is running
- Adjust `OLLAMA_LOG` path in code if different

---

## Advanced Configuration

### Customizing Agent Commands

Edit the `AGENTS` dictionary in `agent_gui.py`:

```python
AGENTS = {
    "claude": {
        "command": "claude",  # Change if using different CLI
        "color": (100, 150, 255),
        "description": "..."
    },
    # ...
}
```

### Adding New Ollama Models

Add to the models list:

```python
"ollama": {
    # ...
    "models": ["deepseek-coder-v2", "your-custom-model", ...]
}
```

### Changing Context Directory

```python
CONTEXT_DIR = Path(".context")  # Relative to execution directory
```

### Adjusting Timeouts

In `run_agent_command()`:

```python
result = subprocess.run(
    command,
    timeout=120  # Change to desired seconds
)
```

---

## Integration with WS-guide.md

The GUI implements the workflows described in `WS-guide.md`:

- **Agent Selection** - Maps to agent specialization (lines 35-135)
- **Workflow Patterns** - Supports all 4 patterns (lines 138-223)
- **Context Management** - Implements shared context strategy (lines 378-398)
- **Ollama Integration** - Supports local development (lines 108-134)

Refer to `WS-guide.md` for:
- When to use each agent
- Multi-agent workflow patterns
- Best practices and tips

---

## Session Export Format

Exported JSON structure:

```json
{
  "timestamp": "2025-12-13T14:30:00",
  "agent": "claude",
  "history": [
    {
      "timestamp": "2025-12-13T14:25:00",
      "agent": "ollama",
      "prompt": "Create beat generator",
      "response": "Here's a beat generator..."
    }
  ],
  "context_files": {
    "current-session.md": "...",
    "decisions.md": "...",
    "research-notes.md": "...",
    "todos.md": "..."
  }
}
```

Use for:
- Sharing work sessions with team
- Documenting decision-making process
- Backup before major changes

---

## Tips & Best Practices

### Performance

- Use **Ollama** for rapid iteration (no network latency)
- Use **Claude** for critical decisions (best quality)
- **Clear Output** regularly to improve scrolling performance

### Context Management

- Update `current-session.md` after each major task
- Use `decisions.md` for architecture choices
- Keep `todos.md` synchronized with actual work
- **Save** context files frequently

### Multi-Agent Coordination

- Export session before switching projects
- Use command history to track which agent did what
- Check activity log for errors before proceeding
- Review ollama.log for model loading issues

### Prompt Engineering

- Be specific and concise
- Reference context files in prompts (e.g., "based on decisions.md")
- For Ollama: shorter prompts = faster responses
- For Claude: detailed prompts = better architecture

---

## Troubleshooting

### GUI Won't Start

```bash
# Check Python environment
uv python --version

# Reinstall dearpygui
uv pip install --force-reinstall dearpygui

# Check for errors
uv python agent_gui.py
```

### Agents Not Responding

```bash
# Test each agent manually
claude "test"
gemini "test"
ollama run deepseek-coder-v2 "test"
codex "test"

# Check PATH
echo $PATH
```

### Context Files Not Saving

```bash
# Check permissions
ls -la .context/
chmod 755 .context/
chmod 644 .context/*.md
```

---

## Future Enhancements

Planned features:

- [ ] Keyboard shortcuts (Ctrl+Enter to send)
- [ ] Syntax highlighting in output
- [ ] Agent response streaming (real-time)
- [ ] Diff viewer for context file changes
- [ ] Custom agent profiles
- [ ] Theme customization
- [ ] Prompt templates/snippets
- [ ] Multi-tab interface
- [ ] Built-in terminal
- [ ] Git integration for context files

---

## Contributing

To add features:

1. Edit `agent_gui.py`
2. Follow existing callback pattern
3. Update this README
4. Test with all agents
5. Update `.context/decisions.md` with changes

---

## Credits

- **Framework:** [Dear PyGui](https://github.com/hoffstadt/DearPyGui)
- **Agents:** Claude, Gemini, Ollama, Codex
- **Workspace:** ableton-mcp multi-agent setup
- **Guide:** WS-guide.md

---

**For more information, see:**
- `WS-guide.md` - Multi-agent workflow patterns
- `.context/` - Active workspace context
- `/Users/alexzh/ollama_crewai_lab/specs/0004_gui.md` - Original spec
