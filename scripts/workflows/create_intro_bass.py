#!/usr/bin/env python3
"""Create Intro Bass - Lane 2.

Creates bass tracks for intro section (Bars 1-16):
1. Rumble - Sub bass with sidechain to kick
2. Rolling Bass - Acid-style pattern
3. Acid - 303 sound

Logs to: intro_bass.log (append-only)
"""

import json
import socket
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Configuration
ABLETON_HOST = "localhost"
ABLETON_PORT = 9877
TEMPO = 136
INTRO_BARS = 16
INTRO_LENGTH = INTRO_BARS * 4  # 64 beats

LOG_FILE = Path(__file__).parent / "intro_bass.log"


def log(msg: str):
    """Append message to log file."""
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")


@dataclass
class BassTrack:
    name: str
    index: int
    device: str
    device_uri: str
    pattern_func: str
    effects: list[dict] | None = None
    needs_sidechain: bool = False


BASS_TRACKS = [
    BassTrack(
        "Rumble", 6, "Operator", "query:Synths#Operator",
        "sub_bass", needs_sidechain=True,
        effects=[
            {"name": "EQ Eight", "uri": "query:AudioFx#EQ%20Eight"},
            {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
        ]
    ),
    BassTrack(
        "Rolling Bass", 7, "Wavetable", "query:Synths#Wavetable",
        "rolling_bass"
    ),
    BassTrack(
        "Acid", 8, "Drift", "query:Synths#Drift",
        "acid_303"
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


def sub_bass() -> list[dict]:
    """Rumble sub bass - sustained low notes."""
    notes = []
    # F minor key - sustained sub bass
    for bar in range(INTRO_BARS):
        notes.append({
            "pitch": 29,  # F0 - deep sub
            "start_time": float(bar * 4),
            "duration": 4.0,
            "velocity": 100,
            "mute": False,
        })
    return notes


def rolling_bass() -> list[dict]:
    """Rolling bass - 16th note pattern."""
    notes = []
    # Intro: sparse, building
    pitches = [41, 41, 44, 41]  # F2, F2, Ab2, F2
    for bar in range(8, INTRO_BARS):  # Only last 8 bars
        for beat in range(4):
            for sixteenth in range(4):
                if (bar < 12 and sixteenth % 2 != 0):
                    continue  # Sparse first 4 bars
                pitch = pitches[(beat + sixteenth) % len(pitches)]
                notes.append({
                    "pitch": pitch,
                    "start_time": bar * 4 + beat + sixteenth * 0.25,
                    "duration": 0.2,
                    "velocity": 85 if sixteenth == 0 else 65,
                    "mute": False,
                })
    return notes


def acid_303() -> list[dict]:
    """303-style acid line."""
    notes = []
    # Classic 303 pattern - only in last 4 bars of intro
    pattern = [
        (0, 36, 0.75, 100),    # F1
        (0.75, 36, 0.25, 70),
        (1, 39, 0.5, 90),      # Ab1
        (1.5, 36, 0.25, 60),
        (2, 41, 0.75, 95),     # Bb1
        (2.75, 43, 0.25, 70),  # C2
        (3, 36, 0.5, 85),
        (3.5, 39, 0.5, 75),
    ]
    for bar in range(12, INTRO_BARS):  # Last 4 bars
        for beat_offset, pitch, duration, vel in pattern:
            notes.append({
                "pitch": pitch,
                "start_time": bar * 4 + beat_offset,
                "duration": duration,
                "velocity": vel,
                "mute": False,
            })
    return notes


PATTERN_FUNCTIONS = {
    "sub_bass": sub_bass,
    "rolling_bass": rolling_bass,
    "acid_303": acid_303,
}


def create_bass_track(client: AbletonClient, track: BassTrack) -> bool:
    log(f"Creating track {track.index}: {track.name}")
    print(f"\n{'='*50}")
    print(f"Creating Track {track.index}: {track.name}")
    print(f"{'='*50}")

    try:
        # Create MIDI track
        print("  Creating MIDI track...")
        client.send_command("create_midi_track", {"index": track.index})
        log(f"  Created MIDI track at index {track.index}")
        time.sleep(0.2)

        # Set name
        print(f"  Setting name to '{track.name}'...")
        client.send_command("set_track_name", {
            "track_index": track.index,
            "name": track.name,
        })
        time.sleep(0.1)

        # Load synth
        print(f"  Loading {track.device}...")
        result = client.send_command("load_browser_item", {
            "track_index": track.index,
            "item_uri": track.device_uri,
        })
        log(f"  Loaded {track.device}: {result.get('new_devices', [])}")
        time.sleep(0.3)

        # Load effects if any
        if track.effects:
            for effect in track.effects:
                print(f"  Loading {effect['name']}...")
                client.send_command("load_browser_item", {
                    "track_index": track.index,
                    "item_uri": effect["uri"],
                })
                log(f"  Loaded effect: {effect['name']}")
                time.sleep(0.2)

        # Set up sidechain if needed
        if track.needs_sidechain:
            print("  Setting up sidechain to Kick...")
            try:
                # Find compressor device index (should be last loaded)
                client.send_command("set_sidechain_input", {
                    "track_index": track.index,
                    "device_index": -1,  # Last device
                    "source_track_index": 0,  # Kick
                })
                log("  Sidechain configured to track 0 (Kick)")
            except Exception as e:
                log(f"  WARNING: Sidechain setup failed: {e}")
                print("    ⚠ Sidechain setup failed (may need manual config)")

        # Create clip
        print(f"  Creating {INTRO_BARS}-bar clip...")
        client.send_command("create_clip", {
            "track_index": track.index,
            "clip_index": 0,
            "length": float(INTRO_LENGTH),
        })
        time.sleep(0.2)

        # Generate and add notes
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

        # Name clip
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
    log("INTRO BASS CREATOR - Lane 2 STARTED")
    log("=" * 60)

    print("=" * 60)
    print("  INTRO BASS CREATOR - Lane 2")
    print("=" * 60)

    client = AbletonClient()
    if not client.connect():
        print("\n✗ Cannot connect to Ableton")
        sys.exit(1)

    try:
        success_count = 0
        for track in BASS_TRACKS:
            if create_bass_track(client, track):
                success_count += 1

        # Fire clips
        print("\nFiring bass clips...")
        for track in BASS_TRACKS:
            client.send_command("fire_clip", {
                "track_index": track.index,
                "clip_index": 0,
            })
            log(f"Fired clip on track {track.index}")
            time.sleep(0.1)

        log(f"COMPLETED: {success_count}/{len(BASS_TRACKS)} tracks created")
        print(f"\n✓ {success_count}/{len(BASS_TRACKS)} bass tracks created!")

    except Exception as e:
        log(f"FATAL ERROR: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
