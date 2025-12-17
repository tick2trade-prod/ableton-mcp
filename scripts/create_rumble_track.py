#!/usr/bin/env python3
"""
Create Rumble track at index 11 (Track 12).
Sub bass with sustained F notes and sidechain preparation.
"""

import json
import socket
import time

RUMBLE_TRACK_INDEX = 11  # Track 12
KICK_TRACK_INDEX = 5  # For sidechain source reference


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


def rumble_intro_pattern():
    """Generate 16 sustained F notes (one per bar)."""
    notes = []
    for bar in range(16):
        notes.append(
            {
                "pitch": 29,  # F0 - deep sub
                "start_time": float(bar * 4),
                "duration": 4.0,  # Full bar sustained
                "velocity": 100,
                "mute": False,
            }
        )
    return notes


print("=" * 60)
print("CREATE RUMBLE TRACK")
print("=" * 60)
print(f"Target: Track 12 (index {RUMBLE_TRACK_INDEX})")
print()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(20)
sock.connect(("localhost", 9877))

try:
    # 1. Check current session
    print("[1/7] Checking session...")
    session = send_command(sock, "get_session_info")
    if session:
        track_count = session.get("track_count", 0)
        print(f"    Current tracks: {track_count}")

        # Create tracks if needed to reach index 11
        while track_count <= RUMBLE_TRACK_INDEX:
            print(f"    Creating track {track_count}...")
            send_command(sock, "create_midi_track", {"index": track_count})
            track_count += 1
            time.sleep(0.5)

    # 2. Check track at index 11
    print(f"\n[2/7] Checking track at index {RUMBLE_TRACK_INDEX}...")
    track_info = send_command(
        sock, "get_track_info", {"track_index": RUMBLE_TRACK_INDEX}
    )
    if track_info:
        print(f"    Current name: {track_info.get('name')}")

    # 3. Name the track
    print("\n[3/7] Naming track 'Rumble'...")
    send_command(
        sock, "set_track_name", {"track_index": RUMBLE_TRACK_INDEX, "name": "Rumble"}
    )
    time.sleep(0.3)

    # 4. Try to load Operator synth
    print("\n[4/7] Loading Operator synth...")
    # First find the URI
    result = send_command(sock, "get_browser_items_at_path", {"path": "Instruments"})
    operator_uri = None
    if result:
        items = result.get("items", [])
        for item in items:
            if "Operator" in item.get("name", ""):
                operator_uri = item.get("uri")
                print(f"    Found Operator: {operator_uri}")
                break

    if operator_uri:
        send_command(
            sock,
            "load_browser_item",
            {"track_index": RUMBLE_TRACK_INDEX, "item_uri": operator_uri},
        )
        time.sleep(1.5)
    else:
        print("    Operator URI not found - will try default")
        # Try common URI patterns
        for uri in ["query:Instruments#Operator", "query:Synths#Operator"]:
            result = send_command(
                sock,
                "load_browser_item",
                {"track_index": RUMBLE_TRACK_INDEX, "item_uri": uri},
            )
            if result:
                break
            time.sleep(0.5)

    # 5. Create 16-bar clip
    print("\n[5/7] Creating 16-bar clip...")
    send_command(
        sock,
        "create_clip",
        {
            "track_index": RUMBLE_TRACK_INDEX,
            "clip_index": 0,
            "length": 64.0,  # 16 bars
        },
    )
    time.sleep(0.5)

    # 6. Add sustained sub bass notes
    print("\n[6/7] Adding 16 sustained F notes...")
    notes = rumble_intro_pattern()
    send_command(
        sock,
        "add_notes_to_clip",
        {"track_index": RUMBLE_TRACK_INDEX, "clip_index": 0, "notes": notes},
    )
    time.sleep(0.3)

    # 7. Name the clip
    print("\n[7/7] Naming clip...")
    send_command(
        sock,
        "set_clip_name",
        {"track_index": RUMBLE_TRACK_INDEX, "clip_index": 0, "name": "Rumble - Intro"},
    )

    # Verify final state
    print("\n" + "=" * 60)
    print("RUMBLE TRACK STATUS")
    print("=" * 60)
    track_info = send_command(
        sock, "get_track_info", {"track_index": RUMBLE_TRACK_INDEX}
    )
    if track_info:
        print(f"Track: {track_info.get('name')}")
        print(f"Devices: {len(track_info.get('devices', []))}")
        for d in track_info.get("devices", []):
            print(f"  - {d.get('name')}")
        clips = track_info.get("clip_slots", [])
        if clips and clips[0].get("has_clip"):
            print(f"Clip: {clips[0]['clip'].get('name')}")
            print(f"Clip length: {clips[0]['clip'].get('length')} beats")

    print("\n⚠️  MANUAL STEPS REQUIRED:")
    print("   1. Load Operator synth if not loaded (Instruments → Operator)")
    print("   2. Set Operator to sine wave for sub bass")
    print("   3. Add Compressor effect")
    print("   4. Configure Compressor sidechain from Kick track")

finally:
    sock.close()
