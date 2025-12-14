#!/usr/bin/env python3
"""
Track 11: Main Synth Stab - Melodic hook/motif.
Per spec: Wavetable, short dissonant stabs, dotted delay, large reverb.

Usage: uv run python live_set/lily_palmer/i_am_machine/track_11_synth_stab.py
"""

from ableton_client import AbletonMCPClient

TRACK_NAME = "11-SynthStab"
TRACK_INDEX = 10

DEVICES = [
    ("Wavetable", "Operator"),
    "Echo",
    "Reverb",
    "Channel EQ",
]

# F minor stab pattern with minor 2nds for tension
FM_STABS = [
    {"pitch": 53, "start_time": 0.0, "duration": 0.2, "velocity": 100},  # F
    {"pitch": 56, "start_time": 0.75, "duration": 0.15, "velocity": 90},  # Ab
    {"pitch": 60, "start_time": 2.0, "duration": 0.2, "velocity": 100},  # C
    {"pitch": 61, "start_time": 3.5, "duration": 0.1, "velocity": 85},  # Db (tension)
]

NOTES = FM_STABS * 4  # Repeat over 4 bars
for i, note in enumerate(NOTES):
    NOTES[i] = {**note, "start_time": note["start_time"] + (i // 4) * 4}


def main():
    print(f"=== Creating {TRACK_NAME} ===")
    client = AbletonMCPClient()

    if not client.get_session_info().success:
        return False

    client.ensure_track(TRACK_INDEX, TRACK_NAME, "midi")
    print(f"   ✓ Track '{TRACK_NAME}'")

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

    client.create_pattern(TRACK_INDEX, 0, "Fm Stabs", NOTES, length=16.0, fire=True)
    print("   ✓ Pattern created")

    print(f"\n=== {TRACK_NAME} Complete ===")
    print("\nEcho: Dotted 1/8, Feedback 60%")
    print("Reverb: Large Hall, Decay 4s+")
    return True


if __name__ == "__main__":
    exit(0 if main() else 1)
