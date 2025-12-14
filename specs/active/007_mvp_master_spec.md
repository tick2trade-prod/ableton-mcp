# MVP Engineering Specification: "I Am Machine" Recreation

**Version**: 1.0.0
**Status**: Active
**Created**: 2025-12-13

## 1. Executive Summary

Recreate Lily Palmer's "I Am Machine" (136 BPM, F Minor, Peak Time Techno) with 16 tracks using Ableton-MCP and custom Python software in Ableton Live 12.3.1 DAW.

### Primary Objective
Build a **DearPyGUI control interface** for developers to orchestrate Ollama DeepAgents/CrewAI agents for automated track recreation.

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DearPyGUI Control Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Research │  │ Composer │  │ Mixer    │  │ Verifier │        │
│  │ Agent    │  │ Agent    │  │ Agent    │  │ Agent    │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼─────────────┼──────────────┼─────────────┼──────────────┘
        │             │              │             │
        ▼             ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DeepAgents Orchestration Layer                  │
│        (LangGraph StateGraph + Middleware Architecture)         │
├─────────────────────────────────────────────────────────────────┤
│  TodoListMiddleware │ FilesystemMiddleware │ SubAgentMiddleware │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Tool Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ ableton_mcp  │  │ableton_code  │  │ research_mcp │          │
│  │ (DAW Control)│  │gen (PDF/AST) │  │ (Web Search) │          │
│  └──────┬───────┘  └──────────────┘  └──────────────┘          │
└─────────┼───────────────────────────────────────────────────────┘
          │ TCP 9877
          ▼
┌─────────────────────────────────────────────────────────────────┐
│              Ableton Live 12.3.1 (AbletonMCP Script)            │
│                      Live Object Model (LOM)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Track Definition (16 Tracks)

| # | Name | Type | Role | Spectral Range | Devices |
|---|------|------|------|----------------|---------|
| 1 | 01-Kick | MIDI | Rhythm | 40-150Hz | Drum Sampler, EQ8, Saturator |
| 2 | 02-Rumble | Audio | Texture | 30-100Hz | Reverb, Roar, Compressor |
| 3 | 03-RollingBass | MIDI | Rhythm | 100-400Hz | Operator, EQ8, Comp |
| 4 | 04-Acid | MIDI | Lead | 100-5kHz | Operator, AutoFilter, Redux |
| 5 | 05-ClosedHats | MIDI | Rhythm | 5-15kHz | Drum Sampler, EQ8 |
| 6 | 06-OpenHats | MIDI | Rhythm | 4-12kHz | Drum Sampler, EQ8 |
| 7 | 07-Clap | MIDI | Rhythm | 400Hz-3kHz | Drum Sampler, Reverb |
| 8 | 08-LowTom | MIDI | Rhythm | 60-500Hz | Drum Sampler, EQ8 |
| 9 | 09-Glitch | MIDI | Texture | 200Hz-15kHz | Simpler, Beat Repeat |
| 10 | 10-Ride | MIDI | Rhythm | 2-18kHz | Drum Sampler, EQ8 |
| 11 | 11-SynthStab | MIDI | Harmony | 200Hz-10kHz | Wavetable, Echo, Reverb |
| 12 | 12-Drone | MIDI | Harmony | 50Hz-8kHz | Operator, Reverb, Chorus |
| 13 | 13-Vocal | Audio | Vocal | 100Hz-8kHz | EQ8, Compressor, Reverb |
| 14 | 14-VocalFX | Audio | Vocal | 200Hz-15kHz | Echo, Reverb, Grain |
| 15 | 15-Riser | MIDI | FX | 200Hz-15kHz | Operator, AutoFilter |
| 16 | 16-Impact | MIDI | FX | 30Hz-10kHz | Drum Sampler, Reverb |

---

## 4. DearPyGUI Control Interface

### 4.1 GUI Layout

```
┌────────────────────────────────────────────────────────────────┐
│ I AM MACHINE - Lily Palmer Recreation                  [─][□][×]│
├────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐ ┌──────────────────────────────────────────┐  │
│ │ AGENTS       │ │ TRACK STATUS                              │  │
│ │ ○ Research   │ │ ■ 01-Kick     [■■■■■■■■■■] 100%           │  │
│ │ ○ Composer   │ │ □ 02-Rumble   [■■■■■░░░░░]  50%           │  │
│ │ ○ Mixer      │ │ □ 03-Bass     [░░░░░░░░░░]   0%           │  │
│ │ ○ Verifier   │ │ ...                                       │  │
│ └──────────────┘ └──────────────────────────────────────────┘  │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ LOGS                                                      │   │
│ │ [12:34:56] Agent: Creating Kick track...                  │   │
│ │ [12:34:57] MCP: create_midi_track(index=0)               │   │
│ │ [12:34:58] Agent: Loading Drum Sampler...                 │   │
│ └──────────────────────────────────────────────────────────┘   │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ [▶ RUN ALL] [⏹ STOP] [🔄 RESET] [📊 VERIFY]             │   │
│ └──────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### 4.2 File Structure

```
scripts/
└── dearpygui_controller/
    ├── __init__.py
    ├── main.py              # DearPyGUI app entry point
    ├── layouts/
    │   ├── track_panel.py   # Track status visualization
    │   ├── agent_panel.py   # Agent control buttons
    │   └── log_panel.py     # Real-time log display
    ├── agents/
    │   ├── research_agent.py    # Searches docs/web
    │   ├── composer_agent.py    # Creates patterns
    │   ├── mixer_agent.py       # Adjusts levels/effects
    │   └── verifier_agent.py    # Validates output
    └── callbacks/
        ├── run_callbacks.py     # Button handlers
        └── agent_callbacks.py   # Agent status updates
```

---

## 5. DeepAgents Integration

### 5.1 Agent Architecture (Ollama + CrewAI)

```python
from deepagents import create_deep_agent
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew

# 1. Ollama LLM Backend
ollama = Ollama(model="llama3")

# 2. Specialized Agents
research_agent = Agent(
    role='Sound Research Engineer',
    goal='Find production techniques for Peak Time Techno',
    llm=ollama,
    tools=[search_ableton_docs, search_production_technique]
)

composer_agent = Agent(
    role='Rhythm Programmer',
    goal='Create 4-on-floor patterns at 136 BPM in F Minor',
    llm=ollama,
    tools=[create_pattern, add_notes_to_clip]
)

mixer_agent = Agent(
    role='Mix Engineer',
    goal='Balance levels and apply effects chains',
    llm=ollama,
    tools=[load_device, set_device_parameter]
)
```

### 5.2 Middleware Configuration

| Middleware | Purpose | Implementation |
|------------|---------|----------------|
| TodoListMiddleware | Tracks 16-track checklist | Syncs with DearPyGUI progress |
| FilesystemMiddleware | Saves patterns to local files | Uses `live_set/lily_palmer/` |
| MemoryMiddleware | Retrieves Ableton docs | Uses Redis vector store |

---

## 6. Boolean Success Criteria

| Flag | Condition | Verification Method |
|------|-----------|---------------------|
| `IS_BPM_VALID` | `song.tempo == 136.0` | Query via MCP |
| `HAS_ALL_TRACKS` | `track_count == 16` | Query via MCP |
| `HAS_KICK_PATTERN` | Track 0 has 4-on-floor notes | Inspect clip notes |
| `HAS_RUMBLE_CHAIN` | Track 1 has Reverb→Roar→Comp | Inspect devices |
| `IS_SIDECHAIN_ACTIVE` | Rumble sidechained to Kick | Check compressor |
| `ALL_DEVICES_LOADED` | No "manual step" warnings | Parse execution log |
| `NO_LATENCY_ERRORS` | Log.txt has 0 RemoteScriptError | Parse Ableton log |

---

## 7. Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Create DearPyGUI main window
- [ ] Implement track status panel
- [ ] Connect to Ableton via MCP

### Phase 2: DeepAgents (Week 2)
- [ ] Configure Ollama with llama3
- [ ] Implement 4 specialized agents
- [ ] Add TodoListMiddleware

### Phase 3: Integration (Week 3)
- [ ] Wire agents to GUI buttons
- [ ] Implement real-time logging
- [ ] Add progress tracking

### Phase 4: Verification (Week 4)
- [ ] Implement boolean success checks
- [ ] Add audio export for comparison
- [ ] Create similarity scoring

---

## 8. Dependencies

```toml
[project.optional-dependencies]
gui-controller = [
    "dearpygui>=2.0.0",
    "deepagents>=0.3.0",
    "crewai>=0.51.0",
    "langchain-community>=0.0.38",
    "langgraph>=0.2.60",
]
```

---

## 9. Quick Start

```bash
# 1. Install dependencies
uv sync --extra gui-controller

# 2. Start Redis (for memory)
docker-compose up -d redis

# 3. Ensure Ableton is running with AbletonMCP

# 4. Launch DearPyGUI controller
uv run python scripts/dearpygui_controller/main.py
```

---

## References

- [005.md](file:///Users/alexzh/ableton-mcp/specs/active/005.md) - PRD Schema Design
- [006.md](file:///Users/alexzh/ableton-mcp/specs/active/006.md) - Master System Design
- [imp_plan_p2.md](file:///Users/alexzh/ableton-mcp/specs/active/imp_plan_p2.md) - CrewAI Agents
- [imp_plan_p3_scaffold.md](file:///Users/alexzh/ableton-mcp/specs/active/imp_plan_p3_scaffold.md) - System Scaffold
- [imo_plan_p4_deepagents.md](file:///Users/alexzh/ableton-mcp/specs/active/imo_plan_p4_deepagents.md) - DeepAgents
