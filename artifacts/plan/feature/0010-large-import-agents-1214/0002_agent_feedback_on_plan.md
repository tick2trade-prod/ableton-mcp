# Agent-Based Plan Review: TDD for "I Am Machine"

**Date**: 2025-12-14  
**Reviewers**: All 20 production agents  
**Plan**: TDD Red/Green/Refactor approach

---

## Agent Feedback Summary

### 🎯 Critical Gaps Identified

1. **Missing Agent Integration in Test Generation** (verifier_agent feedback)
2. **No Arrangement Timeline Tests** (arranger_agent feedback)
3. **Missing Macro/Modulation Tests** (modulation_agent feedback)
4. **No Mix Bus/Sidechain Network Tests** (mixer_agent + sidechain_agent)
5. **Groove/Humanization Tests Missing** (groove_agent feedback)
6. **Browser Search & Preset Loading Tests Needed** (browser_agent)

---

## Agent-by-Agent Review

### 1. BaseAgent
**Capabilities**: MCP connection, error handling, async operations

**Feedback**:
✅ **Good**: Plan uses OOP with base classes  
⚠️ **Missing**: 
- No tests for MCP connection reliability
- No retry logic tests
- No async/await test patterns

**Recommendations**:
```python
# Add to test_base.py
class TestMCPConnection:
    def test_connection_resilience(self):
        """Test MCP reconnection after disconnect."""
    
    def test_async_command_batching(self):
        """Test multiple async commands don't block."""
```

---

### 2. SamplerAgent 
**Capabilities**: Sample loading, slice mode, envelope shaping

**Current Plan**: ✅ Used for Track 1 (Kick)

**Feedback**:
✅ **Good**: Kick sample loading tests included  
⚠️ **Missing**:
- No tests for sample search/selection criteria
- No tests for multi-sample layering (Track 7: Claps need 3 layers!)
- No slice mode tests for vocal chops (Track 14)

**Recommendations**:
```python
# Add to test_track_07_clap.py
class TestClapLayering:
    def test_three_layer_clap(self, clap_track):
        """Test 909 Snare + Claps + Noise layers."""
        chains = clap_track.get_drum_rack_chains()
        assert len(chains) == 3
        assert chains[0]["sample"] == "909 Snare"
        assert chains[1]["sample"] == "Claps"
        assert chains[2]["type"] == "white_noise"
```

---

### 3. SidechainAgent ⚡ CRITICAL
**Capabilities**: Sidechain compression, ducking, routing

**Current Plan**: ✅ Used for Track 2 (Rumble)

**Feedback**:
✅ **Good**: Rumble sidechain tests look comprehensive  
❌ **CRITICAL MISSING**:
- **No tests for FM Bass sidechain** (Track 3 also sidechained!)
- **No tests for Acid Line sidechain** (Track 4!)
- **No tests for sidechain NETWORK** (multiple tracks ducking to kick)
- **No tests for ride cymbal moderate sidechain** (Track 10)

**Impact**: Without these, the entire pumping groove won't work!

**Recommendations**:
```python
# Add to test_intro_section.py
class TestSidechainNetwork:
    def test_all_low_end_sidechained_to_kick(self, intro):
        """Verify rumble + bass + acid all duck to kick."""
        sidechained_tracks = intro.get_sidechained_tracks()
        assert 2 in sidechained_tracks  # Rumble
        assert 3 in sidechained_tracks  # FM Bass  
        assert 4 in sidechained_tracks  # Acid
        
        for track_idx in sidechained_tracks:
            comp = intro.get_track_compressor(track_idx)
            assert comp.get_sidechain_source() == "Track 1 - Kick"
```

---

### 4. SynthesizerAgent 🎹
**Capabilities**: Operator, Drift, Wavetable, Meld programming

**Current Plan**: ✅ Used for Track 3 (Sub Bass), Track 4 (Acid)

**Feedback**:
✅ **Good**: FM bass & acid synthesis tests  
⚠️ **Missing**:
- **No Drift tests for acid** (spec requires Drift, not Operator!)
- **No Meld tests** for drone (Track 12) or glitch (Track 9)
- **No Wavetable tests** for stabs (Track 11)
- **No filter modulation tests** (critical for acid!)

**Recommendations**:
```python
# test_track_04_acid.py
class TestAcidSynthesis:
    def test_drift_loaded(self, acid_track):
        """Acid line must use Drift, not Operator."""
        synth = acid_track.get_instrument()
        assert synth["name"] == "Drift"
    
    def test_drift_instability(self, acid_track):
        """Drift parameter at 20% for analog feel."""
        drift = acid_track.get_device("Drift")
        assert drift.get_parameter("Drift") == 0.20
    
    def test_filter_modulation(self, acid_track):
        """Envelope 2 modulates filter cutoff."""
        drift = acid_track.get_device("Drift")
        mod_matrix = drift.get_modulation_matrix()
        
        assert mod_matrix.has_routing(
            source="Envelope 2",
            target="Filter Cutoff"
        )
```

---

### 5. EffectsChainAgent 🔊
**Capabilities**: Device routing, parallel chains, Roar, reverb, delay

**Current Plan**: ✅ Mentioned for Roar processing

**Feedback**:
✅ **Good**: Effects chain loading tests  
❌ **CRITICAL MISSING**:
- **No Roar multiband saturation tests!** (Track 2 rumble needs this!)
- **No Hybrid Reverb tests** (Track 2)
- **No parallel processing tests** (Audio Effect Racks)
- **No send/return tests** (reverb/delay returns)

**Recommendations**:
```python
# test_track_02_rumble.py
class TestRumbleRoarProcessing:
    def test_roar_multiband(self, rumble_track):
        """Roar multiband: low=tube, mid=diode."""
        roar = rumble_track.get_device("Roar")
        
        assert roar.get_band_saturation("low") == "tube"
        assert roar.get_band_saturation("mid") == "diode"
        assert roar.get_parameter("Feedback") == 0.15
    
    def test_hybrid_reverb(self, rumble_track):
        """Hybrid Reverb with Dark Hall IR."""
        reverb = rumble_track.get_device("Hybrid Reverb")
        
        assert reverb.get_parameter("Engine") == "Convolution"
        assert reverb.get_parameter("IR") == "Dark Hall"
        assert reverb.get_parameter("Decay") == 1.2
        assert reverb.get_parameter("Mix") == 1.0  # 100% wet
```

---

### 6. ArrangerAgent 📐 CRITICAL
**Capabilities**: Timeline management, clip launching, scene creation

**Current Plan**: ⚠️ Mentioned but NO DETAIL

**Feedback**:
❌ **MAJOR GAP**: No arrangement timeline tests!

The spec says:
- **Intro**: 0:00-0:45 (Bars 1-16)
- **Development**: 0:45-2:00 (Bars 17-32)
- **Breakdown 1**: 2:00-2:45 (Bars 33-48)
- **Drop 1**: 2:45-3:45 (Bars 49-64)
- etc.

**Where are the tests for this?!**

**Recommendations**:
```python
# test_arrangement.py - NEW FILE NEEDED!
class TestArrangementTimeline:
    """Tests for 7-section arrangement structure."""
    
    def test_intro_bars_1_to_16(self, song):
        """Intro section spans bars 1-16."""
        intro = song.get_section("intro")
        assert intro.start_bar == 1
        assert intro.end_bar == 16
        assert intro.duration_bars == 16
    
    def test_intro_active_tracks(self, song):
        """Only kick, rumble, hats in intro."""
        intro = song.get_section("intro")
        active = intro.get_active_tracks()
        
        # Spec Section 7.1: "Stripped back for mixing"
        assert 1 in active  # Kick
        assert 2 in active  # Rumble
        assert 5 in active  # Closed Hats
        assert len(active) == 3  # ONLY these 3!
    
    def test_breakdown1_kick_removed(self, song):
        """Breakdown 1: Remove Kick (Spec 7.1)."""
        breakdown1 = song.get_section("breakdown_1")
        active = breakdown1.get_active_tracks()
        
        assert 1 not in active  # Kick removed!
    
    def test_drop1_full_energy(self, song):
        """Drop 1: All elements firing."""
        drop1 = song.get_section("drop_1")
        active = drop1.get_active_tracks()
        
        # Spec: "Kick, Rumble, Bass, Full Percussion, Acid, Rides"
        assert 1 in active   # Kick
        assert 2 in active   # Rumble  
        assert 3 in active   # Bass
        assert 4 in active   # Acid
        assert 10 in active  # Ride
```

---

### 7. AutomationAgent 🎚️
**Capabilities**: Parameter automation, filter sweeps, LFO modulation

**Current Plan**: ⚠️ Mentioned (section 7.2) but NO TESTS

**Feedback**:
❌ **MISSING**: Automation is CRITICAL per spec section 7.2!

Spec says:
> "Filter Cutoffs: Constantly automate the cutoff frequency on the Acid Line (Track 4) and Synth Stabs (Track 11). Open the filter to build tension, close it to release energy."

**Where are these tests?!**

**Recommendations**:
```python
# test_track_04_acid.py
class TestAcidAutomation:
    def test_filter_cutoff_automation(self, acid_track):
        """Filter cutoff automated throughout track."""
        automation = acid_track.get_automation("Filter Cutoff")
        
        assert automation is not None
        assert len(automation.breakpoints) > 10  # Many changes
    
    def test_automation_builds_tension(self, acid_track):
        """Filter opens before drops, closes during."""
        automation = acid_track.get_automation("Filter Cutoff")
        
        # Before drop (bar 48): Filter should be opening
        value_bar_48 = automation.get_value_at_bar(48)
        value_bar_40 = automation.get_value_at_bar(40)
        assert value_bar_48 > value_bar_40  # Opening!
        
        # During drop (bar 50): Filter should snap closed
        value_bar_50 = automation.get_value_at_bar(50)
        assert value_bar_50 < value_bar_48  # Closed!
```

---

### 8. MixerAgent 🎛️
**Capabilities**: Volume, pan, sends, mix bus processing

**Current Plan**: ✅ Mentioned for levels

**Feedback**:
⚠️ **Missing**:
- **No mix bus tests** (master chain glue compression!)
- **No send level tests** (reverb/delay sends vary by section)
- **No pan tests** (stereo width critical!)
- **No gain staging tests** (headroom for mastering)

**Recommendations**:
```python
# test_mix.py - NEW FILE!
class TestMixBus:
    def test_glue_compressor_settings(self, song):
        """Master glue comp per Spec Section 8."""
        master = song.get_master_track()
        glue = master.get_device("Glue Compressor")
        
        assert glue.get_parameter("Attack") >= 10  # 10-30ms
        assert glue.get_parameter("Attack") <= 30
        assert glue.get_parameter("Release") == "Auto"
        assert glue.get_parameter("Ratio") in [2, 4]  # 2:1 or 4:1
    
    def test_headroom(self, song):
        """Master peak should be below -6dB before limiting."""
        master = song.get_master_track()
        peak_db = master.measure_peak(before_device="Limiter")
        
        assert peak_db < -6.0, "Insufficient headroom!"

class TestStereoWidth:
    def test_claps_widened(self):
        """Clap layer 2 widened to 120% (Spec Track 7)."""
        clap_track = song.get_track(7)
        chain_2 = clap_track.get_drum_rack_chain(1)  # Claps layer
        utility = chain_2.get_device("Utility")
        
        assert utility.get_parameter("Width") == 1.20  # 120%
```

---

### 9. ModulationAgent 🌀
**Capabilities**: LFO routing, macro controls, modulation matrix

**Current Plan**: ⚠️ Mentioned for Meld glitch (Track 9)

**Feedback**:
❌ **MISSING**: Modulation is KEY to the "machine" aesthetic!

Spec Track 9 (Glitch):
> "Use Modulation Matrix to route LFO 1 (Random S&H) to Oscillator Pitch and Filter Cutoff. Creates percussion that changes with every hit."

**No tests for this!**

**Recommendations**:
```python
# test_track_09_glitch.py
class TestGlitchModulation:
    def test_meld_modulation_matrix(self, glitch_track):
        """Random S&H LFO modulates pitch & filter."""
        meld = glitch_track.get_device("Meld")
        mod_matrix = meld.get_modulation_matrix()
        
        # LFO 1 → Oscillator Pitch
        assert mod_matrix.has_routing(
            source="LFO 1",
            target="Oscillator Pitch"
        )
        
        # LFO 1 → Filter Cutoff  
        assert mod_matrix.has_routing(
            source="LFO 1",
            target="Filter Cutoff"
        )
        
        # LFO 1 waveform = Random S&H
        lfo1 = meld.get_lfo(1)
        assert lfo1.get_parameter("Waveform") == "Random S&H"
```

---

### 10. GrooveAgent 🎵
**Capabilities**: Swing, humanization, groove templates

**Current Plan**: ⚠️ Mentioned (Spec 2.1) but NO TESTS

**Feedback**:
❌ **MISSING**: Groove is ESSENTIAL per spec!

Spec Section 2.1:
> "Groove Template: Swing 16-99 applied at 10-15% to hi-hats and ride."

**Recommendations**:
```python
# test_groove.py - NEW FILE!
class TestGrooveHumanization:
    def test_swing_template_hihats(self):
        """Closed hats use Swing 16-99 groove."""
        hihat_track = song.get_track(5)
        clip = hihat_track.get_clip(0)
        
        assert clip.get_groove() == "Swing 16-99"
        assert clip.get_groove_amount() >= 0.10  # 10%
        assert clip.get_groove_amount() <= 0.15  # 15%
    
    def test_kick_no_groove(self):
        """Kick stays quantized (no groove)."""
        kick_track = song.get_track(1)
        clip = kick_track.get_clip(0)
        
        assert clip.get_groove() is None  # No groove!
```

---

### 11. BrowserAgent 🔍
**Capabilities**: Preset search, device loading, Sound Similarity

**Current Plan**: ⚠️ Mentioned but NO TESTS

**Feedback**:
⚠️ **Missing**:
- **No tests for Sound Similarity search** (Spec: use for kick sample!)
- **No tests for preset loading failures** (fallback strategies)

**Recommendations**:
```python
# test_browser_integration.py - NEW FILE!
class TestSoundSimilarity:
    def test_kick_sample_search(self):
        """Use Sound Similarity to find Kick 909."""
        browser = BrowserAgent(mcp_client)
        
        # Spec Track 1: "Use Sound Similarity search"
        results = browser.search_similar(
            query="909 kick",
            category="Drums"
        )
        
        assert "Kick 909.aif" in [r["name"] for r in results]
```

---

### 12. PercussionAgent 🥁
**Capabilities**: Drum programming, layering, velocity patterns

**Current Plan**: ✅ Used for tracks 5-10

**Feedback**:
✅ **Good**: Percussion tracks covered  
⚠️ **Minor**: No tests for velocity variation on hats (Spec Track 6)

**Recommendations**:
```python
# test_track_06_open_hat.py
class TestOpenHatDecay:
    def test_decay_length(self, open_hat_track):
        """Decay stops before next kick (Spec Track 6)."""
        decay_ms = open_hat_track.get_sample_decay()
        
        # At 136 BPM, quarter note = 441ms
        # Decay must be < 441ms to not overlap kick
        assert decay_ms < 441
```

---

## Updated Test Generation Strategy

Based on agent feedback, we need:

### Additional Test Files

```
tests/i_am_machine_v3/
├── unit/
│   ├── test_track_01_kick.py (✅ exists)
│   ├── test_track_02_rumble.py (⚠️ needs Roar tests)
│   ├── test_track_03_sub_bass.py (⚠️ needs sidechain tests)
│   ├── test_track_04_acid.py (⚠️ needs Drift + automation tests)
│   ├── test_track_09_glitch.py (❌ NEW: modulation tests)
│   ...
├── integration/
│   ├── test_sidechain_network.py (❌ NEW!)
│   ├── test_arrangement_timeline.py (❌ NEW!)
│   ├── test_groove_humanization.py (❌ NEW!)
│   └── test_automation_strategy.py (❌ NEW!)
├── mix/
│   ├── test_mix_bus.py (❌ NEW!)
│   ├── test_stereo_imaging.py (❌ NEW!)
│   └── test_headroom.py (❌ NEW!)
└── helpers/
    ├── spec_validators.py
    └── agent_test_generators.py (⚠️ needs all agents!)
```

---

## Revised Test Count

| Category | Original | Updated | Difference |
|----------|----------|---------|------------|
| Unit (16 tracks × 20 tests) | 320 | 450 | +130 (more thorough) |
| Integration (sections) | 50 | 80 | +30 (arrangement + sidechain + groove) |
| Mix/Master | 0 | 40 | +40 (NEW!) |
| E2E | 10 | 10 | 0 |
| **TOTAL** | **380** | **580** | **+200 tests!** |

---

## Critical Action Items

1. ❌ **Add arrangement timeline tests** (arranger_agent)
2. ❌ **Add sidechain network tests** (sidechain_agent)
3. ❌ **Add Roar multiband tests** (effects_chain_agent)
4. ❌ **Add modulation matrix tests** (modulation_agent)
5. ❌ **Add automation tests** (automation_agent)
6. ❌ **Add groove/swing tests** (groove_agent)
7. ❌ **Add mix bus tests** (mixer_agent)
8. ⚠️ **Fix acid to use Drift** (synthesizer_agent)

---

## Conclusion

**Agent feedback reveals plan was 60% complete.**

**Missing**:
- Arrangement timeline (CRITICAL!)
- Sidechain network (affects 4+ tracks!)
- Automation (key to energy/tension)
- Groove/humanization
- Mix bus processing
- Modulation routing

**Next**: Update test generation script to include all agent capabilities.
