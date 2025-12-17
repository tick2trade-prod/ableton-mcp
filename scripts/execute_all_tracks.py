#!/usr/bin/env python3
"""
Master Execution Script for Phase 1 Intro (Bars 1-16)

Creates all 14 tracks with correct devices, clips, and MIDI patterns.
Tracks 1-5 are reference/stems (already exist).
This script creates tracks 6-19.

UPDATED: Now uses reference-based patterns extracted from stem analysis
of "I Am Machine" by Lilly Palmer for improved similarity to the original.

Run:
    python scripts/execute_all_tracks.py
"""

import json
import socket
import time
from typing import Any

# Import reference-based pattern generators
from scripts.patterns.reference_patterns import PATTERN_GENERATORS

# =============================================================================
# TRACK CONFIGURATION
# =============================================================================

TRACK_OFFSET = 5  # First 5 tracks are reference + stems

TRACKS = {
    "kick": {
        "index": TRACK_OFFSET + 0,  # 5
        "name": "Kick",
        "synth_uri": "query:Drums#FileId_14946",  # 909 Core Kit
        "pattern": "four_on_floor",
    },
    "snare": {
        "index": TRACK_OFFSET + 1,  # 6
        "name": "Snare",
        "synth_uri": "query:Drums#FileId_14946",  # 909 Core Kit
        "pattern": "backbeat",
    },
    "hihats": {
        "index": TRACK_OFFSET + 2,  # 7
        "name": "Hi-hats",
        "synth_uri": "query:Drums#FileId_14946",  # 909 Core Kit
        "pattern": "offbeat_8ths",
    },
    "toms": {
        "index": TRACK_OFFSET + 3,  # 8
        "name": "Toms",
        "synth_uri": "query:Drums#FileId_14946",  # 909 Core Kit
        "pattern": "fills",
    },
    "glitch": {
        "index": TRACK_OFFSET + 4,  # 9
        "name": "Glitch",
        "synth_uri": "query:Drums#FileId_14946",  # 909 Core Kit for now
        "pattern": "glitch_sparse",
    },
    "ride": {
        "index": TRACK_OFFSET + 5,  # 10
        "name": "Ride",
        "synth_uri": "query:Drums#FileId_14946",  # 909 Core Kit
        "pattern": "quarter_notes",
    },
    "rumble": {
        "index": TRACK_OFFSET + 6,  # 11
        "name": "Rumble",
        "synth_uri": "query:Synths#Operator",
        "pattern": "sustained_sub",
    },
    "rolling": {
        "index": TRACK_OFFSET + 7,  # 12
        "name": "Rolling Bass",
        "synth_uri": "query:Synths#Operator",
        "pattern": "rolling_16ths",
    },
    "acid": {
        "index": TRACK_OFFSET + 8,  # 13
        "name": "Acid",
        "synth_uri": "query:Synths#Drift",
        "pattern": "acid_303",
    },
    "stabs": {
        "index": TRACK_OFFSET + 9,  # 14
        "name": "Stabs",
        "synth_uri": "query:Synths#Operator",
        "pattern": "offbeat_stabs",
    },
    "drone": {
        "index": TRACK_OFFSET + 10,  # 15
        "name": "Drone",
        "synth_uri": "query:Synths#Wavetable",
        "pattern": "sustained_drone",
    },
    "main_vocal": {
        "index": TRACK_OFFSET + 11,  # 16
        "name": "Main Vocal",
        "synth_uri": None,  # Audio track placeholder
        "pattern": "empty",
    },
    "vocal_fx": {
        "index": TRACK_OFFSET + 12,  # 17
        "name": "Vocal FX",
        "synth_uri": "query:Synths#Simpler",
        "pattern": "vocal_chops",
    },
    "risers": {
        "index": TRACK_OFFSET + 13,  # 18
        "name": "Risers",
        "synth_uri": "query:Synths#Operator",
        "pattern": "riser_sweep",
    },
}

# =============================================================================
# PATTERN GENERATORS
# =============================================================================
# All patterns are now imported from scripts.patterns.reference_patterns
# which uses the stem analysis data from assets/analysis/stem_analysis.json
# to generate patterns that match the "I Am Machine" reference track.
#
# The PATTERN_GENERATORS dict maps pattern names used in TRACKS config
# to reference-based generator functions:
#   - four_on_floor → kick_from_reference (with 4-on-floor fallback)
#   - backbeat → snare_from_reference
#   - offbeat_8ths → hihats_from_reference
#   - sustained_sub → sub_bass_from_reference (transposed to sub range)
#   - rolling_16ths → rolling_bass_from_reference (original pitches)
#   - acid_303 → acid_from_reference (303-style articulation)
#   - etc.
# =============================================================================


# =============================================================================
# MCP CONNECTION
# =============================================================================


def send_command(sock: socket.socket, command_type: str, params: dict = None) -> Any:
    """Send command to Ableton MCP."""
    command = {"type": command_type, "params": params or {}}
    print(f"  → {command_type}")
    sock.sendall(json.dumps(command).encode("utf-8"))

    chunks = []
    sock.settimeout(15)
    while True:
        try:
            chunk = sock.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                data = b"".join(chunks)
                response = json.loads(data.decode("utf-8"))
                if response.get("status") == "error":
                    print(f"    ✗ {response.get('message')}")
                    return None
                print("    ✓ OK")
                return response.get("result", {})
            except json.JSONDecodeError:
                continue
        except TimeoutError:
            break
    return {}


def create_track(sock: socket.socket, track_key: str, track_config: dict) -> bool:
    """Create a single track with device and pattern."""
    index = track_config["index"]
    name = track_config["name"]
    synth_uri = track_config.get("synth_uri")
    pattern_name = track_config["pattern"]

    print(f"\n{'=' * 60}")
    print(f"CREATING TRACK: {name} (index {index})")
    print(f"{'=' * 60}")

    # 1. Check if track exists, create if needed
    session = send_command(sock, "get_session_info")
    if not session:
        return False

    track_count = session.get("track_count", 0)
    while track_count <= index:
        print(f"  Creating track {track_count}...")
        send_command(sock, "create_midi_track", {"index": track_count})
        track_count += 1
        time.sleep(0.3)

    # 2. Name the track
    print(f"\n[1/4] Naming track '{name}'...")
    send_command(sock, "set_track_name", {"track_index": index, "name": name})
    time.sleep(0.2)

    # 3. Load synth/device
    if synth_uri:
        print(f"\n[2/4] Loading device: {synth_uri}...")
        send_command(
            sock, "load_browser_item", {"track_index": index, "item_uri": synth_uri}
        )
        time.sleep(1.0)
    else:
        print("\n[2/4] No device to load (placeholder track)")

    # 4. Create clip
    print("\n[3/4] Creating 16-bar clip...")
    send_command(
        sock, "create_clip", {"track_index": index, "clip_index": 0, "length": 64.0}
    )
    time.sleep(0.3)

    # 5. Add MIDI pattern
    pattern_func = PATTERN_GENERATORS.get(pattern_name)
    if pattern_func:
        notes = pattern_func()
        if notes:
            print(f"\n[4/4] Adding {len(notes)} notes ({pattern_name})...")
            send_command(
                sock,
                "add_notes_to_clip",
                {"track_index": index, "clip_index": 0, "notes": notes},
            )
            time.sleep(0.2)
        else:
            print("\n[4/4] Empty pattern (placeholder)")
    else:
        print(f"\n[4/4] Unknown pattern: {pattern_name}")

    # 6. Name the clip
    send_command(
        sock,
        "set_clip_name",
        {"track_index": index, "clip_index": 0, "name": f"{name} - Intro"},
    )

    print(f"\n✓ Track '{name}' created successfully")
    return True


def main():
    """Main execution."""
    print("=" * 60)
    print("PHASE 1 INTRO - MASTER EXECUTION SCRIPT")
    print("=" * 60)
    print(f"Creating {len(TRACKS)} tracks...")
    print()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)

    try:
        print("Connecting to Ableton MCP on localhost:9877...")
        sock.connect(("localhost", 9877))
        print("✓ Connected\n")

        success_count = 0
        fail_count = 0

        for track_key, track_config in TRACKS.items():
            try:
                if create_track(sock, track_key, track_config):
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"✗ Error creating {track_key}: {e}")
                fail_count += 1

            # Small delay between tracks
            time.sleep(0.5)

        # Final summary
        print("\n" + "=" * 60)
        print("EXECUTION COMPLETE")
        print("=" * 60)
        print(f"✓ Success: {success_count}/{len(TRACKS)} tracks")
        if fail_count > 0:
            print(f"✗ Failed: {fail_count}/{len(TRACKS)} tracks")

        print("\n📋 Run tests to verify:")
        print("   pytest tests/phases/phase1_intro/ -v")

    except ConnectionRefusedError:
        print("✗ Could not connect to Ableton MCP on port 9877")
        print("  Make sure Ableton is running with AbletonMCP enabled")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
