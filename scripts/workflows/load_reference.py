#!/usr/bin/env python3
"""Load Reference Track and Guide Stem Separation.

This script:
1. Creates an audio track for the reference song
2. Provides guidance for loading the reference MP3
3. Provides instructions for stem separation in Ableton 12.3

Reference file: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3

Logs to: load_reference.log (append-only)
"""

import json
import socket
import sys
import time
from pathlib import Path
from typing import Any

ABLETON_HOST = "localhost"
ABLETON_PORT = 9877
REFERENCE_FILE = Path(__file__).parent.parent.parent / (
    "assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3"
)

LOG_FILE = Path(__file__).parent / "load_reference.log"


def log(msg: str):
    """Append message to log file."""
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")


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


def get_session_track_count(client: AbletonClient) -> int:
    """Get the current number of tracks."""
    result = client.send_command("get_session_info")
    return result.get("track_count", 0)


def main():
    log("=" * 60)
    log("LOAD REFERENCE TRACK - Started")
    log("=" * 60)

    print("=" * 60)
    print("  LOAD REFERENCE TRACK")
    print("  Reference: I Am Machine - Lilly Palmer")
    print("=" * 60)

    # Check if reference file exists
    if not REFERENCE_FILE.exists():
        print("\nERROR: Reference file not found at:")
        print(f"  {REFERENCE_FILE}")
        log(f"ERROR: Reference file not found: {REFERENCE_FILE}")
        sys.exit(1)

    print(f"\nReference file: {REFERENCE_FILE.name}")
    print(f"Size: {REFERENCE_FILE.stat().st_size / (1024*1024):.1f} MB")

    client = AbletonClient()
    if not client.connect():
        print("\nERROR: Cannot connect to Ableton")
        sys.exit(1)

    try:
        # Get current track count
        track_count = get_session_track_count(client)
        print(f"\nCurrent track count: {track_count}")

        # Create audio track at the end
        print("\nCreating audio track for reference...")
        result = client.send_command("create_audio_track", {"index": -1})
        ref_track_idx = result.get("index", track_count)
        log(f"Created audio track at index {ref_track_idx}")
        print(f"  Created audio track at index {ref_track_idx}")
        time.sleep(0.2)

        # Set track name
        client.send_command("set_track_name", {
            "track_index": ref_track_idx,
            "name": "Reference - I Am Machine"
        })
        log("Set track name to 'Reference - I Am Machine'")
        print("  Named track 'Reference - I Am Machine'")

        # Try to load the audio file
        print("\nAttempting to load reference file...")
        result = client.send_command("load_audio_file", {
            "track_index": ref_track_idx,
            "file_path": str(REFERENCE_FILE),
            "clip_slot": 0
        })

        if result.get("loaded"):
            print(f"  Loaded: {result.get('file_name')}")
            log("Successfully loaded reference file")
        else:
            print(f"\n  Note: {result.get('error', 'Could not load automatically')}")
            print("\n  MANUAL STEP REQUIRED:")
            print("  1. Open Ableton's browser (Cmd+Alt+B on Mac)")
            print(f"  2. Navigate to: {REFERENCE_FILE.parent}")
            print(f"  3. Drag '{REFERENCE_FILE.name}' onto track {ref_track_idx}")
            print("\n  OR add the folder to Places in Ableton's browser:")
            print("  1. In Ableton browser, click 'Add Folder...'")
            print(f"  2. Select: {REFERENCE_FILE.parent}")
            log(f"Manual load required: {result.get('error')}")

        # Provide stem separation guidance
        print("\n" + "=" * 60)
        print("  STEM SEPARATION INSTRUCTIONS")
        print("=" * 60)
        print("""
After loading the reference track:

1. Select the audio clip on the Reference track

2. Go to Create menu > "Separate Stems to New Audio Tracks"
   OR right-click the clip > "Separate Stems to New Audio Tracks"

3. Choose quality mode:
   - High Speed: ~2-3 min processing, good for quick preview
   - High Quality: ~5-10 min processing, better separation

4. Wait for processing to complete
   (Ableton will show a progress indicator)

5. A new Group Track will be created with 4 stem tracks:
   - Vocals (will be mostly empty for this techno track)
   - Drums  (kick, snare, hi-hats, percussion)
   - Bass   (sub bass, bass synths)
   - Others (synths, pads, FX)

6. Stems are saved to:
   <Project>/Samples/Processed/Stems/

After separation, you can:
- Solo each stem to analyze patterns
- Export stems for external analysis with librosa
- Compare drum stem to our recreated drum tracks
""")
        log("Displayed stem separation instructions")

        print("\n" + "=" * 60)
        print("  NEXT STEPS")
        print("=" * 60)
        print("""
1. Load the reference MP3 (if not loaded automatically)
2. Run stem separation in Ableton
3. Run compare_stems.py to analyze the separated stems
4. Update workflow scripts based on analysis
""")

        log("COMPLETED: Reference track setup")

    except Exception as e:
        log(f"FATAL ERROR: {e}")
        print(f"\nERROR: {e}")
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
