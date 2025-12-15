#!/usr/bin/env python3
"""
Track 02: Industrial Rumble - Fills space between kicks with textured sub-bass.
Per spec: Roar multiband saturation on sidechained reverb tail from kick.

Optimized version using shared AbletonMCPClient.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_02_rumble.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "02-Rumble"
TRACK_INDEX = 1

# Device chain for sub rumble with saturation
DEVICES = [
    ("Hybrid Reverb", "Reverb"),  # (primary, fallback)
    ("Roar", "Saturator"),  # Live 12 only, fallback to Saturator
    "Channel EQ",
    "Compressor",
]


def main():
    print(f"=== Creating {TRACK_NAME} ===")

    client = AbletonMCPClient()

    # 1. Verify connection
    info = client.get_session_info()
    if not info.success:
        print(f"   ✗ Cannot connect: {info.message}")
        return False
    print(f"   Connected at {info.data.get('tempo')} BPM")

    # 2. Create audio track for receiving from kick
    result = client.ensure_track(TRACK_INDEX, TRACK_NAME, "audio")
    if not result.success:
        print(f"   ✗ Failed: {result.message}")
        return False
    print(f"   ✓ Audio track '{TRACK_NAME}' at index {TRACK_INDEX}")

    # 3. Load devices (with fallbacks for Live 12 exclusive)
    print("   Loading devices:")
    for device in DEVICES:
        if isinstance(device, tuple):
            primary, fallback = device
            result = client.load_device(TRACK_INDEX, primary, fallback=fallback)
            loaded = primary if result.success else fallback
            symbol = "✓" if result.success else "↳"
            print(f"     {symbol} {loaded}")
        else:
            result = client.load_device(TRACK_INDEX, device)
            symbol = "✓" if result.success else "✗"
            print(f"     {symbol} {device}")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nManual configuration needed:")
    print("  Audio From: 01-Kick (Post FX)")
    print("  Monitor: In")
    print("  Reverb: Large Hall, Decay 4s+, 100% Wet")
    print("  Roar/Saturator: Multiband, Low band +6dB")
    print("  Compressor: Sidechain from 01-Kick")

    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
