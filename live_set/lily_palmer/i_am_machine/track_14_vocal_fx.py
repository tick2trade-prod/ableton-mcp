#!/usr/bin/env python3
"""
Track 14: Vocal FX - Processed/mangled vocal bus.
Per spec: Spectral effects, grain processing.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_14_vocal_fx.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "14-VocalFX"
TRACK_INDEX = 13

DEVICES = [
    ("Grain Scanner", "Corpus"),
    ("Spectral Resonator", "Vocoder"),
    "Echo",
    "Reverb",
]


def main():
    print(f"=== Creating {TRACK_NAME} ===")
    client = AbletonMCPClient()

    if not client.get_session_info().success:
        return False

    client.ensure_track(TRACK_INDEX, TRACK_NAME, "audio")
    print(f"   ✓ Audio Track '{TRACK_NAME}'")

    print("   Loading devices:")
    for device in DEVICES:
        if isinstance(device, tuple):
            primary, fallback = device
            result = client.load_device(TRACK_INDEX, primary, fallback=fallback)
            print(
                f"     {'✓' if result.success else '↳'} {primary if result.success else fallback}"
            )
        else:
            result = client.load_device(TRACK_INDEX, device)
            print(f"     {'✓' if result.success else '✗'} {device}")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nAudio From: 13-Vocal (Post FX)")
    print("Monitor: In")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
