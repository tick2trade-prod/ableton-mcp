#!/usr/bin/env python3
"""
Track 02: Rumble - Industrial rumble from sidechained kick reverb

Creates audio track that receives from kick, processes with Roar.
After running, you should HEAR the rumble pumping with the kick.

Usage: uv run python live_set/lily_palmer/i_am_machine_v3/create_track_02_rumble.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient


def create_rumble_track():
    """Create Track 02: Rumble with audio routing from kick."""
    print("🌊 Creating Track 02: Rumble")
    print("=" * 50)

    client = AbletonMCPClient()

    # 1. Check connection
    print("\n1. Checking Ableton connection...")
    info = client.get_session_info()
    if not info.success:
        print(f"   ❌ Cannot connect: {info.message}")
        return False
    print(f"   ✅ Connected! Tempo: {info.data.get('tempo')} BPM")

    # 2. Create audio track
    print("\n2. Creating audio track...")
    track_name = "02 - Rumble"
    result = client.ensure_track(1, track_name, "audio")
    if not result.success:
        print(f"   ❌ Failed: {result.message}")
        return False
    print(f"   ✅ Track '{track_name}' created")

    # 3. Set audio input routing (from Track 01 - Kick)
    print("\n3. Setting audio input routing...")
    print("   Manual: In Ableton, set Audio From: '01 - Kick' → Post FX")
    print("   Manual: Set Monitor to 'In'")

    # 4. Add processing chain
    print("\n4. Adding processing chain...")
    # Note: load_device API not working, manual setup needed
    print("   Manual: Load these devices in order:")
    print("   1. Hybrid Reverb")
    print("      - Engine: Convolution")
    print("      - IR: Dark Hall")
    print("      - Decay: 1.2s")
    print("      - Pre-delay: 10ms")
    print("      - Mix: 100% Wet")
    print("   2. Roar (CRITICAL for industrial texture!)")
    print("      - Low Band: Tube saturation")
    print("      - Mid Band: Diode clipping")
    print("      - Feedback: 15%")
    print("   3. EQ Eight")
    print("      - Lowpass @ 150Hz (aggressive)")
    print("   4. Compressor")
    print("      - Sidechain: Audio From '01 - Kick'")
    print("      - Ratio: Infinite:1")
    print("      - Attack: 0.1ms")
    print("      - Release: 1/8 (synced)")

    # Summary
    print("\n" + "=" * 50)
    print("✅ Track 02: Rumble READY!")
    print("")
    print("🎧 AFTER MANUAL SETUP, YOU SHOULD HEAR:")
    print("   • Reverb tail from kick")
    print("   • Industrial, gritty texture (Roar)")
    print("   • Pumping/ducking with kick (sidechain)")
    print("   • Contained below 150Hz")
    print("")
    print("⚠️  CRITICAL: Manual setup required for:")
    print("   • Audio routing (Audio From: '01 - Kick')")
    print("   • All 4 devices (Hybrid Reverb, Roar, EQ Eight, Compressor)")
    print("   • Sidechain routing to kick")
    print("=" * 50)

    return True


if __name__ == "__main__":
    success = create_rumble_track()
    sys.exit(0 if success else 1)
