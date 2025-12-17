#!/usr/bin/env python3
"""Load effects using correct URI format."""

import json
import socket
import time

KICK_TRACK_INDEX = 5


def send_command(sock, command_type: str, params: dict = None):
    command = {"type": command_type, "params": params or {}}
    print(f"→ {command_type}: {params.get('item_uri', params) if params else ''}")
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
sock.settimeout(20)
sock.connect(("localhost", 9877))

print("Loading effects with correct URI format...\n")

# First, explore AudioFx to find the items
print("[1] Getting AudioFx items...")
result = send_command(sock, "get_browser_items_at_path", {"path": "AudioFx"})

if result:
    items = result.get("items", [])
    print(f"  Found {len(items)} items")

    drum_buss_uri = None
    saturator_uri = None

    for item in items:
        name = item.get("name", "")
        uri = item.get("uri", "")
        if "Drum Buss" in name:
            drum_buss_uri = uri
            print(f"  → Drum Buss: {uri}")
        elif name == "Saturator":
            saturator_uri = uri
            print(f"  → Saturator: {uri}")

    # Load effects
    if drum_buss_uri:
        print("\n[2] Loading Drum Buss...")
        send_command(
            sock,
            "load_browser_item",
            {"track_index": KICK_TRACK_INDEX, "item_uri": drum_buss_uri},
        )
        time.sleep(1.5)

    if saturator_uri:
        print("\n[3] Loading Saturator...")
        send_command(
            sock,
            "load_browser_item",
            {"track_index": KICK_TRACK_INDEX, "item_uri": saturator_uri},
        )
        time.sleep(1.5)

# Verify
print("\n[4] Checking devices...")
track = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
if track:
    devices = track.get("devices", [])
    print(f"\nDevices on Kick: {len(devices)}")
    for d in devices:
        print(f"  - {d.get('name')}")

sock.close()
