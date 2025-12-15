# REVISED TDD Implementation Plan
**Based on**: Agent feedback analysis  
**Status**: Ready for RED Phase

---

## Critical Gaps Fixed

Original plan was **60% complete**. Agent feedback revealed:

❌ **Missing**: Arrangement timeline (arranger_agent)  
❌ **Missing**: Sidechain network (4+ tracks!) (sidechain_agent)  
❌ **Missing**: Roar multiband saturation (effects_chain_agent)  
❌ **Missing**: Modulation matrix (modulation_agent)  
❌ **Missing**: Automation (automation_agent)  
❌ **Missing**: Groove/swing (groove_agent)  
❌ **Missing**: Mix bus (mixer_agent)  
⚠️ **Wrong**: Acid should use Drift, not Operator (synthesizer_agent)

---

## Revised Test Count

| Category | Tests | Agent Responsible |
|----------|-------|-------------------|
| **Unit (Tracks 1-16)** | 450 | sampler, synthesizer, percussion, vocals |
| **Sidechain Network** | 30 | sidechain_agent |
| **Arrangement Timeline** | 50 | arranger_agent |
| **Automation** | 40 | automation_agent |
| **Groove/Humanization** | 20 | groove_agent |
| **Mix Bus/Master** | 40 | mixer_agent, mastering_agent |
| **Modulation Routing** | 20 | modulation_agent |
| **E2E** | 10 | verifier_agent |
| **TOTAL** | **660 tests** | All 20 agents |

---

## Proposed Changes

### New Test Files (RED Phase)

```
tests/i_am_machine_v3/
├── unit/
│   ├── test_track_02_rumble.py (UPDATE: Add Roar tests)
│   ├── test_track_03_sub_bass.py (UPDATE: Add sidechain tests)
│   ├── test_track_04_acid.py (UPDATE: Use Drift, add automation)
│   └── test_track_09_glitch.py (UPDATE: Add modulation matrix)
├── integration/
│   ├── test_sidechain_network.py (NEW!)
│   ├── test_arrangement_timeline.py (NEW!)
│   ├── test_automation_strategy.py (NEW!)
│   └── test_groove_humanization.py (NEW!)
├── mix/
│   ├── test_mix_bus.py (NEW!)
│   ├── test_stereo_imaging.py (NEW!)
│   └── test_headroom.py (NEW!)
└── helpers/
    └── agent_test_generator.py (UPDATE: Use ALL agents)
```

---

## Implementation Steps

### Step 1: Create Test Generation Script
**File**: `scripts/generate_all_tests.py`

Uses agents to generate tests:
- `research_agent`: Extract specs from technical doc
- `verifier_agent`: Generate validation criteria
- `sidechain_agent`: Generate sidechain network tests
- `arranger_agent`: Generate timeline tests  
- `automation_agent`: Generate automation tests
- `groove_agent`: Generate humanization tests

**Command**: `python scripts/generate_all_tests.py`

**Output**: 660 test files (ALL RED)

### Step 2: Verify All Tests Run (and Fail)
**Command**: `pytest tests/i_am_machine_v3/ -v --tb=short`

**Expected**: 660 tests, 660 failures

### Step 3: Implement Track 1 (Kick)
**File**: `live_set/lily_palmer/i_am_machine_v3/tracks/low_end/kick_track.py`

Use `sampler_agent` to:
- Load Kick 909
- Set pitch envelope
- Add EQ Eight
- Add Saturator
- Set bass mono

**Command**: `pytest tests/i_am_machine_v3/unit/test_track_01_kick.py -v`

**Expected**: ~20 tests turn GREEN

### Step 4: Implement Track 2 (Rumble)
**File**: `live_set/lily_palmer/i_am_machine_v3/tracks/low_end/rumble_track.py`

Use `sidechain_agent` + `effects_chain_agent` to:
- Receive from kick
- Add Hybrid Reverb
- **Add Roar multiband** (NEW!)
- Add lowpass
- Configure sidechain

**Command**: `pytest tests/i_am_machine_v3/unit/test_track_02_rumble.py -v`

**Expected**: ~25 tests turn GREEN

### Step 5: Implement Track 3 (Sub Bass) + Sidechain Network
**Files**:
- `live_set/lily_palmer/i_am_machine_v3/tracks/low_end/sub_bass_track.py`
- `live_set/lily_palmer/i_am_machine_v3/helpers/sidechain_network.py`

Use `synthesizer_agent` + `sidechain_agent`:
- Load Operator
- Configure FM
- **Add sidechain to kick** (NEW!)
- Create rolling pattern

**Command**: 
```bash
pytest tests/i_am_machine_v3/unit/test_track_03_sub_bass.py -v
pytest tests/i_am_machine_v3/integration/test_sidechain_network.py -v
```

**Expected**: ~20 unit + 10 integration tests GREEN

### Step 6: Complete All LOW-End Tracks (1-4)

Implement Track 4 (Acid) with:
- **Drift (not Operator!)** (synthesizer_agent)
- Filter modulation (modulation_agent)
- **Automation** (automation_agent)

### Step 7: Implement Arrangement Timeline

**File**: `live_set/lily_palmer/i_am_machine_v3/arrangement/song_structure.py`

Use `arranger_agent`:
- Define 7 sections × 16 bars
- Set active tracks per section
- Intro: Only kick + rumble + hats
- Breakdown1: Remove kick
- Drop1: Full energy

**Command**: `pytest tests/i_am_machine_v3/integration/test_arrangement_timeline.py -v`

**Expected**: ~50 tests GREEN

### Step 8: Implement Automation

Use `automation_agent`:
- Acid filter cutoff automation
- Reverb send automation
- Roar distortion automation

**Command**: `pytest tests/i_am_machine_v3/integration/test_automation_strategy.py -v`

**Expected**: ~40 tests GREEN

### Step 9: Implement Groove/Humanization

Use `groove_agent`:
- Apply Swing 16-99 to hats/ride
- Keep kick quantized
- Set groove amount 10-15%

**Command**: `pytest tests/i_am_machine_v3/integration/test_groove_humanization.py -v`

**Expected**: ~20 tests GREEN

### Step 10: Complete All 16 Tracks

Continue until all track tests pass.

### Step 11: Implement Mix Bus

Use `mixer_agent` + `mastering_agent`:
- Glue compressor
- Mid/Side EQ
- Roar (mastering config)
- Limiter

**Command**: `pytest tests/i_am_machine_v3/mix/ -v`

**Expected**: ~40 tests GREEN

### Step 12: E2E Full Song Test

**Command**: `pytest tests/i_am_machine_v3/e2e/test_full_song.py -v`

**Expected**: All 10 E2E tests GREEN

---

## Verification Plan

### Automated Tests
All 660 pytest tests must pass:
```bash
pytest tests/i_am_machine_v3/ -v
```

### Manual Verification in Ableton

1. **Low-End Check**:
   - Play intro (bars 1-16)
   - Listen for kick punch
   - Listen for rumble pump (sidechain ducking)
   - Listen for FM bass rolling 16ths
   - **Check**: No frequency masking

2. **Arrangement Check**:
   - Scrub through all 7 sections
   - **Intro** (bars 1-16): Only kick, rumble, hats
   - **Breakdown1** (bars 33-48): Kick removed
   - **Drop1** (bars 49-64): All elements firing

3. **Automation Check**:
   - Watch acid filter cutoff automate
   - Filter opens before drops
   - Filter closes during drops

4. **Groove Check**:
   - Solo hi-hats
   - Listen for subtle swing (not robotic)
   - Kick stays quantized (tight)

### Spectrum Analysis

Use `verifier_agent.configure_spectrum_analyzer()`:
- Check kick fundamental @ ~43Hz
- Check no frequency masking
- Check stereo width

---

## Dependencies

- Ableton Live 12 with:
  - 909 Core Kit
  - Roar device
  - Drift synthesizer
  - Hybrid Reverb
- Python 3.11+
- pytest
- MCP server running

---

## Success Criteria

### RED Phase Complete
✅ 660 tests written  
✅ All tests run without syntax errors  
✅ All 660 tests fail initially (RED)  
✅ Test generation script uses all 20 agents

### GREEN Phase Milestone 1
✅ Tracks 1-3 (kick, rumble, sub bass): All tests pass  
✅ Sidechain network: Integration test passes  
✅ Intro section: Sounds like the spec

### GREEN Phase Complete
✅ All 16 tracks: Unit tests pass (450 tests)  
✅ Arrangement: Timeline test passes (50 tests)  
✅ Automation: All automation tests pass (40 tests)  
✅ Groove: Humanization tests pass (20 tests)  
✅ Mix bus: Master chain tests pass (40 tests)  
✅ E2E: Full song test passes (10 tests)  
✅ **Total: 660/660 tests GREEN** ✅

---

## Risk Mitigation

1. **Risk**: Roar not available in user's edition  
   **Mitigation**: Test with `effects_chain_agent.test_roar_availability()` first

2. **Risk**: Drift not available  
   **Mitigation**: `synthesizer_agent` has fallback to Operator

3. **Risk**: Automation API not working  
   **Mitigation**: Manual breakpoint entry in Ableton as backup

4. **Risk**: Context loss during implementation  
   **Mitigation**: 660 RED tests = permanent roadmap!

---

## Timeline

**Week 1**: RED Phase (write all tests)  
**Week 2-3**: GREEN Phase (implement)  
**Week 4**: REFACTOR Phase (optimize)

**Total**: ~4 weeks to complete full song
