# Execution Plan: Intro Section

## Fastest Path Using Available Tools

Based on documented capabilities:
- **Antigravity workflows** (`.agent/workflows/`) with `// turbo-all`
- **Gemini CLI headless** for parallel batch execution
- **Claude agent mode** for complex multi-step tasks

---

## Phase 0: Foundation Setup (5 min)

### One-time setup (must complete first)

```bash
# In Ableton (manual):
1. Set tempo to 136 BPM
2. Create Return A (Reverb)
3. Create Return B (Delay)

# Verify MCP connection:
make check-port
```

---

## Phase 1: Parallel Track Creation (30 min target)

### Method: 4 Terminals with Gemini Headless

Open 4 terminal tabs and run simultaneously:

```bash
# Terminal 1: Drums
gemini --headless "Create Track 01 Kick for intro bars 1-16 at 136 BPM. Use Drum Rack. 4-on-floor pattern." -d scripts/dearpygui_controller/agents/
gemini --headless "Create Track 02 Snare for intro bars 1-16. Sparse pattern for intro." -d scripts/dearpygui_controller/agents/
gemini --headless "Create Track 03 Hi-hats for intro bars 1-16." -d scripts/dearpygui_controller/agents/
# ...continue for all 6 drum tracks

# Terminal 2: Bass
gemini --headless "Create Track 07 Rumble/Sub for intro bars 1-16. Sidechain to kick." -d scripts/dearpygui_controller/agents/
gemini --headless "Create Track 08 Rolling Bass for intro bars 1-16. May be silent for intro." -d scripts/dearpygui_controller/agents/
gemini --headless "Create Track 09 Acid Line for intro bars 1-16." -d scripts/dearpygui_controller/agents/

# Terminal 3: Synths
gemini --headless "Create Track 10 Synth Stabs for intro bars 1-16." -d scripts/dearpygui_controller/agents/
gemini --headless "Create Track 11 Drone/Pad for intro bars 1-16. Atmospheric texture." -d scripts/dearpygui_controller/agents/

# Terminal 4: Vocals/FX
gemini --headless "Create Track 12 Main Vocal for intro bars 1-16." -d scripts/dearpygui_controller/agents/
gemini --headless "Create Track 13 Vocal FX for intro bars 1-16." -d scripts/dearpygui_controller/agents/
gemini --headless "Create Track 14 Risers for intro bars 1-16." -d scripts/dearpygui_controller/agents/
```

---

## Phase 2: Alternative - Antigravity Workflows

### Create workflow files first:

#### `.agent/workflows/intro-drums.md`
```markdown
---
description: Create all drum tracks for intro section
---
// turbo-all

1. Create Track 01 Kick bars 1-16:
   ```bash
   python scripts/workflows/create_track.py kick intro
   ```
2. Create Track 02 Snare bars 1-16:
   ```bash
   python scripts/workflows/create_track.py snare intro
   ```
3. Create Track 03 Hi-hats bars 1-16:
   ```bash
   python scripts/workflows/create_track.py hihats intro
   ```
4. Create Track 04 Toms bars 1-16:
   ```bash
   python scripts/workflows/create_track.py toms intro
   ```
5. Create Track 05 Glitch bars 1-16:
   ```bash
   python scripts/workflows/create_track.py glitch intro
   ```
6. Create Track 06 Ride bars 1-16:
   ```bash
   python scripts/workflows/create_track.py ride intro
   ```
```

#### `.agent/workflows/intro-bass.md`
```markdown
---
description: Create all bass tracks for intro section
---
// turbo-all

1. Create Track 07 Rumble bars 1-16:
   ```bash
   python scripts/workflows/create_track.py rumble intro
   ```
2. Create Track 08 Rolling Bass bars 1-16:
   ```bash
   python scripts/workflows/create_track.py rolling_bass intro
   ```
3. Create Track 09 Acid bars 1-16:
   ```bash
   python scripts/workflows/create_track.py acid intro
   ```
```

#### `.agent/workflows/intro-synths.md`
```markdown
---
description: Create all synth tracks for intro section
---
// turbo-all

1. Create Track 10 Stabs bars 1-16:
   ```bash
   python scripts/workflows/create_track.py stabs intro
   ```
2. Create Track 11 Drone bars 1-16:
   ```bash
   python scripts/workflows/create_track.py drone intro
   ```
```

#### `.agent/workflows/intro-vocals.md`
```markdown
---
description: Create all vocal/FX tracks for intro section
---
// turbo-all

1. Create Track 12 Main Vocal bars 1-16:
   ```bash
   python scripts/workflows/create_track.py main_vocal intro
   ```
2. Create Track 13 Vocal FX bars 1-16:
   ```bash
   python scripts/workflows/create_track.py vocal_fx intro
   ```
3. Create Track 14 Risers bars 1-16:
   ```bash
   python scripts/workflows/create_track.py risers intro
   ```
```

### Then run in 4 Antigravity windows:

```
Window 1: /intro-drums
Window 2: /intro-bass
Window 3: /intro-synths
Window 4: /intro-vocals
```

---

## Phase 3: Claude Agent for Complex Tasks

Use Claude for tasks requiring reasoning:

```bash
# For complex sidechain routing:
claude "Set up sidechain compression from Track 01 Kick to Track 07 Rumble" --allow-bash

# For debugging:
claude "The kick track has no notes, debug and fix" --allow-bash
```

---

## Comparison: Methods

| Method | Parallel? | Context Aware? | Speed |
|--------|-----------|----------------|-------|
| Gemini headless (4 terminals) | ✅ Yes | ❌ No | Fastest |
| Antigravity workflows (4 windows) | ✅ Yes | ✅ Yes | Fast |
| Claude agent mode | ❌ No | ✅ Yes | Slow |

### Recommendation: Hybrid

1. **Gemini headless** for simple track creation (parallel)
2. **Antigravity workflows** for multi-step tasks (semi-auto)
3. **Claude agent** for debugging/complex routing

---

## Files to Create

| File | Purpose |
|------|---------|
| `scripts/workflows/create_track.py` | Entry point for track creation |
| `.agent/workflows/intro-drums.md` | Drum workflow |
| `.agent/workflows/intro-bass.md` | Bass workflow |
| `.agent/workflows/intro-synths.md` | Synths workflow |
| `.agent/workflows/intro-vocals.md` | Vocals workflow |

---

## Immediate Next Steps

1. ✅ Create `scripts/workflows/create_track.py`
2. ✅ Create 4 workflow files
3. 🔄 Open 4 Antigravity windows
4. 🔄 Run `/intro-drums`, `/intro-bass`, `/intro-synths`, `/intro-vocals`
5. ✅ Verify all 16 tracks in Ableton

---

## Decision Record

**D009: Execution Method**
- **Status**: PROPOSED
- **Decision**: Hybrid approach
  - Gemini headless for parallel simple tasks
  - Antigravity workflows with `// turbo-all` for multi-step
  - Claude agent for complex debugging
- **Rationale**: Maximizes parallelism while maintaining context where needed
