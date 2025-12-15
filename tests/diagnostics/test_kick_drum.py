#!/usr/bin/env python3
"""Diagnostic test for kick drum loading.

Tests the exact MCP commands needed to create an audible kick drum.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "i_am_machine"))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient


def test_kick_drum_creation():
    """Test creating Track 01 with audible kick drum."""
    print("\n" + "=" * 70)
    print("DIAGNOSTIC: Track 01 - Kick Drum Creation")
    print("=" * 70 + "\n")

    client = AbletonMCPClient()

    # Step 1: Connection test
    print("Step 1: Testing connection...")
    result = client.get_session_info()
    if not result.success:
        print(f"❌ Connection failed: {result.message}")
        return False
    print(f"✅ Connected! Tempo: {result.data.get('tempo')} BPM\n")

    # Step 2: Create MIDI track
    print("Step 2: Creating MIDI track at index 0...")
    result = client.ensure_track(
        target_index=0, name="Track 01 - Kick", track_type="midi"
    )
    if not result.success:
        print(f"❌ Track creation failed: {result.message}")
        return False
    print(f"✅ Track created: {result.message}\n")

    # Step 3: Load 909 Core Kit (has kicks, snares, hats pre-loaded!)
    print("\nStep 3: Loading 909 Core Kit Drum Rack...")
    result = client.load_browser_item(
        track_index=0,
        item_uri="query:Drums#FileId_5447",  # 909 Core Kit.adg
    )

    if not result.success:
        print(f"❌ 909 Kit failed: {result.message}")
        print("   Trying generic Drum Rack...")
        result = client.load_browser_item(
            track_index=0, item_uri="query:Drums#Drum%20Rack"
        )

    if result.success:
        print(f"✅ Loaded: {result.data.get('item_name')}")
        print("   (Should have kick on C1, snare on D1, hats on F#1/G#1)")
    else:
        print(f"❌ Failed: {result.message}")
        return False

    print("\n" + "=" * 70)

    print("\n✨ 909 Core Kit has samples pre-loaded on pads!")
    print("   C1 (note 36) = Kick")
    print("   D1 (note 38) = Snare")
    print("   F#1 (note 42) = Closed Hi-Hat")
    print("   G#1 (note 44) = Open Hi-Hat")

    print("\n" + "=" * 70)

    # Step 4: Clear any existing clips
    print("\nStep 4: Clearing existing clips...")
    try:
        result = client.send_command("remove_clip", {"track_index": 0, "clip_index": 0})
        if result.success:
            print("✅ Cleared clip slot 0")
        else:
            print("⚠️  Clip slot might be empty (this is fine)")
    except Exception as e:
        print(f"⚠️  Could not clear clip: {e} (continuing anyway)")

    # Step 5: Create simple kick pattern
    print("\nStep 5: Creating kick pattern (4-on-floor)...")
    kick_notes = [
        {
            "pitch": 36,
            "start_time": 0.0,
            "duration": 0.25,
            "velocity": 100,
            "mute": False,
        },
        {
            "pitch": 36,
            "start_time": 1.0,
            "duration": 0.25,
            "velocity": 100,
            "mute": False,
        },
        {
            "pitch": 36,
            "start_time": 2.0,
            "duration": 0.25,
            "velocity": 100,
            "mute": False,
        },
        {
            "pitch": 36,
            "start_time": 3.0,
            "duration": 0.25,
            "velocity": 100,
            "mute": False,
        },
    ]

    result = client.create_pattern(
        track_index=0,
        clip_index=0,
        clip_name="Kick Pattern",
        notes=kick_notes,
        length=4.0,
        fire=True,  # Auto-fire the clip!
    )

    if result.success:
        print("✅ Kick pattern created and FIRED!")
        print("   🔊 You should hear the kick playing now!")
    else:
        print(f"❌ Pattern creation failed: {result.message}")
        return False

    print("\n" + "=" * 70)
    print("✅ SUCCESS! Track 01 - Kick is playing!")
    print("   🎵 Listen for the 4-on-floor kick pattern")
    print("=" * 70 + "\n")

    return True


if __name__ == "__main__":
    success = test_kick_drum_creation()
    sys.exit(0 if success else 1)
