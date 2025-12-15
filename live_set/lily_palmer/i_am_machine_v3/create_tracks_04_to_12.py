#!/usr/bin/env python3
"""
Create Tracks 04-12 - Complete intro percussion and atmosphere

Batch creates all remaining MIDI tracks with basic patterns.
After running, configure instruments manually in Ableton.

Usage: uv run python live_set/lily_palmer/i_am_machine_v3/create_tracks_04_to_12.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

# Track configurations
TRACKS_TO_CREATE = [
    # (index, name, pattern_func, notes_desc)
    (3, "04 - Acid", "acid_pattern", "Acid line in F minor"),
    (4, "05 - Closed Hat", "hihat_16th", "16th notes continuous"),
    (5, "06 - Open Hat", "hihat_offbeat", "Off-beat accents"),
    (6, "07 - Claps", "clap_backbeat", "Backbeat 2,4"),
    (7, "08 - Toms", "tom_fills", "Tribal fills"),
    (8, "09 - Glitch", "glitch_pattern", "Glitch rhythms"),
    (9, "10 - Ride", "ride_pattern", "Ride cymbals"),
    (10, "11 - Stabs", "stab_pattern", "Synth stabs"),
    (11, "12 - Drone", "drone_sustained", "Sustained drone"),
]


def acid_pattern():
    """303-style acid line in F minor."""
    notes = []
    f_minor = [53, 55, 56, 58, 60, 61, 63, 65]

    for bar in range(16):
        for beat in range(4):
            for sixteenth in range(4):
                if sixteenth % 2 == 0:  # On 8th notes
                    pitch = f_minor[(bar * 4 + beat) % len(f_minor)]
                    time = bar * 4 + beat + sixteenth * 0.25
                    notes.append(
                        {
                            "pitch": pitch,
                            "start_time": time,
                            "duration": 0.2,
                            "velocity": 100,
                        }
                    )
    return notes


def hihat_16th():
    """16th note hi-hats."""
    notes = []
    for i in range(256):  # 16 bars * 4 beats * 4 sixteenths
        notes.append(
            {
                "pitch": 42,  # Closed hi-hat
                "start_time": i * 0.25,
                "duration": 0.1,
                "velocity": 80 if i % 4 == 0 else 60,  # Accent on beats
            }
        )
    return notes


def hihat_offbeat():
    """Off-beat open hi-hats."""
    notes = []
    for i in range(64):  # 16 bars * 4 beats
        if i % 2 == 1:  # Off-beats only
            notes.append(
                {
                    "pitch": 46,  # Open hi-hat
                    "start_time": float(i),
                    "duration": 0.3,
                    "velocity": 90,
                }
            )
    return notes


def clap_backbeat():
    """Claps on 2 and 4."""
    notes = []
    for bar in range(16):
        # Beat 2
        notes.append(
            {
                "pitch": 39,  # Clap
                "start_time": bar * 4 + 1,
                "duration": 0.1,
                "velocity": 110,
            }
        )
        # Beat 4
        notes.append(
            {"pitch": 39, "start_time": bar * 4 + 3, "duration": 0.1, "velocity": 110}
        )
    return notes


def tom_fills():
    """Tribal tom fills."""
    notes = []
    tom_pitches = [45, 43, 41]  # Low, mid, high toms

    # Every 4 bars, add a fill
    for bar in [3, 7, 11, 15]:
        for i, pitch in enumerate(tom_pitches):
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": bar * 4 + 2.5 + i * 0.5,
                    "duration": 0.3,
                    "velocity": 100,
                }
            )
    return notes


def glitch_pattern():
    """Glitch pattern."""
    notes = []
    for i in range(32):  # Sparse glitches
        notes.append(
            {"pitch": 60, "start_time": i * 2.0 + 0.25, "duration": 0.1, "velocity": 90}
        )
    return notes


def ride_pattern():
    """Ride cymbal pattern."""
    notes = []
    for i in range(128):  # 8th notes
        if i % 4 in [0, 2]:  # 8th note pattern
            notes.append(
                {
                    "pitch": 51,  # Ride
                    "start_time": i * 0.5,
                    "duration": 0.4,
                    "velocity": 75,
                }
            )
    return notes


def stab_pattern():
    """Synth stab pattern."""
    notes = []
    stab_times = [0, 4, 8, 12, 32, 36, 40, 44]  # Sparse stabs
    for time in stab_times:
        notes.append(
            {
                "pitch": 60,  # C
                "start_time": float(time),
                "duration": 0.5,
                "velocity": 110,
            }
        )
    return notes


def drone_sustained():
    """Sustained drone note."""
    return [
        {
            "pitch": 53,  # F root note
            "start_time": 0.0,
            "duration": 64.0,  # 16 bars
            "velocity": 70,
        }
    ]


# Pattern function map
PATTERN_FUNCS = {
    "acid_pattern": acid_pattern,
    "hihat_16th": hihat_16th,
    "hihat_offbeat": hihat_offbeat,
    "clap_backbeat": clap_backbeat,
    "tom_fills": tom_fills,
    "glitch_pattern": glitch_pattern,
    "ride_pattern": ride_pattern,
    "stab_pattern": stab_pattern,
    "drone_sustained": drone_sustained,
}


def main():
    print("🎵 Creating Tracks 04-12")
    print("=" * 60)

    client = AbletonMCPClient()

    # Check connection
    info = client.get_session_info()
    if not info.success:
        print(f"❌ Cannot connect: {info.message}")
        return False
    print(f"✅ Connected! Tempo: {info.data.get('tempo')} BPM\n")

    created_count = 0

    for index, name, pattern_func_name, desc in TRACKS_TO_CREATE:
        print(f"[{index:02d}] {name}")
        print(f"    Pattern: {desc}")

        # Generate pattern
        pattern_func = PATTERN_FUNCS[pattern_func_name]
        notes = pattern_func()

        if notes:
            result = client.create_pattern(
                track_index=index,
                clip_index=0,
                clip_name=f"{name} Pattern",
                notes=notes,
                length=64.0,
                fire=True,
            )

            if result.success:
                print(f"    ✅ Pattern created ({len(notes)} notes) and PLAYING!")
                created_count += 1
            else:
                print(f"    ❌ Failed: {result.message}")
        else:
            print("    ⚠️  No notes generated")

        print()

    print("=" * 60)
    print(f"✅ Created {created_count}/{len(TRACKS_TO_CREATE)} track patterns!")
    print("\n📝 Manual steps needed:")
    print("  04 - Acid: Load Drift synth")
    print("  05 - Closed Hat: Load 909 hats")
    print("  06 - Open Hat: Load 909 hats")
    print("  07 - Claps: Load clap samples")
    print("  08 - Toms: Load tom samples")
    print("  09 - Glitch: Load Meld synth")
    print("  10 - Ride: Load ride cymbal")
    print("  11 - Stabs: Load Wavetable")
    print("  12 - Drone: Load Operator/Meld")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
