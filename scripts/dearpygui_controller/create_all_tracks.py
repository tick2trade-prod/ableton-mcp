#!/usr/bin/env python3
"""Automation script to create all 16 tracks programmatically.

This script creates the complete "I Am Machine" project structure
in Ableton Live using the DearPyGUI controller agents.

Usage:
    cd /Users/alexzh/ableton-mcp/scripts
    uv run python dearpygui_controller/create_all_tracks.py
"""

import asyncio
import sys
from pathlib import Path

# Ensure package is importable
scripts_dir = Path(__file__).parent.parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from dearpygui_controller.agents import ComposerAgent, MixerAgent, VerifierAgent
from dearpygui_controller.config import TRACKS


def get_mcp_client():
    """Get the Ableton MCP client."""
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

        return AbletonMCPClient()
    except ImportError as e:
        print(f"Warning: Could not import AbletonMCPClient: {e}")
        return None


async def create_all_tracks():
    """Create all 16 tracks with patterns and devices."""
    print("=" * 60)
    print("I AM MACHINE - Automated Track Creation")
    print("=" * 60)

    mcp = get_mcp_client()
    if not mcp:
        print("\n⚠️  Running in MOCK mode (no Ableton connection)")

    composer = ComposerAgent(verbose=True)
    mixer = MixerAgent(verbose=True)

    results = {
        "tracks_created": 0,
        "patterns_added": 0,
        "devices_loaded": 0,
        "errors": [],
    }

    # Set tempo first
    if mcp:
        print("\n[1/4] Setting tempo to 136 BPM...")
        tempo_result = mcp.set_tempo(136.0)
        if tempo_result.success:
            print("✓ Tempo set to 136 BPM")
        else:
            print(f"⚠ Could not set tempo: {tempo_result.message}")

    # Create tracks
    print("\n[2/4] Creating tracks...")
    for track in TRACKS:
        print(f"  Creating {track.name}...", end=" ")

        if mcp:
            # Use ensure_track which handles creation and naming
            result = mcp.ensure_track(
                target_index=track.index,
                name=track.name,
                track_type=track.track_type,
            )

            if result.success:
                print("✓")
                results["tracks_created"] += 1
            else:
                print(f"⚠ {result.message}")
                results["errors"].append(f"{track.name}: {result.message}")
        else:
            print("✓ (mock)")
            results["tracks_created"] += 1

    # Add patterns to MIDI tracks
    print("\n[3/4] Adding MIDI patterns...")
    midi_tracks = [t for t in TRACKS if t.track_type == "midi"]

    for track in midi_tracks:
        notes = composer.get_pattern_for_track(track, bars=4)
        if not notes:
            print(f"  {track.name}: No pattern (skipped)")
            continue

        print(f"  {track.name}: {len(notes)} notes...", end=" ")

        if mcp:
            # Create clip
            clip_result = mcp.create_clip(
                track_index=track.index,
                clip_index=0,
                length=16.0,  # 4 bars
            )

            if clip_result.success:
                # Add notes
                notes_result = mcp.add_notes_to_clip(
                    track_index=track.index,
                    clip_index=0,
                    notes=notes,
                )
                if notes_result.success:
                    print("✓")
                    results["patterns_added"] += 1
                else:
                    print(f"⚠ {notes_result.message}")
            else:
                print(f"⚠ {clip_result.message}")
        else:
            print("✓ (mock)")
            results["patterns_added"] += 1

    # Load devices
    print("\n[4/4] Loading device chains...")
    for track in TRACKS:
        chain = mixer.get_chain_for_track(track)
        if not chain:
            continue

        device_names = [d["name"] for d in chain]
        print(f"  {track.name}: {device_names}...", end=" ")

        if mcp:
            all_loaded = True
            for device_spec in chain:
                result = mcp.load_device(
                    track_index=track.index,
                    device_name=device_spec["name"],
                    fallback=device_spec.get("fallback"),
                )
                if not result.success:
                    all_loaded = False
                    break

            if all_loaded:
                print("✓")
                results["devices_loaded"] += 1
            else:
                print("⚠")
        else:
            print("✓ (mock)")
            results["devices_loaded"] += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Tracks created:  {results['tracks_created']}/16")
    print(f"  Patterns added:  {results['patterns_added']}")
    print(f"  Device chains:   {results['devices_loaded']}")
    print(f"  Errors:          {len(results['errors'])}")

    if results["errors"]:
        print("\nErrors:")
        for err in results["errors"][:5]:
            print(f"  - {err}")

    # Verify
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    verifier = VerifierAgent(verbose=False)
    verify_result = await verifier.execute()
    print(verify_result.data.get("report", ""))

    return results


def main():
    """Main entry point."""
    print("\nStarting I AM MACHINE track creation...")
    print("Ensure Ableton Live is running with AbletonMCP control surface.\n")

    results = asyncio.run(create_all_tracks())

    print("\n✅ Done!")

    if results["tracks_created"] < 16:
        print("\n⚠️  Some tracks were not created. Check Ableton connection.")
        sys.exit(1)


if __name__ == "__main__":
    main()
