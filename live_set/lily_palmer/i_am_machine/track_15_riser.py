#!/usr/bin/env python3
"""
Track 15: Risers / White Noise - Tension builder before drops.
Per spec: 8-16 bar white noise, auto filter automation, heavy sidechain.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_15_riser.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "15-Riser"
TRACK_INDEX = 14

DEVICES = ["Operator", "Auto Filter", "Compressor", "Utility"]

# Long sustained noise
NOTES = [
    {"pitch": 60, "start_time": 0.0, "duration": 16.0, "velocity": 80},
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
        TRACK_INDEX, 0, "White Noise Riser", NOTES, length=16.0, fire=True
    )
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nOperator: White noise oscillator")
    print("Auto Filter: Automate 200Hz → 15kHz over 16 bars")
    print("Compressor: Sidechain from Kick")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
