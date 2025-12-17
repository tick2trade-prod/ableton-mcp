#!/usr/bin/env python3
"""Find Audio Effects URIs in browser."""

import json
import socket


def send_command(sock, command_type: str, params: dict = None):
    command = {"type": command_type, "params": params or {}}
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
                    return None
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(20)
sock.connect(("localhost", 9877))

print("Finding Audio Effects URIs...\n")

result = send_command(sock, "get_browser_items_at_path", {"path": "Audio Effects"})

if result:
    items = result.get("items", [])
    print(f"Found {len(items)} items in Audio Effects:\n")

    # Print all items looking for Drum Buss and Saturator
    for item in items:
        name = item.get("name", "")
        uri = item.get("uri", "")
        loadable = item.get("is_loadable", False)

        # Filter for relevant effects
        if any(
            keyword in name.lower() for keyword in ["drum", "satur", "compress", "eq"]
        ):
            print(f"  {name}")
            print(f"    URI: {uri}")
            print(f"    Loadable: {loadable}")
            print()
else:
    print("No results from get_browser_items_at_path")

sock.close()
