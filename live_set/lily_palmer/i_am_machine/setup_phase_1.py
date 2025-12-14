#!/usr/bin/env python3
"""
Setup Phase 1: Rhythm & Bass Foundation (Kick, Rumble, Rolling Bass)

This is a consolidated, robust script to create and configure the first 3 core tracks.
Prerequisite: Ableton Live running with updated AbletonMCP script (restart if recently updated).

Tracks:
1. 01-Kick (MIDI) -> Drum Sampler -> 4-on-floor pattern
2. 02-Rumble (Audio) -> Hybrid Reverb + Roar -> Receives audio from Kick
3. 03-RollingBass (MIDI) -> Operator -> 16th note bassline

Usage: uv run python live_set/lily_palmer/i_am_machine/setup_phase_1.py
"""

import json
import os
import socket
import subprocess
import time

# --- Configuration ---
TRACKS = [
    {
        "index": 0,
        "name": "01-Kick",
        "type": "midi",
        "devices": [
            {"name": "Drum Sampler", "uri": "query:Synths#Drum%20Sampler"},
            {"name": "Channel EQ", "uri": "query:AudioFx#Channel%20EQ"},
            {"name": "Saturator", "uri": "query:AudioFx#Saturator"},
        ],
        "notes": [
            {"pitch": 36, "start_time": fl, "duration": 0.25, "velocity": 110}
            for fl in [float(b * 4 + i) for b in range(4) for i in range(4)]  # 4 bars, 4 beats
        ],
    },
    {
        "index": 1,
        "name": "02-Rumble",
        "type": "audio",
        "devices": [
            {"name": "Reverb", "uri": "query:AudioFx#Reverb"},
            {"name": "Saturator", "uri": "query:AudioFx#Saturator"},
            {"name": "Channel EQ", "uri": "query:AudioFx#Channel%20EQ"},
            {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
        ],
        "notes": None,  # Audio track
    },
    {
        "index": 2,
        "name": "03-RollingBass",
        "type": "midi",
        "devices": [
            {"name": "Simpler", "uri": "query:Synths#Simpler"},
            {"name": "Channel EQ", "uri": "query:AudioFx#Channel%20EQ"},
            {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
        ],
        "notes": [
            {"pitch": p, "start_time": st, "duration": 0.2, "velocity": 95}
            for p, st in zip(
                [29, 32, 34, 36, 39] * 13,  # F minor scale pattern
                [float(i * 0.25) for i in range(16 * 4)],
                strict=False,  # 16th notes for 4 bars
            )
        ],
    },
]

# --- Utilities ---


def detect_host():
    try:
        route = subprocess.check_output(
            ["sh", "-c", "ip route show default | awk '{print $3}'"], text=True
        ).strip()
        return route or "127.0.0.1"
    except:
        return os.getenv("ABLETON_MCP_HOST", "127.0.0.1")


def send_command(command: dict, timeout: float = 20.0) -> dict:
    host = detect_host()
    port = int(os.getenv("ABLETON_MCP_PORT", "9877"))
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        data = (json.dumps(command) + "\n").encode("utf-8")
        sock.sendall(data)
        buffer = b""
        start = time.time()
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            buffer += chunk
            try:
                result = json.loads(buffer.decode("utf-8"))
                sock.close()
                return result
            except json.JSONDecodeError:
                if time.time() - start > timeout:
                    sock.close()
                    raise TimeoutError("Timed out")
                continue
        sock.close()
    except Exception as e:
        print(f"   !!! Connection Error: {e}")
        return {"status": "error", "message": str(e)}
    return {}


def ensure_track(target_index, name, track_type="midi"):
    """Ensure track exists at index, creating if needed."""
    print(f"\n--- Ensuring Track {target_index}: {name} ({track_type}) ---")

    # 1. Check current tracks
    info = send_command({"type": "get_session_info"})
    if info.get("status") != "success":
        print("   ✗ Failed to get session info.")
        return False

    current_count = info.get("result", {}).get("track_count", 0)
    print(f"   Current total tracks: {current_count}")

    # 2. Create if missing
    if current_count <= target_index:
        print(f"   Creating new {track_type} track...")
        cmd_type = "create_audio_track" if track_type == "audio" else "create_midi_track"

        result = send_command({"type": cmd_type, "params": {"index": -1}})

        if result.get("status") == "success":
            new_idx = result.get("result", {}).get("index")
            print(f"   ✓ Created track at index {new_idx}")
            if new_idx != target_index:
                print(f"   ⚠ Warning: Created index {new_idx} != Target {target_index}")
        else:
            print(f"   ✗ Failed to create track: {result.get('message')}")
            print("   ⚠ Please create track manually if possible.")
            return False

    # 3. Rename
    result = send_command(
        {"type": "set_track_name", "params": {"track_index": target_index, "name": name}}
    )
    print(f"   ✓ Track name set to '{name}'")
    return True


def load_devices_for_track(track_index, devices):
    """Load list of devices."""
    if not devices:
        return
    print(f"   Loading devices: {', '.join([d['name'] for d in devices])}")
    for device in devices:
        result = send_command(
            {
                "type": "load_browser_item",
                "params": {"track_index": track_index, "item_uri": device["uri"]},
            }
        )
        if result.get("status") != "success":
            print(f"     ✗ Failed to load '{device['name']}': {result.get('message')}")
        else:
            print(f"     ✓ Loaded '{device['name']}'")


def add_midi_pattern(track_index, name, notes):
    """Create clip and add notes."""
    if not notes:
        return
    print("   Adding MIDI pattern...")

    # Create clip
    send_command(
        {
            "type": "create_clip",
            "params": {"track_index": track_index, "clip_index": 0, "length": 16.0},
        }
    )

    # Add notes
    send_command(
        {
            "type": "add_notes_to_clip",
            "params": {"track_index": track_index, "clip_index": 0, "notes": notes},
        }
    )

    # Rename clip
    send_command(
        {
            "type": "set_clip_name",
            "params": {"track_index": track_index, "clip_index": 0, "name": f"{name} Pattern"},
        }
    )

    # Fire clip
    send_command({"type": "fire_clip", "params": {"track_index": track_index, "clip_index": 0}})
    print("     ✓ Pattern created and playing")


# --- Main Flow ---


def main():
    print("========================================")
    print(" SETUP PHASE 1: Kick, Rumble, Bass")
    print("========================================")

    connection = send_command({"type": "get_session_info"})
    if connection.get("status") != "success":
        print("CRITICAL: Cannot connect to Ableton Live.")
        print("1. Ensure Ableton is open.")
        print("2. Ensure 'AbletonMCP' is selected as Control Surface.")
        print("3. IMPORTANT: Restart Ableton if you just updated the script.")
        return 1

    success_count = 0
    for cfg in TRACKS:
        idx = cfg["index"]
        name = cfg["name"]

        if ensure_track(idx, name, cfg["type"]):
            load_devices_for_track(idx, cfg["devices"])
            add_midi_pattern(idx, name, cfg["notes"])
            success_count += 1
            time.sleep(0.5)  # small pause
        else:
            print(f"   ⚠ Skipping configuration for {name} due to track error.")

    print("\n----------------------------------------")
    if success_count == 3:
        print("✓ All 3 foundational tracks setup successfully!")
        send_command({"type": "start_playback"})
        print("▶ Playback started.")
    else:
        print(f"⚠ Partially completed ({success_count}/3). Check errors above.")

    print("\nNext Manual Steps:")
    print("1. Track 01 (Kick): Drop a nice kick sample into the Drum Sampler/Simpler.")
    print("2. Track 02 (Rumble): Configure routing 'Audio From' -> '01-Kick' (Post FX).")
    print("3. Track 03 (Bass): Tweak Simpler to create a bass sound.")

    return 0


if __name__ == "__main__":
    exit(main())
