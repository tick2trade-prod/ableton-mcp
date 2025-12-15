#!/usr/bin/env python3
"""
Track 01: Anchor Kick - The metronomic anchor with sharp transient and sub punch.
Per spec: 909-style kick, F1 (43Hz), short decay (350ms), pitch envelope +18st/15ms.

Optimized version using shared AbletonMCPClient.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_01_kick.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "01-Kick"
TRACK_INDEX = 0

# Device chain for punchy 909-style kick
DEVICES = [
    "Drum Sampler",  # Core: 909-style kick sample
    "Channel EQ",  # HP @ 30Hz, notch @ 200Hz
    "Saturator",  # Analog Clip mode, +3dB drive
    "Utility",  # Bass Mono @ 120Hz
]

# 4-on-floor kick pattern: 16 quarter notes over 4 bars
NOTES = [
    {"pitch": 36, "start_time": float(i), "duration": 0.25, "velocity": 110}
    for i in range(16)  # C1 (36) on every beat
]


def main():
    print(f"=== Creating {TRACK_NAME} ===")

    client = AbletonMCPClient()

    # 1. Verify connection
    info = client.get_session_info()
    if not info.success:
        print(f"   ✗ Cannot connect to Ableton: {info.message}")
        return False
    print(f"   Tempo: {info.data.get('tempo')} BPM")

    # 2. Create/ensure track
    result = client.ensure_track(TRACK_INDEX, TRACK_NAME, "midi")
    if not result.success:
        print(f"   ✗ Failed to create track: {result.message}")
        return False
    print(f"   ✓ Track created at index {TRACK_INDEX}")

    # 3. Load device chain
    print("   Loading devices:")
    client.load_device_chain(TRACK_INDEX, DEVICES)

    # 4. Create 4-on-floor pattern
    result = client.create_pattern(
        track_index=TRACK_INDEX,
        clip_index=0,
        clip_name="4-on-floor",
        notes=NOTES,
        length=16.0,
        fire=True,
    )
    if result.success:
        print("   ✓ 4-on-floor pattern created and playing")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nDevice settings to configure:")
    print("  Drum Sampler: Load 909 kick, Decay ~350ms")
    print("  Channel EQ: HP @ 30Hz, -3dB @ 200Hz")
    print("  Saturator: Analog Clip, Drive +3dB")
    print("  Utility: Bass Mono @ 120Hz")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
