# 0001: Rack Chain Tools

| Field | Value |
|-------|-------|
| Branch | `feature/0001-rack-chain-tools` |
| PR | #50 (GitHub), MR pending (GitLab) |
| Status | ✅ All 38 Tests Passing |

---

## Objective
Complete integration test coverage for all MCP tools before PR submission.
All tests run against **live Ableton DAW** - no mocks.

## Prerequisites
- [x] Ableton Live running with AbletonMCP control surface
- [x] `make test-connection` passes
- [x] `pytest` and dependencies installed

---

## Test Checklist (38 Tests Total)

### Session & Track Tools (7 tests)
- [x] `test_get_session_info`
- [x] `test_get_track_info`
- [x] `test_create_midi_track`
- [x] `test_set_track_name`
- [x] `test_set_track_volume`
- [x] `test_set_master_volume`
- [x] `test_set_tempo`

### Clip Tools (6 tests)
- [x] `test_create_clip`
- [x] `test_add_notes_to_clip`
- [x] `test_set_clip_name`
- [x] `test_duplicate_clip`
- [x] `test_empty_clip_slot`
- [x] `test_relocate_clip`

### Transport Tools (4 tests)
- [x] `test_fire_clip`
- [x] `test_stop_clip`
- [x] `test_start_playback`
- [x] `test_stop_playback`

### Device & Rack Tools (7 tests) - NEW
- [x] `test_create_audio_effect_rack`
- [x] `test_create_audio_effect_rack_appends`
- [x] `test_create_audio_effect_rack_at_index`
- [x] `test_create_rack_chain`
- [x] `test_load_effect_to_chain`
- [x] `test_get_device_parameters`
- [x] `test_set_device_parameter`

### Device in Chain Tests (3 tests) - NEW
- [x] `test_get_device_parameters_in_chain`
- [x] `test_set_device_parameter_in_chain`
- [x] `test_load_effect_on_master`

### Browser Tools (6 tests)
- [x] `test_get_browser_tree`
- [x] `test_get_browser_tree_audio_effects`
- [x] `test_get_browser_tree_instruments`
- [x] `test_get_browser_items_at_path`
- [x] `test_load_instrument_or_effect`
- [x] `test_load_drum_kit`

---

## Infrastructure Added

### Testing
- [x] `tests/conftest.py` - Ableton socket fixture
- [x] `tests/test_tools.py` - 27 general tool tests
- [x] `tests/test_rack_chain_tools.py` - 11 branch-specific tests
- [x] Pytest markers: `live`, `session`, `clip`, `device`, `browser`, `transport`

### Development Tooling
- [x] `Makefile` with test commands
- [x] `.pre-commit-config.yaml` - linting + conventional commits
- [x] `pyproject.toml` - dev dependencies + pytest config

### Conventions
- [x] Conventional commits (`feat:`, `fix:`, `test:`, etc.)
- [x] Conventional branch naming (`feature/<id>-<slug>`)
- [x] Spec file system (`.gemini/specs/NNNN-<slug>.md`)
- [x] Spec index (`.gemini/SPECS.md`)

---

## PR Submission Criteria
- [x] All 38 tool tests passing
- [x] Tests run against live Ableton (no mocks)
- [x] Conventional commits used
- [x] `make test-connection` documents connection requirement
- [ ] Create MR on GitLab
- [ ] Merge to main
