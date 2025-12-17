# MCP Tools Documentation

## Overview

**Current Tools**: 28 implemented in `MCP_Server/server.py`
**Edition**: Suite (auto-detected or from config)

---

## Current Tools by Category

### Session & Tracks
| Tool | Edition | Description |
|------|---------|-------------|
| `get_session_info` | Intro | Get tempo, track count, etc. |
| `get_track_info` | Intro | Get track details |
| `create_midi_track` | Intro | Create new MIDI track |
| `delete_track` | Intro | Delete a track |
| `set_track_name` | Intro | Rename a track |
| `set_track_volume` | Intro | Set track volume |
| `set_master_volume` | Intro | Set master volume |

### Clips & Notes
| Tool | Edition | Description |
|------|---------|-------------|
| `create_clip` | Intro | Create MIDI clip |
| `add_notes_to_clip` | Intro | Add MIDI notes |
| `set_clip_name` | Intro | Rename clip |
| `duplicate_clip` | Intro | Copy clip to new slot |
| `empty_clip_slot` | Intro | Clear clip slot |
| `relocate_clip` | Intro | Move clip to new slot |

### Devices & Effects
| Tool | Edition | Description |
|------|---------|-------------|
| `load_instrument_or_effect` | Intro | Load device by URI |
| `load_effect_on_main` | Intro | Load effect on master |
| `set_device_parameter` | Intro | Set device param |
| `get_device_parameters` | Intro | Get device params |
| `create_audio_effect_rack` | Standard | Create effect rack |
| `create_rack_chain` | Standard | Add chain to rack |
| `load_effect_to_chain` | Standard | Load effect into chain |
| `load_drum_kit` | Intro | Load drum rack + kit |

### Browser
| Tool | Edition | Description |
|------|---------|-------------|
| `get_browser_tree` | Intro | Browse categories |
| `get_browser_items_at_path` | Intro | Browse specific path |

### Transport
| Tool | Edition | Description |
|------|---------|-------------|
| `set_tempo` | Intro | Set BPM |
| `fire_clip` | Intro | Start clip |
| `stop_clip` | Intro | Stop clip |
| `start_playback` | Intro | Start transport |
| `stop_playback` | Intro | Stop transport |

---

## Edition Backlog

### Suite-Only (Priority)

| Tool | Status | Priority | Needed For |
|------|--------|----------|------------|
| `separate_stems` | ❌ TODO | P0 | Benchmark comparison |
| `load_roar` | ✅ Working | P0 | `query:AudioFx#Roar` |
| `load_meld` | ❌ TODO | P1 | Synth textures |
| `load_drift` | ✅ Working | P2 | `query:Synths#Drift` |
| `load_wavetable` | ⚠️ Partial | P1 | Synth leads |

> **Prerequisite**: Install Core Library pack in Ableton to access Suite devices.

### Standard (Incremental)

| Tool | Status | Priority | Notes |
|------|--------|----------|-------|
| `set_sidechain_input` | ✅ Done | P0 | Rumble pumping |
| `create_return_track` | ✅ Done | P0 | FX buses |
| `set_send_level` | ✅ Done | P1 | Send routing |
| `set_track_output` | ⚠️ Partial | P1 | Routing |

### Intro (Base) - Missing

| Tool | Status | Priority | Notes |
|------|--------|----------|-------|
| `create_audio_track` | ❌ TODO | P1 | Audio clips |
| `set_track_arm` | ❌ TODO | P2 | Recording |
| `set_track_mute` | ❌ TODO | P1 | Mixing |
| `set_track_solo` | ❌ TODO | P1 | Mixing |
| `get_clip_notes` | ❌ TODO | P2 | Read MIDI |
| `delete_notes` | ❌ TODO | P2 | Edit MIDI |

---

## Phase 1 Required Tools

For "I Am Machine" Intro section (16 tracks):

| Track | Required Tools | Status |
|-------|----------------|--------|
| Kick | create_midi_track, load_drum_kit, add_notes_to_clip | ✅ |
| Rumble | load_roar, set_sidechain_input | ❌ Need Roar + SC |
| Snare | create_midi_track, add_notes_to_clip | ✅ |
| Hi-hats | create_midi_track, add_notes_to_clip | ✅ |
| Returns | create_return_track, set_send_level | ❌ Need returns |
| Acid | load_instrument_or_effect (Wavetable) | ✅ |

---

## Agent → MCP Gap Analysis

Methods referenced in agents but **NOT in MCP**:

| Agent | Missing Method | Priority |
|-------|----------------|----------|
| SidechainAgent | `load_device` | P0 |
| SidechainAgent | `set_sidechain_input` | P0 |
| EffectsChainAgent | `set_chain_selector_zone` | P2 |
| EffectsChainAgent | `map_macro_control` | P2 |
| ReturnTrackAgent | `create_return_track` | P0 |
| MixerAgent | `set_send_level` | P1 |

---

## Priority Implementation Order

### Sprint 1: Phase 1 Blockers
1. `set_sidechain_input` - Rumble track pumping
2. `create_return_track` - FX buses
3. `load_roar` (Suite) - Rumble saturation

### Sprint 2: Mixing
4. `set_send_level` - Send routing
5. `set_track_mute` / `set_track_solo`
6. `set_track_output` (complete)

### Sprint 3: Suite Features
7. `separate_stems` (Suite) - Reference analysis
8. `load_meld` / `load_drift` (Suite)

---

## Workflow: Adding New Tool

```bash
/add-tool
```

1. Add to `MCP_Server/server.py` with `@mcp.tool()` + `@requires_edition()`
2. Add handler to `AbletonMCP_Remote_Script/__init__.py`
3. Run `just mcp-tools` to verify
4. Run `just doctor` to validate
5. Create test in `tests/test_tools.py`
