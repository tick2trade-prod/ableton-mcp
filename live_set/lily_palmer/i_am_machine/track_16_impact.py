#!/usr/bin/env python3
"""
Track 16: Impact/Downlifters - Transition effects.
Per spec: Crash, impacts, reverse elements.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_16_impact.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "16-Impact"
TRACK_INDEX = 15

DEVICES = ["Drum Sampler", "Reverb", "Saturator"]

# Impact on bar 1 and end of phrase
NOTES = [
    {"pitch": 49, "start_time": 0.0, "duration": 1.0, "velocity": 120},  # Crash
    {"pitch": 36, "start_time": 15.5, "duration": 0.5, "velocity": 110},  # Impact
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

    client.create_pattern(TRACK_INDEX, 0, "Impacts", NOTES, length=16.0, fire=True)
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nDrum Sampler: Load crash and impact samples")
    print("Reverb: Large, 100% wet for tails")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
