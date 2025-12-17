#!/usr/bin/env python3
"""
Fix Kick track: routing, devices, and verify MIDI notes.
"""

import json
import socket
import time

KICK_TRACK_INDEX = 5  # Track 6


def send_command(sock, command_type: str, params: dict = None):
    """Send MCP command and return result."""
    command = {"type": command_type, "params": params or {}}
    print(f"  → {command_type}")
    sock.sendall(json.dumps(command).encode("utf-8"))

    chunks = []
    sock.settimeout(10)
    while True:
        try:
            chunk = sock.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                data = b"".join(chunks)
                response = json.loads(data.decode("utf-8"))
                if response.get("status") == "error":
                    print(f"    ✗ Error: {response.get('message')}")
                    return None
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


print("=" * 60)
print("FIX KICK TRACK")
print("=" * 60)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(15)
sock.connect(("localhost", 9877))

try:
    # 1. Get current track info
    print("\n[1] Getting track info...")
    track_info = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if track_info:
        print(f"    Name: {track_info.get('name')}")
        print(f"    Volume: {track_info.get('volume')}")
        print(f"    Mute: {track_info.get('mute')}")
        print(f"    Arm: {track_info.get('arm')}")
        print(f"    Devices: {[d.get('name') for d in track_info.get('devices', [])]}")
        clip_slots = track_info.get("clip_slots", [])
        if clip_slots and clip_slots[0].get("has_clip"):
            print(f"    Clip: {clip_slots[0].get('clip', {}).get('name')}")

    # 2. Set volume to audible level
    print("\n[2] Setting volume to 0.85...")
    send_command(
        sock, "set_track_volume", {"track_index": KICK_TRACK_INDEX, "volume": 0.85}
    )
    time.sleep(0.2)

    # 3. Get clip notes
    print("\n[3] Getting clip notes...")
    notes_result = send_command(
        sock, "get_clip_notes", {"track_index": KICK_TRACK_INDEX, "clip_index": 0}
    )
    if notes_result:
        notes = notes_result.get("notes", [])
        print(f"    ✓ Got {len(notes)} notes")
        if notes:
            first, last = notes[0], notes[-1]
            fp, ft = first.get('pitch'), first.get('start_time')
            lp, lt = last.get('pitch'), last.get('start_time')
            print(f"    First: pitch={fp}, time={ft}")
            print(f"    Last: pitch={lp}, time={lt}")
    else:
        print("    ✗ No notes returned")

    # 4. Load a simple instrument if no devices
    if track_info and len(track_info.get("devices", [])) == 0:
        print("\n[4] No devices - loading Drum Rack...")
        # Try to load a drum rack
        result = send_command(
            sock,
            "load_browser_item",
            {"track_index": KICK_TRACK_INDEX, "item_uri": "Drums/Drum Rack"},
        )
        time.sleep(1)

        # Check again
        track_info = send_command(
            sock, "get_track_info", {"track_index": KICK_TRACK_INDEX}
        )
        if track_info:
            devices = [d.get('name') for d in track_info.get('devices', [])]
            print(f"    Devices now: {devices}")

    # 5. Fire the clip to test
    print("\n[5] Firing clip to test audio...")
    send_command(sock, "fire_clip", {"track_index": KICK_TRACK_INDEX, "clip_index": 0})

    print("\n" + "=" * 60)
    print("KICK TRACK STATUS")
    print("=" * 60)

    # Final status
    track_info = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if track_info:
        print(f"Track: {track_info.get('name')}")
        print(f"Volume: {track_info.get('volume')}")
        print(f"Devices: {len(track_info.get('devices', []))}")

    if notes_result:
        notes = notes_result.get("notes", [])
        print(f"MIDI Notes: {len(notes)}")

    print("\nIf no sound:")
    print("  1. Check Master output routing")
    print("  2. Load an instrument manually (Drum Rack with 909)")
    print("  3. Verify clip is playing (should see green indicator)")

finally:
    sock.close()
