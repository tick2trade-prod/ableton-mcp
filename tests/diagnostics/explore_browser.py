#!/usr/bin/env python3
"""Explore Ableton browser to find drum rack presets with samples."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "i_am_machine"))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

client = AbletonMCPClient()

print("\n=== Exploring Drums Browser ===\n")

# Get browser tree
result = client.send_command("get_browser_tree", {"category_type": "drums"})
if result.success:
    print("Drums browser structure:")
    print(result.data)
else:
    print(f"Failed: {result.message}")

print("\n=== Trying to browse Drums category ===\n")

# Browse drums path
result = client.send_command("get_browser_items_at_path", {"path": "drums"})
if result.success:
    print("Items in 'drums':")
    items = result.data.get("items", [])
    for item in items[:20]:  # Show first 20
        print(
            f"  - {item.get('name')} (loadable: {item.get('is_loadable')}, uri: {item.get('uri')})"
        )
else:
    print(f"Failed: {result.data}")
