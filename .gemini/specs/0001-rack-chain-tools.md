# 0001: Rack Chain Tools

| Field | Value |
|-------|-------|
| Branch | `feature/rack-chain-tools` |
| PR | #50 |
| Status | ✅ All Tests Passing |

---

## Objective
Complete integration test coverage for all MCP tools before PR submission.
All tests run against **live Ableton DAW** - no mocks.

## Prerequisites
- [x] Ableton Live running with AbletonMCP control surface
- [x] `make test-connection` passes
- [x] `pytest` and dependencies installed
- [ ] `test_get_track_info`
- [ ] `test_create_midi_track`
- [ ] `test_set_track_name`
- [ ] `test_set_track_volume`
- [ ] `test_set_master_volume`
- [ ] `test_set_tempo`

### Clip Tools
- [ ] `test_create_clip` - Create MIDI clip
- [ ] `test_add_notes_to_clip` - Add notes to clip
- [ ] `test_set_clip_name` - Rename clip
- [ ] `test_duplicate_clip` - Duplicate MIDI clip
- [ ] `test_empty_clip_slot` - Delete clip from slot
- [ ] `test_relocate_clip` - Move clip to different slot

### Transport Tools
- [ ] `test_fire_clip` - Start clip playback
- [ ] `test_stop_clip` - Stop clip
- [ ] `test_start_playback` - Start session playback
- [ ] `test_stop_playback` - Stop session playback

### Device & Rack Tools (New in this branch)
- [ ] `test_create_audio_effect_rack` - Create rack on track
- [ ] `test_create_rack_chain` - Add chain to rack
- [ ] `test_load_effect_to_chain` - Load effect into chain
- [ ] `test_get_device_parameters` - Get device params
- [ ] `test_set_device_parameter` - Modify device param

### Browser Tools
- [ ] `test_get_browser_tree` - Get browser categories
- [ ] `test_get_browser_items_at_path` - Navigate browser
- [ ] `test_load_instrument_or_effect` - Load from browser
- [ ] `test_load_effect_on_main` - Load effect on master
- [ ] `test_load_drum_kit` - Load drum rack with kit

---

## Workflow
1. Write test for one tool
2. Run: `pytest tests/test_tools.py::test_<name> -v`
3. Fix issues until passing
4. Commit: `git commit -m "test: add test for <tool_name>"`
5. Repeat for next tool

## PR Submission Criteria
- [ ] All 27 tool tests passing
- [ ] Tests run against live Ableton (no mocks)
- [ ] Each test committed atomically
- [ ] `make test-connection` documents connection requirement
