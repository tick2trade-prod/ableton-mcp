#!/usr/bin/env python3
"""Explore Ableton browser for drum kits."""

import json
import socket


def send_command(sock, command_type: str, params: dict = None):
    command = {"type": command_type, "params": params or {}}
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

print("Exploring browser for drum kits...\n")

# Try get_browser_tree
result = send_command(sock, "get_browser_tree", {"category_type": "drums"})
if result:
    print("Browser tree:")
    print(json.dumps(result, indent=2)[:2000])
else:
    print("No browser tree result")

# Try get_browser_items_at_path
print("\n\nTrying get_browser_items_at_path...")
result = send_command(sock, "get_browser_items_at_path", {"path": "Drums"})
if result:
    print("Items at 'Drums':")
    print(json.dumps(result, indent=2)[:2000])

sock.close()
