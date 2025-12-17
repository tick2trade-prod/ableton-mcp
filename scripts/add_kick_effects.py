#!/usr/bin/env python3
"""Add processing effects to Kick track: Drum Buss, Saturator."""

import json
import socket
import time

KICK_TRACK_INDEX = 5


def send_command(sock, command_type: str, params: dict = None):
    command = {"type": command_type, "params": params or {}}
    print(f"→ {command_type}")
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


print("Adding processing effects to Kick track...\n")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(20)
sock.connect(("localhost", 9877))

try:
    # First, explore Audio Effects to find URIs
    print("[1] Finding Audio Effects URIs...")
    result = send_command(sock, "get_browser_items_at_path", {"path": "Audio Effects"})

    drum_buss_uri = None
    saturator_uri = None

    if result:
        items = result.get("items", [])
        for item in items:
            name = item.get("name", "")
            uri = item.get("uri", "")
            if "Drum Buss" in name:
                drum_buss_uri = uri
                print(f"  Found Drum Buss: {uri}")
            elif name == "Saturator":
                saturator_uri = uri
                print(f"  Found Saturator: {uri}")

    # Load Drum Buss
    if drum_buss_uri:
        print("\n[2] Loading Drum Buss...")
        send_command(
            sock,
            "load_browser_item",
            {"track_index": KICK_TRACK_INDEX, "item_uri": drum_buss_uri},
        )
        time.sleep(1)
    else:
        print("\n[2] Drum Buss URI not found, trying default...")
        send_command(
            sock,
            "load_browser_item",
            {
                "track_index": KICK_TRACK_INDEX,
                "item_uri": "query:Audio Effects#Drum Buss",
            },
        )
        time.sleep(1)

    # Load Saturator
    if saturator_uri:
        print("\n[3] Loading Saturator...")
        send_command(
            sock,
            "load_browser_item",
            {"track_index": KICK_TRACK_INDEX, "item_uri": saturator_uri},
        )
        time.sleep(1)
    else:
        print("\n[3] Saturator URI not found, trying default...")
        send_command(
            sock,
            "load_browser_item",
            {
                "track_index": KICK_TRACK_INDEX,
                "item_uri": "query:Audio Effects#Saturator",
            },
        )
        time.sleep(1)

    # Verify devices
    print("\n[4] Verifying devices...")
    track = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if track:
        devices = track.get("devices", [])
        print(f"\nDevices on Kick track: {len(devices)}")
        for d in devices:
            print(f"  - {d.get('name')} ({d.get('class_name')})")

finally:
    sock.close()
