#!/usr/bin/env python3
"""Test get_clip_notes command."""

import json
import socket


def send_command(sock, command_type: str, params: dict = None):
    """Send MCP command and return result."""
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
                    print(f"✗ Error: {response.get('message')}")
                    return None
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
    print("Testing get_clip_notes...\n")

    # Test getting notes from Kick track (index 5, clip 0)
    result = send_command(sock, "get_clip_notes", {"track_index": 5, "clip_index": 0})

    if result:
        notes = result.get("notes", [])
        print(f"\n✓ Got {len(notes)} notes")
        if notes:
            print(f"First note: {notes[0]}")
            print(f"Last note: {notes[-1]}")
    else:
        print("\n✗ No result returned")

finally:
    sock.close()
