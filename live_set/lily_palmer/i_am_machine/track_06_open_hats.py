#!/usr/bin/env python3
"""
Track 06: Open Hi-Hats - Accented open hats on off-beats.
Per spec: Drum Sampler, offbeat pattern, longer decay.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_06_open_hats.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "06-OpenHats"
TRACK_INDEX = 5

DEVICES = ["Drum Sampler", "Channel EQ", "Reverb"]

# Open hats on offbeats (8th note upbeats)
NOTES = [
    {"pitch": 46, "start_time": float(i * 0.5 + 0.25), "duration": 0.3, "velocity": 90}
    for i in range(32)  # Every offbeat in 4 bars
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
        TRACK_INDEX, 0, "Offbeat Opens", NOTES, length=16.0, fire=True
    )
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
