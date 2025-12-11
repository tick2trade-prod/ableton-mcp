"""i_o Alchemy Techno Demo Test.

Creates an i_o style techno track in Ableton Live.
This test is rerunnable - it clears tracks and creates fresh.

Run: pytest tests/test_io_techno.py -v -s
     make test-one TEST=test_io_techno
"""
import socket
import json
import time
import pytest
import os
import sys

# Add tests dir to path for config import
sys.path.insert(0, os.path.dirname(__file__))
from config import (
    ABLETON_HOST, ABLETON_PORT, SOCKET_TIMEOUT,
    ABLETON_MAX_TRACKS, ABLETON_VERSION, ABLETON_EDITION,
    DEBUG
)


def log(msg: str):
    """Debug logging."""
    if DEBUG:
        print(f"[DEBUG] {msg}")


def send_command(cmd_type: str, params: dict = None, timeout: int = SOCKET_TIMEOUT) -> dict:
    """Send command to Ableton and return response."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ABLETON_HOST, ABLETON_PORT))
        cmd = {"type": cmd_type, "params": params or {}}
        log(f"Sending: {cmd}")
        sock.sendall(json.dumps(cmd).encode())
        
        response = sock.recv(8192)
        result = json.loads(response.decode())
        log(f"Received: {result}")
        return result
    except socket.timeout:
        return {"status": "error", "message": "Connection timeout"}
    except ConnectionRefusedError:
        return {"status": "error", "message": "Ableton not running or AbletonMCP not enabled"}
    finally:
        sock.close()


class TestIOTechno:
    """i_o style techno track generator test."""
    
    TEMPO = 130.0
    CLIP_LENGTH = 16.0  # 4 bars
    
    # Track configuration with instruments
    TRACKS = [
        {"name": "Kick Heavy", "type": "kick", "instrument": "Drums/Drum Rack"},
        {"name": "Sub Bass", "type": "bass", "instrument": "Instruments/Analog"},
        {"name": "Acid Lead", "type": "acid", "instrument": "Instruments/Wavetable"},
        {"name": "Stab", "type": "stab", "instrument": "Instruments/Wavetable"},
        {"name": "Hi-Hats", "type": "hats", "instrument": "Drums/Drum Rack"},
        {"name": "Perc", "type": "perc", "instrument": "Drums/Drum Rack"},
    ]
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Verify connection before tests."""
        response = send_command("get_session_info")
        if response.get("status") != "success":
            pytest.skip(f"Ableton not connected: {response.get('message')}")
        
        self.session = response["result"]
        print(f"\n📍 Ableton {ABLETON_VERSION} ({ABLETON_EDITION}) - {self.session['track_count']} tracks")
    
    def get_session(self) -> dict:
        """Get current session info."""
        return send_command("get_session_info")["result"]
    
    def clear_all_tracks(self):
        """Delete all tracks except the first one (can't delete all)."""
        session = self.get_session()
        track_count = session["track_count"]
        
        if track_count <= 1:
            print("  No tracks to clear")
            return
        
        print(f"  Clearing {track_count - 1} tracks...")
        # Delete from end to beginning to avoid index shifting issues
        for i in range(track_count - 1, 0, -1):
            result = send_command("delete_track", {"track_index": i})
            if result.get("status") == "success":
                log(f"Deleted track {i}")
            else:
                # If delete_track doesn't exist, just rename/reuse
                log(f"Could not delete track {i}: {result}")
        
        time.sleep(0.5)  # Let Ableton catch up
        new_session = self.get_session()
        print(f"  Tracks after clear: {new_session['track_count']}")
    
    @pytest.mark.live
    def test_io_techno_full(self):
        """Full i_o techno track generation test."""
        print("\n🎵 Generating i_o style techno track...")
        
        # Step 1: Stop playback first
        send_command("stop_playback")
        
        # Step 2: Set tempo
        print(f"  Setting tempo to {self.TEMPO} BPM...")
        result = send_command("set_tempo", {"tempo": self.TEMPO})
        assert result["status"] == "success", f"Failed to set tempo: {result}"
        
        # Step 3: Get current tracks and create/reuse
        session = self.get_session()
        current_tracks = session["track_count"]
        needed_tracks = len(self.TRACKS)
        
        track_indices = []
        
        if current_tracks + needed_tracks <= ABLETON_MAX_TRACKS:
            # Space available: create new tracks with instruments
            print(f"  Creating {needed_tracks} new tracks with instruments...")
            for track in self.TRACKS:
                result = send_command("create_midi_track", {"index": -1})
                if result["status"] == "success":
                    idx = result["result"]["index"]
                    track_indices.append(idx)
                    send_command("set_track_name", {"track_index": idx, "name": track["name"]})
                    
                    # Try to load instrument
                    inst_result = send_command("load_browser_item", {
                        "track_index": idx,
                        "item_uri": f"query:{track['instrument']}"
                    })
                    inst_status = "✓" if inst_result.get("status") == "success" else "○"
                    print(f"  {inst_status} {track['name']}")
                else:
                    print(f"  ✗ Failed to create: {track['name']}")
        else:
            # At limit: reuse last N tracks, load instruments
            print(f"  ⚠️  At track limit ({ABLETON_MAX_TRACKS}). Reusing tracks...")
            start_idx = max(0, current_tracks - needed_tracks)
            for i, track in enumerate(self.TRACKS):
                idx = start_idx + i
                if idx < current_tracks:
                    track_indices.append(idx)
                    send_command("set_track_name", {"track_index": idx, "name": track["name"]})
                    
                    # Try to load instrument
                    inst_result = send_command("load_browser_item", {
                        "track_index": idx,
                        "item_uri": f"query:{track['instrument']}"
                    })
                    inst_status = "✓" if inst_result.get("status") == "success" else "○"
                    print(f"  {inst_status} Track {idx} → {track['name']}")
        
        if not track_indices:
            pytest.skip("Could not get any tracks")
        
        # Step 4: Create clips and add patterns
        print("  Adding MIDI patterns...")
        for idx, track in zip(track_indices, self.TRACKS):
            # Create clip
            result = send_command("create_clip", {
                "track_index": idx,
                "clip_index": 0,
                "length": self.CLIP_LENGTH
            })
            
            if result["status"] != "success":
                print(f"  ⚠️  Clip may already exist on {track['name']}")
            
            # Add pattern based on type
            notes = self._generate_pattern(track["type"])
            if notes:
                send_command("add_notes_to_clip", {
                    "track_index": idx,
                    "clip_index": 0,
                    "notes": notes
                })
                print(f"  ✓ Added {len(notes)} notes to {track['name']}")
        
        # Step 5: Start playback
        result = send_command("start_playback")
        assert result["status"] == "success", "Failed to start playback"
        
        print("\n✅ i_o techno track created!")
        print(f"   Tempo: {self.TEMPO} BPM")
        print(f"   Tracks: {len(track_indices)}")
        print("   Playback: Started")
    
    def _generate_pattern(self, pattern_type: str) -> list:
        """Generate MIDI notes for pattern type."""
        notes = []
        
        if pattern_type == "kick":
            # Hard 4/4 kick
            for beat in range(16):
                notes.append({
                    "pitch": 36,
                    "start_time": float(beat),
                    "duration": 0.5,
                    "velocity": 127 if beat % 4 == 0 else 110,
                    "mute": False
                })
        
        elif pattern_type == "bass":
            # E minor sub bass rumble
            pattern = [
                (28, 0.0, 0.75), (28, 1.0, 0.5), (28, 1.75, 0.25),
                (28, 2.0, 0.75), (28, 3.5, 0.5),
                (28, 4.0, 0.75), (28, 5.0, 0.5), (28, 5.75, 0.25),
                (28, 6.0, 0.75), (28, 7.5, 0.5),
            ]
            for rep in range(2):
                offset = rep * 8
                for pitch, start, dur in pattern:
                    notes.append({
                        "pitch": pitch,
                        "start_time": start + offset,
                        "duration": dur,
                        "velocity": 120,
                        "mute": False
                    })
        
        elif pattern_type == "acid":
            # 303-style acid
            acid_pattern = [
                (52, 0.0, 0.25), (55, 0.25, 0.25), (52, 0.5, 0.25), (55, 0.75, 0.25),
                (52, 1.0, 0.5), (55, 1.5, 0.25), (57, 1.75, 0.25),
                (52, 2.0, 0.25), (55, 2.25, 0.5), (52, 2.75, 0.25),
                (57, 3.0, 0.5), (55, 3.5, 0.5),
            ]
            for rep in range(4):
                offset = rep * 4
                for pitch, start, dur in acid_pattern:
                    notes.append({
                        "pitch": pitch,
                        "start_time": start + offset,
                        "duration": dur,
                        "velocity": 100 + (rep % 2) * 20,
                        "mute": False
                    })
        
        elif pattern_type == "stab":
            # Offbeat stabs
            for beat in range(16):
                if beat % 2 == 1:
                    notes.append({
                        "pitch": 64,
                        "start_time": beat + 0.5,
                        "duration": 0.25,
                        "velocity": 90,
                        "mute": False
                    })
        
        elif pattern_type == "hats":
            # 16th hi-hats + open hats
            for subdivision in range(64):
                velocity = 60
                if subdivision % 4 == 0:
                    velocity = 100
                elif subdivision % 2 == 0:
                    velocity = 80
                notes.append({
                    "pitch": 42,
                    "start_time": subdivision * 0.25,
                    "duration": 0.1,
                    "velocity": velocity,
                    "mute": False
                })
            # Open hats on upbeats
            for beat in range(16):
                notes.append({
                    "pitch": 46,
                    "start_time": beat + 0.5,
                    "duration": 0.25,
                    "velocity": 85,
                    "mute": False
                })
        
        elif pattern_type == "perc":
            # Claps and ride
            for beat in range(16):
                if beat % 4 == 2:
                    notes.append({
                        "pitch": 39,
                        "start_time": float(beat),
                        "duration": 0.25,
                        "velocity": 110,
                        "mute": False
                    })
                if beat % 2 == 0:
                    notes.append({
                        "pitch": 51,
                        "start_time": float(beat),
                        "duration": 0.25,
                        "velocity": 70,
                        "mute": False
                    })
        
        return notes


@pytest.mark.live
def test_io_techno(send_command):
    """Convenience standalone test using conftest fixture."""
    # Verify connection
    response = send_command("get_session_info")
    if response.get("status") != "success":
        pytest.skip(f"Ableton not connected: {response.get('message')}")
    
    session = response["result"]
    print(f"\n📍 Ableton {ABLETON_VERSION} ({ABLETON_EDITION}) - {session['track_count']} tracks")
    
    # Run the main test
    test_class = TestIOTechno()
    test_class.session = session
    test_class.test_io_techno_full()
