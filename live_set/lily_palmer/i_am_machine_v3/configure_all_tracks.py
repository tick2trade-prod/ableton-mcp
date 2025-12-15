#!/usr/bin/env python3
"""
Batch Configure All Tracks 01-12

Runs all track configuration scripts in sequence.
Makes the full 16-bar intro loop audible.

Usage: uv run python live_set/lily_palmer/i_am_machine_v3/configure_all_tracks.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SCRIPT_DIR = Path(__file__).parent

TRACK_SCRIPTS = [
    "create_track_01_kick.py",  # Already working
    # "create_track_02_rumble.py",  # Needs manual audio routing
    "create_track_03_sub_bass.py",
    # Add more as they're created
]


def main():
    print("🎵 Configuring All Tracks for 'I Am Machine' Intro")
    print("=" * 60)

    success_count = 0
    total = len(TRACK_SCRIPTS)

    for script in TRACK_SCRIPTS:
        script_path = SCRIPT_DIR / script
        if not script_path.exists():
            print(f"\n⚠️  {script} not found, skipping...")
            continue

        print(f"\n{'=' * 60}")
        print(f"Running: {script}")
        print("=" * 60)

        result = subprocess.run(
            ["uv", "run", "python", str(script_path)],
            cwd=PROJECT_ROOT,
            capture_output=False,
        )

        if result.returncode == 0:
            success_count += 1
            print(f"\n✅ {script} completed successfully")
        else:
            print(f"\n❌ {script} failed")

    print("\n" + "=" * 60)
    print(f"✅ Configured {success_count}/{total} tracks")
    print("=" * 60)

    return success_count == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
