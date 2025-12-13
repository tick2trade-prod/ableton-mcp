# Ableton MCP - TODO

## Planned Features

### MIDI Editing
- [ ] **Transpose MIDI notes in clip** - Add ability to transpose all MIDI notes in a clip by a semitone offset

### Clip Operations
- [ ] **Audio clip support** - Extend clip operations to work with audio clips (currently MIDI only)

## Completed

### v1.1.0 (Rack Chain Tools)
- [x] **Master track effects** - `load_effect_on_main` adds effects to Master
- [x] **Rack chain management** - Create racks, add chains, load effects to chains
- [x] **Device parameters in chains** - Get/set params for devices inside rack chains
- [x] **Browser navigation** - `get_browser_tree`, `get_browser_items_at_path`
- [x] **Integration tests** - 38 tests against live Ableton DAW

Focus on updating @0002-io-alchemy-techno.md  with what heckbox items have been completed. Then add new tsks to better implement the tracks to recreate /Users/alexzh/ableton-mcp/assets/audio/reference/ALCHEMY_I_O.mp3 with tests in
tests/techno
tests/techno/__pycache__
tests/techno/conftest.py
tests/techno/test_arrangement.py
tests/techno/test_instruments.py

implement all of these successfully as part of this branch for the upcoming PR
