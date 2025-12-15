#!/usr/bin/env python3
"""
Track 08: Low Tom - Deep, processed tom fills.
Per spec: Pitched down tom, reverb, appearing in fills.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_08_low_tom.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "08-LowTom"
TRACK_INDEX = 7

DEVICES = ["Drum Sampler", "Channel EQ", "Reverb"]

# Tom fills - sparse, on phrase ends
NOTES = [
    {"pitch": 43, "start_time": 15.0, "duration": 0.5, "velocity": 100},
    {"pitch": 41, "start_time": 15.5, "duration": 0.5, "velocity": 95},
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

    client.create_pattern(TRACK_INDEX, 0, "Tom Fill", NOTES, length=16.0, fire=True)
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
