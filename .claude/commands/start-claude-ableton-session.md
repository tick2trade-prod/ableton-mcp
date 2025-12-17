# Start Claude Ableton Session

Initialize a Claude CLI session for the "I Am Machine" recreation project.

## Project Context

**Goal**: Recreate "I Am Machine" by Lilly Palmer in Ableton Live 12 Suite

**Reference Track**: `/Users/alexzh/ableton-mcp/assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
- Duration: 6:17
- BPM: 136
- Key: F minor
- Style: Hard Techno / Industrial Techno
- Total: ~224 bars (9 sections)

**Phase 1 Objective**: Complete **first 16 bars (Intro section)** for all 16 tracks

## Session Startup Checklist

### 1. Setup (if first time)
```bash
just setup
```

### 2. Quick Validation
```bash
just quick
```

### 3. Check MCP Tools
```bash
just mcp-tools
```
Expected: **32 tools** available

### 4. Run Doctor
```bash
just doctor
```
Expected: **4/4 checks pass**

## Verify Ableton Connection

### Check Port
```bash
just check-port
```
Should show: `Port 9877 active`

### Test MCP Connection
```bash
just mcp-test
```

If port not active:
1. Open Ableton Live 12
2. Go to Preferences > Link, Tempo & MIDI
3. Set Control Surface to "AbletonMCP"
4. Re-run `just check-port`

## Phase 1: Intro Section (Bars 1-16)

### 16 Tracks to Create

| # | Track | Category | Priority |
|---|-------|----------|----------|
| 01 | Kick | Drums | **HIGH** |
| 02 | Snare | Drums | Medium |
| 03 | Hi-hats | Drums | Medium |
| 04 | Toms | Drums | Low |
| 05 | Glitch | Drums | Low |
| 06 | Ride | Drums | Low |
| 07 | Rumble | Bass | **HIGH** |
| 08 | Rolling Bass | Bass | Medium |
| 09 | Acid | Bass | Medium |
| 10 | Stabs | Synths | Low |
| 11 | Drone | Synths | Medium |
| 12 | Main Vocal | Vocals | Low |
| 13 | Vocal FX | Vocals | Low |
| 14 | Risers | FX | Low |
| 15 | Return A | Returns | Setup |
| 16 | Return B | Returns | Setup |

### Priority Order
1. **Kick** - Foundation, sidechain source
2. **Rumble** - Sub bass with sidechain pumping
3. Remaining drums
4. Remaining bass
5. Synths
6. Vocals/FX

## If Tools Are Missing

This is a **custom ableton-mcp project**. If a tool doesn't exist:

### 1. Check Available Tools
```bash
just mcp-tools
```

### 2. Check TOOLS.md
```bash
cat TOOLS.md
```

### 3. Add Missing Tool
Use `/add-tool` workflow:
- Add to `MCP_Server/server.py`
- Add handler to `AbletonMCP_Remote_Script/__init__.py`
- Verify: `just build`
- Confirm: `just mcp-tools`

### 4. Ensure Build Passes
```bash
just ci
```

## Current Tool Count: 32

Key tools for track creation:
- `create_midi_track` / `create_audio_track`
- `set_track_name`
- `load_browser_item` (instruments, effects)
- `create_clip`
- `add_notes_to_clip`
- `get_clip_notes`
- `set_sidechain_input`
- `create_return_track`
- `set_send_level`
- `fire_clip` / `start_playback`

## Workflow Scripts

Execute existing scripts:
```bash
# Priority tracks (Kick + Rumble)
python scripts/workflows/create_intro_drums.py
python scripts/workflows/create_intro_bass.py

# All lanes
python scripts/workflows/create_intro_synths.py
python scripts/workflows/create_intro_vocals.py
```

## Log Files

All workflow execution is logged:
- `scripts/workflows/intro_drums.log`
- `scripts/workflows/intro_bass.log`
- `scripts/workflows/intro_synths.log`
- `scripts/workflows/intro_vocals.log`

## Session Commands

| Command | Purpose |
|---------|---------|
| `/project-status` | Overall progress |
| `/run-priority` | Execute Kick + Rumble |
| `/track-01-kick` | Kick track details |
| `/track-07-rumble` | Rumble track details |
| `/build-claude-ableton-session` | Build/validate codebase |
| `/validate` | Run CI checks |
| `/add-tool` | Add new MCP tool |

## Reference Analysis

To compare with reference:
```bash
# Load reference track for stem separation
python scripts/workflows/load_reference.py
```

Then in Ableton:
1. Right-click reference clip
2. "Separate Stems to New Audio Tracks"
3. Compare stems to recreated tracks

## Success Criteria for Phase 1

- [ ] All 16 tracks created
- [ ] Each track has instrument/device loaded
- [ ] Each track has 16-bar intro clip
- [ ] Patterns match reference style
- [ ] Sidechain pumping on Rumble
- [ ] Return tracks configured
- [ ] Full intro plays cohesively
- [ ] Sound matches reference reasonably

## Ready to Start

After validation passes:
1. Run `/run-priority` for Kick + Rumble
2. A/B compare with reference
3. Iterate on sound design
4. Complete remaining tracks
5. Move to Phase 2 (Build 1, bars 17-32)
