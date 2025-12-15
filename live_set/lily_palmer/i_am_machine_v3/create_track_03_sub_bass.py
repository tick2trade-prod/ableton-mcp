#!/usr/bin/env python3
"""
Track 03: Sub Bass - FM rolling bass with 16th note pattern

Creates FM bass using Operator, rolling 16th note pattern in F minor.
After running, you should HEAR the rolling bass interlocking with kick.

Usage: uv run python live_set/lily_palmer/i_am_machine_v3/create_track_03_sub_bass.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient


def create_sub_bass_track():
    """Create Track 03: Sub Bass with FM synthesis."""
    print("🎹 Creating Track 03: Sub Bass")
    print("=" * 50)

    client = AbletonMCPClient()

    # 1. Check connection
    print("\n1. Checking Ableton connection...")
    info = client.get_session_info()
    if not info.success:
        print(f"   ❌ Cannot connect: {info.message}")
        return False
    print(f"   ✅ Connected! Tempo: {info.data.get('tempo')} BPM")

    # 2. Create MIDI track
    print("\n2. Creating MIDI track...")
    track_name = "03 - Sub Bass"
    result = client.ensure_track(2, track_name, "midi")
    if not result.success:
        print(f"   ❌ Failed: {result.message}")
        return False
    print(f"   ✅ Track '{track_name}' created")

    # 3. Load Operator
    print("\n3. Loading Operator (FM synthesis)...")
    result = client.load_browser_item(
        track_index=2,
        item_uri="query:Instruments#FileId_2374",  # Operator
    )
    if result.success:
        print("   ✅ Operator loaded")
    else:
        print(f"   ⚠️  Operator failed: {result.message}")
        print("   → Manual: Load Operator from Instruments")

    # 4. Create 16th note rolling pattern (F minor)
    print("\n4. Creating rolling 16th note pattern (F minor)...")
    notes = []
    f_minor_scale = [53, 55, 56, 58, 60, 61, 63, 65]  # F, G, Ab, Bb, C, Db, Eb, F

    beat_count = 64  # 16 bars
    sixteenth_count = beat_count * 4  # 4 sixteenths per beat

    for i in range(sixteenth_count):
        # Rolling pattern: emphasize off-beats
        if i % 4 in [1, 3]:  # Off-beat 16ths
            pitch = f_minor_scale[i % len(f_minor_scale)]
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": i * 0.25,  # 16th notes = 0.25 beats apart
                    "duration": 0.2,  # Slightly shorter for pluck
                    "velocity": 90,
                }
            )

    result = client.create_pattern(
        track_index=2,
        clip_index=0,
        clip_name="FM Rolling (F minor)",
        notes=notes,
        length=64.0,
        fire=True,
    )

    if result.success:
        print(f"   ✅ Pattern created with {len(notes)} notes and PLAYING!")
    else:
        print(f"   ❌ Pattern failed: {result.message}")
        return False

    # Manual configuration
    print("\n5. Manual Operator configuration...")
    print("   Algorithm: 1 (vertical stack - series FM)")
    print("   Oscillator A (Carrier):")
    print("      - Wave: Sine")
    print("      - Decay: 600ms")
    print("   Oscillator B (Modulator):")
    print("      - Wave: Sine")
    print("      - Coarse: 2.0 (octave up)")
    print("      - Velocity modulation: ON")
    print("   Filter:")
    print("      - Type: Lowpass 24dB")
    print("      - Envelope Amount: 40%")
    print("      - Decay: 300ms (plucky attack)")
    print("   Add Compressor with sidechain to '01 - Kick'")

    # Summary
    print("\n" + "=" * 50)
    print("✅ Track 03: Sub Bass READY!")
    print("")
    print("🎧 YOU SHOULD HEAR:")
    print("   • Rolling 16th note pattern")
    print("   • FM plucky bass sound")
    print("   • F minor scale")
    print("   • Interlocking with kick rhythm")
    print("")
    print("⚠️  Manual: Configure Operator FM parameters")
    print("⚠️  Manual: Add sidechain compression to kick")
    print("=" * 50)

    return True


if __name__ == "__main__":
    success = create_sub_bass_track()
    sys.exit(0 if success else 1)
