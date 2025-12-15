#!/usr/bin/env python3
"""Test script for track generator with live Ableton.

Usage:
    python test_track_generator_live.py [config_file]

Examples:
    python test_track_generator_live.py                      # Uses example.json
    python test_track_generator_live.py i_am_machine_full.json  # Full 16 tracks
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from live_set.lily_palmer.i_am_machine_v2.generators.track_generator import (
    ValidatedTrackGenerator,
)


def main():
    """Run track generator test."""
    # Get config file from command line or use default
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "example.json"

    # Build full path
    config_path = Path(__file__).parent / "configs" / config_file

    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        print("\nAvailable configs:")
        configs_dir = Path(__file__).parent / "configs"
        for cfg in sorted(configs_dir.glob("*.json")):
            print(f"  - {cfg.name}")
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print("🎹 ABLETON TRACK GENERATOR - LIVE TEST")
    print(f"{'=' * 70}")
    print(f"\nConfig: {config_path.name}\n")

    # Create generator (auto-connects to Ableton if available)
    generator = ValidatedTrackGenerator()

    # Generate tracks
    result = generator.generate_from_config(config_path)

    # Print summary
    if result["success"]:
        print("\n✅ SUCCESS!")
        print(f"   Project: {result['project_name']}")
        print(f"   Tracks Generated: {result['tracks_generated']}")
    else:
        print("\n❌ FAILED!")
        print(f"   Successful: {result['tracks_generated']}")
        print(f"   Failed: {result['tracks_failed']}")

    print(f"\n{'=' * 70}\n")

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
