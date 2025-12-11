
import pytest
import time

@pytest.mark.live
def test_load_simpler(client, live_session):
    """Verify loading a basic synth (Simpler)."""
    # 1. Use Track 0
    info = client("get_track_info", {"track_index": 0})
    if info.get("status") != "success":
        client("create_midi_track", {"index": 0})
    
    # 2. Clear devices (hack: just delete track and recreate if messy? No, let's just load over)
    
    # 3. Load
    uri = "query:Synths#Simpler"
    res = client("load_browser_item", {"track_index": 0, "item_uri": uri})
    assert res.get("status") == "success", f"Failed to load Simpler: {res}"
    
    # 4. Verify
    time.sleep(1)
    info = client("get_track_info", {"track_index": 0})
    devices = [d["name"] for d in info["result"]["devices"]]
    assert "Simpler" in devices

@pytest.mark.live
def test_load_drum_kit(client, find_loadable):
    """Verify loading a drum kit from browser."""
    # 1. Use Track 1
    client("create_midi_track", {"index": 1})
    
    # 2. Find Kit
    uri = find_loadable("Drums")
    if not uri:
        pytest.skip("No drum kits found")
        
    # 3. Load
    print(f"Loading {uri}...")
    res = client("load_browser_item", {"track_index": 1, "item_uri": uri})
    assert res.get("status") == "success"
    
    # 4. Verify
    time.sleep(2)
    info = client("get_track_info", {"track_index": 1})
    classes = [d["class_name"] for d in info["result"]["devices"]]
    assert "DrumGroupDevice" in classes, "Drum Rack not found"
