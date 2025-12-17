#!/usr/bin/env python3
"""Explore Ableton browser to find device URIs."""

import json
import socket


def send_command(sock, command_type: str, params: dict = None):
    """Send MCP command and return result."""
    command = {"type": command_type, "params": params or {}}
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
                    print(f"Error: {response.get('message')}")
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

print("Exploring Ableton Browser...\n")

# Get browser tree
result = send_command(sock, "get_browser_tree", {})

if result:
    print("Browser Categories:")
    for key, value in result.items():
        if isinstance(value, dict):
            name = value.get("name", key)
            uri = value.get("uri", "N/A")
            children_count = len(value.get("children", []))
            print(f"\n  {key}: {name}")
            print(f"    URI: {uri}")
            print(f"    Children: {children_count}")

            # Show first few children
            children = value.get("children", [])[:5]
            for child in children:
                if isinstance(child, dict):
                    name = child.get('name', 'unnamed')
                    uri = child.get('uri', 'no uri')
                    print(f"      - {name}: {uri}")

sock.close()
