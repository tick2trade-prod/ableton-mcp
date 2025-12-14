#!/usr/bin/env python3
"""
Track 05: Closed Hi-Hats - Tight, driving 16th note hats.
Per spec: Drum Sampler, 16th notes with velocity variation.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_05_closed_hats.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "05-ClosedHats"
TRACK_INDEX = 4

DEVICES = ["Drum Sampler", "Channel EQ", "Saturator"]

# 16th note hi-hats with velocity variation
NOTES = [
    {
        "pitch": 42,  # Closed hi-hat
        "start_time": float(i * 0.25),
        "duration": 0.1,
        "velocity": 80 + (25 if i % 4 == 0 else 0) - (10 if i % 2 == 1 else 0),
    }
    for i in range(64)
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

    client.create_pattern(TRACK_INDEX, 0, "16th Hats", NOTES, length=16.0, fire=True)
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
