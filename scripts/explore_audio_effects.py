#!/usr/bin/env python3
"""Explore Audio Effects in browser."""

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
                    print(f"Error: {response.get('message')}")
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

# Try browser tree for audio_effects
print("Getting browser tree for audio_effects...")
result = send_command(sock, "get_browser_tree", {"category_type": "audio_effects"})
if result:
    print(json.dumps(result, indent=2)[:3000])

sock.close()
