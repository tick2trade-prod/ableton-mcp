#!/usr/bin/env python3
"""Create Intro Synths - Lane 3.

Creates synth tracks for intro section (Bars 1-16):
1. Stabs - Techno chord stabs
2. Drone - Atmospheric pad

Logs to: intro_synths.log (append-only)
"""

import json
import socket
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ABLETON_HOST = "localhost"
ABLETON_PORT = 9877
INTRO_BARS = 16
INTRO_LENGTH = INTRO_BARS * 4

LOG_FILE = Path(__file__).parent / "intro_synths.log"


def log(msg: str):
    """Append message to log file."""
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")


@dataclass
class SynthTrack:
    name: str
    index: int
    device: str
    device_uri: str
    pattern_func: str
    effects: list[dict] | None = None


SYNTH_TRACKS = [
    SynthTrack(
        "Stabs", 9, "Wavetable", "query:Synths#Wavetable",
        "stab_chords",
        effects=[
            {"name": "Auto Filter", "uri": "query:AudioFx#Auto%20Filter"},
            {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
        ]
    ),
    SynthTrack(
        "Drone", 10, "Operator", "query:Synths#Operator",
        "ambient_drone",
        effects=[
            {"name": "Hybrid Reverb", "uri": "query:AudioFx#Hybrid%20Reverb"},
            {"name": "Auto Pan", "uri": "query:AudioFx#Auto%20Pan"},
        ]
    ),
]


class AbletonClient:
    def __init__(self, host: str = ABLETON_HOST, port: int = ABLETON_PORT):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None

    def connect(self) -> bool:
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            log(f"Connected to Ableton at {self.host}:{self.port}")
            return True
        except Exception as e:
            log(f"ERROR: Failed to connect: {e}")
            self.sock = None
            return False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_command(
        self, command_type: str, params: dict[str, Any] | None = None
    ) -> dict:
        if not self.sock:
            raise ConnectionError("Not connected")
        command = {"type": command_type, "params": params or {}}
        try:
            self.sock.sendall(json.dumps(command).encode("utf-8"))
            time.sleep(0.1)
            self.sock.settimeout(15.0)
            chunks = []
            while True:
                try:
                    chunk = self.sock.recv(8192)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    try:
                        data = b"".join(chunks)
                        response = json.loads(data.decode("utf-8"))
                        if response.get("status") == "error":
                            raise Exception(response.get("message"))
                        return response.get("result", {})
                    except json.JSONDecodeError:
                        continue
                except socket.timeout:
                    break
            if chunks:
                data = b"".join(chunks)
                response = json.loads(data.decode("utf-8"))
                return response.get("result", {})
            raise Exception("No response")
        except Exception as e:
            log(f"ERROR: Command {command_type} failed: {e}")
            raise


def stab_chords() -> list[dict]:
    """Techno stab chords - off-beat hits."""
    notes = []
    # Fm chord: F3, Ab3, C4
    chord = [53, 56, 60]

    # Off-beat stabs: & of 1, & of 3 in each bar
    for bar in range(4, INTRO_BARS):  # Start at bar 5
        for beat_offset in [0.5, 2.5]:
            for pitch in chord:
                notes.append({
                    "pitch": pitch,
                    "start_time": bar * 4 + beat_offset,
                    "duration": 0.2,
                    "velocity": 80 if bar < 12 else 90,
                    "mute": False,
                })
    return notes


def ambient_drone() -> list[dict]:
    """Atmospheric drone pad."""
    notes = []
    # Fm7 chord spread: F2, Ab2, C3, Eb3
    chord = [41, 44, 48, 51]

    # Long sustained notes spanning multiple bars
    for section in range(4):  # 4 sections of 4 bars each
        start = section * 16  # Every 4 bars
        for pitch in chord:
            notes.append({
                "pitch": pitch,
                "start_time": float(start),
                "duration": 16.0,  # 4 bars
                "velocity": 50 + section * 5,  # Gradually louder
                "mute": False,
            })
    return notes


PATTERN_FUNCTIONS = {
    "stab_chords": stab_chords,
    "ambient_drone": ambient_drone,
}


def create_synth_track(client: AbletonClient, track: SynthTrack) -> bool:
    log(f"Creating track {track.index}: {track.name}")
    print(f"\n{'='*50}")
    print(f"Creating Track {track.index}: {track.name}")
    print(f"{'='*50}")

    try:
        print("  Creating MIDI track...")
        client.send_command("create_midi_track", {"index": track.index})
        log(f"  Created MIDI track at index {track.index}")
        time.sleep(0.2)

        print(f"  Setting name to '{track.name}'...")
        client.send_command("set_track_name", {
            "track_index": track.index,
            "name": track.name,
        })
        time.sleep(0.1)

        print(f"  Loading {track.device}...")
        result = client.send_command("load_browser_item", {
            "track_index": track.index,
            "item_uri": track.device_uri,
        })
        log(f"  Loaded {track.device}: {result.get('new_devices', [])}")
        time.sleep(0.3)

        if track.effects:
            for effect in track.effects:
                print(f"  Loading {effect['name']}...")
                client.send_command("load_browser_item", {
                    "track_index": track.index,
                    "item_uri": effect["uri"],
                })
                log(f"  Loaded effect: {effect['name']}")
                time.sleep(0.2)

        print(f"  Creating {INTRO_BARS}-bar clip...")
        client.send_command("create_clip", {
            "track_index": track.index,
            "clip_index": 0,
            "length": float(INTRO_LENGTH),
        })
        time.sleep(0.2)

        print(f"  Generating {track.pattern_func} pattern...")
        pattern_func = PATTERN_FUNCTIONS.get(track.pattern_func)
        if not pattern_func:
            raise ValueError(f"Unknown pattern: {track.pattern_func}")

        notes = pattern_func()
        log(f"  Generated {len(notes)} notes for {track.pattern_func}")
        print(f"    Generated {len(notes)} notes")

        if notes:
            batch_size = 100
            for i in range(0, len(notes), batch_size):
                batch = notes[i:i + batch_size]
                client.send_command("add_notes_to_clip", {
                    "track_index": track.index,
                    "clip_index": 0,
                    "notes": batch,
                })
                time.sleep(0.1)

        client.send_command("set_clip_name", {
            "track_index": track.index,
            "clip_index": 0,
            "name": f"{track.name} - Intro",
        })

        log(f"  SUCCESS: Track '{track.name}' created")
        print(f"  ✓ Track '{track.name}' created successfully!")
        return True

    except Exception as e:
        log(f"  ERROR: Failed to create '{track.name}': {e}")
        print(f"  ✗ Failed: {e}")
        return False


def main():
    log("=" * 60)
    log("INTRO SYNTHS CREATOR - Lane 3 STARTED")
    log("=" * 60)

    print("=" * 60)
    print("  INTRO SYNTHS CREATOR - Lane 3")
    print("=" * 60)

    client = AbletonClient()
    if not client.connect():
        print("\n✗ Cannot connect to Ableton")
        sys.exit(1)

    try:
        success_count = 0
        for track in SYNTH_TRACKS:
            if create_synth_track(client, track):
                success_count += 1

        print("\nFiring synth clips...")
        for track in SYNTH_TRACKS:
            client.send_command("fire_clip", {
                "track_index": track.index,
                "clip_index": 0,
            })
            log(f"Fired clip on track {track.index}")
            time.sleep(0.1)

        log(f"COMPLETED: {success_count}/{len(SYNTH_TRACKS)} tracks created")
        print(f"\n✓ {success_count}/{len(SYNTH_TRACKS)} synth tracks created!")

    except Exception as e:
        log(f"FATAL ERROR: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
