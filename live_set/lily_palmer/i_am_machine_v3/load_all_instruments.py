#!/usr/bin/env python3
"""
Load instruments for all tracks 01-12

Loads the correct instruments/drum kits for each track so they sound right.

Usage: uv run python live_set/lily_palmer/i_am_machine_v3/load_all_instruments.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

# Instrument configurations
INSTRUMENTS = [
    (0, "01 - Kick", "query:Drums#FileId_5447"),  # 909 Core Kit
    # Track 02 is audio, skip
    (2, "03 - Sub Bass", "query:Instruments#FileId_2374"),  # Operator
    (3, "04 - Acid", "query:Instruments#FileId_2374"),  # Operator (or Drift if found)
    (4, "05 - Closed Hat", "query:Drums#FileId_5447"),  # 909 Core Kit
    (5, "06 - Open Hat", "query:Drums#FileId_5447"),  # 909 Core Kit
    (6, "07 - Claps", "query:Drums#FileId_5447"),  # 909 Core Kit
    (7, "08 - Toms", "query:Drums#FileId_5447"),  # 909 Core Kit
    (8, "09 - Glitch", "query:Instruments#FileId_2374"),  # Operator (placeholder)
    (9, "10 - Ride", "query:Drums#FileId_5447"),  # 909 Core Kit
    (10, "11 - Stabs", "query:Instruments#FileId_2468"),  # Wavetable
    (11, "12 - Drone", "query:Instruments#FileId_2374"),  # Operator
]


def main():
    print("🎹 Loading Instruments for All Tracks")
    print("=" * 60)

    client = AbletonMCPClient()

    # Check connection
    info = client.get_session_info()
    if not info.success:
        print(f"❌ Cannot connect: {info.message}")
        return False
    print("✅ Connected!\n")

    loaded_count = 0

    for index, name, uri in INSTRUMENTS:
        print(f"[{index:02d}] {name}")
        result = client.load_browser_item(index, uri)

        if result.success:
            print("     ✅ Instrument loaded")
            loaded_count += 1
        else:
            print(f"     ⚠️  Failed: {result.message}")
            print("     → Manual: Load instrument in Ableton")
        print()

    print("=" * 60)
    print(f"✅ Loaded {loaded_count}/{len(INSTRUMENTS)} instruments")
    print("\n📝 Next steps:")
    print("  1. Set 'Audio To' → 'Main' for all tracks")
    print("  2. Adjust volumes as needed")
    print("  3. Add effects chains")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
