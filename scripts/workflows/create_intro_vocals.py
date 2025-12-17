#!/usr/bin/env python3
"""Create Intro Vocals/FX - Lane 4.

Creates vocal and FX tracks for intro section (Bars 1-16):
1. Main Vocal - Placeholder track
2. Vocal FX - Effects processing track
3. Risers - Build tension
4. Return A - Reverb
5. Return B - Delay

Logs to: intro_vocals.log (append-only)
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

LOG_FILE = Path(__file__).parent / "intro_vocals.log"


def log(msg: str):
    """Append message to log file."""
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")


@dataclass
class VocalTrack:
    name: str
    index: int
    device: str
    device_uri: str
    pattern_func: str
    effects: list[dict] | None = None
    is_return: bool = False


VOCAL_TRACKS = [
    VocalTrack(
        "Main Vocal", 11, "Sampler", "query:Instruments#Sampler",
        "vocal_placeholder",
        effects=[
            {"name": "EQ Eight", "uri": "query:AudioFx#EQ%20Eight"},
            {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
        ]
    ),
    VocalTrack(
        "Vocal FX", 12, "Vocoder", "query:AudioFx#Vocoder",
        "vocal_fx_texture",
        effects=[
            {"name": "Reverb", "uri": "query:AudioFx#Reverb"},
        ]
    ),
    VocalTrack(
        "Risers", 13, "Wavetable", "query:Synths#Wavetable",
        "riser_sweep",
        effects=[
            {"name": "Auto Filter", "uri": "query:AudioFx#Auto%20Filter"},
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


def vocal_placeholder() -> list[dict]:
    """Placeholder for vocal samples - empty for now."""
    return []


def vocal_fx_texture() -> list[dict]:
    """Vocal FX texture notes."""
    notes = []
    # Some atmospheric vocal-like texture hits
    positions = [
        (4, 60, 2.0, 40),   # Bar 5
        (8, 62, 1.5, 45),   # Bar 9
        (12, 58, 2.0, 50),  # Bar 13
    ]
    for bar, pitch, dur, vel in positions:
        notes.append({
            "pitch": pitch,
            "start_time": float(bar * 4),
            "duration": dur,
            "velocity": vel,
            "mute": False,
        })
    return notes


def riser_sweep() -> list[dict]:
    """Riser sweep building toward end of intro."""
    notes = []
    # Long rising sweep in last 8 bars (pitch bend would be ideal but we use C3)
    start_bar = 8

    # One long note that sweeps up
    notes.append({
        "pitch": 48,  # C3
        "start_time": float(start_bar * 4),
        "duration": float((INTRO_BARS - start_bar) * 4),  # 8 bars
        "velocity": 60,
        "mute": False,
    })

    # Add some tension notes building
    for i in range(8):
        bar = start_bar + i
        notes.append({
            "pitch": 48 + i * 2,  # Rising pitch
            "start_time": float(bar * 4 + 2),
            "duration": 2.0,
            "velocity": 40 + i * 5,
            "mute": False,
        })

    return notes


PATTERN_FUNCTIONS = {
    "vocal_placeholder": vocal_placeholder,
    "vocal_fx_texture": vocal_fx_texture,
    "riser_sweep": riser_sweep,
}


def create_return_tracks(client: AbletonClient) -> bool:
    """Create return tracks A and B."""
    log("Creating return tracks")
    print("\nCreating Return Tracks...")

    try:
        # Return A - Reverb
        print("  Creating Return A (Reverb)...")
        result = client.send_command("create_return_track", {"name": "Reverb"})
        log(f"  Created Return A: {result}")
        time.sleep(0.3)

        # Load reverb
        client.send_command("load_browser_item", {
            "track_index": -1,  # Return track
            "item_uri": "query:AudioFx#Hybrid%20Reverb",
        })
        log("  Loaded Hybrid Reverb on Return A")
        time.sleep(0.2)

        # Return B - Delay
        print("  Creating Return B (Delay)...")
        result = client.send_command("create_return_track", {"name": "Delay"})
        log(f"  Created Return B: {result}")
        time.sleep(0.3)

        # Load delay
        client.send_command("load_browser_item", {
            "track_index": -1,
            "item_uri": "query:AudioFx#Echo",
        })
        log("  Loaded Echo on Return B")

        print("  ✓ Return tracks created!")
        return True

    except Exception as e:
        log(f"ERROR: Failed to create return tracks: {e}")
        print(f"  ✗ Failed: {e}")
        return False


def create_vocal_track(client: AbletonClient, track: VocalTrack) -> bool:
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
    log("INTRO VOCALS/FX CREATOR - Lane 4 STARTED")
    log("=" * 60)

    print("=" * 60)
    print("  INTRO VOCALS/FX CREATOR - Lane 4")
    print("=" * 60)

    client = AbletonClient()
    if not client.connect():
        print("\n✗ Cannot connect to Ableton")
        sys.exit(1)

    try:
        # Create return tracks first
        create_return_tracks(client)

        success_count = 0
        for track in VOCAL_TRACKS:
            if create_vocal_track(client, track):
                success_count += 1

        print("\nFiring vocal/FX clips...")
        for track in VOCAL_TRACKS:
            client.send_command("fire_clip", {
                "track_index": track.index,
                "clip_index": 0,
            })
            log(f"Fired clip on track {track.index}")
            time.sleep(0.1)

        log(f"COMPLETED: {success_count}/{len(VOCAL_TRACKS)} tracks + returns created")
        total = len(VOCAL_TRACKS)
        print(f"\n✓ {success_count}/{total} vocal/FX tracks + 2 returns created!")

    except Exception as e:
        log(f"FATAL ERROR: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
