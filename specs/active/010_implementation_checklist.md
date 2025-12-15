# Implementation Checklist: I Am Machine MVP

**Parent Spec**: [007_mvp_master_spec.md](file:///Users/alexzh/ableton-mcp/specs/active/007_mvp_master_spec.md)

## Quick Reference

### ✅ Prerequisites
- [x] Redis running (port 6379)
- [x] Ableton Live 12.3.1 with AbletonMCP
- [x] PDF embedded (2,268 chunks)
- [ ] Ollama installed with llama3
- [ ] DearPyGUI installed

### 🎯 Phase 1: Foundation
- [x] Create `ableton_client.py` shared library
- [ ] Install DearPyGUI: `uv add dearpygui>=2.0.0`
- [ ] Create `scripts/dearpygui_controller/main.py`
- [ ] Verify MCP connection from GUI

### 🎯 Phase 2: Agents
- [ ] Create `research_agent.py`
- [ ] Create `composer_agent.py`
- [ ] Create `mixer_agent.py`
- [ ] Create `verifier_agent.py`
- [ ] Test each agent independently

### 🎯 Phase 3: Integration
- [ ] Wire agents to GUI buttons
- [ ] Implement progress tracking
- [ ] Add real-time logging
- [ ] Test full 16-track pipeline

### 🎯 Phase 4: Verification
- [ ] Implement boolean success checks
- [ ] All 7 criteria passing
- [ ] Export verification report

---

## Commands

```bash
# Install all dependencies
uv sync --extra gui-controller --extra ableton-codegen

# Start Redis
docker-compose up -d redis

# Test Ollama
ollama run llama3

# Run GUI controller
uv run python scripts/dearpygui_controller/main.py

# Run verification
uv run python -c "from verifier import verify_project; verify_project()"
```

---

## File Location Map

| Component | Path |
|-----------|------|
| Master Spec | `/specs/active/007_mvp_master_spec.md` |
| GUI Spec | `/specs/active/008_dearpygui_controller.md` |
| Agent Spec | `/specs/active/009_agent_specifications.md` |
| GUI Code | `/scripts/dearpygui_controller/` |
| Track Scripts | `/live_set/lily_palmer/i_am_machine/` |
| MCP Client | `/live_set/lily_palmer/i_am_machine/ableton_client.py` |
