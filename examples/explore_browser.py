#!/usr/bin/env python3
"""Extended browser exploration to find all available categories."""

import json
import os
import socket
import sys

# Add tests root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tests.config import ABLETON_HOST, ABLETON_PORT, SOCKET_TIMEOUT  # noqa: E402


def send_command(cmd_type, params=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SOCKET_TIMEOUT)
    try:
        sock.connect((ABLETON_HOST, ABLETON_PORT))
        cmd = {"type": cmd_type, "params": params or {}}
        sock.sendall(json.dumps(cmd).encode())

        response = b""
        while True:
            chunk = sock.recv(32768)
            if not chunk:
                break
            response += chunk
            if response.strip().endswith(b"}") and response.count(
                b"{"
            ) == response.count(b"}"):
                break
        return json.loads(response.decode())
    finally:
        sock.close()


# Get browser tree to see all categories
print("\n🌳 Getting Browser Tree...")
res = send_command("get_browser_tree", {"category_type": "all"})
if res.get("status") == "success":
    categories = res["result"].get("categories", [])
    print(f"\nFound {len(categories)} root categories:")
    for cat in categories:
        print(f"\n  📁 {cat['name']}")
        if cat.get("children"):
            for child in cat["children"][:10]:
                print(f"    - {child.get('name', 'Unknown')}")
            if len(cat.get("children", [])) > 10:
                print(f"    ... and {len(cat['children']) - 10} more")

# Try to find 808 kit specifically
print("\n\n🔍 Searching for 808 Core Kit...")
res = send_command("get_browser_items_at_path", {"path": "drums"})
if res.get("status") == "success":
    items = res["result"].get("items", [])
    for item in items:
        if "808" in item.get("name", "") and "Core" in item.get("name", ""):
            print(f"  ✓ Found: {item['name']}")
            print(f"    URI: {item['uri']}")

# Check what's in instruments
print("\n\n🎹 Available Instruments:")
res = send_command("get_browser_items_at_path", {"path": "instruments"})
if res.get("status") == "success":
    items = res["result"].get("items", [])
    for item in items:
        if item.get("is_loadable"):
            print(f"  - {item['name']}: {item['uri']}")
