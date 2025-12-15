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

    # Step 3: Try loading Drum Rack
    print("Step 3: Loading Drum Rack...")
    result = client.load_browser_item(track_index=0, item_uri="query:Drums#Drum%20Rack")
    if not result.success:
        print(f"❌ Drum Rack failed: {result.message}")
        print("   Trying alternative URI...")
        result = client.load_browser_item(track_index=0, item_uri="query:Drums")

    if result.success:
        print("✅ Drum Rack loaded!")
        print(f"   Data: {result.data}")
    else:
        print(f"❌ All Drum Rack attempts failed: {result.message}")
        return False

    print("\n" + "=" * 70)
    # Step 3.5: Load Kick 909 sample from Core Library
    print("\nStep 3.5: Loading Kick 909 sample from Core Library...")

    # Exact path from user's recommendation
    kick_sample_paths = [
        "Packs/Core Library/Drums/Samples/Kicks/Kick 909.aif",
        "Core Library/Drums/Samples/Kicks/Kick 909.aif",
        "Drums/Samples/Kicks/Kick 909",
    ]

    kick_loaded = False
    for sample_path in kick_sample_paths:
        print(f"   Trying: {sample_path}")
        result = client.send_command("get_browser_items_at_path", {"path": sample_path})

        if result.success:
            items = result.data.get("items", [])
            if items:
                # Try to load the first item
                uri = items[0].get("uri")
                print(f"   Found sample, loading with URI: {uri}")
                load_result = client.load_browser_item(track_index=0, item_uri=uri)
                if load_result.success:
                    print("   ✅ Kick 909 loaded!")
                    kick_loaded = True
                    break

    if not kick_loaded:
        print("   ⚠️  Could not auto-load kick - trying direct URI...")
        # Try direct browser query
        for uri in ["query:Drums/Samples/Kicks#Kick%20909", "query:Samples#Kick"]:
            result = client.load_browser_item(track_index=0, item_uri=uri)
            if result.success:
                print(f"   ✅ Loaded via URI: {uri}")
                kick_loaded = True
                break

    if not kick_loaded:
        print("   ⚠️  Manual intervention needed: Drag Kick 909.aif onto C1 pad")

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
