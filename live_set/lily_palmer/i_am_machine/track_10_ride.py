#!/usr/bin/env python3
"""
Track 10: Ride Cymbal - Continuous ride for momentum.
Per spec: Ride with light touch, constant motion.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_10_ride.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "10-Ride"
TRACK_INDEX = 9

DEVICES = ["Drum Sampler", "Channel EQ", "Saturator"]

# 8th note ride pattern
NOTES = [
    {
        "pitch": 51,
        "start_time": float(i * 0.5),
        "duration": 0.4,
        "velocity": 75 + (15 if i % 2 == 0 else 0),
    }
    for i in range(32)
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

    client.create_pattern(TRACK_INDEX, 0, "8th Ride", NOTES, length=16.0, fire=True)
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
