# Project Catalog & V3 Strategy
**Branch**: `feature/0010-large-import-agents-1214`  
**Date**: 2025-12-14  

## TRUE Objective

**Ultimate Goal**: Recreate the ENTIRE "I Am Machine - Lily Palmer" song  
**Strategy**: Break into 16-bar milestones, building iteratively

### Milestone 1: First 16 Bars (Intro) 
**Focus**: Low-End Engine - Get these PERFECT first
- Track 1: Kick (909, 43Hz, tight decay)
- Track 2: Rumble (sidechained reverb tail from kick)  
- Track 3: Sub Bass (FM synthesis, rolling 16ths)

**Then**: Add remaining intro elements (hats, percussion)

### Future Milestones
- Milestone 2: Development section (bars 17-32)
- Milestone 3: Breakdown 1
- Milestone 4: Drop 1
- ... continue until full song complete

---

## V2 vs V3 Decision

### Why NOT Continue V2?

**V2 Problems**:
- ❌ Bulk approach (all 16 tracks at once)
- ❌ Generic content, not "I Am Machine" specific
- ❌ Can't iterate on individual tracks
- ❌ No agent integration
- ❌ Hard to validate against detailed spec

**V2 Value**:
- ✅ Proved 909 Core Kit works
- ✅ Proved MCP integration works
- ✅ Can reference for infrastructure patterns

### Why V3 (RECOMMENDED) ✅

**V3 Approach**:
- ✅ **One track at a time** - focus deeply on each
- ✅ **Agent-based** - leverage 20 specialized agents
- ✅ **Spec-driven** - follows technical document exactly
- ✅ **Iterative** - perfect kick → add rumble → add sub bass
- ✅ **Testable** - validate each layer independently
- ✅ **Milestone-based** - clear progress tracking

---

## V3 Implementation Plan

### Phase 1a: Low-End Foundation (Days 1-3)

#### Track 1: The Anchor Kick
**Agent**: `sampler_agent`  
**Spec**: Section 3, Track 1
```python
# live_set/lily_palmer/i_am_machine_v3/milestone_01/track_01_kick.py
from scripts.dearpygui_controller.agents.sampler_agent import SamplerAgent

kick = SamplerAgent(mcp_client)
kick.load_sample("Kick 909.aif")  
kick.set_pitch_envelope(amount=18, decay=15)  # Creates transient click
kick.add_eq_eight(hp_freq=30, notch_freq=200)
kick.add_saturator(mode="analog_clip", drive=3)
kick.set_bass_mono(freq=120)
```

**Validation**:
- ✅ Fundamental @ ~43Hz (F1)
- ✅ Transient click @ 2-5kHz
- ✅ Decay < 350ms
- ✅ Mono below 120Hz

#### Track 2: Industrial Rumble 
**Agent**: `sidechain_agent` + `effects_chain_agent`  
**Spec**: Section 3, Track 2
```python
# track_02_rumble.py
from scripts.dearpygui_controller.agents.sidechain_agent import SidechainAgent
from scripts.dearpygui_controller.agents.effects_chain_agent import EffectsChainAgent

rumble = SidechainAgent(mcp_client)
rumble.receive_from_track(1)  # Get kick signal
rumble.add_hybrid_reverb(decay=1.2, predelay=10, mix=100)
rumble.add_roar_multiband(
    low_band="tube",
    mid_band="diode", 
    feedback=15
)
rumble.add_lowpass(freq=150)
rumble.sidechain_to_kick(ratio="inf:1", attack=0.1, release="1/8")
```

**Validation**:
- ✅ Pumps with kick (infinite sidechain)
- ✅ Industrial texture (Roar feedback)
- ✅ Contained below 150Hz
- ✅ Creates "wall of sound"

#### Track 3: FM Rolling Bass
**Agent**: `synthesizer_agent`  
**Spec**: Section 3, Track 3
```python
# track_03_sub_bass.py  
from scripts.dearpygui_controller.agents.synthesizer_agent import SynthesizerAgent

bass = SynthesizerAgent(mcp_client)
bass.load_operator()
bass.set_fm_algorithm(1)  # Vertical stack
bass.configure_carrier(wave="sine", decay=600)
bass.configure_modulator(wave="sine", coarse=2, velocity_mod=True)
bass.set_filter(cutoff_env=40, decay=300)
bass.create_rolling_pattern(key="F_minor", rhythm="16th_offbeat")
bass.sidechain_to_kick()
```

**Validation**:
- ✅ F Minor scale
- ✅ 16th note rolling rhythm
- ✅ Plucky attack (300ms filter decay)
- ✅ Interlocks with rumble

### Phase 1b: Complete Intro (Days 4-5)

Add tracks 5-8 (hats, claps, toms, glitch) using:
- `percussion_agent`
- `modulation_agent` (for glitch)

### Phase 1c: Validation & Mix (Day 6)

Use `verifier_agent` to check against spec:
- Low-end phase coherence
- Frequency spectrum (kick+rumble+bass no masking)
- Groove pocket (sidechain pumping)
