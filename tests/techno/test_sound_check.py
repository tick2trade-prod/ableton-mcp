
import pytest
import time
import socket
import json
import sys
import os

# Add tests dir to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import ABLETON_HOST, ABLETON_PORT, SOCKET_TIMEOUT

def send_command(cmd_type: str, params: dict = None, timeout: int = SOCKET_TIMEOUT) -> dict:
    """Send command helper."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ABLETON_HOST, ABLETON_PORT))
        cmd = {"type": cmd_type, "params": params or {}}
        sock.sendall(json.dumps(cmd).encode())
        
        # Buffer loop for reliability
        response = b""
        while True:
            chunk = sock.recv(32768)
            if not chunk: break
            response += chunk
            if response.strip().endswith(b"}") and response.count(b"{") == response.count(b"}"):
                break
        return json.loads(response.decode())
    finally:
        sock.close()

@pytest.mark.live
def test_single_track_sound():
    """
    Hypothesis: Loading 'Simpler' from browser produces a track with 1 device 
    and output capability.
    """
    print("\n🔊 Sound Check Test...")
    
    # 1. New Track via create_midi_track (which might reuse if limit hit, but we'll try)
    # Actually, let's target track index 0 for simplicity.
    print("  Targeting Track 0...")
    
    # Ensure track 0 exists (it usually does) or create it
    info = send_command("get_track_info", {"track_index": 0})
    if info.get("status") != "success":
        # Try to create
        send_command("create_midi_track", {"index": 0})
    
    # 2. Stop playback
    send_command("stop_playback")
    
    # 3. Load Simpler (guaranteed sound source)
    print("  Loading Simpler...")
    res = send_command("load_browser_item", {
        "track_index": 0, 
        "item_uri": "query:Synths#Simpler"
    })
    
    if res.get("status") != "success":
        # Fallback to recursion if simple URI fails (unlikely based on check)
        pytest.fail(f"Could not load Simpler: {res}")
        
    time.sleep(1.0) # Wait for load
    
    # 4. Verify Device Check
    info = send_command("get_track_info", {"track_index": 0})
    devices = info["result"]["devices"]
    print(f"  Devices on track 0: {devices}")
    
    assert len(devices) > 0, "No devices found on track! Browser load failed silently?"
    assert "Simpler" in [d["name"] for d in devices], "Simpler device not found on track"
    
    # 5. Add Note & Play
    print("  Adding Note...")
    send_command("create_clip", {"track_index": 0, "clip_index": 0, "length": 4.0})
    send_command("add_notes_to_clip", {
        "track_index": 0, 
        "clip_index": 0, 
        "notes": [{"pitch": 60, "start_time": 0, "duration": 1.0, "velocity": 127, "mute": False}]
    })
    
    print("  Firing Clip...")
    send_command("fire_clip", {"track_index": 0, "clip_index": 0})
    send_command("start_playback")
    
    time.sleep(2)
    print("  ✅ Heard that? Track 0 should be beeping.")
