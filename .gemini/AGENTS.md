# Agent Instructions

## Goal
Verify `ableton-mcp` MCP tools work with live Ableton DAW via integration tests.

## Testing Rules
1. **No mocks** - Connect to real Ableton on port 9877
2. **One tool per test** - Incremental verification
3. **Run and fix** - Execute test, observe results, fix until passing

## Tools to Test (feature/rack-chain-tools)
- [ ] get_session_info
- [ ] create_midi_track
- [ ] create_audio_effect_rack
- [ ] create_rack_chain
- [ ] load_effect_to_chain
- [ ] get_device_parameters
- [ ] set_device_parameter
- [ ] duplicate_clip (MIDI only)
- [ ] relocate_clip (MIDI only)

## Commands
```bash
make test-connection  # Verify Ableton connected
make logs-mcp         # Check Remote Script logs
pytest tests/ -v      # Run tests
```
