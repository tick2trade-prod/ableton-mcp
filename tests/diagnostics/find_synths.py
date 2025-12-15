#!/usr/bin/env python3
"""Find available synth instruments in browser."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "i_am_machine"))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

client = AbletonMCPClient()


print("\n=== Finding Synth Instruments ===\n")

# Browse both Instruments and Sounds
for category in ["Instruments", "Sounds"]:
    print(f"\n--- Category: {category} ---")
    result = client.send_command("get_browser_items_at_path", {"path": category})

    if result.success:
        items = result.data.get("items", [])
        print(f"Found {len(items)} items")

        # Look for bass/lead/pad presets
        if category == "Sounds":
            for keyword in ["Bass", "Lead", "Pad", "Synth"]:
                matches = [item for item in items if keyword in item.get("name", "")][
                    :3
                ]
                if matches:
                    print(f"\n{keyword}:")
                    for item in matches:
                        name = item.get("name", "")
                        uri = item.get("uri", "")
                        loadable = item.get("is_loadable", False)
                        print(f"  {'✓' if loadable else '·'} {name} - {uri}")
        else:
            # Show all instruments
            for item in items[:15]:
                name = item.get("name", "")
                uri = item.get("uri", "")
                print(f"  {name} - {uri}")
    else:
        print(f"Failed: {result.data}")
