# Available Tools

The Ableton MCP Server provides 27 tools to control Ableton Live.

## Session & Transport

| Tool | Description |
|------|-------------|
| `get_session_info()` | Get details about tracks, clips, and tempo. |
| `start_playback()` | Start global playback. |
| `stop_playback()` | Stop global playback. |
| `set_tempo(tempo)` | Set global BPM (e.g., 120.0). |

## Track Management

| Tool | Description |
|------|-------------|
| `get_track_info(track_index)` | Get detailed info for a specific track. |
| `create_midi_track(index)` | Create a new MIDI track. |
| `delete_track(track_index)` | Delete a track. |
| `set_track_name(track_index, name)` | Rename a track. |
| `set_track_volume(track_index, volume)` | Set track volume (0.0 - 1.0). |
| `set_master_volume(volume)` | Set master volume (0.0 - 1.0). |

## Clip Management

| Tool | Description |
|------|-------------|
| `create_clip(track_index, clip_index, length)` | Create a new empty MIDI clip. |
| `add_notes_to_clip(track_index, clip_index, notes)` | Add MIDI notes to a clip. |
| `fire_clip(track_index, clip_index)` | Launch a clip. |
| `stop_clip(track_index, clip_index)` | Stop a playing clip. |
| `set_clip_name(track_index, clip_index, name)` | Rename a clip. |
| `duplicate_clip(source_track, source_clip, dest_track, dest_clip)` | Duplicate a clip to a new slot. |
| `empty_clip_slot(track_index, clip_index)` | Delete a clip from a slot. |
| `relocate_clip(source_track, source_clip, dest_track, dest_clip)` | Move a clip to a new slot. |

## Devices & Racks

| Tool | Description |
|------|-------------|
| `load_instrument_or_effect(track_index, uri)` | Load device from Browser URI. |
| `load_effect_on_main(uri)` | Load effect onto Master track. |
| `create_audio_effect_rack(track_index, device_index)` | Create an empty Audio Effect Rack. |
| `create_rack_chain(track_index, device_index, chain_name)` | Add a chain to a Rack. |
| `load_effect_to_chain(track, rack_dev, chain, uri)` | Load effect into a Rack Chain. |
| `get_device_parameters(track, device, ...)` | Get list of device parameters. |
| `set_device_parameter(track, device, param, value)` | Control device parameters. |

## Browser & Loading

| Tool | Description |
|------|-------------|
| `get_browser_tree(category_type)` | Explore browser categories. |
| `get_browser_items_at_path(path)` | List items in a browser folder. |
| `load_drum_kit(track, rack_uri, kit_path)` | Helper to load Drum Rack + Kit. |
