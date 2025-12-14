#!/usr/bin/env python3
"""
Track 12: Drone/Pad - Atmospheric bed of sound.
Per spec: Operator/Analog, long sustain, evolving texture.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_12_drone.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "12-Drone"
TRACK_INDEX = 11

DEVICES = ["Operator", "Reverb", "Chorus", "Auto Filter"]

# Sustained F minor chord
NOTES = [
    {"pitch": 41, "start_time": 0.0, "duration": 16.0, "velocity": 60},  # F2
    {"pitch": 44, "start_time": 0.0, "duration": 16.0, "velocity": 55},  # Ab2
    {"pitch": 48, "start_time": 0.0, "duration": 16.0, "velocity": 55},  # C3
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

    client.create_pattern(TRACK_INDEX, 0, "Fm Drone", NOTES, length=16.0, fire=True)
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nOperator: Long attack (2s), infinite decay")
    print("Auto Filter: Slow LFO sweep")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
