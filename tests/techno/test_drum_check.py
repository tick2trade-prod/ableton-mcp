
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
def test_drum_kit_sound():
    """
    Hypothesis: Loading a specific Drum Kit from 'Drums' category works.
    """
    print("\n🥁 Drum Check Test...")
    
    # 1. Target Track 1
    info = send_command("get_track_info", {"track_index": 1})
    if info.get("status") != "success":
        send_command("create_midi_track", {"index": 1})
        
    send_command("stop_playback")
    
    # 2. Find a Kit
    print("  Searching for a Drum Kit...")
    res = send_command("get_browser_items_at_path", {"path": "Drums"})
    
    kit_uri = None
    if res.get("status") == "success":
        # Look for "Core 808" or just "Kit"
        for item in res["result"]["items"]:
            if item["is_loadable"] and "Kit" in item["name"]:
                kit_uri = item["uri"]
                print(f"  Found Kit: {item['name']}")
                break
    
    if not kit_uri:
        # Fallback to just first loadable item
        for item in res["result"]["items"]:
            if item["is_loadable"]:
                kit_uri = item["uri"]
                print(f"  Fallback to: {item['name']}")
                break
                
    if not kit_uri:
        pytest.fail("No drum kits found in browser 'Drums' category")
        
    # 3. Load it
    print(f"  Loading: {kit_uri}...")
    load_res = send_command("load_browser_item", {
        "track_index": 1, 
        "item_uri": kit_uri
    })
    
    time.sleep(2.0) # Drums take longer
    
    # 4. Verify
    info = send_command("get_track_info", {"track_index": 1})
    devices = info["result"]["devices"]
    print(f"  Devices: {devices}")
    
    assert len(devices) > 0, "No devices loaded"
    # Drum Racks usually have class_name 'DrumGroupDevice'
    assert any(d["class_name"] == "DrumGroupDevice" for d in devices), "Device is not a Drum Rack"
    
    # 5. Play Beat
    print("  Playing Kick (C1)...")
    send_command("create_clip", {"track_index": 1, "clip_index": 0, "length": 4.0})
    send_command("add_notes_to_clip", {
        "track_index": 1, 
        "clip_index": 0, 
        "notes": [
            {"pitch": 36, "start_time": 0, "duration": 0.5, "velocity": 127, "mute": False},
            {"pitch": 36, "start_time": 1, "duration": 0.5, "velocity": 127, "mute": False},
            {"pitch": 36, "start_time": 2, "duration": 0.5, "velocity": 127, "mute": False},
            {"pitch": 36, "start_time": 3, "duration": 0.5, "velocity": 127, "mute": False},
        ]
    })
    
    send_command("fire_clip", {"track_index": 1, "clip_index": 0})
    send_command("start_playback")
    
    time.sleep(4)
    print("  ✅ Heard the kick?")
