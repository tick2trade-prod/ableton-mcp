#!/usr/bin/env python3
"""
Execute Track 01: Kick - I Am Machine Recreation

Track Layout:
- Track 1: Reference MP3
- Tracks 2-5: Stems (Vocals, Drums, Bass, Others)
- Track 6 (index 5): Kick ← THIS TRACK
"""

import json
import socket
import sys
import time

# Track index (0-based)
KICK_TRACK_INDEX = 5  # Track 6


def send_command(sock, command_type: str, params: dict = None):
    """Send MCP command and return result."""
    command = {"type": command_type, "params": params or {}}
    print(f"  → {command_type}: {params}")
    sock.sendall(json.dumps(command).encode("utf-8"))

    chunks = []
    sock.settimeout(10)
    while True:
        try:
            chunk = sock.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                data = b"".join(chunks)
                response = json.loads(data.decode("utf-8"))
                if response.get("status") == "error":
                    print(f"  ✗ Error: {response.get('message')}")
                    return None
                result = response.get("result", {})
                print("  ✓ OK")
                return result
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break

    if chunks:
        data = b"".join(chunks)
        return json.loads(data.decode("utf-8")).get("result", {})
    return {}


def kick_intro_pattern():
    """Generate 64 kick notes for 4-on-floor pattern (16 bars)."""
    notes = []
    for i in range(64):  # 16 bars × 4 beats
        notes.append(
            {
                "pitch": 36,  # C1 - standard kick
                "start_time": float(i),
                "duration": 0.5,
                "velocity": 100,
                "mute": False,
            }
        )
    return notes


def main():
    print("=" * 60)
    print("EXECUTION: Track 01 - Kick")
    print("=" * 60)
    print(f"Target: Track 6 (index {KICK_TRACK_INDEX})")
    print()

    # Connect to Ableton MCP
    print("[1/7] Connecting to Ableton MCP...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        sock.connect(("localhost", 9877))
        print("  ✓ Connected to Ableton on port 9877")
    except ConnectionRefusedError:
        print("  ✗ Cannot connect to Ableton. Is AbletonMCP Remote Script running?")
        sys.exit(1)

    try:
        # Get session info
        print("\n[2/7] Getting session info...")
        session = send_command(sock, "get_session_info")
        if session:
            print(f"  Track count: {session.get('track_count', 0)}")
            print(f"  BPM: {session.get('tempo', 0)}")

        # Check if track already exists at index 5
        print(f"\n[3/7] Checking track at index {KICK_TRACK_INDEX}...")
        track_info = send_command(
            sock, "get_track_info", {"track_index": KICK_TRACK_INDEX}
        )

        track_exists = track_info is not None and "name" in track_info
        if track_exists:
            current_name = track_info.get("name", "")
            print(f"  Track exists: '{current_name}'")
            if "kick" in current_name.lower():
                print("  → Kick track already exists, updating...")
            else:
                print("  → Renaming to 'Kick'")
        else:
            print("  Track doesn't exist, will create...")
            # Create MIDI track
            print(f"\n  Creating MIDI track at index {KICK_TRACK_INDEX}...")
            send_command(sock, "create_midi_track", {"index": KICK_TRACK_INDEX})
            time.sleep(0.5)

        # Name the track
        print("\n[4/7] Naming track 'Kick'...")
        send_command(
            sock, "set_track_name", {"track_index": KICK_TRACK_INDEX, "name": "Kick"}
        )
        time.sleep(0.3)

        # Load 909 Core Kit
        print("\n[5/7] Loading 909 Core Kit and processing...")
        # Use load_browser_item (the actual socket command)
        send_command(
            sock,
            "load_browser_item",
            {"track_index": KICK_TRACK_INDEX, "item_uri": "query:Drums#909"},
        )
        time.sleep(1)

        # Add Drum Buss
        send_command(
            sock,
            "load_browser_item",
            {
                "track_index": KICK_TRACK_INDEX,
                "item_uri": "query:Audio Effects#Drum Buss",
            },
        )
        time.sleep(0.5)

        # Add Saturator
        send_command(
            sock,
            "load_browser_item",
            {
                "track_index": KICK_TRACK_INDEX,
                "item_uri": "query:Audio Effects#Saturator",
            },
        )
        time.sleep(0.5)

        # Create 16-bar clip
        print("\n[6/7] Creating 16-bar clip...")
        send_command(
            sock,
            "create_clip",
            {
                "track_index": KICK_TRACK_INDEX,
                "clip_index": 0,
                "length": 64.0,  # 16 bars = 64 beats
            },
        )
        time.sleep(0.5)

        # Add 4-on-floor kick pattern
        print("\n[7/7] Adding 64 kick notes (4-on-floor)...")
        notes = kick_intro_pattern()
        send_command(
            sock,
            "add_notes_to_clip",
            {"track_index": KICK_TRACK_INDEX, "clip_index": 0, "notes": notes},
        )
        time.sleep(0.3)

        # Name the clip
        send_command(
            sock,
            "set_clip_name",
            {"track_index": KICK_TRACK_INDEX, "clip_index": 0, "name": "Kick - Intro"},
        )

        print("\n" + "=" * 60)
        print("✓ KICK TRACK CREATED SUCCESSFULLY")
        print("=" * 60)
        print(f"Track 6 (index {KICK_TRACK_INDEX}): Kick")
        print("Devices: 909 Kit → Drum Buss → Saturator")
        print("Clip: 'Kick - Intro' (16 bars, 64 notes)")
        print()
        print("Next: Run tests with:")
        print("  pytest tests/phases/phase1_intro/test_track_01_kick.py -v")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
