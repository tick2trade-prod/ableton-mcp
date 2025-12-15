#!/usr/bin/env python3
"""
Track 04: Acid Line - Classic 303-style acid with resonant filter.
Per spec: Operator/Drift in 303 mode, Auto Filter, Chorus.

Optimized version using shared AbletonMCPClient.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_04_acid.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "04-Acid"
TRACK_INDEX = 3

# Device chain for acid sound
DEVICES = [
    ("Drift", "Operator"),  # Drift preferred, Operator fallback
    "Auto Filter",  # Resonant LP sweep
    "Chorus",  # Stereo width
    "Compressor",
]

# Classic acid pattern with slides and accents
# F minor with chromatic passing tones
ACID_NOTES = [
    29,
    29,
    32,
    33,
    29,
    36,
    34,
    32,  # Variation 1
    29,
    32,
    29,
    36,
    33,
    29,
    32,
    34,  # Variation 2
] * 4  # 4 bars

NOTES = [
    {
        "pitch": ACID_NOTES[i],
        "start_time": float(i * 0.25),
        "duration": 0.15 if i % 2 == 0 else 0.25,  # Short/long variation
        "velocity": 100 if i % 4 == 0 else 80,
    }
    for i in range(64)
]


def main():
    print(f"=== Creating {TRACK_NAME} ===")

    client = AbletonMCPClient()

    info = client.get_session_info()
    if not info.success:
        print(f"   ✗ Cannot connect: {info.message}")
        return False

    result = client.ensure_track(TRACK_INDEX, TRACK_NAME, "midi")
    if not result.success:
        print(f"   ✗ Failed: {result.message}")
        return False
    print(f"   ✓ Track '{TRACK_NAME}' at index {TRACK_INDEX}")

    print("   Loading devices:")
    for device in DEVICES:
        if isinstance(device, tuple):
            primary, fallback = device
            result = client.load_device(TRACK_INDEX, primary, fallback=fallback)
            symbol = "✓" if result.success else "↳"
            print(f"     {symbol} {primary if result.success else fallback}")
        else:
            result = client.load_device(TRACK_INDEX, device)
            symbol = "✓" if result.success else "✗"
            print(f"     {symbol} {device}")

    result = client.create_pattern(
        track_index=TRACK_INDEX,
        clip_index=0,
        clip_name="Acid Line",
        notes=NOTES,
        length=16.0,
        fire=True,
    )
    if result.success:
        print("   ✓ Acid pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nAuto Filter settings:")
    print("  Type: LP 12dB")
    print("  Frequency: Automate 200Hz → 8kHz")
    print("  Resonance: 60-70%")
    print("  Envelope: Amount 50%, Attack 0, Decay 150ms")

    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
