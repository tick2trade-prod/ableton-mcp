# Phase 1 Task Sequence

## Overview

**Goal**: Create all 16 tracks for Intro section (Bars 1-16)
**Target Time**: 30-60 minutes (parallel execution)

---

## Current Capabilities Assessment

### MCP Server Tools Available (27 tools)

| Tool | Works | Notes |
|------|-------|-------|
| `get_session_info` | ✅ | |
| `create_midi_track` | ✅ | |
| `set_track_name` | ✅ | |
| `set_tempo` | ✅ | |
| `create_clip` | ✅ | |
| `add_notes_to_clip` | ✅ | |
| `load_instrument_or_effect` | ✅ | Needs URI |
| `set_device_parameter` | ✅ | |
| `create_audio_effect_rack` | ✅ | |
| `create_rack_chain` | ✅ | |
| `get_browser_tree` | ✅ | Find instrument URIs |
| `fire_clip` / `stop_clip` | ✅ | |
| `start_playback` / `stop_playback` | ✅ | |

### Suite Features NOT in MCP

| Feature | Implemented? | Workaround |
|---------|--------------|------------|
| Stem Separation | ❌ | Manual in Ableton |
| Roar | ⚠️ Partial | Load via URI, set params |
| Meld | ⚠️ Partial | Load via URI, set params |
| Drift | ⚠️ Partial | Load via URI, set params |

### MCP Registration in Antigravity

**Current**: NOT registered in `~/.gemini/antigravity/mcp_config.json`

**Action**: Add `ableton_mcp` to config to enable Antigravity to call MCP tools directly.

---

## Pre-Phase 1: MCP Registration

### Step 0.1: Add ableton-mcp to Antigravity MCP Config

```json
{
  "mcpServers": {
    "ableton_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/alexzh/ableton-mcp",
        "python",
        "-m",
        "MCP_Server.server"
      ],
      "env": {
        "PYTHONPATH": "/Users/alexzh/ableton-mcp"
      }
    }
  }
}
```

### Step 0.2: Verify MCP Connection

```bash
# Ensure Ableton is running with AbletonMCP Control Surface
make check-port
```

---

## Phase 1: Task Sequence

### Layer 0: Foundation (Sequential, 5 min)

| Task | Tool | Command |
|------|------|---------|
| 0.1 | Set tempo | `set_tempo(136)` |
| 0.2 | Create Return A | Manual in Ableton |
| 0.3 | Create Return B | Manual in Ableton |
| 0.4 | Verify connection | `get_session_info()` |

---

### Layer 1: Parallel Track Creation (4 Lanes, 25 min)

#### Lane 1: Drums (Antigravity Window 1)

```
Developer: /intro-drums
```

| Task | Action | MCP Calls |
|------|--------|-----------|
| 1.1 | Create Kick track | `create_midi_track()`, `set_track_name(0, "Kick")` |
| 1.2 | Load Drum Rack | `load_instrument_or_effect(0, uri)` |
| 1.3 | Create 16-bar clip | `create_clip(0, 0, 64.0)` |
| 1.4 | Add 4-on-floor pattern | `add_notes_to_clip(0, 0, notes)` |
| 1.5 | Create Snare track | Same pattern... |
| 1.6 | Create Hi-hats track | Same pattern... |
| 1.7 | Create Toms track | Same pattern... |
| 1.8 | Create Glitch track | Same pattern... |
| 1.9 | Create Ride track | Same pattern... |

#### Lane 2: Bass (Antigravity Window 2)

```
Developer: /intro-bass
```

| Task | Action | MCP Calls |
|------|--------|-----------|
| 2.1 | Create Rumble track | `create_midi_track()`, `set_track_name(6, "Rumble")` |
| 2.2 | Load Hybrid Reverb | `load_instrument_or_effect(6, uri)` |
| 2.3 | Load Roar | `load_instrument_or_effect(6, roar_uri)` |
| 2.4 | Configure sidechain | Manual / params |
| 2.5 | Create Rolling Bass | Same pattern... |
| 2.6 | Create Acid track | Same pattern... |

#### Lane 3: Synths (Antigravity Window 3)

```
Developer: /intro-synths
```

| Task | Action | MCP Calls |
|------|--------|-----------|
| 3.1 | Create Stabs track | `create_midi_track()`, etc. |
| 3.2 | Load Wavetable | `load_instrument_or_effect(9, uri)` |
| 3.3 | Create Drone track | Same pattern... |

#### Lane 4: Vocals/FX (Antigravity Window 4)

```
Developer: /intro-vocals
```

| Task | Action | MCP Calls |
|------|--------|-----------|
| 4.1 | Create Main Vocal track | `create_midi_track()`, etc. |
| 4.2 | Create Vocal FX track | Same... |
| 4.3 | Create Risers track | Same... |

---

## Tool Choice by Task Type

| Task Type | Best Tool | Why |
|-----------|-----------|-----|
| Simple MCP call | **Gemini headless** | Fast, parallel |
| Multi-step workflow | **Antigravity workflow** | Context, turbo-all |
| Complex debugging | **Claude agent** | Reasoning |
| Manual in Ableton | **Human** | No API |

---

## Execution Method

### Option A: Antigravity Workflows (Recommended)

Create workflow files, run with `/slash-command`:

```bash
# Terminal 1
antigravity> /intro-drums

# Terminal 2
antigravity> /intro-bass

# Terminal 3
antigravity> /intro-synths

# Terminal 4
antigravity> /intro-vocals
```

### Option B: Gemini Headless Batch

```bash
# drums.sh
gemini --headless "Call MCP: create_midi_track then set_track_name(0, 'Kick')"
gemini --headless "Call MCP: load_instrument_or_effect(0, 'query:Drums#...')"
# ...
```

### Option C: Python Script Direct

```bash
python scripts/workflows/create_intro.py --lane=drums
```

---

## Files to Create

### Workflows (`.agent/workflows/`)

| File | Purpose |
|------|---------|
| `/intro-drums.md` | Create drum tracks |
| `/intro-bass.md` | Create bass tracks |
| `/intro-synths.md` | Create synth tracks |
| `/intro-vocals.md` | Create vocal/FX tracks |

### Supporting Scripts

| File | Purpose |
|------|---------|
| `scripts/workflows/create_intro.py` | Python entry point |
| `scripts/workflows/patterns.py` | MIDI patterns (isobar) |
| `state/progress.json` | Track completion |

---

## Decision: D011 - MCP Registration

**Status**: NEEDS ACTION
**Decision**: Register `ableton_mcp` in Antigravity's `mcp_config.json`
**Rationale**: Enables Antigravity to call MCP tools directly
**Action**:
```bash
# Edit ~/.gemini/antigravity/mcp_config.json
# Add ableton_mcp server entry
```

---

## Immediate Next Steps

1. [ ] **Register MCP** in Antigravity config
2. [ ] **Install Suite** (in progress)
3. [ ] **Verify MCP connection** post-upgrade
4. [ ] **Create workflow files** (4 files)
5. [ ] **Run parallel workflows**
6. [ ] **Verify Intro in Ableton**

---

## Blockers

| Blocker | Status | Resolution |
|---------|--------|------------|
| Suite not installed | ⏳ Pending | Installing now |
| MCP not in Antigravity | ❌ Not done | Add to config |
| Stem separation API | ❌ Not implemented | Manual only (not needed for Phase 1) |
