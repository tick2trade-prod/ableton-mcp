# TDD Workflow Summary: 6 New Agents

## Established Pattern

Based on `/Users/alexzh/ableton-mcp/tests/agents/` analysis:

### Test Template
```python
"""Tests for <Agent> - <Purpose>.

Reference: Ableton Manual Section X.Y "Title" (page ZZZ)

TDD Workflow:
- 🔴 RED: Write failing test
- 🟢 GREEN: Implement minimum code to pass
- 🔄 REFACTOR: Clean up with tests as safety net
"""
# Arrange → Act → Assert
# Use mock_mcp_client fixture
# Test success, mock mode, edge cases
```

### Implementation Cycle

For each agent:

1. **🔴 RED**: Write `tests/agents/test_<agent>_agent.py`
   - Run: `uv run pytest tests/agents/test_<agent>_agent.py -v`
   - Expected: FAILED (ImportError or method doesn't exist)

2. **🟢 GREEN**: Implement `scripts/dearpygui_controller/agents/<agent>_agent.py`
   - Inherit from `BaseAgent`
   - Return `AgentResult(success, message, data, errors)`
   - Support mock mode (`if not mcp: return mock result`)
   - Run: `uv run pytest tests/agents/test_<agent>_agent.py -v`
   - Expected: PASSED

3. **🔄 REFACTOR**:
   - Clean up code
   - Add Ableton Manual references
   - Extract utilities
   - Update `conftest.py` if needed

## Agent Priority & Implementation Order

### Phase 1: Critical Path (2-3 days each)

#### 1. Sidechain Agent
**Purpose**: Rumble pumping, sidechain compression routing  
**Blocks**: Track 2 (rumble), Track 10 (ride), Track 15 (risers)  
**Tests**:
- `test_setup_sidechain_kick_to_rumble()` - infinite:1 ratio
- `test_setup_sidechain_preset_patterns()` - kick_pump/rhythmic_duck/gentle_pump
- `test_setup_sidechain_no_mcp_client()` - mock mode

**Key Methods**:
- `setup_sidechain(source_track, target_track, preset, ratio, attack_ms, release)`

---

#### 2. Sampler/Granular Agent
**Purpose**: Vocal FX, slicing, granular synthesis  
**Blocks**: Track 14 (vocal FX), Track 9 (glitch), Track 8 (tribal loops)  
**Tests**:
- `test_load_sample_slice_mode()` - Vocal chop slicing
- `test_setup_granular_synthesis()` - Grain clouds
- `test_random_slice_triggering()` - Glitch percussion
- `test_no_mcp_client()` - mock mode

**Key Methods**:
- `load_sample(track_name, sample_path, mode="slice", slice_count=32)`
- `setup_granular(track_name, grain_size_ms, density, randomize_pitch)`

---

### Phase 2: Workflow Enhancement (1-2 days each)

#### 3. Groove/Quantization Agent
**Purpose**: Swing 16-99, humanization, groove templates  
**Affects**: Tracks 5-10 (percussion), all MIDI tracks  
**Tests**:
- `test_apply_groove_template()` - Swing 16-99 at 10-15% intensity
- `test_set_clip_quantization()` - Strict vs humanized
- `test_velocity_humanization()` - Randomize velocities

**Key Methods**:
- `apply_groove(track_name, clip_index, groove_name, intensity=0.15)`
- `set_quantization(track_name, clip_index, quantize_mode="strict")`

---

#### 4. Return Track Agent
**Purpose**: Reverb/delay sends, spatial FX routing  
**Affects**: All tracks (reverb automation, delay sends)  
**Tests**:
- `test_create_return_track_reverb()` - Load Hybrid Reverb
- `test_set_send_levels()` - Configure send amounts
- `test_automate_send_levels()` - Breakdowns, transitions

**Key Methods**:
- `create_return_track(name, effects=["Reverb", "EQ Eight"])`
- `set_send_level(track_name, return_index, level_db)`

---

### Phase 3: Advanced Features (2-3 days each)

#### 5. Advanced Automation Agent  
**Purpose**: Filter sweeps, parameter envelopes, breakpoint automation  
**Affects**: Track 4 (acid filter), Track 11 (stabs), Track 2 (Roar drive), Track 15 (risers)  
**Tests**:
- `test_create_filter_sweep()` - 200Hz → 15kHz over 16 bars
- `test_create_breakpoint_envelope()` - Custom curves (linear/exp/log)
- `test_record_parameter_automation()` - Live automation writing

**Key Methods**:
- `create_automation_envelope(track_name, device_name, param_name, points=[(time, value)])`
- `create_filter_sweep(track_name, start_freq, end_freq, duration_bars, curve="linear")`

---

#### 6. Browser/Library Agent
**Purpose**: Sound Similarity search, efficient preset loading  
**Affects**: All tracks (sample/preset selection)  
**Tests**:
- `test_search_by_sound_similarity()` - Find optimal 909 kick
- `test_load_core_library_preset()` - Load Dark Hall reverb IR
- `test_browse_by_tags()` - Filter by tags

**Key Methods**:
- `search_browser(query, category="Samples", sound_similarity=True)`
- `load_preset(track_name, device_name, preset_path)`

---

## Testing Plan

### Red/Green/Refactor Cycle

```bash
# For each agent (example: Sidechain Agent)

# 🔴 RED: Write failing test
cat > tests/agents/test_sidechain_agent.py << 'EOF'
# ... test code ...
EOF

uv run pytest tests/agents/test_sidechain_agent.py -v
# Expected: FAILED ❌

# 🟢 GREEN: Implement agent
cat > scripts/dearpygui_controller/agents/sidechain_agent.py << 'EOF'
# ... agent code ...
EOF

uv run pytest tests/agents/test_sidechain_agent.py -v
# Expected: PASSED ✅

# 🔄 REFACTOR: Clean up
# - Extract utilities
# - Add docstrings
# - Update conftest.py
```

### Integration Test

Create `tests/techno/test_i_am_machine.py`:
```python
@pytest.mark.integration
async def test_i_am_machine_16_track_workflow():
    """Verify all 16 tracks can be created with new agents."""
    # Low-End Engine (Tracks 1-4)
    # - Test sidechain: rumble → kick
    
    # Rhythmic Core (Tracks 5-10)
    # - Test groove: Swing 16-99 on hats
    # - Test sampler: glitch percussion slicing
    
    # Harmonics (Tracks 11-14)
    # - Test sampler: vocal FX granular
    # - Test automation: filter sweeps
    
    # FX & Transitions (Tracks 15-16)
    # - Test return tracks: reverb/delay
    # - Test automation: riser sweeps
    
    assert all_tracks_created
    assert sidechain_routing_works
    assert groove_applied
```

### Test Execution Order

```bash
# Individual agent tests
uv run pytest tests/agents/test_sidechain_agent.py -v
uv run pytest tests/agents/test_sampler_agent.py -v  
uv run pytest tests/agents/test_groove_agent.py -v
uv run pytest tests/agents/test_return_track_agent.py -v
uv run pytest tests/agents/test_automation_agent.py -v
uv run pytest tests/agents/test_browser_agent.py -v

# All agent tests
uv run pytest tests/agents/ -v

# Integration test
uv run pytest tests/techno/test_i_am_machine.py -v
```

---

## File Checklist

### Phase 1 (Critical)

#### Sidechain Agent
- [ ] `tests/agents/test_sidechain_agent.py` (RED)
- [ ] `scripts/dearpygui_controller/agents/sidechain_agent.py` (GREEN)
- [ ] Update `scripts/dearpygui_controller/agents/__init__.py` (export)
- [ ] Update `tests/agents/conftest.py` (add sidechain mocks)

#### Sampler/Granular Agent
- [ ] `tests/agents/test_sampler_agent.py` (RED)
- [ ] `scripts/dearpygui_controller/agents/sampler_agent.py` (GREEN)
- [ ] Update `scripts/dearpygui_controller/agents/__init__.py`
- [ ] Update `tests/agents/conftest.py` (add sampler mocks)

### Phase 2 (Medium)

#### Groove Agent
- [ ] `tests/agents/test_groove_agent.py`
- [ ] `scripts/dearpygui_controller/agents/groove_agent.py`

#### Return Track Agent
- [ ] `tests/agents/test_return_track_agent.py`
- [ ] `scripts/dearpygui_controller/agents/return_track_agent.py`

### Phase 3 (Advanced)

#### Automation Agent
- [ ] `tests/agents/test_automation_agent.py`
- [ ] `scripts/dearpygui_controller/agents/automation_agent.py`

#### Browser Agent
- [ ] `tests/agents/test_browser_agent.py`
- [ ] `scripts/dearpygui_controller/agents/browser_agent.py`

### Integration
- [ ] `tests/techno/test_i_am_machine.py` (full 16-track workflow)

---

## Success Criteria

✅ All 6 agents pass individual tests  
✅ Integration test creates all 16 tracks  
✅ Sidechain rumble pumps to kick (manual verification)  
✅ Vocal FX slicing works (manual verification)  
✅ Groove humanization audible (manual verification)  
✅ Return tracks route correctly (manual verification)  
✅ Automation envelopes record smoothly (manual verification)  
✅ Browser loads samples efficiently (manual verification)

---

**Total Estimated Time**: 12-18 days (2-3 weeks)

**Phase 1** (Critical): 5-6 days  
**Phase 2** (Medium): 3-4 days  
**Phase 3** (Advanced): 4-6 days  
**Integration & Polish**: 2-3 days
