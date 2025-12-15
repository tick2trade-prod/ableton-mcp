# Phase 6: DeepAgents/CrewAI Agent Specifications

**Parent Spec**: [007_mvp_master_spec.md](file:///Users/alexzh/ableton-mcp/specs/active/007_mvp_master_spec.md)

## Overview

Define the 4 specialized agents for the "I Am Machine" recreation pipeline.

---

## 1. Agent Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator (DearPyGUI)                     │
│                         ┌─────────┐                             │
│                         │  TODO   │                             │
│                         │  LIST   │                             │
│                         └────┬────┘                             │
│     ┌────────────────────────┼────────────────────────┐         │
│     ▼                        ▼                        ▼         │
│ ┌─────────┐            ┌─────────┐             ┌─────────┐      │
│ │Research │───────────▶│Composer │────────────▶│ Mixer   │      │
│ │ Agent   │  context   │ Agent   │  patterns   │ Agent   │      │
│ └─────────┘            └─────────┘             └────┬────┘      │
│                                                     │           │
│                                                     ▼           │
│                                               ┌─────────┐       │
│                                               │Verifier │       │
│                                               │ Agent   │       │
│                                               └─────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Research Agent

**Role**: Sound Research Engineer
**Model**: llama3 (Ollama)

### Tools
- `search_ableton_docs` - Query embedded PDF documentation
- `search_production_technique` - Web search for tutorials
- `search_device_docs` - Device-specific documentation

### Tasks
```python
research_tasks = [
    Task(
        description="Research Techno Rumble Kick production technique",
        expected_output="Summary of Reverb→Distortion→Filter signal chain",
    ),
    Task(
        description="Find Roar multiband saturation settings for low-end",
        expected_output="Parameter recommendations for Roar device",
    ),
]
```

### Context Output
```json
{
  "technique": "rumble_kick",
  "signal_chain": ["Reverb", "Roar", "EQ Eight", "Compressor"],
  "parameters": {
    "reverb_decay": 0.6,
    "roar_drive": 6.0,
    "eq_high_cut": 150
  }
}
```

---

## 3. Composer Agent

**Role**: Rhythm Programmer
**Model**: llama3 (Ollama)

### Tools
- `create_midi_track` - Create new MIDI track
- `create_clip` - Create empty clip
- `add_notes_to_clip` - Add MIDI notes
- `fire_clip` - Start playback

### Tasks per Track Type

| Track Type | Pattern | Notes Format |
|------------|---------|--------------|
| Kick | 4-on-floor | `[{pitch:36, start:0}, {pitch:36, start:1}, ...]` |
| Closed Hat | 16th notes | `[{pitch:42, start:0}, {pitch:42, start:0.25}, ...]` |
| Open Hat | Off-beat | `[{pitch:46, start:0.5}, {pitch:46, start:1.5}, ...]` |
| Clap | 2 & 4 | `[{pitch:39, start:1}, {pitch:39, start:3}, ...]` |
| Bass | Rolling 16ths | F Minor scale: F, Ab, Bb, C |

### Pattern Generation

```python
def generate_kick_pattern(bars: int = 4) -> list[dict]:
    """Generate 4-on-floor kick pattern."""
    notes = []
    for bar in range(bars):
        for beat in range(4):
            notes.append({
                "pitch": 36,  # C1
                "start_time": float(bar * 4 + beat),
                "duration": 0.25,
                "velocity": 110 if beat in [0, 2] else 100
            })
    return notes

def generate_hihat_pattern(bars: int = 4, open_hat: bool = False) -> list[dict]:
    """Generate 16th note hi-hat pattern."""
    notes = []
    pitch = 46 if open_hat else 42  # Open or Closed hat
    for bar in range(bars):
        for sixteenth in range(16):
            start = bar * 4 + sixteenth * 0.25
            # Skip positions where kick hits for closed hats
            if not open_hat or (sixteenth % 4 == 2):
                notes.append({
                    "pitch": pitch,
                    "start_time": start,
                    "duration": 0.1,
                    "velocity": 80 + (10 if sixteenth % 4 == 0 else 0)
                })
    return notes
```

---

## 4. Mixer Agent

**Role**: Mix Engineer
**Model**: llama3 (Ollama)

### Tools
- `load_device` - Load effect or instrument
- `set_device_parameter` - Adjust device knob
- `set_track_volume` - Adjust track level
- `set_track_pan` - Adjust stereo position

### Device Chains per Track

```python
DEVICE_CHAINS = {
    "kick": [
        {"name": "Drum Sampler", "params": {}},
        {"name": "Channel EQ", "params": {"high_cut": 200}},
        {"name": "Saturator", "params": {"drive": 3.0}},
    ],
    "rumble": [
        {"name": "Reverb", "params": {"decay": 0.6, "dry_wet": 1.0}},
        {"name": "Roar", "params": {"drive": 6.0}},
        {"name": "EQ Eight", "params": {"high_cut": 150}},
        {"name": "Compressor", "params": {"sidechain": True}},
    ],
    "bass": [
        {"name": "Operator", "params": {}},
        {"name": "Channel EQ", "params": {}},
        {"name": "Compressor", "params": {"ratio": 4.0}},
    ],
}
```

### Mixing Rules

| Track | Volume (dB) | Pan | Notes |
|-------|-------------|-----|-------|
| Kick | -6 | C | Reference level |
| Rumble | -12 | C | Sits below kick |
| Bass | -9 | C | Fills between |
| Hats | -18 | L10-R10 | Stereo spread |
| Clap | -12 | C | Slight verb |

---

## 5. Verifier Agent

**Role**: QA Engineer
**Model**: llama3 (Ollama)

### Tools
- `get_session_info` - Query current session state
- `get_track_info` - Query track details
- `get_clip_info` - Query clip notes
- `get_device_parameters` - Query device state

### Verification Tasks

```python
async def verify_project(self) -> dict:
    """Run all boolean success criteria checks."""
    results = {}

    # Check tempo
    session = await self.get_session_info()
    results["IS_BPM_VALID"] = abs(session.tempo - 136.0) < 0.1

    # Check track count
    results["HAS_ALL_TRACKS"] = session.track_count == 16

    # Check kick pattern
    kick_clip = await self.get_clip_info(0, 0)
    results["HAS_KICK_PATTERN"] = (
        len(kick_clip.notes) >= 16 and
        all(n.pitch == 36 for n in kick_clip.notes)
    )

    # Check rumble chain
    rumble_devices = await self.get_track_devices(1)
    device_names = [d.name for d in rumble_devices]
    results["HAS_RUMBLE_CHAIN"] = (
        "Reverb" in device_names and
        ("Roar" in device_names or "Saturator" in device_names)
    )

    return results
```

### Report Format

```
═══════════════════════════════════════════════════════
  I AM MACHINE - Verification Report
═══════════════════════════════════════════════════════
  ✓ IS_BPM_VALID          : 136.0 BPM
  ✓ HAS_ALL_TRACKS        : 16/16 tracks
  ✓ HAS_KICK_PATTERN      : 64 notes, C1
  ✓ HAS_RUMBLE_CHAIN      : Reverb→Roar→EQ→Comp
  ✗ IS_SIDECHAIN_ACTIVE   : Compressor not sidechained
───────────────────────────────────────────────────────
  Score: 4/5 (80%)
═══════════════════════════════════════════════════════
```

---

## 6. Crew Configuration

```python
from crewai import Crew, Process

techno_crew = Crew(
    agents=[
        research_agent,
        composer_agent,
        mixer_agent,
        verifier_agent
    ],
    tasks=[
        research_rumble_task,
        create_kick_task,
        create_rumble_task,
        apply_effects_task,
        verify_task
    ],
    process=Process.sequential,  # Order matters
    verbose=True,
    memory=True,  # Enable mem0 integration
)

# Execute with DearPyGUI progress updates
result = techno_crew.kickoff(
    inputs={"tempo": 136, "key": "F", "scale": "minor"}
)
```

---

## 7. Error Recovery

| Error | Recovery Action |
|-------|-----------------|
| Device not found | Try fallback device (Roar→Saturator) |
| Track limit reached | Delete unused tracks first |
| Connection timeout | Retry with exponential backoff |
| Pattern validation fail | Regenerate with corrected prompt |
