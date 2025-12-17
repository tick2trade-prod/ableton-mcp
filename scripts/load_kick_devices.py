#!/usr/bin/env python3
"""Load devices for Kick track (909 + Drum Buss + Saturator)."""

import json
import socket
import time

KICK_TRACK_INDEX = 5


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
                print(f"  ✓ OK: {response.get('result', {})}")
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


print("Loading devices for Kick track...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(15)
sock.connect(("localhost", 9877))

try:
    # Load 909 Core Kit
    print("\n[1/3] Loading 909 drum kit...")
    send_command(
        sock,
        "load_browser_item",
        {"track_index": KICK_TRACK_INDEX, "item_uri": "query:Drums#909"},
    )
    time.sleep(1.5)

    # Add Drum Buss
    print("\n[2/3] Adding Drum Buss...")
    send_command(
        sock,
        "load_browser_item",
        {"track_index": KICK_TRACK_INDEX, "item_uri": "query:Audio Effects#Drum Buss"},
    )
    time.sleep(0.8)

    # Add Saturator
    print("\n[3/3] Adding Saturator...")
    send_command(
        sock,
        "load_browser_item",
        {"track_index": KICK_TRACK_INDEX, "item_uri": "query:Audio Effects#Saturator"},
    )
    time.sleep(0.5)

    # Verify track devices
    print("\nVerifying track...")
    result = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if result:
        print(f"\nTrack: {result.get('name')}")
        print(f"Devices: {[d.get('name') for d in result.get('devices', [])]}")

    print("\n✓ Device loading complete!")

finally:
    sock.close()
