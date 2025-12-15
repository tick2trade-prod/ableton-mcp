#!/usr/bin/env python3
"""
Track 04: 303 Acid Line - Hypnotic squelchy hook with high-mid energy.
Per spec: Drift synth, sawtooth, high resonance filter, slides.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_04_acid_v2.py
"""

import json
import os
import socket
import subprocess
import time

# --- Configuration ---
TRACK_NAME = "04-Acid303"
TRACK_INDEX = 3
DEVICES = [
    {"name": "Drift", "uri": "query:Synths#Drift"},
    {"name": "Saturator", "uri": "query:AudioFx#Saturator"},
    {"name": "Delay", "uri": "query:AudioFx#Delay"},
]
NOTES = [
    {"pitch": 41, "start_time": 0.0, "duration": 0.25, "velocity": 100},
    {"pitch": 41, "start_time": 0.5, "duration": 0.25, "velocity": 100},
    {"pitch": 41, "start_time": 1.0, "duration": 0.25, "velocity": 100},
    {"pitch": 41, "start_time": 1.5, "duration": 0.25, "velocity": 100},
    {"pitch": 41, "start_time": 2.0, "duration": 0.25, "velocity": 100},
    {"pitch": 41, "start_time": 2.5, "duration": 0.25, "velocity": 100},
    {"pitch": 41, "start_time": 3.0, "duration": 0.25, "velocity": 100},
    {"pitch": 41, "start_time": 3.5, "duration": 0.25, "velocity": 100},
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
            "params": {"track_index": track_index, "clip_index": 0, "length": 4.0},
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
    print(f" Creating {TRACK_NAME}")
    print("========================================")

    connection = send_command({"type": "get_session_info"})
    if connection.get("status") != "success":
        print("CRITICAL: Cannot connect to Ableton Live.")
        print("1. Ensure Ableton is open.")
        print("2. Ensure 'AbletonMCP' is selected as Control Surface.")
        print("3. IMPORTANT: Restart Ableton if you just updated the script.")
        return 1

    if ensure_track(TRACK_INDEX, TRACK_NAME, "midi"):
        load_devices_for_track(TRACK_INDEX, DEVICES)
        add_midi_pattern(TRACK_INDEX, TRACK_NAME, NOTES)
        print(f"\n--- {TRACK_NAME} Complete ---")
        print("\nConfigure in Ableton:")
        print("  - Drift: Sawtooth, Drift 20%, LP 18dB, Res 60-70%")
        print("  - Env 2 \u2192 Filter Cutoff (short decay)")
        print("  - Pattern: F Minor pentatonic, use legato for slides")
        print("  - Saturator: Center 1kHz, Drive 60%")
        print("  - Delay: Ping-pong 1/8D, Feedback 40%")
        return 0
    else:
        print(f"⚠ Failed to create track {TRACK_NAME}. Check errors above.")
        return 1


if __name__ == "__main__":
    exit(main())
