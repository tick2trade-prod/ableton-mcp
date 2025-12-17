#!/usr/bin/env python3
"""Create Intro Drums - Lane 1.

This script creates all 6 drum tracks for the intro section (Bars 1-16)
of "I Am Machine" at 136 BPM.

Tracks created:
1. Kick - 4-on-floor pattern
2. Snare - Off-beat hits (sparse for intro)
3. Hi-hats - 16th notes with velocity variation
4. Toms - Fill/accent pattern
5. Glitch - Industrial percussion
6. Ride - Cymbal texture

Usage:
    python scripts/workflows/create_intro_drums.py

Requirements:
    - Ableton Live running with AbletonMCP Remote Script
    - Remote Script listening on port 9877
"""

import json
import socket
import sys
import time
from dataclasses import dataclass
from typing import Any

# Configuration
ABLETON_HOST = "localhost"
ABLETON_PORT = 9877
TEMPO = 136
INTRO_BARS = 16
BEATS_PER_BAR = 4
INTRO_LENGTH = INTRO_BARS * BEATS_PER_BAR  # 64 beats


@dataclass
class DrumTrack:
    """Drum track specification."""

    name: str
    index: int
    pattern_func: str  # Name of pattern generation function
    velocity_base: int = 100
    color: int = 0  # Ableton track color index


# Track definitions
DRUM_TRACKS = [
    DrumTrack("Kick", 0, "four_on_floor", 100),
    DrumTrack("Snare", 1, "sparse_snare", 90),
    DrumTrack("Hi-hats", 2, "sixteenth_hats", 70),
    DrumTrack("Toms", 3, "tom_accents", 85),
    DrumTrack("Glitch", 4, "glitch_perc", 75),
    DrumTrack("Ride", 5, "ride_pattern", 60),
]


class AbletonClient:
    """Client for communicating with Ableton via socket."""

    def __init__(self, host: str = ABLETON_HOST, port: int = ABLETON_PORT):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None

    def connect(self) -> bool:
        """Connect to Ableton Remote Script."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"✓ Connected to Ableton at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            self.sock = None
            return False

    def disconnect(self):
        """Disconnect from Ableton."""
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_command(
        self, command_type: str, params: dict[str, Any] | None = None
    ) -> dict:
        """Send command to Ableton and return response."""
        if not self.sock:
            raise ConnectionError("Not connected to Ableton")

        command = {"type": command_type, "params": params or {}}

        try:
            # Send command
            self.sock.sendall(json.dumps(command).encode("utf-8"))

            # Small delay for processing
            time.sleep(0.1)

            # Receive response
            self.sock.settimeout(15.0)
            chunks = []
            while True:
                try:
                    chunk = self.sock.recv(8192)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    # Try to parse as complete JSON
                    try:
                        data = b"".join(chunks)
                        response = json.loads(data.decode("utf-8"))
                        if response.get("status") == "error":
                            raise Exception(response.get("message", "Unknown error"))
                        return response.get("result", {})
                    except json.JSONDecodeError:
                        continue
                except socket.timeout:
                    break

            if chunks:
                data = b"".join(chunks)
                response = json.loads(data.decode("utf-8"))
                if response.get("status") == "error":
                    raise Exception(response.get("message", "Unknown error"))
                return response.get("result", {})

            raise Exception("No response from Ableton")

        except Exception as e:
            print(f"  ✗ Command failed: {e}")
            raise


# Pattern Generation Functions


def four_on_floor() -> list[dict]:
    """Generate 4-on-floor kick pattern.

    One kick on every beat (quarter notes).
    """
    notes = []
    for beat in range(INTRO_LENGTH):
        notes.append({
            "pitch": 36,  # C1 - Standard kick
            "start_time": float(beat),
            "duration": 0.5,
            "velocity": 100,
            "mute": False,
        })
    return notes


def sparse_snare() -> list[dict]:
    """Generate sparse snare pattern for intro.

    For intro, snare is minimal - just occasional hits to build tension.
    Every 4 bars, one hit on beat 4.
    """
    notes = []
    # Sparse intro snare - one hit every 4 bars on beat 4
    for bar in range(0, INTRO_BARS, 4):
        beat = bar * 4 + 3  # Beat 4 (0-indexed as 3)
        notes.append({
            "pitch": 38,  # D1 - Standard snare
            "start_time": float(beat),
            "duration": 0.25,
            "velocity": 80,
            "mute": False,
        })
    return notes


def sixteenth_hats() -> list[dict]:
    """Generate 16th note hi-hat pattern.

    Closed hi-hats on every 16th note with velocity accents.
    """
    notes = []
    for step in range(INTRO_LENGTH * 4):  # 16th notes = 4x beats
        # Accent on downbeats
        if step % 16 == 0:  # First 16th of each bar
            velocity = 90
        elif step % 4 == 0:  # First 16th of each beat
            velocity = 75
        else:
            velocity = 55

        notes.append({
            "pitch": 42,  # F#1 - Closed hi-hat
            "start_time": step * 0.25,
            "duration": 0.125,
            "velocity": velocity,
            "mute": False,
        })

    # Add some open hats for variation (every 8 bars on the "and" of 4)
    for bar in range(0, INTRO_BARS, 8):
        beat = bar * 4 + 3.5  # "and" of beat 4
        notes.append({
            "pitch": 46,  # A#1 - Open hi-hat
            "start_time": beat,
            "duration": 0.5,
            "velocity": 70,
            "mute": False,
        })

    return notes


def tom_accents() -> list[dict]:
    """Generate tom accent pattern.

    Sparse tom hits for texture and fills.
    """
    notes = []
    tom_pitches = [45, 47, 50]  # A1, B1, D2 - Low, Mid, High tom

    # Intro toms: minimal, building pattern
    # Add some hits in the last 4 bars
    for bar in range(12, 16):  # Last 4 bars
        # One tom hit per bar
        if bar == 12:
            pitch = tom_pitches[0]  # Low
            beat = bar * 4 + 3
        elif bar == 13:
            pitch = tom_pitches[1]  # Mid
            beat = bar * 4 + 3
        elif bar == 14:
            pitch = tom_pitches[2]  # High
            beat = bar * 4 + 2.5
        else:  # bar == 15, fill
            # Quick tom roll
            for i, p in enumerate(reversed(tom_pitches)):
                notes.append({
                    "pitch": p,
                    "start_time": bar * 4 + 3 + i * 0.25,
                    "duration": 0.2,
                    "velocity": 85 + i * 5,
                    "mute": False,
                })
            continue

        notes.append({
            "pitch": pitch,
            "start_time": float(beat),
            "duration": 0.25,
            "velocity": 80,
            "mute": False,
        })

    return notes


def glitch_perc() -> list[dict]:
    """Generate industrial/glitch percussion pattern.

    Random-feeling but rhythmic industrial hits.
    """
    notes = []
    # Available pitches: 37=Rimshot, 39=Clap, 40=Snare2, 54=Tambourine

    # Glitch pattern: sparse, rhythmic noise hits
    positions = [
        (2, 1.5, 37, 70),   # Bar 3, beat 1.5, rimshot
        (4, 0.75, 39, 65),  # Bar 5, beat 0.75, clap
        (6, 2.25, 40, 60),  # Bar 7
        (8, 1.0, 54, 55),   # Bar 9
        (10, 3.5, 37, 75),  # Bar 11
        (12, 0.5, 39, 70),  # Bar 13
        (14, 2.0, 40, 65),  # Bar 15
        (15, 1.5, 54, 60),  # Bar 16
    ]

    for bar, beat_offset, pitch, vel in positions:
        notes.append({
            "pitch": pitch,
            "start_time": float(bar * 4 + beat_offset),
            "duration": 0.125,
            "velocity": vel,
            "mute": False,
        })

    return notes


def ride_pattern() -> list[dict]:
    """Generate ride cymbal pattern.

    Subtle ride texture for intro.
    """
    notes = []

    # Ride: very sparse in intro, just adding shimmer
    # Hit on beat 1 of every 4 bars
    for bar in range(0, INTRO_BARS, 4):
        notes.append({
            "pitch": 51,  # D#2 - Ride
            "start_time": float(bar * 4),
            "duration": 2.0,  # Let it ring
            "velocity": 50,
            "mute": False,
        })

    # Add bell hit at end of intro
    notes.append({
        "pitch": 53,  # F2 - Ride bell
        "start_time": float(15 * 4 + 3),  # Last bar, beat 4
        "duration": 1.0,
        "velocity": 70,
        "mute": False,
    })

    return notes


# Pattern function mapping
PATTERN_FUNCTIONS = {
    "four_on_floor": four_on_floor,
    "sparse_snare": sparse_snare,
    "sixteenth_hats": sixteenth_hats,
    "tom_accents": tom_accents,
    "glitch_perc": glitch_perc,
    "ride_pattern": ride_pattern,
}


def create_drum_track(client: AbletonClient, track: DrumTrack) -> bool:
    """Create a single drum track with pattern."""
    print(f"\n{'='*50}")
    print(f"Creating Track {track.index}: {track.name}")
    print(f"{'='*50}")

    try:
        # Step 1: Create MIDI track
        print("  Creating MIDI track...")
        client.send_command("create_midi_track", {"index": track.index})
        time.sleep(0.2)

        # Step 2: Set track name
        print(f"  Setting name to '{track.name}'...")
        client.send_command("set_track_name", {
            "track_index": track.index,
            "name": track.name,
        })
        time.sleep(0.1)

        # Step 3: Load Drum Rack
        print("  Loading Drum Rack...")
        drum_rack_uri = "query:Drums#Drum%20Rack"
        result = client.send_command("load_browser_item", {
            "track_index": track.index,
            "item_uri": drum_rack_uri,
        })
        print(f"    Loaded: {result.get('new_devices', ['Drum Rack'])}")
        time.sleep(0.3)

        # Step 4: Create clip (16 bars = 64 beats)
        print(f"  Creating {INTRO_BARS}-bar clip...")
        client.send_command("create_clip", {
            "track_index": track.index,
            "clip_index": 0,
            "length": float(INTRO_LENGTH),
        })
        time.sleep(0.2)

        # Step 5: Generate and add notes
        print(f"  Generating {track.pattern_func} pattern...")
        pattern_func = PATTERN_FUNCTIONS.get(track.pattern_func)
        if not pattern_func:
            raise ValueError(f"Unknown pattern: {track.pattern_func}")

        notes = pattern_func()
        print(f"    Generated {len(notes)} notes")

        # Add notes in batches if there are many
        batch_size = 100
        for i in range(0, len(notes), batch_size):
            batch = notes[i:i + batch_size]
            client.send_command("add_notes_to_clip", {
                "track_index": track.index,
                "clip_index": 0,
                "notes": batch,
            })
            time.sleep(0.1)
        print("    Added all notes to clip")

        # Step 6: Name the clip
        client.send_command("set_clip_name", {
            "track_index": track.index,
            "clip_index": 0,
            "name": f"{track.name} - Intro",
        })

        print(f"  ✓ Track '{track.name}' created successfully!")
        return True

    except Exception as e:
        print(f"  ✗ Failed to create track '{track.name}': {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("  INTRO DRUMS CREATOR - Lane 1")
    print("  'I Am Machine' Recreation")
    print("=" * 60)
    print("\nConfiguration:")
    print(f"  Tempo: {TEMPO} BPM")
    print(f"  Section: Intro (Bars 1-{INTRO_BARS})")
    print(f"  Tracks: {len(DRUM_TRACKS)}")

    # Connect to Ableton
    client = AbletonClient()
    if not client.connect():
        print("\n✗ Cannot connect to Ableton. Make sure:")
        print("  1. Ableton Live is running")
        print("  2. AbletonMCP is selected as Control Surface")
        print("  3. Remote Script is listening on port 9877")
        sys.exit(1)

    try:
        # Set tempo first
        print(f"\nSetting tempo to {TEMPO} BPM...")
        client.send_command("set_tempo", {"tempo": TEMPO})
        print(f"  ✓ Tempo set to {TEMPO} BPM")

        # Create each track
        success_count = 0
        for track in DRUM_TRACKS:
            if create_drum_track(client, track):
                success_count += 1

        # Summary
        print("\n" + "=" * 60)
        print("  SUMMARY")
        print("=" * 60)
        print(f"  Tracks created: {success_count}/{len(DRUM_TRACKS)}")

        if success_count == len(DRUM_TRACKS):
            print("\n  ✓ ALL DRUM TRACKS CREATED SUCCESSFULLY!")
            print("\n  Next steps:")
            print("    1. Fire clip slot 0 on any drum track to preview")
            print("    2. Run /intro-bass for Lane 2")
            print("    3. Adjust velocities/timing as needed")
        else:
            print("\n  ⚠ Some tracks failed. Check errors above.")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
