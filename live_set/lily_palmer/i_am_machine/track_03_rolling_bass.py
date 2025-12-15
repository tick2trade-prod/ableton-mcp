#!/usr/bin/env python3
"""
Track 03: Rolling Bass - The perpetual motion 16th-note F minor bassline.
Per spec: Operator/FM, 16th notes, sub 40-50Hz, sidechain ducking.

Optimized version using shared AbletonMCPClient.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_03_rolling_bass.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "03-RollingBass"
TRACK_INDEX = 2

# Device chain for FM bass
DEVICES = [
    "Operator",  # FM synthesis for buzzy bass
    "Channel EQ",  # HPF @ 30Hz, roll off highs
    "Saturator",  # Warm harmonics
    "Compressor",  # Glue + sidechain to kick
]

# F minor 16th note pattern over 4 bars
# F1=29, Ab1=32, C2=36 (F minor triad root notes)
F_MINOR_PATTERN = [29, 32, 34, 36, 39, 41, 36, 34] * 8  # 64 16th notes
NOTES = [
    {
        "pitch": F_MINOR_PATTERN[i],
        "start_time": float(i * 0.25),  # 16th note grid
        "duration": 0.2,
        "velocity": 90 + (5 if i % 4 == 0 else 0),  # Accent on beats
    }
    for i in range(64)
]


def main():
    print(f"=== Creating {TRACK_NAME} ===")

    client = AbletonMCPClient()

    # 1. Verify connection
    info = client.get_session_info()
    if not info.success:
        print(f"   ✗ Cannot connect: {info.message}")
        return False

    # 2. Create MIDI track
    result = client.ensure_track(TRACK_INDEX, TRACK_NAME, "midi")
    if not result.success:
        print(f"   ✗ Failed: {result.message}")
        return False
    print(f"   ✓ Track '{TRACK_NAME}' at index {TRACK_INDEX}")

    # 3. Load device chain
    print("   Loading devices:")
    client.load_device_chain(TRACK_INDEX, DEVICES)

    # 4. Create rolling bass pattern
    result = client.create_pattern(
        track_index=TRACK_INDEX,
        clip_index=0,
        clip_name="Rolling Bass",
        notes=NOTES,
        length=16.0,
        fire=True,
    )
    if result.success:
        print("   ✓ Rolling bass pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nOperator settings:")
    print("  Algorithm: 1 (FM modulation)")
    print("  Osc A: Sine @ 43Hz (F1)")
    print("  Osc B: Sine, Coarse ratio 2x, Level 40%")
    print("  Filter: None (pure sub)")
    print("  Compressor: Sidechain from 01-Kick")

    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
