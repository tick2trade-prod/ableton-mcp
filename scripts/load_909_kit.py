#!/usr/bin/env python3
"""Load 909 Core Kit onto Kick track."""

import json
import socket
import time

KICK_TRACK_INDEX = 5
KIT_909_URI = "query:Drums#FileId_14946"


def send_command(sock, command_type: str, params: dict = None):
    command = {"type": command_type, "params": params or {}}
    print(f"→ {command_type}: {params}")
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
                    print(f"  ✗ Error: {response.get('message')}")
                    return None
                print(f"  ✓ OK: {response.get('result', {})}")
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


print("Loading 909 Core Kit onto Kick track...\n")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(20)
sock.connect(("localhost", 9877))

try:
    # Load 909 Core Kit
    print("[1] Loading 909 Core Kit...")
    result = send_command(
        sock,
        "load_browser_item",
        {"track_index": KICK_TRACK_INDEX, "item_uri": KIT_909_URI},
    )
    time.sleep(2)

    # Check track devices
    print("\n[2] Checking track devices...")
    track = send_command(sock, "get_track_info", {"track_index": KICK_TRACK_INDEX})
    if track:
        devices = track.get("devices", [])
        print(f"\nDevices loaded: {len(devices)}")
        for d in devices:
            print(f"  - {d.get('name')}")

        if len(devices) > 0:
            print("\n✓ 909 Kit loaded successfully!")
        else:
            print("\n✗ No devices - try manually loading 909 Core Kit")

finally:
    sock.close()
