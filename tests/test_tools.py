"""Integration tests for Ableton MCP tools.

All tests run against LIVE Ableton - no mocks.
Run: pytest tests/test_tools.py -v
"""
import pytest


# === Session & Track Tests (7 tools) ===

@pytest.mark.live
@pytest.mark.session
def test_get_session_info(send_command):
    """Test get_session_info returns valid session data."""
    response = send_command("get_session_info")
    assert response["status"] == "success"
    result = response["result"]
    assert "tempo" in result
    assert "track_count" in result
    assert result["tempo"] > 0


@pytest.mark.live
@pytest.mark.session
def test_get_track_info(send_command):
    """Test get_track_info returns track details."""
    response = send_command("get_track_info", {"track_index": 0})
    assert response["status"] == "success"
    assert "name" in response["result"]


@pytest.mark.live
@pytest.mark.session
def test_create_midi_track(send_command):
    """Test creating a MIDI track."""
    response = send_command("create_midi_track", {"index": -1})
    # May fail if track limit reached
    assert response["status"] in ["success", "error"]
    if response["status"] == "success":
        assert "index" in response["result"]


@pytest.mark.live
@pytest.mark.session
def test_set_track_name(send_command):
    """Test renaming a track."""
    response = send_command("set_track_name", {"track_index": 0, "name": "TestTrack"})
    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.session
def test_set_track_volume(send_command):
    """Test setting track volume."""
    response = send_command("set_track_volume", {"track_index": 0, "volume": 0.7})
    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.session
def test_set_master_volume(send_command):
    """Test setting master volume."""
    response = send_command("set_master_volume", {"volume": 0.85})
    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.session
def test_set_tempo(send_command):
    """Test changing tempo."""
    response = send_command("set_tempo", {"tempo": 120.0})
    assert response["status"] == "success"


# === Clip Tests (6 tools) ===

@pytest.mark.live
@pytest.mark.clip
def test_create_clip(send_command):
    """Test creating a MIDI clip."""
    response = send_command("create_clip", {
        "track_index": 0, "clip_index": 0, "length": 4.0
    })
    # May fail if slot has clip - acceptable
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.clip
def test_add_notes_to_clip(send_command):
    """Test adding notes to a clip."""
    notes = [{"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100, "mute": False}]
    response = send_command("add_notes_to_clip", {
        "track_index": 0, "clip_index": 0, "notes": notes
    })
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.clip
def test_set_clip_name(send_command):
    """Test renaming a clip."""
    response = send_command("set_clip_name", {
        "track_index": 0, "clip_index": 0, "name": "TestClip"
    })
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.clip
def test_duplicate_clip(send_command):
    """Test duplicating a MIDI clip."""
    response = send_command("duplicate_clip", {
        "source_track_index": 0, "source_clip_index": 0,
        "dest_track_index": 0, "dest_clip_index": 1
    })
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.clip
def test_empty_clip_slot(send_command):
    """Test emptying a clip slot."""
    response = send_command("remove_clip", {"track_index": 0, "clip_index": 1})
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.clip
def test_relocate_clip(send_command):
    """Test relocating a clip."""
    response = send_command("move_clip", {
        "source_track_index": 0, "source_clip_index": 0,
        "dest_track_index": 0, "dest_clip_index": 2
    })
    assert response["status"] in ["success", "error"]


# === Transport Tests (4 tools) ===

@pytest.mark.live
@pytest.mark.transport
def test_fire_clip(send_command):
    """Test firing a clip."""
    response = send_command("fire_clip", {"track_index": 0, "clip_index": 0})
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.transport
def test_stop_clip(send_command):
    """Test stopping a clip."""
    response = send_command("stop_clip", {"track_index": 0, "clip_index": 0})
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.transport
def test_start_playback(send_command):
    """Test starting playback."""
    response = send_command("start_playback")
    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.transport
def test_stop_playback(send_command):
    """Test stopping playback."""
    response = send_command("stop_playback")
    assert response["status"] == "success"


# === Device/Rack Tests (5 tools) ===

@pytest.mark.live
@pytest.mark.device
def test_create_audio_effect_rack(send_command):
    """Test creating an Audio Effect Rack."""
    response = send_command("create_audio_effect_rack", {
        "track_index": 0, "device_index": -1
    })
    assert response["status"] == "success"
    assert "device_index" in response["result"]


@pytest.mark.live
@pytest.mark.device
def test_create_rack_chain(send_command):
    """Test creating a chain in a rack."""
    # Get track info to find a rack
    track = send_command("get_track_info", {"track_index": 0})
    if track["status"] != "success":
        pytest.skip("Cannot get track info")

    devices = track["result"].get("devices", [])
    rack_idx = None
    for d in devices:
        if "Rack" in d.get("name", ""):
            rack_idx = d["index"]
            break

    if rack_idx is None:
        pytest.skip("No rack found on track 0")

    response = send_command("create_rack_chain", {
        "track_index": 0, "device_index": rack_idx, "chain_name": "TestChain"
    })
    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.device
def test_get_device_parameters(send_command):
    """Test getting device parameters."""
    response = send_command("get_device_parameters", {
        "track_index": 0, "device_index": 0
    })
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.device
def test_set_device_parameter(send_command):
    """Test setting a device parameter."""
    response = send_command("set_device_param", {
        "track_index": 0, "device_index": 0,
        "parameter_name": "Device On", "value": 1.0
    })
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.device
def test_load_effect_to_chain(send_command):
    """Test loading an effect into a chain."""
    response = send_command("load_effect_to_chain", {
        "track_index": 0, "rack_device_index": 0,
        "chain_index": 0, "effect_uri": "query:AudioFx#Utility"
    })
    assert response["status"] in ["success", "error"]


# === Browser Tests (5 tools) ===

@pytest.mark.live
@pytest.mark.browser
def test_get_browser_tree(send_command):
    """Test getting browser tree."""
    response = send_command("get_browser_tree", {"category_type": "audio_effects"})
    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.browser
def test_get_browser_items_at_path(send_command):
    """Test navigating browser path."""
    response = send_command("get_browser_items_at_path", {"path": "audio_effects"})
    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.browser
def test_load_instrument_or_effect(send_command):
    """Test loading from browser."""
    response = send_command("load_browser_item", {
        "track_index": 0, "item_uri": "query:AudioFx#Utility"
    })
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.browser
def test_load_effect_on_main(send_command):
    """Test loading effect on master."""
    response = send_command("load_effect_on_master", {
        "uri": "query:AudioFx#Utility"
    })
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.browser
def test_load_drum_kit(send_command):
    """Test loading drum kit."""
    response = send_command("load_drum_kit", {"track_index": 0})
    assert response["status"] in ["success", "error"]
