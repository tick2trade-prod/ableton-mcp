# Agent Gap Analysis: I Am Machine (16 Tracks)

## Executive Summary

**Objective**: Recreate Lily Palmer's "I Am Machine" using MCP agents  
**Current State**: 14 agents implemented  
**Required**: 6 additional specialized agents  
**Critical Blockers**: Sidechain Agent, Sampler/Granular Agent

## Quick Reference: Missing Agents

| Agent | Priority | Reason | Blocks Tracks |
|-------|----------|--------|---------------|
| **Sidechain Agent** | 🔴 HIGH | Rumble pumping (essential techno technique) | 2, 10, 15 |
| **Sampler/Granular Agent** | 🔴 HIGH | Vocal FX, glitches, slicing | 14, 9, 8 |
| **Groove/Quantization Agent** | 🟡 MEDIUM | Humanization, swing templates | 5-10 |
| **Return Track Agent** | 🟡 MEDIUM | Reverb/delay sends, spatial FX | All |
| **Advanced Automation Agent** | 🟡 MEDIUM | Filter sweeps, dynamic changes | 4, 11, 2, 15 |
| **Browser/Library Agent** | 🟢 LOW | Efficient sample/preset loading | All |

## Track-to-Agent Mapping

### ✅ Fully Covered Tracks

| Track | Instrument | Existing Agent |
|-------|------------|----------------|
| 1 | Anchor Kick (Drum Sampler) | `percussion_agent.py` |
| 3 | FM Rolling Bass (Operator) | `synthesizer_agent.py` |
| 4 | 303 Acid Line (Drift) | `synthesizer_agent.py` |
| 6 | Open Hi-Hats (Drum Sampler) | `percussion_agent.py` |
| 7 | Clap/Snare (Drum Rack) | `percussion_agent.py` |
| 11 | Synth Stab (Wavetable) | `synthesizer_agent.py` |
| 13 | Lead Vocal | `vocals_agent.py` |

### ⚠️ Partially Covered Tracks (Need Enhancement)

| Track | Instrument | Current Agent | Missing Capability |
|-------|------------|---------------|-------------------|
| 2 | Industrial Rumble | `effects_chain_agent.py` | ❌ Sidechain to kick |
| 9 | Glitch Percussion (Meld) | `sound_design_agent.py` | ❌ Random slice triggering |
| 12 | Atmospheric Drone (Meld) | `sound_design_agent.py` | ✅ Covered |
| 14 | Vocal FX/Glitches | `vocals_agent.py` | ❌ Granular synthesis, slicing |

### ❌ Workflow Gaps

| Requirement | Description | Impact |
|-------------|-------------|--------|
| **Sidechain Routing** | Rumble, pads, risers duck to kick | High - defines techno "pump" |
| **Groove Templates** | Swing 16-99 on hi-hats | Medium - adds humanization |
| **Return Tracks** | Reverb/delay sends | Medium - spatial mixing |
| **Parameter Automation** | Filter sweeps, drive changes | Medium - dynamics & tension |
| **Sample Browser** | Sound Similarity search | Low - workflow speed |

## Phase 1 Agents (Critical - Start Here)

### 1. Sidechain Agent 🔴

**What it does**: Automates sidechain compression routing for techno pumping effect.

**Key Features**:
- Configure Compressor with sidechain input
- Preset patterns: kick sidechain (infinite:1), rhythmic ducking
- Support multiple targets (rumble, pads, risers, leads)

**Example Usage**:
```python
sidechain_agent = SidechainAgent(session)

# Track 2 rumble sidechained to Track 1 kick
await sidechain_agent.setup_sidechain(
    source_track="01 - Kick",
    target_track="02 - Rumble",
    ratio="infinite:1",
    attack_ms=0.1,
    release="1/8n"  # Synced to tempo
)

# Track 10 ride moderate sidechain
await sidechain_agent.setup_sidechain(
    source_track="01 - Kick",
    target_track="10 - Ride",
    ratio="4:1",
    attack_ms=5,
    release="1/16n"
)
```

**Affects Tracks**: 2 (rumble), 10 (ride), 15 (risers), 12 (pad), 11 (stabs)

---

### 2. Sampler/Granular Agent 🔴

**What it does**: Advanced sample manipulation, slicing, granular synthesis.

**Key Features**:
- Load samples into Sampler/Simpler
- Configure slice mode for vocal chops
- Set up Granulator III for grain clouds
- Random slice triggering for glitch percussion

**Example Usage**:
```python
sampler_agent = SamplerAgent(session)

# Track 14: Vocal FX with slicing
await sampler_agent.load_sample(
    track_name="14 - Vocal FX",
    sample_path="/path/to/vocal.wav",
    mode="slice",
    slice_count=32
)

# Track 9: Glitch percussion random slices
await sampler_agent.setup_granular(
    track_name="09 - Glitch",
    grain_size_ms=50,
    density=0.7,
    randomize_pitch=True
)
```

**Affects Tracks**: 14 (vocal FX), 9 (glitch percussion), 8 (tribal loops)

## Implementation Recommendations

### Start Order
1. **Sidechain Agent** (2-3 days) - Most impactful, well-defined scope
2. **Sampler/Granular Agent** (3-4 days) - Complex but essential
3. **Groove Agent** (1-2 days) - Simple, high value
4. **Return Track Agent** (2 days) - Workflow improvement
5. **Automation Agent** (3 days) - May extend existing `arranger_agent.py`
6. **Browser Agent** (2 days) - Nice to have

### Testing Strategy (TDD)
For each agent:
1. ✅ **Red**: Write failing test in `tests/agents/test_<agent>_agent.py`
2. ✅ **Green**: Implement minimum code to pass
3. ✅ **Refactor**: Clean up, add docstrings, edge cases

### Integration Test
Create `tests/techno/test_i_am_machine.py`:
```python
@pytest.mark.integration
async def test_complete_i_am_machine_workflow():
    """Verify all 16 tracks can be created end-to-end"""
    # Test Low-End Engine (1-4)
    # Test Rhythmic Core (5-10) 
    # Test Harmonics (11-14)
    # Test FX & Transitions (15-16)
    # Verify sidechain routing works
    # Verify groove applied correctly
    # Verify automation recorded
```

## Resources for Implementation

### Ableton Manual (Embedded in Redis)
- Chapter 14.1: Groove Pool
- Chapter 24.4: Chain List (rack routing)
- Chapter 34.3: Simpler/Sampler slicing
- Chapter 40: Automation envelopes

### External References
- [Making A Techno Rumble Kick](https://www.studiobrootle.com/making-a-techno-rumble-kick-in-ableton-live-step-by-step/)
- [MusicRadar: Rumbling Techno Kick Guide](https://www.musicradar.com/how-to/rumbling-techno-kick)
- [Ableton Drum Sampler Tutorial](https://www.pushpatterns.com/blog/AbletonLive12DrumSampler)

## Success Metrics

- [ ] All 16 tracks can be created programmatically
- [ ] Sidechain routing confirmed in Ableton
- [ ] Groove templates apply correctly
- [ ] Automation curves recorded smoothly
- [ ] Integration test passes end-to-end
- [ ] Manual verification in Ableton shows pumping rumble

---

**Next Step**: Review this analysis and approve Phase 1 agents for implementation.
