# CLAUDE.md - Ableton MCP Setup Guide

This document provides setup instructions for using Ableton MCP with Claude Desktop and Claude CLI (Claude Code).

## Prerequisites

- **Ableton Live 10+** installed and running
- **Python 3.10+**
- **UV package manager** - Install via `brew install uv` (macOS) or see [uv docs](https://docs.astral.sh/uv/getting-started/installation/)

## Installing the Ableton Remote Script

Before using the MCP server, you must install the Ableton Remote Script:

1. Copy the `AbletonMCP_Remote_Script` folder to Ableton's MIDI Remote Scripts directory:

   **macOS:**
   ```
   /Applications/Ableton Live <version>/Contents/App-Resources/MIDI Remote Scripts/
   ```
   Or user directory:
   ```
   ~/Library/Preferences/Ableton/Live <version>/User Remote Scripts/
   ```

   **Windows:**
   ```
   C:\ProgramData\Ableton\Live <version>\Resources\MIDI Remote Scripts\
   ```
   Or:
   ```
   C:\Users\<Username>\AppData\Roaming\Ableton\Live <version>\Preferences\User Remote Scripts\
   ```

2. Rename the folder to `AbletonMCP` (it should contain `__init__.py`)

3. Launch Ableton Live

4. Go to **Preferences → Link, Tempo & MIDI**

5. Set Control Surface dropdown to **AbletonMCP**

6. Set Input and Output to **None**

---

## Claude Desktop Setup

Edit your Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Option 1: Using Published Package (Upstream)

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "uvx",
      "args": ["ableton-mcp"]
    }
  }
}
```

### Option 2: Using Local Clone

If you've cloned this repository locally:

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/ableton-mcp",
        "run",
        "ableton-mcp"
      ]
    }
  }
}
```

### Option 3: Using GitHub Fork

To use a specific branch from a GitHub fork:

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/<owner>/ableton-mcp.git@<branch>",
        "ableton-mcp"
      ]
    }
  }
}
```

After editing the config, **restart Claude Desktop**. You should see a hammer icon indicating MCP tools are available.

---

## Claude CLI (Claude Code) Setup

Claude CLI uses MCP servers defined in its settings. There are multiple ways to configure:

### Option 1: Global User Settings

Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "uvx",
      "args": ["ableton-mcp"]
    }
  }
}
```

### Option 2: Project-Level Settings

Create `.claude/settings.json` in your project root:

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/ableton-mcp",
        "run",
        "ableton-mcp"
      ]
    }
  }
}
```

### Option 3: Using Claude CLI Commands

Add an MCP server interactively:

```bash
claude mcp add AbletonMCP -- uvx ableton-mcp
```

Or for a local installation:

```bash
claude mcp add AbletonMCP -- uv --directory /path/to/ableton-mcp run ableton-mcp
```

### Verifying MCP Connection

After configuring, start Claude CLI and verify the MCP is loaded:

```bash
claude
```

Then type `/mcp` to see available MCP servers and their tools.

---

## Available Tools

Once connected, the following tools are available:

### Session & Track Info
- `get_session_info` - Get current Ableton session details
- `get_track_info` - Get information about a specific track

### Track Management
- `create_midi_track` - Create a new MIDI track
- `set_track_name` - Rename a track
- `set_track_volume` - Set track volume (0.0-1.0)
- `set_master_volume` - Set master volume

### Clip Operations
- `create_clip` - Create a new MIDI clip
- `add_notes_to_clip` - Add MIDI notes to a clip
- `set_clip_name` - Rename a clip
- `duplicate_clip` - Copy a clip to another slot
- `empty_clip_slot` - Remove a clip
- `relocate_clip` - Move a clip to another slot
- `fire_clip` - Start playing a clip
- `stop_clip` - Stop a clip

### Playback & Tempo
- `start_playback` - Start session playback
- `stop_playback` - Stop session playback
- `set_tempo` - Set session tempo in BPM

### Browser & Loading
- `get_browser_tree` - Browse Ableton's library categories
- `get_browser_items_at_path` - Get items at a browser path
- `load_instrument_or_effect` - Load instrument/effect by URI
- `load_drum_kit` - Load a drum rack with a kit
- `load_effect_on_main` - Load effect on master track

### Rack & Device Control
- `create_audio_effect_rack` - Create an empty audio effect rack
- `create_rack_chain` - Add a chain to a rack
- `load_effect_to_chain` - Load effect into a rack chain
- `get_device_parameters` - Get all parameters of a device
- `set_device_parameter` - Set a device parameter value

---

## Debugging

### Claude Desktop Logs

**macOS:**
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

**Windows:**
```powershell
Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Wait
```

### Claude CLI Logs

Run with verbose logging:
```bash
claude --mcp-debug
```

### Common Issues

1. **Connection refused**: Ensure Ableton is running with the Remote Script loaded before starting Claude

2. **Timeout errors**: The MCP connects to `localhost:9877`. Check that no firewall is blocking this port

3. **Script not appearing in Ableton**: Verify the folder is named exactly `AbletonMCP` and contains `__init__.py`

4. **UV not found**: Ensure UV is installed and in your PATH. Try `which uv` or reinstall via `brew install uv`

---

## Development

### Running the Server Locally

```bash
cd /path/to/ableton-mcp
uv run ableton-mcp
```

### Running with Debug Logging

```bash
cd /path/to/ableton-mcp
uv run python -c "import logging; logging.basicConfig(level=logging.DEBUG); from MCP_Server.server import main; main()"
```

### Testing Connection

The MCP server connects to Ableton via TCP socket on port 9877. You can test the connection:

```bash
nc -zv localhost 9877
```

---

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Server Development Guide](https://modelcontextprotocol.io/docs/develop/build-server)
- [Claude Desktop MCP Setup](https://modelcontextprotocol.io/docs/quickstart)
- [Ableton Live MIDI Remote Scripts](https://docs.ableton.com/)
