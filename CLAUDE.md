# Ableton-MCP Project

MCP (Model Context Protocol) server for controlling Ableton Live 12 via Claude CLI.

## Current Goal

**Recreate "I Am Machine" by Lilly Palmer** in Ableton Live 12 Suite.

- Reference: `assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
- BPM: 136 | **Key: G (MIDI 31)** | Duration: 6:17 (~224 bars)
- **Phase 1**: Complete first 16 bars (Intro) - sound similar to reference

---

## The Core Problem

### What We Have
- 16 tracks created with instruments loaded
- Each track has 16-bar intro clip
- All tests pass (153 tests)
- Sidechain routing configured

### What's Wrong
**Tracks pass structural tests but SOUND AWFUL because:**

| Issue | Current | Reference | Impact |
|-------|---------|-----------|--------|
| Root note | F (MIDI 29) | **G (MIDI 31)** | WRONG KEY |
| Pitch accuracy | 21.1% | Target: 45%+ | Sounds wrong |
| Note density | 16/bar | 12.8/bar | Too busy |
| Scale | F minor hardcoded | G-chromatic derived | Wrong pitches |

### Why This Happened
The `ComposerAgent` and workflow scripts have **hardcoded F minor patterns** without consulting the reference analysis data at `assets/analysis/stem_analysis.json`.

---

## Autonomous Improvement Plan

### Claude's Capabilities (What Claude CAN Do)

| Capability | How | Example |
|------------|-----|---------|
| Read reference data | `Read` tool | Load stem_analysis.json |
| Extract patterns | Python analysis | Get intro bass pitches |
| Call MCP tools | Tool calls | `add_notes_to_clip`, `set_device_parameter` |
| Create new MCP tools | `/add-tool` workflow | `clear_clip_notes`, `get_reference_pattern` |
| Run tests | `Bash` | `pytest tests/...` |
| Measure accuracy | Python | Compare pitches to reference |
| Research techniques | `WebFetch` | Ableton manual, sound design guides |
| Iterate autonomously | Tool loop | Fix → Measure → Improve |

### Claude's Constraints (What Claude CANNOT Do)

| Constraint | Workaround |
|------------|------------|
| Cannot hear audio | Human provides "better/worse/same" feedback |
| Cannot do realtime A/B | Human listens, reports back |
| Cannot see Ableton GUI | Use MCP tools to query state |
| Cannot know "sounds good" | Use metrics as proxy (pitch %, density) |

---

## Ranked Improvement Ideas

### TIER 0: CRITICAL (Do Immediately)

#### 1. Fix Wrong Root Note (Highest Impact)
**Problem**: All bass patterns use F (29) but reference uses G (31)
**Solution**: Update all pattern generators to use G-based pitches
**Validation**: `test_agent_reference_accuracy.py` should pass

```python
# WRONG (current):
scale = [29, 32, 34, 36, 39]  # F1, Ab1, Bb1, C2, Eb2

# CORRECT (from analysis):
scale = [31, 32, 33, 34]  # G1, G#1, A1, A#1
```

**Files to Fix**:
- `scripts/workflows/create_intro_bass.py` (lines 128-131, 144)
- `scripts/dearpygui_controller/agents/composer_agent.py` (line 100)

#### 2. Create `clear_clip_notes` MCP Tool
**Why**: Before we can fix patterns, we need to clear existing wrong notes
**Priority**: P0 - Blocker for autonomous track fixing

```python
@mcp.tool()
def clear_clip_notes(track_index: int, clip_index: int) -> str:
    """Clear all MIDI notes from a clip."""
```

### TIER 1: HIGH IMPACT (Do This Week)

#### 3. Reference-Data-Driven Pattern Generation
**Problem**: Patterns are hardcoded, not derived from analysis
**Solution**: Load `stem_analysis.json` and extract intro section

```python
# What Claude should do before generating any pattern:
import json
with open('assets/analysis/stem_analysis.json') as f:
    data = json.load(f)

INTRO_DURATION = 28.24  # seconds (16 bars at 136 BPM)
intro_bass = [n for n in data['bass']['notes'] if n['start'] < INTRO_DURATION]

# Use actual pitch distribution:
# G1 (31): 39 notes - PRIMARY ROOT
# G#1 (32): 23 notes
# F#1 (30): 19 notes
# A1 (33): 18 notes
```

#### 4. Per-Track Fix Commands
Create `/fix-track-NN` slash commands that:
1. Load reference data from stem_analysis.json
2. Clear existing notes with `clear_clip_notes`
3. Generate reference-accurate pattern
4. Apply via `add_notes_to_clip`
5. Run accuracy test to verify improvement

**Priority Order**:
| Command | Track | Why First |
|---------|-------|-----------|
| `/fix-track-07` | Rumble (sub bass) | Foundation of track |
| `/fix-track-01` | Kick | Drives everything |
| `/fix-track-08` | Rolling Bass | Main melodic bass |
| `/fix-track-02` | Snare | Core groove |
| `/fix-track-03` | Hi-hats | Rhythm texture |

#### 5. Pitch Accuracy Metric Function
Create reusable accuracy measurement:

```python
def measure_pitch_accuracy(track_notes: list, reference_notes: list) -> dict:
    """
    Returns:
    - pitch_accuracy: % of notes matching reference pitches
    - density_ratio: track density / reference density
    - pitch_distribution: Counter of pitches used
    """
```

### TIER 2: MEDIUM IMPACT (Do Next Week)

#### 6. New MCP Tools for Comparison

| Tool | Purpose | Priority |
|------|---------|----------|
| `get_reference_pattern` | Load pattern from stem_analysis.json for section | P1 |
| `compare_clip_accuracy` | Return pitch/timing accuracy vs reference | P1 |
| `get_pitch_histogram` | Return pitch distribution of clip | P2 |

**Example `get_reference_pattern` implementation**:
```python
@mcp.tool()
def get_reference_pattern(
    stem_type: str,  # "bass" or "drums"
    start_bar: int = 0,
    end_bar: int = 16
) -> str:
    """Get reference pattern from stem analysis."""
    # Load analysis, filter to bar range, return notes
```

#### 7. Iterative Refinement Loop
```
┌──────────────────────────────────────────────────────────────┐
│  1. Claude reads reference data                              │
│              ↓                                               │
│  2. Claude generates pattern based on reference pitches      │
│              ↓                                               │
│  3. Claude clears old notes, adds new notes via MCP          │
│              ↓                                               │
│  4. Claude measures accuracy (pitch %, density)              │
│              ↓                                               │
│  5. If accuracy < target: Claude refines pattern             │
│              ↓                                               │
│  6. Human listens: "better/worse/same"                       │
│              ↓                                               │
│  7. Claude incorporates feedback, iterates                   │
└──────────────────────────────────────────────────────────────┘
```

#### 8. Research-Apply Workflow
Claude can research sound design autonomously:

```
1. WebFetch Ableton manual for "sidechain compression settings"
2. Extract recommended values for techno
3. Apply via set_device_parameter MCP tool
4. Ask human to verify sound
```

**Research Topics**:
- Techno sub bass synthesis (Operator settings)
- Sidechain compression for pumping effect
- EQ separation between kick and bass
- 303 acid sound design

### TIER 3: LOWER IMPACT (Future)

#### 9. Timing Accuracy (After Pitch is Fixed)
Once pitches are correct, refine timing:
- Compare note start times to reference onsets
- Quantize or humanize as needed
- Target: 80% of notes within 50ms of reference

#### 10. Velocity Dynamics
Match velocity curves to reference:
- Extract velocity patterns from analysis
- Apply accent patterns (beat 1 louder, etc.)

#### 11. Device Parameter Tuning
Once notes are correct, tune synth parameters:
- A/B compare with reference
- Adjust filter, envelope, etc.
- Requires human ears for feedback

---

## Implementation Roadmap

### Day 1: Critical Fixes
```bash
# 1. Create clear_clip_notes MCP tool
# Follow /add-tool workflow

# 2. Fix root note in workflow scripts
# Edit create_intro_bass.py: change 29 → 31

# 3. Run accuracy test
pytest tests/phases/phase1_intro/test_agent_reference_accuracy.py -v
```

### Day 2: Track 07 Rumble (Priority Bass)
```bash
# 1. Clear existing rumble notes
# Use new clear_clip_notes tool

# 2. Generate G-based pattern from reference
# Load stem_analysis.json, filter intro bass

# 3. Apply new notes
# Use add_notes_to_clip

# 4. Verify accuracy improved
pytest tests/phases/phase1_intro/test_track_07_rumble.py -v
```

### Day 3: Remaining Bass Tracks
- Track 08: Rolling Bass
- Track 09: Acid

### Day 4: Drum Tracks
- Track 01: Kick
- Track 02: Snare
- Track 03: Hi-hats

### Day 5: Validation & Human Feedback
```bash
# Run all accuracy tests
pytest tests/phases/phase1_intro/test_agent_reference_accuracy.py -v

# Fire all clips
# Human A/B compares with reference
# Claude iterates based on feedback
```

---

## Reference Data (Validated)

**Source**: `assets/analysis/stem_analysis.json`

### Intro Section Stats (First 16 Bars)
| Data | Count | Density |
|------|-------|---------|
| Drum onsets | 207 | 12.9/bar |
| Bass notes | 204 | 12.8/bar |

### Bass Pitch Distribution (Intro)
```
Primary Sub-Bass Range (< MIDI 40):
┌──────────────────────────────────────┐
│ G1  (31): ████████████████████ 39    │ ← ROOT
│ G#1 (32): ████████████ 23            │
│ F#1 (30): ██████████ 19              │
│ A1  (33): █████████ 18               │
│ A#1 (34): █████ 11                   │
│ C1  (24): ████ 9                     │
│ F1  (29): ████ 8   ← CURRENT WRONG   │
└──────────────────────────────────────┘
```

### Key Finding
**Reference root is G1 (MIDI 31), not F1 (MIDI 29)**

Current ComposerAgent uses F minor scale which overlaps only 8/152 sub-bass notes (5.3%).
Corrected G-based scale would overlap 91/152 sub-bass notes (60%).

---

## Architecture

```
Claude CLI ─────► MCP_Server/server.py (32+ tools)
                         │
                         ▼ TCP:9877
           AbletonMCP_Remote_Script/__init__.py
                         │
                         ▼
                  Ableton Live API

Reference Data Flow:
assets/analysis/stem_analysis.json
         │
         ▼
Claude reads → extracts patterns → calls MCP tools → modifies Ableton
         │
         ▼
Claude measures accuracy → iterates if needed
```

---

## Quick Commands

```bash
just setup          # First-time setup
just quick          # Quick validation (no Ableton)
just ci             # Full CI (lint + test + doctor)
just mcp-tools      # List available tools
just doctor         # Health check
just deploy         # Deploy Remote Script
just check-port     # Verify port 9877
```

## Slash Commands

### Session Management
| Command | Purpose |
|---------|---------|
| `/start-claude-ableton-session` | Initialize session |
| `/build-claude-ableton-session` | Build validation |
| `/project-status` | Current progress |
| `/validate` | Run CI validation |
| `/add-tool` | Add new MCP tool |

### Track Creation
| Command | Purpose |
|---------|---------|
| `/intro-drums` | Create drum tracks 1-6 |
| `/intro-bass` | Create bass tracks 7-9 |
| `/intro-synths` | Create synth tracks 10-11 |
| `/intro-vocals` | Create vocal tracks 12-13 |

### Track Fixing (To Implement)
| Command | Track | Priority | Status |
|---------|-------|----------|--------|
| `/fix-track-07` | Rumble | P0 | TODO |
| `/fix-track-01` | Kick | P0 | TODO |
| `/fix-track-08` | Rolling Bass | P1 | TODO |
| `/fix-track-02` | Snare | P1 | TODO |
| `/fix-track-03` | Hi-hats | P1 | TODO |

---

## Key MCP Tools

### Currently Available (32 tools)
```python
# Session & Tracks
create_midi_track, create_audio_track, set_track_name, get_track_info, delete_track

# Clips & Notes
create_clip, add_notes_to_clip, get_clip_notes, set_clip_name, duplicate_clip

# Devices
load_instrument_or_effect, load_drum_kit, set_device_parameter, get_device_parameters

# Transport
fire_clip, stop_clip, start_playback, stop_playback, set_tempo

# Routing
set_sidechain_input, create_return_track, set_send_level
```

### Priority Tools to Add

| Tool | Purpose | Priority | Blocker For |
|------|---------|----------|-------------|
| `clear_clip_notes` | Remove all notes from clip | P0 | Track fixing |
| `get_reference_pattern` | Load from stem_analysis.json | P1 | Automation |
| `compare_clip_accuracy` | Pitch/timing accuracy | P1 | Metrics |
| `set_track_mute` | Mute/unmute tracks | P1 | A/B testing |

---

## Success Criteria

### Structural (Current - All Pass)
- [x] All 16 tracks created with instruments
- [x] Each track has 16-bar intro clip
- [x] Sidechain routing configured
- [x] 153 tests pass

### Sound Quality (New - In Progress)
- [ ] Bass tracks use G-based pitches (not F)
- [ ] Pitch accuracy > 40% on bass tracks
- [ ] Note density within 20% of reference
- [ ] Human A/B test: "sounds similar" rating

### Accuracy Targets

| Track | Current | Target | Metric |
|-------|---------|--------|--------|
| Rumble | 21.1% | 45%+ | Pitch accuracy |
| Rolling | TBD | 40%+ | Pitch accuracy |
| Acid | TBD | 35%+ | Pitch accuracy |
| All | 16/bar | 12.8/bar | Density |

---

## Autonomous Workflow Example

### Fixing Track 07 Rumble

```python
# Step 1: Read reference data
stem_data = read("assets/analysis/stem_analysis.json")
intro_bass = filter_to_intro(stem_data['bass']['notes'])

# Step 2: Analyze pitch distribution
pitches = Counter([round(n['pitch']) for n in intro_bass if n['pitch'] < 40])
# Result: G1(31)=39, G#1(32)=23, F#1(30)=19...

# Step 3: Generate corrected pattern
def corrected_rumble_pattern():
    notes = []
    for bar in range(16):
        notes.append({
            "pitch": 31,  # G1 - CORRECT ROOT
            "start_time": float(bar * 4),
            "duration": 4.0,
            "velocity": 100,
        })
    return notes

# Step 4: Clear old notes (need new MCP tool)
clear_clip_notes(track_index=6, clip_index=0)

# Step 5: Add corrected notes
add_notes_to_clip(track_index=6, clip_index=0, notes=corrected_rumble_pattern())

# Step 6: Measure improvement
# Run test: pitch accuracy should improve from 21% to 40%+

# Step 7: Human verification
# Play clip, compare to reference
# Feedback: "better" / "worse" / "same"
```

---

## Project Structure

```
ableton-mcp/
├── MCP_Server/server.py          # MCP tools (32 tools)
├── AbletonMCP_Remote_Script/     # Ableton Remote Script
├── scripts/
│   ├── workflows/                # Track creation scripts
│   └── dearpygui_controller/
│       └── agents/               # Agent classes
├── tests/phases/phase1_intro/    # TDD test files
├── assets/
│   ├── audio/reference/          # Reference track
│   └── analysis/                 # stem_analysis.json
├── .claude/commands/             # Slash commands
├── TOOLS.md                      # Tool documentation
└── justfile                      # Build commands
```

---

## Troubleshooting

### Accuracy Tests Fail
1. Check pitch values in pattern generators
2. Verify using G (31) not F (29) as root
3. Run: `pytest test_agent_reference_accuracy.py -v`

### Port 9877 Not Active
1. Open Ableton Live 12
2. Preferences > Link, Tempo & MIDI > Control Surface = "AbletonMCP"
3. Re-run `just check-port`

### Tracks Sound Wrong After Fix
1. Verify new notes were added: `get_clip_notes(track, clip)`
2. Check pitch distribution matches reference
3. Ask human for A/B comparison feedback

---

## Next Actions for Claude

When starting a session, Claude should:

1. **Load reference data first**:
   ```python
   with open('assets/analysis/stem_analysis.json') as f:
       REF_DATA = json.load(f)
   ```

2. **Check current accuracy**:
   ```bash
   pytest tests/phases/phase1_intro/test_agent_reference_accuracy.py -v
   ```

3. **Prioritize by impact**:
   - If `clear_clip_notes` tool missing → create it first
   - If accuracy < 40% → fix patterns
   - If tests pass but sounds wrong → ask human

4. **Iterate with feedback**:
   - Make change → measure → ask human → refine

---

## Change Log

| Date | Change | Impact |
|------|--------|--------|
| 2024-12 | Created autonomous improvement plan | Added TIER 0-3 priorities |
| 2024-12 | Identified root note error (F→G) | Key finding |
| 2024-12 | Added reference data analysis | 204 intro bass notes documented |
