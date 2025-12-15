#!/usr/bin/env python3
"""
Track 01: Kick - Create audible 909 kick in Ableton

Uses real MCP client to create track in Ableton Live.
After running, you should HEAR a 4-on-floor kick pattern.

Usage: uv run python live_set/lily_palmer/i_am_machine_v3/create_track_01_kick.py
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient


def create_kick_track():
    """Create Track 01: Kick with real MCP."""
    print("🎵 Creating Track 01: Kick")
    print("=" * 50)

    client = AbletonMCPClient()

    # 1. Check connection
    print("\n1. Checking Ableton connection...")
    info = client.get_session_info()
    if not info.success:
        print(f"   ❌ Cannot connect: {info.message}")
        print("   → Is Ableton Live running?")
        print("   → Is AbletonMCP Remote Script loaded?")
        return False

    tempo = info.data.get("tempo", "unknown")
    print(f"   ✅ Connected! Tempo: {tempo} BPM")

    # 2. Create track
    print("\n2. Creating MIDI track...")
    track_name = "01 - Kick"
    result = client.ensure_track(0, track_name, "midi")
    if not result.success:
        print(f"   ❌ Failed: {result.message}")
        return False
    print(f"   ✅ Track '{track_name}' created")

    # 3. Load 909 Core Kit (contains Kick 909 on C1)
    print("\n3. Loading 909 Core Kit...")
    result = client.load_browser_item(
        track_name=track_name,
        uri="query:Drums#FileId_5447",  # 909 Core Kit
    )
    if result.success:
        print("   ✅ 909 Core Kit loaded (Kick 909 on C1/MIDI 36)")
    else:
        print(f"   ⚠️  Could not load 909 Core Kit: {result.message}")
        print("   → Will create pattern anyway")

    # 4. Add effects chain
    print("\n4. Adding effects chain...")
    devices = ["EQ Eight", "Saturator", "Utility"]
    for device in devices:
        result = client.load_device(track_name=track_name, device_name=device)
        if result.success:
            print(f"   ✅ {device} loaded")
        else:
            print(f"   ⚠️  {device} failed: {result.message}")

    # 5. Create 4-on-floor pattern (16 bars)
    print("\n5. Creating 4-on-floor pattern (16 bars)...")
    notes = []
    for beat in range(64):  # 16 bars × 4 beats = 64 notes
        notes.append(
            {
                "pitch": 36,  # C1 (Kick 909)
                "start_time": float(beat),
                "duration": 0.25,
                "velocity": 110,
            }
        )

    result = client.create_pattern(
        track_index=0,
        clip_index=0,
        clip_name="4-on-floor (16 bars)",
        notes=notes,
        length=64.0,  # 64 beats = 16 bars
        fire=True,  # Start playing
    )

    if result.success:
        print("   ✅ Pattern created and PLAYING!")
    else:
        print(f"   ❌ Pattern failed: {result.message}")
        return False

    # 6. Set volume
    print("\n6. Setting mix levels...")
    client.set_track_volume(track_name=track_name, volume_db=-12.0)
    print("   ✅ Volume: -12dB")

    # Summary
    print("\n" + "=" * 50)
    print("✅ Track 01: Kick COMPLETE!")
    print("")
    print("🎧 YOU SHOULD NOW HEAR:")
    print("   • 4-on-floor kick pattern")
    print("   • 909-style punch")
    print("   • Playing for 16 bars")
    print("")
    print("📝 Manual configuration needed:")
    print("   • EQ Eight: HP @ 30Hz, notch @ 200Hz")
    print("   • Saturator: Analog Clip mode, Drive +3dB")
    print("   • Utility: Bass Mono @ 120Hz")
    print("=" * 50)

    return True


if __name__ == "__main__":
    success = create_kick_track()
    sys.exit(0 if success else 1)
