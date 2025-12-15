#!/usr/bin/env python3
"""Find the correct URI for Kick 909 sample."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "i_am_machine"))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

client = AbletonMCPClient()

print("\n=== Finding Kick 909 Sample ===\n")

# Try browsing the samples category
paths_to_try = [
    "Drums",
    "Drums/Samples",
    "Drums/Samples/Kicks",
]

for path in paths_to_try:
    print(f"\n--- Browsing: {path} ---")
    result = client.send_command("get_browser_items_at_path", {"path": path})

    if result.success:
        items = result.data.get("items", [])
        print(f"Found {len(items)} items")

        if path == "Drums":
            # Show first 30 items to see structure
            print("\nFirst 30 items:")
            for i, item in enumerate(items[:30]):
                name = item.get("name", "")
                uri = item.get("uri", "")
                is_folder = item.get("is_folder", False)
                loadable = item.get("is_loadable", False)
                print(
                    f"{i + 1}. {name} ({'folder' if is_folder else 'loadable' if loadable else 'other'}) - {uri}"
                )

        # Look for Kick 909
        kick_items = [
            item
            for item in items
            if "Kick" in item.get("name", "") or "kick" in item.get("name", "")
        ]
        if kick_items:
            print(f"\n🎯 Found {len(kick_items)} kick items:")
            for item in kick_items[:5]:  # Show first 5
                print(
                    f"   {item.get('name')} - {item.get('uri')} (loadable: {item.get('is_loadable')})"
                )
    else:
        print(f"Failed: {result.data}")
