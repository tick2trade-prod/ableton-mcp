#!/bin/bash
# ableton-mcp-available-tools-doctor.sh - List available MCP tools
set -e

echo "=== Ableton MCP Available Tools ==="

SERVER_FILE="/Users/alexzh/ableton-mcp/MCP_Server/server.py"

if [[ ! -f "$SERVER_FILE" ]]; then
    echo "❌ Server file not found: $SERVER_FILE"
    exit 1
fi

# Extract @mcp.tool() decorated functions
echo ""
echo "Tools defined in MCP_Server/server.py:"
echo "---------------------------------------"
grep -A1 '@mcp.tool()' "$SERVER_FILE" | grep 'def ' | sed 's/def /  /' | sed 's/(.*/:/' | sort

# Count tools
TOOL_COUNT=$(grep -c '@mcp.tool()' "$SERVER_FILE")
echo ""
echo "Total: $TOOL_COUNT tools"

# List by category
echo ""
echo "By Category:"
echo "  Session:  get_session_info, get_track_info"
echo "  Tracks:   create_midi_track, delete_track, set_track_name"
echo "  Clips:    create_clip, add_notes_to_clip, duplicate_clip, relocate_clip"
echo "  Devices:  load_instrument_or_effect, set_device_parameter"
echo "  Racks:    create_audio_effect_rack, create_rack_chain"
echo "  Browser:  get_browser_tree"
echo "  Transport: fire_clip, stop_clip, start_playback, stop_playback"
echo "  Volume:   set_track_volume, set_master_volume, set_tempo"

echo ""
echo "=== Done ==="
