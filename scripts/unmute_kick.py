#!/usr/bin/env python3
"""Unmute kick track and check available commands."""

import json
import socket

KICK_TRACK_INDEX = 5


def send_command(sock, command_type: str, params: dict = None):
    command = {"type": command_type, "params": params or {}}
    print(f"→ {command_type}: {params}")
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
                    print(f"  ✗ {response.get('message')}")
                    return None
                print("  ✓ OK")
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(15)
sock.connect(("localhost", 9877))

try:
    # Check session info first
    print("Session info:")
    session = send_command(sock, "get_session_info")
    if session:
        print(f"  Tracks: {session.get('track_count')}")
        print(f"  BPM: {session.get('tempo')}")

    # Get track info showing mute state
    print("\nKick track before:")
    track = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if track:
        print(f"  Mute: {track.get('mute')}")
        print(f"  Volume: {track.get('volume')}")

    # We need to unmute - but there's no unmute command directly
    # The track info shows mute=True, need to toggle it in Ableton UI
    # or add an unmute command to the Remote Script

    print("\n⚠️  Track is MUTED - please unmute in Ableton UI")
    print("   Click the track's Mute button (yellow 'M') to toggle off")

finally:
    sock.close()
