#!/usr/bin/env python3
"""
Track 09: Glitch/Noise Percussion - Industrial texture and chaos.
Per spec: Beat Repeat, random noise bursts.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_09_glitch.py
"""

import random

from ableton_client import AbletonMCPClient

TRACK_NAME = "09-Glitch"
TRACK_INDEX = 8

DEVICES = ["Simpler", "Beat Repeat", "Phaser", "Delay"]

# Random glitch hits
random.seed(42)  # Reproducible randomness
NOTES = [
    {
        "pitch": random.randint(60, 72),
        "start_time": float(random.uniform(0, 16)),
        "duration": 0.05,
        "velocity": random.randint(70, 120),
    }
    for _ in range(24)
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

    client.create_pattern(TRACK_INDEX, 0, "Glitch Hits", NOTES, length=16.0, fire=True)
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nBeat Repeat: Chance 30%, Interval 1/16")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
