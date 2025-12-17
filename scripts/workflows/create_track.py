#!/usr/bin/env python3
"""
Create track for I Am Machine recreation.

This script creates tracks using the Ableton MCP connection.
Usage:
    python create_track.py kick intro --pattern 4-on-floor
    python create_track.py rumble intro --pattern sub_bass --effects hybrid_reverb,roar
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_ableton_mcp_add_notes_to_clip import mcp_ableton_mcp_add_notes_to_clip
from mcp_ableton_mcp_create_clip import mcp_ableton_mcp_create_clip
from mcp_ableton_mcp_create_midi_track import mcp_ableton_mcp_create_midi_track
from mcp_ableton_mcp_get_session_info import mcp_ableton_mcp_get_session_info
from mcp_ableton_mcp_load_instrument_or_effect import (
    mcp_ableton_mcp_load_instrument_or_effect,
)
from mcp_ableton_mcp_set_tempo import mcp_ableton_mcp_set_tempo
from mcp_ableton_mcp_set_track_name import mcp_ableton_mcp_set_track_name

# Track configurations
TRACK_CONFIGS = {
    "kick": {
        "name": "Kick",
        "device_uri": "query:Drums#Drum%20Rack",
        "pitch": 36,  # C1 - Kick drum
    },
    "snare": {
        "name": "Snare",
        "device_uri": "query:Drums#Drum%20Rack",
        "pitch": 38,  # D1 - Snare
    },
    "hihats": {
        "name": "Hi-hats",
        "device_uri": "query:Drums#Drum%20Rack",
        "pitch": 42,  # F#1 - Closed hat
    },
    "toms": {
        "name": "Toms",
        "device_uri": "query:Drums#Drum%20Rack",
        "pitch": 45,  # A1 - Low tom
    },
    "glitch": {
        "name": "Glitch",
        "device_uri": "query:Drums#Drum%20Rack",
        "pitch": 49,  # C#2 - Crash
    },
    "ride": {
        "name": "Ride",
        "device_uri": "query:Drums#Drum%20Rack",
        "pitch": 51,  # D#2 - Ride
    },
    "rumble": {
        "name": "Rumble",
        "device_uri": "query:Synths#Operator",
        "pitch": 33,  # A0 - Sub bass
    },
    "rolling_bass": {
        "name": "Rolling Bass",
        "device_uri": "query:Synths#Operator",
        "pitch": 45,  # A1
    },
    "acid": {
        "name": "Acid",
        "device_uri": "query:Synths#Operator",
        "pitch": 45,  # A1
    },
    "stabs": {
        "name": "Stabs",
        "device_uri": "query:Synths#Wavetable",
        "pitch": 57,  # A2
    },
    "drone": {
        "name": "Drone",
        "device_uri": "query:Synths#Operator",
        "pitch": 45,  # A1
    },
    "main_vocal": {
        "name": "Main Vocal",
        "device_uri": None,  # Audio track
    },
    "vocal_fx": {
        "name": "Vocal FX",
        "device_uri": None,
    },
    "risers": {
        "name": "Risers",
        "device_uri": "query:Synths#Wavetable",
        "pitch": 57,
    },
}


# Pattern generators
def generate_4_on_floor(bars: int, bpm: int = 136) -> list[dict]:
    """Generate 4-on-floor kick pattern."""
    notes = []
    beats_per_bar = 4
    total_beats = bars * beats_per_bar

    for beat in range(total_beats):
        notes.append(
            {
                "pitch": 36,  # C1
                "start_time": beat * 1.0,  # 1 quarter note per beat
                "duration": 0.25,
                "velocity": 100,
                "mute": False,
            }
        )

    return notes


def generate_sparse_pattern(bars: int, pitch: int) -> list[dict]:
    """Generate sparse intro pattern."""
    notes = []
    # Spars pattern: only on beats 2 and 4 of every other bar
    for bar in range(bars):
        if bar % 2 == 0:  # Every other bar
            # Beat 2 (index 1)
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": bar * 4.0 + 1.0,
                    "duration": 0.25,
                    "velocity": 80,
                    "mute": False,
                }
            )
            # Beat 4 (index 3)
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": bar * 4.0 + 3.0,
                    "duration": 0.25,
                    "velocity": 80,
                    "mute": False,
                }
            )

    return notes


def generate_closed_8th_hats(bars: int, pitch: int) -> list[dict]:
    """Generate closed hi-hat 8th note pattern."""
    notes = []
    eighth_notes = bars * 4 * 2  # 4 beats per bar, 2 eighths per beat

    for i in range(eighth_notes):
        velocity = 70 if i % 2 == 1 else 90  # Accent on beats
        notes.append(
            {
                "pitch": pitch,
                "start_time": i * 0.5,  # 8th notes
                "duration": 0.125,
                "velocity": velocity,
                "mute": False,
            }
        )

    return notes


def generate_sub_bass(bars: int, pitch: int) -> list[dict]:
    """Generate sub bass rumble pattern."""
    notes = []

    # Simple sustained bass note every 4 bars
    for bar in range(0, bars, 4):
        notes.append(
            {
                "pitch": pitch,
                "start_time": bar * 4.0,
                "duration": 16.0,  # 4 bars
                "velocity": 100,
                "mute": False,
            }
        )

    return notes


def generate_pad(bars: int, pitch: int) -> list[dict]:
    """Generate atmospheric pad pattern."""
    notes = []

    # Sustained chord (root, fifth, octave)
    for offset in [0, 7, 12]:  # Root, fifth, octave
        notes.append(
            {
                "pitch": pitch + offset,
                "start_time": 0.0,
                "duration": bars * 4.0,
                "velocity": 60,
                "mute": False,
            }
        )

    return notes


PATTERN_GENERATORS = {
    "4-on-floor": generate_4_on_floor,
    "sparse": generate_sparse_pattern,
    "closed_8th": generate_closed_8th_hats,
    "sub_bass": generate_sub_bass,
    "pad": generate_pad,
}


def load_section_config(section: str) -> dict:
    """Load section configuration."""
    config_path = Path(__file__).parent.parent.parent / "sections" / "i_am_machine.json"
    with open(config_path) as f:
        data = json.load(f)
    return data["sections"][section]


def create_track(
    track_type: str,
    section: str,
    pattern: str = None,
    effects: list[str] = None,
    silent: bool = False,
) -> bool:
    """
    Create a track with the specified configuration.

    Args:
        track_type: Type of track (kick, rumble, etc.)
        section: Section name (intro, build1, etc.)
        pattern: Pattern type (4-on-floor, sparse, etc.)
        effects: List of effect URIs to load
        silent: If True, create empty clip

    Returns:
        True if successful
    """
    try:
        # Get session info
        session = mcp_ableton_mcp_get_session_info()
        current_track_count = len(session.get("tracks", []))

        # Get track config
        config = TRACK_CONFIGS.get(track_type)
        if not config:
            print(f"❌ Unknown track type: {track_type}")
            return False

        # Get section config
        section_config = load_section_config(section)
        start_bar = section_config["start"]
        end_bar = section_config["end"]
        bars = end_bar - start_bar + 1

        # Create MIDI track
        print(f"Creating track: {config['name']}")
        mcp_ableton_mcp_create_midi_track(index=-1)

        # Set track name
        track_index = current_track_count
        mcp_ableton_mcp_set_track_name(track_index=track_index, name=config["name"])

        # Load instrument if specified
        if config["device_uri"]:
            print(f"  Loading instrument: {config['device_uri']}")
            mcp_ableton_mcp_load_instrument_or_effect(
                track_index=track_index, uri=config["device_uri"]
            )

        # Load additional effects
        if effects:
            effect_uris = {
                "hybrid_reverb": "query:AudioFx#Hybrid%20Reverb",
                "roar": "query:AudioFx#Roar",
                "eq_eight": "query:AudioFx#EQ%20Eight",
                "compressor": "query:AudioFx#Compressor",
            }
            for effect_name in effects:
                uri = effect_uris.get(effect_name)
                if uri:
                    print(f"  Loading effect: {effect_name}")
                    mcp_ableton_mcp_load_instrument_or_effect(
                        track_index=track_index, uri=uri
                    )

        # Create clip
        clip_length = bars * 4.0  # 4 beats per bar
        print(f"  Creating {bars}-bar clip (Bars {start_bar}-{end_bar})")
        mcp_ableton_mcp_create_clip(
            track_index=track_index, clip_index=0, length=clip_length
        )

        # Add notes if not silent
        if not silent and pattern:
            generator = PATTERN_GENERATORS.get(pattern)
            if generator:
                pitch = config.get("pitch", 60)
                if pattern == "4-on-floor":
                    notes = generator(bars)
                else:
                    notes = generator(bars, pitch)

                print(f"  Adding {len(notes)} notes ({pattern} pattern)")
                mcp_ableton_mcp_add_notes_to_clip(
                    track_index=track_index, clip_index=0, notes=notes
                )

        print(f"✅ {config['name']} created successfully")
        return True

    except Exception as e:
        print(f"❌ Error creating track: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Create track for I Am Machine")
    parser.add_argument(
        "track", choices=list(TRACK_CONFIGS.keys()), help="Track type to create"
    )
    parser.add_argument("section", help="Section name (intro, build1, etc.)")
    parser.add_argument("--pattern", help="Pattern type")
    parser.add_argument("--effects", help="Comma-separated effect names")
    parser.add_argument("--silent", action="store_true", help="Create empty clip")
    parser.add_argument("--action", help="Special action (set_tempo)")
    parser.add_argument("--bpm", type=int, default=136, help="BPM for set_tempo action")

    args = parser.parse_args()

    # Handle special actions
    if args.action == "set_tempo":
        print(f"Setting tempo to {args.bpm} BPM")
        mcp_ableton_mcp_set_tempo(tempo=args.bpm)
        print(f"✅ Tempo set to {args.bpm} BPM")
        return

    # Parse effects
    effects = args.effects.split(",") if args.effects else None

    # Create track
    success = create_track(
        track_type=args.track,
        section=args.section,
        pattern=args.pattern,
        effects=effects,
        silent=args.silent,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
