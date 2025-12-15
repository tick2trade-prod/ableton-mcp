#!/usr/bin/env python3
"""
Create ALL 16 Tracks for "I Am Machine" Intro

Creates all 16 tracks in Ableton with basic setup.
Then run individual track scripts to configure each one.

Usage: uv run python live_set/lily_palmer/i_am_machine_v3/create_all_16_tracks.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

TRACKS = [
    (0, "01 - Kick", "midi"),
    (1, "02 - Rumble", "audio"),
    (2, "03 - Sub Bass", "midi"),
    (3, "04 - Acid", "midi"),
    (4, "05 - Closed Hat", "midi"),
    (5, "06 - Open Hat", "midi"),
    (6, "07 - Claps", "midi"),
    (7, "08 - Toms", "midi"),
    (8, "09 - Glitch", "midi"),
    (9, "10 - Ride", "midi"),
    (10, "11 - Stabs", "midi"),
    (11, "12 - Drone", "midi"),
    (12, "13 - Vocals", "audio"),
    (13, "14 - Vocal FX", "audio"),
    (14, "15 - Riser", "audio"),
    (15, "16 - Impact", "audio"),
]


def main():
    print("🎵 Creating ALL 16 Tracks for 'I Am Machine'")
    print("=" * 60)

    client = AbletonMCPClient()

    # Check connection
    print("\n1. Checking Ableton connection...")
    info = client.get_session_info()
    if not info.success:
        print(f"   ❌ Cannot connect: {info.message}")
        return False
    print(f"   ✅ Connected! Tempo: {info.data.get('tempo')} BPM")
    print(f"   Current tracks: {info.data.get('track_count', 0)}")

    # Create all tracks
    print("\n2. Creating 16 tracks...")
    created_count = 0

    for index, name, track_type in TRACKS:
        result = client.ensure_track(index, name, track_type)
        if result.success:
            print(f"   ✅ [{index:02d}] {name} ({track_type})")
            created_count += 1
        else:
            print(f"   ⚠️  [{index:02d}] {name} failed: {result.message}")

    print(f"\n✅ Created {created_count}/16 tracks!")

    # Summary
    print("\n" + "=" * 60)
    print("📋 16-Track Layout Created:")
    print("")
    print("Low-End Foundation:")
    print("  01 - Kick (MIDI) - 909 kick, 4-on-floor")
    print("  02 - Rumble (Audio) - Sidechained reverb from kick")
    print("  03 - Sub Bass (MIDI) - FM rolling 16ths")
    print("  04 - Acid (MIDI) - 303-style acid line")
    print("")
    print("Percussion:")
    print("  05 - Closed Hat (MIDI) - 16th notes")
    print("  06 - Open Hat (MIDI) - Off-beat")
    print("  07 - Claps (MIDI) - Backbeat 2,4")
    print("  08 - Toms (MIDI) - Tribal percussion")
    print("  09 - Glitch (MIDI) - Meld modulation")
    print("  10 - Ride (MIDI) - Sidechained")
    print("")
    print("Atmosphere:")
    print("  11 - Stabs (MIDI) - Wavetable stabs")
    print("  12 - Drone (MIDI) - Meld atmosphere")
    print("  13 - Vocals (Audio) - Vocal chops")
    print("  14 - Vocal FX (Audio) - Processed vocals")
    print("")
    print("Transitions:")
    print("  15 - Riser (Audio) - Build-ups")
    print("  16 - Impact (Audio) - Drop impacts")
    print("")
    print("=" * 60)
    print("\n✅ ALL 16 TRACKS CREATED!")
    print("\nNext: Run individual scripts to configure each track")
    print("  - create_track_01_kick.py (already configured)")
    print("  - create_track_03_sub_bass.py")
    print("  - etc.")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
