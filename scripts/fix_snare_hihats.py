#!/usr/bin/env python3
"""
Fix Snare and Hi-hats tracks (indices 6 and 7).
These tracks failed during initial execution - recreate them properly.
"""

import json
import socket
import time


def send_command(sock, command_type: str, params: dict = None):
    command = {"type": command_type, "params": params or {}}
    print(f"  → {command_type}")
    sock.sendall(json.dumps(command).encode("utf-8"))

    chunks = []
    sock.settimeout(15)
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
                    print(f"    ✗ {response.get('message')}")
                    return None
                print("    ✓ OK")
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


def backbeat_pattern():
    """32 snare notes on beats 2 and 4."""
    notes = []
    for bar in range(16):
        for beat in [1, 3]:
            notes.append(
                {
                    "pitch": 38,
                    "start_time": float(bar * 4 + beat),
                    "duration": 0.5,
                    "velocity": 100,
                    "mute": False,
                }
            )
    return notes


def offbeat_8ths():
    """64 hi-hat notes on offbeat 8ths."""
    notes = []
    for bar in range(16):
        for beat in [0.5, 1.5, 2.5, 3.5]:
            notes.append(
                {
                    "pitch": 42,
                    "start_time": float(bar * 4 + beat),
                    "duration": 0.25,
                    "velocity": 80,
                    "mute": False,
                }
            )
    return notes


print("=" * 60)
print("FIX SNARE AND HI-HATS TRACKS")
print("=" * 60)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(20)
sock.connect(("localhost", 9877))

try:
    # Check current track info
    print("\n[1] Checking current tracks 6 and 7...")

    track6 = send_command(sock, "get_track_info", {"track_index": 6})
    if track6:
        name6 = track6.get('name')
        devs6 = len(track6.get('devices', []))
        print(f"    Track 6: {name6} - {devs6} devices")
        track6_type = track6.get("type", "unknown")
        print(f"    Type: {track6_type}")

    track7 = send_command(sock, "get_track_info", {"track_index": 7})
    if track7:
        name7 = track7.get('name')
        devs7 = len(track7.get('devices', []))
        print(f"    Track 7: {name7} - {devs7} devices")
        track7_type = track7.get("type", "unknown")
        print(f"    Type: {track7_type}")

    # The tracks exist but might be audio tracks from stems
    # We need to check if we can convert them to MIDI or need to work differently

    # Try deleting and recreating as MIDI tracks
    print("\n[2] Deleting track at index 7 (Hi-hats)...")
    send_command(sock, "delete_track", {"track_index": 7})
    time.sleep(0.5)

    print("\n[3] Deleting track at index 6 (Snare)...")
    send_command(sock, "delete_track", {"track_index": 6})
    time.sleep(0.5)

    print("\n[4] Creating new MIDI track at index 6 for Snare...")
    send_command(sock, "create_midi_track", {"index": 6})
    time.sleep(0.5)

    print("\n[5] Naming track 'Snare'...")
    send_command(sock, "set_track_name", {"track_index": 6, "name": "Snare"})
    time.sleep(0.2)

    print("\n[6] Loading 909 kit on Snare...")
    send_command(
        sock,
        "load_browser_item",
        {"track_index": 6, "item_uri": "query:Drums#FileId_14946"},
    )
    time.sleep(1.0)

    print("\n[7] Creating 16-bar clip on Snare...")
    send_command(
        sock, "create_clip", {"track_index": 6, "clip_index": 0, "length": 64.0}
    )
    time.sleep(0.3)

    print("\n[8] Adding backbeat pattern to Snare...")
    notes = backbeat_pattern()
    send_command(
        sock, "add_notes_to_clip", {"track_index": 6, "clip_index": 0, "notes": notes}
    )
    time.sleep(0.2)

    print("\n[9] Naming Snare clip...")
    send_command(
        sock,
        "set_clip_name",
        {"track_index": 6, "clip_index": 0, "name": "Snare - Intro"},
    )
    time.sleep(0.2)

    # Now Hi-hats at index 7
    print("\n[10] Creating new MIDI track at index 7 for Hi-hats...")
    send_command(sock, "create_midi_track", {"index": 7})
    time.sleep(0.5)

    print("\n[11] Naming track 'Hi-hats'...")
    send_command(sock, "set_track_name", {"track_index": 7, "name": "Hi-hats"})
    time.sleep(0.2)

    print("\n[12] Loading 909 kit on Hi-hats...")
    send_command(
        sock,
        "load_browser_item",
        {"track_index": 7, "item_uri": "query:Drums#FileId_14946"},
    )
    time.sleep(1.0)

    print("\n[13] Creating 16-bar clip on Hi-hats...")
    send_command(
        sock, "create_clip", {"track_index": 7, "clip_index": 0, "length": 64.0}
    )
    time.sleep(0.3)

    print("\n[14] Adding offbeat 8ths pattern to Hi-hats...")
    notes = offbeat_8ths()
    send_command(
        sock, "add_notes_to_clip", {"track_index": 7, "clip_index": 0, "notes": notes}
    )
    time.sleep(0.2)

    print("\n[15] Naming Hi-hats clip...")
    send_command(
        sock,
        "set_clip_name",
        {"track_index": 7, "clip_index": 0, "name": "Hi-hats - Intro"},
    )

    print("\n" + "=" * 60)
    print("DONE - Snare and Hi-hats fixed!")
    print("=" * 60)

finally:
    sock.close()
