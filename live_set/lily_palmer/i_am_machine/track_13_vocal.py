#!/usr/bin/env python3
"""
Track 13: Vocal - Main vocal sample processing.
Per spec: Audio track for vocal samples with FX chain.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_13_vocal.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "13-Vocal"
TRACK_INDEX = 12

DEVICES = ["Channel EQ", "Compressor", "Reverb"]


def main():
    print(f"=== Creating {TRACK_NAME} ===")
    client = AbletonMCPClient()

    if not client.get_session_info().success:
        return False

    client.ensure_track(TRACK_INDEX, TRACK_NAME, "audio")
    print(f"   ✓ Audio Track '{TRACK_NAME}'")

    print("   Loading devices:")
    client.load_device_chain(TRACK_INDEX, DEVICES)

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nDrop vocal sample into this track")
    print("EQ: HP @ 100Hz, notch harsh freqs")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
