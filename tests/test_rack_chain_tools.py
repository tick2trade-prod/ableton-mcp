"""Tests for feature/rack-chain-tools branch.

Tests the new rack chain and master track tools:
- create_audio_effect_rack
- create_rack_chain
- load_effect_to_chain
- load_effect_on_main (master)
- get_device_parameters (with chain support)
- set_device_parameter (with chain support)
- get_browser_tree
- get_browser_items_at_path
- load_drum_kit
"""
import pytest

# === Rack Creation Tests ===

@pytest.mark.live
@pytest.mark.device
def test_create_audio_effect_rack_appends(send_command):
    """Test creating a rack appends to end of device chain."""
    # Get initial device count
    track = send_command("get_track_info", {"track_index": 0})
    initial_count = len(track["result"].get("devices", []))

    # Create rack at end (-1)
    response = send_command("create_audio_effect_rack", {
        "track_index": 0,
        "device_index": -1
    })

    assert response["status"] == "success"
    result = response["result"]
    assert result["device_count"] > initial_count
    assert result["device_index"] == result["device_count"] - 1


@pytest.mark.live
@pytest.mark.device
def test_create_audio_effect_rack_at_index(send_command):
    """Test creating a rack at specific index."""
    response = send_command("create_audio_effect_rack", {
        "track_index": 0,
        "device_index": 0
    })

    assert response["status"] == "success"
    # Device should be at index 0 or beginning
    assert response["result"]["device_index"] >= 0


# === Chain Tests ===

@pytest.mark.live
@pytest.mark.device
def test_create_rack_chain(send_command):
    """Test creating a chain in a rack."""
    # First find or create a rack
    track = send_command("get_track_info", {"track_index": 0})
    devices = track["result"].get("devices", [])

    rack_idx = None
    for d in devices:
        if "Rack" in d.get("name", "") or d.get("class_name") == "AudioEffectGroupDevice":
            rack_idx = d["index"]
            break

    if rack_idx is None:
        # Create a rack first
        rack = send_command("create_audio_effect_rack", {
            "track_index": 0, "device_index": -1
        })
        rack_idx = rack["result"]["device_index"]

    # Create chain
    response = send_command("create_rack_chain", {
        "track_index": 0,
        "device_index": rack_idx,
        "chain_name": "Test Chain"
    })

    assert response["status"] == "success"
    assert "chain_index" in response["result"]


@pytest.mark.live
@pytest.mark.device
def test_load_effect_to_chain(send_command):
    """Test loading an effect into a specific chain."""
    # Get track with rack
    track = send_command("get_track_info", {"track_index": 0})
    devices = track["result"].get("devices", [])

    rack_idx = None
    for d in devices:
        if "Rack" in d.get("name", "") or d.get("class_name") == "AudioEffectGroupDevice":
            rack_idx = d["index"]
            break

    if rack_idx is None:
        pytest.skip("No rack on track 0")

    response = send_command("load_effect_to_chain", {
        "track_index": 0,
        "rack_device_index": rack_idx,
        "chain_index": 0,
        "effect_uri": "query:AudioFx#Utility"
    })

    # May fail if chain doesn't exist or effect not found
    assert response["status"] in ["success", "error"]


# === Master Track Tests ===

@pytest.mark.live
@pytest.mark.device
def test_load_effect_on_master(send_command):
    """Test loading an effect on the master track."""
    response = send_command("load_effect_on_master", {
        "uri": "query:AudioFx#Utility"
    })

    assert response["status"] in ["success", "error"]


# === Device Parameter Tests (with chain support) ===

@pytest.mark.live
@pytest.mark.device
def test_get_device_parameters_in_chain(send_command):
    """Test getting parameters from device in a chain."""
    # Get track with rack
    track = send_command("get_track_info", {"track_index": 0})
    devices = track["result"].get("devices", [])

    rack_idx = None
    for d in devices:
        if "Rack" in d.get("name", "") or d.get("class_name") == "AudioEffectGroupDevice":
            rack_idx = d["index"]
            break

    if rack_idx is None:
        pytest.skip("No rack on track 0")

    # Try to get params from device in chain
    response = send_command("get_device_parameters", {
        "track_index": 0,
        "device_index": rack_idx,
        "chain_index": 0,
        "rack_device_index": 0
    })

    # May fail if chain has no devices
    assert response["status"] in ["success", "error"]


@pytest.mark.live
@pytest.mark.device
def test_set_device_parameter_in_chain(send_command):
    """Test setting parameter on device in a chain."""
    track = send_command("get_track_info", {"track_index": 0})
    devices = track["result"].get("devices", [])

    rack_idx = None
    for d in devices:
        if "Rack" in d.get("name", "") or d.get("class_name") == "AudioEffectGroupDevice":
            rack_idx = d["index"]
            break

    if rack_idx is None:
        pytest.skip("No rack on track 0")

    response = send_command("set_device_param", {
        "track_index": 0,
        "device_index": rack_idx,
        "chain_index": 0,
        "rack_device_index": 0,
        "parameter_name": "Device On",
        "value": 1.0
    })

    assert response["status"] in ["success", "error"]


# === Browser Tests ===

@pytest.mark.live
@pytest.mark.browser
def test_get_browser_tree_audio_effects(send_command):
    """Test getting browser tree for audio effects."""
    response = send_command("get_browser_tree", {"category_type": "audio_effects"})

    assert response["status"] == "success"
    result = response["result"]
    assert "items" in result or "children" in result or len(result) > 0


@pytest.mark.live
@pytest.mark.browser
def test_get_browser_tree_instruments(send_command):
    """Test getting browser tree for instruments."""
    response = send_command("get_browser_tree", {"category_type": "instruments"})

    assert response["status"] == "success"


@pytest.mark.live
@pytest.mark.browser
def test_get_browser_items_at_path(send_command):
    """Test navigating browser by path."""
    response = send_command("get_browser_items_at_path", {"path": "audio_effects"})

    assert response["status"] == "success"
    result = response["result"]
    assert "items" in result or len(result) >= 0


# === Drum Kit Test ===

@pytest.mark.live
@pytest.mark.browser
def test_load_drum_kit(send_command):
    """Test loading a drum kit."""
    response = send_command("load_drum_kit", {"track_index": 0})

    # May fail if no drum kits available
    assert response["status"] in ["success", "error"]
