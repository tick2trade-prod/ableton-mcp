#!/usr/bin/env python3
"""
Run ALL 16 Tracks - Unified Execution Script

This is the SINGLE entry point for creating all tracks in Ableton.
It uses the track classes from the tracks/ module.

Usage:
    uv run python live_set/lily_palmer/i_am_machine_v3/run_all_tracks.py
    uv run python live_set/lily_palmer/i_am_machine_v3/run_all_tracks.py --track 1
    uv run python live_set/lily_palmer/i_am_machine_v3/run_all_tracks.py --track 1 3 5
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

# Track class registry - each track class and its configuration
TRACK_REGISTRY = [
    # (track_number, track_name, track_type, class_name)
    (1, "Kick", "midi", "Track01Kick"),
    (2, "Rumble", "audio", "Track02Rumble"),
    (3, "Sub Bass", "midi", "Track03SubBass"),
    (4, "Acid", "midi", "Track04Acid"),
    (5, "Closed Hat", "midi", "Track05ClosedHat"),
    (6, "Open Hat", "midi", "Track06OpenHat"),
    (7, "Clap", "midi", "Track07Clap"),
    (8, "Tom", "midi", "Track08Tom"),
    (9, "Glitch", "midi", "Track09Glitch"),
    (10, "Ride", "midi", "Track10Ride"),
    (11, "Stab", "midi", "Track11Stab"),
    (12, "Drone", "midi", "Track12Drone"),
    (13, "Vocal", "midi", "Track13Vocal"),
    (14, "Vocal FX", "midi", "Track14VocalFx"),
    (15, "Riser", "midi", "Track15Riser"),
    (16, "Impact", "midi", "Track16Impact"),
]


def get_track_class(class_name: str):
    """Dynamically import and return track class."""
    from live_set.lily_palmer.i_am_machine_v3 import tracks

    return getattr(tracks, class_name)


def run_single_track(client: AbletonMCPClient, track_num: int) -> bool:
    """Run a single track by number (1-16)."""
    if track_num < 1 or track_num > 16:
        print(f"❌ Invalid track number: {track_num} (must be 1-16)")
        return False

    track_info = TRACK_REGISTRY[track_num - 1]
    num, name, track_type, class_name = track_info
    track_index = num - 1  # 0-indexed

    print(f"\n{'=' * 50}")
    print(f"🎵 Track {num:02d}: {name}")
    print(f"{'=' * 50}")

    # Ensure track exists
    full_name = f"{num:02d} - {name}"
    result = client.ensure_track(track_index, full_name, track_type)
    if not result.success:
        print(f"   ❌ Failed to create track: {result.message}")
        return False
    print(f"   ✓ Track '{full_name}' ready")

    # Instantiate and run the track class
    try:
        TrackClass = get_track_class(class_name)
        track = TrackClass(client, track_index)
        track.create()
        print(f"   ✓ Track configured with {class_name}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def run_all_tracks(client: AbletonMCPClient, selected_tracks: list = None):
    """Run all 16 tracks (or selected subset)."""
    print("🎵 I Am Machine V3 - 16-Bar Intro Loop")
    print("=" * 60)

    # Check connection
    info = client.get_session_info()
    if not info.success:
        print(f"❌ Cannot connect to Ableton: {info.message}")
        return False

    tempo = info.data.get("tempo", "unknown")
    print(f"✅ Connected! Tempo: {tempo} BPM")

    # Determine which tracks to run
    if selected_tracks:
        tracks_to_run = selected_tracks
    else:
        tracks_to_run = list(range(1, 17))  # All 16

    print(f"\nRunning {len(tracks_to_run)} tracks: {tracks_to_run}")

    success_count = 0
    for track_num in tracks_to_run:
        if run_single_track(client, track_num):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"✅ {success_count}/{len(tracks_to_run)} tracks completed")
    print("=" * 60)

    return success_count == len(tracks_to_run)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Run I Am Machine V3 tracks")
    parser.add_argument(
        "--track",
        "-t",
        nargs="+",
        type=int,
        help="Specific track numbers to run (1-16)",
    )
    args = parser.parse_args()

    client = AbletonMCPClient()
    success = run_all_tracks(client, args.track)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
