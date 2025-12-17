#!/usr/bin/env python3
"""
Complete Kick track setup:
1. Unmute the track
2. Verify MIDI notes
3. Fire clip for playback
"""

import json
import socket

KICK_TRACK_INDEX = 5


def send_command(sock, command_type: str, params: dict = None):
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
                    print(f"    ✗ {response.get('message')}")
                    return None
                print("    ✓ OK")
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


print("=" * 60)
print("COMPLETE KICK TRACK SETUP")
print("=" * 60)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(15)
sock.connect(("localhost", 9877))

try:
    # 1. Unmute the kick track
    print("\n[1/4] Unmuting Kick track...")
    result = send_command(
        sock, "set_track_mute", {"track_index": KICK_TRACK_INDEX, "mute": False}
    )
    if result:
        print(f"    Mute state: {result.get('mute')}")

    # 2. Get track info
    print("\n[2/4] Getting track info...")
    track = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if track:
        print(f"    Name: {track.get('name')}")
        print(f"    Mute: {track.get('mute')}")
        print(f"    Volume: {track.get('volume')}")
        print(f"    Devices: {len(track.get('devices', []))}")
        clips = track.get("clip_slots", [])
        if clips and clips[0].get("has_clip"):
            print(f"    Clip: {clips[0]['clip'].get('name')}")

    # 3. Get clip notes
    print("\n[3/4] Getting MIDI notes...")
    notes_result = send_command(
        sock, "get_clip_notes", {"track_index": KICK_TRACK_INDEX, "clip_index": 0}
    )
    if notes_result:
        notes = notes_result.get("notes", [])
        print(f"    Note count: {len(notes)}")
        if len(notes) == 64:
            print("    ✓ Correct: 64 notes for 4-on-floor")
        elif len(notes) > 0:
            first = notes[0]
            p, t = first.get('pitch'), first.get('start_time')
            print(f"    First: pitch={p}, time={t}")

    # 4. Fire the clip
    print("\n[4/4] Firing clip...")
    send_command(sock, "fire_clip", {"track_index": KICK_TRACK_INDEX, "clip_index": 0})

    # Summary
    print("\n" + "=" * 60)
    print("KICK TRACK STATUS")
    print("=" * 60)

    track = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if track:
        print(f"Track: {track.get('name')}")
        muted = track.get('mute')
        status = '(UNMUTED ✓)' if not muted else '(STILL MUTED ✗)'
        print(f"Mute: {muted} {status}")
        print(f"Volume: {track.get('volume'):.2f}")
        print(f"Devices: {len(track.get('devices', []))}")

    if notes_result:
        notes = notes_result.get("notes", [])
        print(
            f"MIDI Notes: {len(notes)} {'✓' if len(notes) == 64 else '(expected 64)'}"
        )

    print("\n⚠️  If no devices, manually load a Drum Rack with 909 kit")
    print("   Or run: /track-01-kick to add 909 Core Kit")

finally:
    sock.close()
