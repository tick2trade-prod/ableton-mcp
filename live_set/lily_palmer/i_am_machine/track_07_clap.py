#!/usr/bin/env python3
"""
Track 07: Clap - Industrial clap on beats 2 and 4.
Per spec: Layered clap with short reverb tail.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_07_clap.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "07-Clap"
TRACK_INDEX = 6

DEVICES = ["Drum Sampler", "Reverb", "Channel EQ"]

# Claps on 2 and 4 (backbeat)
NOTES = [
    {
        "pitch": 39,
        "start_time": float(bar * 4 + beat),
        "duration": 0.25,
        "velocity": 105,
    }
    for bar in range(4)
    for beat in [1, 3]  # Beats 2 and 4 (0-indexed: 1 and 3)
]


def main():
    print(f"=== Creating {TRACK_NAME} ===")
    client = AbletonMCPClient()

    if not client.get_session_info().success:
        return False

    client.ensure_track(TRACK_INDEX, TRACK_NAME, "midi")
    print(f"   ✓ Track '{TRACK_NAME}'")

    print("   Loading devices:")
    client.load_device_chain(TRACK_INDEX, DEVICES)

    client.create_pattern(
        TRACK_INDEX, 0, "Backbeat Clap", NOTES, length=16.0, fire=True
    )
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nReverb settings: Room, Decay 300ms, 20% Wet")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
