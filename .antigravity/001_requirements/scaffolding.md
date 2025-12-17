# Scaffolding: I Am Machine Full Recreation

## Overview

**Song**: Lily Palmer - I Am Machine (~6 min, ~136 BPM, ~224 bars)
**Total Tasks**: 16 tracks × 9 sections = **144 discrete tasks**

---

## 1. Directory Structure

```
ableton-mcp/
├── .agent/workflows/           # Antigravity workflows
│   ├── create-section.md      # Create one track×section
│   ├── verify-section.md      # Verify against stem
│   └── full-track.md          # Create all sections for one track
│
├── state/                      # Task state persistence
│   ├── progress.json          # Overall progress
│   └── tracks/
│       ├── kick.json          # Per-track state
│       ├── rumble.json
│       └── ...
│
├── sections/                   # Section definitions
│   └── i_am_machine.json      # Bar ranges, tempo, key
│
├── scripts/
│   ├── dearpygui_controller/  # GUI task master
│   │   ├── main.py           # Entry point
│   │   ├── task_manager.py   # Task state management
│   │   └── agents/           # 22 agents (modify as needed)
│   │
│   └── workflows/             # CLI workflow scripts
│       ├── create_section.py
│       ├── verify_section.py
│       └── checkpoint.py
│
└── live_set/
    └── i_am_machine/
        ├── project.als        # Ableton project
        └── stems/             # Reference stems for comparison
```

---

## 2. Workflow Files

### `.agent/workflows/create-section.md`

```markdown
---
description: Create one section of one track
---

1. Read section config: `cat sections/i_am_machine.json | jq '.sections["{section}"]'`
2. Read track config: `cat state/tracks/{track}.json`
// turbo
3. Run creation: `python scripts/workflows/create_section.py {track} {section}`
4. Verify in Ableton: clip exists with notes
5. Checkpoint: `python scripts/workflows/checkpoint.py {track} {section} complete`
```

### `.agent/workflows/full-track.md`

```markdown
---
description: Create all sections for one track
---
// turbo-all

1. For each section in [intro, build1, drop1, breakdown1, build2, drop2, breakdown2, build3, outro]:
   Run: `/create-section {track} {section}`
2. Verify full track plays through
3. Mark track complete
```

---

## 3. Section Configuration

### `sections/i_am_machine.json`

```json
{
  "song": "I Am Machine",
  "artist": "Lily Palmer",
  "bpm": 136,
  "key": "A minor",
  "total_bars": 224,
  "sections": {
    "intro":       {"start": 1,   "end": 16,  "energy": "low"},
    "build1":      {"start": 17,  "end": 32,  "energy": "rising"},
    "drop1":       {"start": 33,  "end": 64,  "energy": "high"},
    "breakdown1":  {"start": 65,  "end": 96,  "energy": "low"},
    "build2":      {"start": 97,  "end": 112, "energy": "rising"},
    "drop2":       {"start": 113, "end": 144, "energy": "high"},
    "breakdown2":  {"start": 145, "end": 176, "energy": "low"},
    "build3":      {"start": 177, "end": 192, "energy": "rising"},
    "outro":       {"start": 193, "end": 224, "energy": "high"}
  }
}
```

---

## 4. Track Configuration

### `state/tracks/kick.json`

```json
{
  "track": "kick",
  "index": 0,
  "agent": "PercussionAgent",
  "device": "Drum Rack",
  "sections": {
    "intro": {"status": "pending", "bars": [1, 16]},
    "build1": {"status": "pending", "bars": [17, 32]},
    "drop1": {"status": "pending", "bars": [33, 64]},
    "breakdown1": {"status": "pending", "bars": [65, 96]},
    "build2": {"status": "pending", "bars": [97, 112]},
    "drop2": {"status": "pending", "bars": [113, 144]},
    "breakdown2": {"status": "pending", "bars": [145, 176]},
    "build3": {"status": "pending", "bars": [177, 192]},
    "outro": {"status": "pending", "bars": [193, 224]}
  }
}
```

---

## 5. Progress Tracking

### `state/progress.json`

```json
{
  "total_tasks": 144,
  "completed": 0,
  "current": {"track": "kick", "section": "intro"},
  "tracks": {
    "kick": {"complete": 0, "total": 9},
    "rumble": {"complete": 0, "total": 9},
    ...
  }
}
```

---

## 6. DearPyGUI Task Master

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ I Am Machine Recreation - Task Master                      [0%] │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TRACKS              SECTIONS                                    │
│  ─────────────────────────────────────────────────────────────  │
│  [●] Kick            [I][B1][D1][BD1][B2][D2][BD2][B3][O]       │
│  [ ] Rumble          [ ][ ][ ][ ][ ][ ][ ][ ][ ]                │
│  [ ] Snare           [ ][ ][ ][ ][ ][ ][ ][ ][ ]                │
│  [ ] Hi-hats         [ ][ ][ ][ ][ ][ ][ ][ ][ ]                │
│  ...                                                             │
│                                                                  │
│  CURRENT: Kick > Intro (Bars 1-16)                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ [Create Section] [Verify] [Skip] [Mark Complete]        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  LOG:                                                            │
│  > Ready to create Kick intro...                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Agent Execution Flow

```
User clicks [Create Section]
    │
    ▼
DearPyGUI calls: subprocess.run(["python", "scripts/workflows/create_section.py", "kick", "intro"])
    │
    ▼
create_section.py:
    1. Load track config (kick.json)
    2. Load section config (i_am_machine.json)
    3. Connect to Ableton via MCP
    4. Create clip at bars 1-16
    5. Program MIDI notes (kick pattern)
    6. Save checkpoint
    7. Return success/failure
    │
    ▼
DearPyGUI updates UI
    │
    ▼
User clicks [Verify] or [Next]
```

---

## 8. CLI Integration

### Gemini CLI (via `.gemini/docs/headless.md`)

```bash
# Create section headlessly
echo "Create kick intro section bars 1-16" | gemini --yolo

# Batch create
gemini --headless < scripts/batch_create.txt
```

### Claude CLI (via `.claude/docs/agent-mode.md`)

```bash
# Agent mode for complex section
claude "Create the drop1 section for kick with 4-on-floor pattern" --allow-bash
```

### Ollama (via agents)

```python
# In agent, use Ollama for pattern suggestions
response = await self.ollama_query(
    "Suggest a techno kick pattern for a breakdown section at 136 BPM"
)
```

---

## 9. Antigravity Workflows

### Build & Validation Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| `/build` | `just ci` | Run CI validation |
| `/add-tool` | - | Add new MCP tool end-to-end |
| `/ci` | `just ci-live` | Full CI with Ableton |

### Track Creation Workflows

| Workflow | Purpose |
|----------|---------|
| `/create-section {track} {section}` | Create one section |
| `/verify-section {track} {section}` | Compare to stem |
| `/full-track {track}` | All sections for track |

### Justfile Commands

```bash
just              # List all recipes
just ci           # CI (no Ableton)
just ci-live      # CI with Ableton
just doctor       # Smart doctor
just mcp-tools    # List 28 MCP tools
just run          # Start MCP server
```

---

## 10. Execution Order

### Phase 1: Foundation (Kick + Rumble)
```
/full-track kick
/full-track rumble
```

### Phase 2: Rhythm
```
/full-track snare
/full-track hihats
/full-track toms
/full-track glitch
/full-track ride
```

### Phase 3: Bass
```
/full-track rolling_bass
/full-track acid
```

### Phase 4: Synths
```
/full-track stabs
/full-track drone
```

### Phase 5: Vocals
```
/full-track main_vocal
/full-track vocal_fx
```

### Phase 6: FX & Returns
```
/full-track risers
/full-track return_reverb
/full-track return_delay
```

---

## 11. Files to Create

| File | Purpose | Priority |
|------|---------|----------|
| `sections/i_am_machine.json` | Section definitions | 1 |
| `state/progress.json` | Progress tracking | 1 |
| `state/tracks/*.json` | Per-track state | 1 |
| `.agent/workflows/create-section.md` | Workflow | 1 |
| `scripts/workflows/create_section.py` | Execution script | 1 |
| `scripts/dearpygui_controller/task_manager.py` | GUI updates | 2 |
| `.agent/workflows/full-track.md` | Workflow | 2 |
| `.agent/workflows/verify-section.md` | Workflow | 3 |

---

## 12. Immediate Next Steps

1. Create `sections/i_am_machine.json`
2. Create `state/` directory structure
3. Create first workflow: `/create-section`
4. Test on Kick > Intro
5. Iterate
