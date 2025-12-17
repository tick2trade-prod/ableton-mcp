"""
Fixtures for Phase 1 Intro TDD Tests.

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Target: Recreate first 16 bars (Intro section) with high similarity.

Track Layout (assumed):
- Track 1 (idx 0): Reference MP3 (full 6:17)
- Track 2 (idx 1): Drums stem
- Track 3 (idx 2): Bass stem
- Track 4 (idx 3): Vocals stem
- Track 5 (idx 4): Others stem
- Track 6 (idx 5): Kick (our recreation starts here)
- Track 7 (idx 6): Snare
- Track 8 (idx 7): Hi-hats
- Track 9 (idx 8): Toms
- Track 10 (idx 9): Glitch
- Track 11 (idx 10): Ride
- Track 12 (idx 11): Rumble
- Track 13 (idx 12): Rolling Bass
- Track 14 (idx 13): Acid
- Track 15 (idx 14): Stabs
- Track 16 (idx 15): Drone
- Track 17 (idx 16): Main Vocal
- Track 18 (idx 17): Vocal FX
- Track 19 (idx 18): Risers
"""

import json
import socket
from pathlib import Path

import pytest

# Reference track path
REFERENCE_PATH = Path(
    "/Users/alexzh/ableton-mcp/assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3"
)

# Song parameters
BPM = 136
INTRO_BARS = 16
INTRO_BEATS = INTRO_BARS * 4  # 64 beats
INTRO_DURATION_SEC = (60 / BPM) * INTRO_BEATS  # ~28.2 seconds

# Track indices (0-based) - accounting for reference + 4 stems
TRACK_OFFSET = 5  # First 5 tracks are reference + stems

# Drums (Lane 1)
KICK_TRACK_INDEX = TRACK_OFFSET + 0  # Track 6 = index 5
SNARE_TRACK_INDEX = TRACK_OFFSET + 1  # Track 7 = index 6
HIHATS_TRACK_INDEX = TRACK_OFFSET + 2  # Track 8 = index 7
TOMS_TRACK_INDEX = TRACK_OFFSET + 3  # Track 9 = index 8
GLITCH_TRACK_INDEX = TRACK_OFFSET + 4  # Track 10 = index 9
RIDE_TRACK_INDEX = TRACK_OFFSET + 5  # Track 11 = index 10

# Bass (Lane 2)
RUMBLE_TRACK_INDEX = TRACK_OFFSET + 6  # Track 12 = index 11
ROLLING_TRACK_INDEX = TRACK_OFFSET + 7  # Track 13 = index 12
ACID_TRACK_INDEX = TRACK_OFFSET + 8  # Track 14 = index 13

# Synths (Lane 3)
STABS_TRACK_INDEX = TRACK_OFFSET + 9  # Track 15 = index 14
DRONE_TRACK_INDEX = TRACK_OFFSET + 10  # Track 16 = index 15

# Vocals/FX (Lane 4)
MAIN_VOCAL_TRACK_INDEX = TRACK_OFFSET + 11  # Track 17 = index 16
VOCAL_FX_TRACK_INDEX = TRACK_OFFSET + 12  # Track 18 = index 17
RISERS_TRACK_INDEX = TRACK_OFFSET + 13  # Track 19 = index 18


@pytest.fixture(scope="module")
def ableton_connection():
    """Real connection to Ableton via MCP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(15)
    try:
        sock.connect(("localhost", 9877))
        yield sock
    except ConnectionRefusedError:
        pytest.skip("Ableton not running or AbletonMCP not enabled on port 9877")
    finally:
        sock.close()


@pytest.fixture(scope="module")
def mcp(ableton_connection):
    """MCP command sender."""

    def send_command(command_type: str, params: dict = None):
        command = {"type": command_type, "params": params or {}}
        ableton_connection.sendall(json.dumps(command).encode("utf-8"))

        chunks = []
        ableton_connection.settimeout(10)
        while True:
            try:
                chunk = ableton_connection.recv(8192)
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
            return json.loads(data.decode("utf-8")).get("result", {})
        return {}

    return send_command


@pytest.fixture(scope="module")
def session_info(mcp):
    """Get current Ableton session info."""
    return mcp("get_session_info")


@pytest.fixture(scope="module")
def reference_exists():
    """Check if reference file exists."""
    return REFERENCE_PATH.exists()


# =============================================================================
# REFERENCE ANALYSIS FIXTURES (requires librosa)
# =============================================================================


@pytest.fixture(scope="module")
def reference_audio():
    """Load reference audio for analysis (first 30 seconds for intro)."""
    try:
        import librosa
    except ImportError:
        pytest.skip("librosa not installed - run: uv pip install librosa")

    if not REFERENCE_PATH.exists():
        pytest.skip(f"Reference file not found: {REFERENCE_PATH}")

    # Load first 30 seconds (intro + buffer)
    y, sr = librosa.load(str(REFERENCE_PATH), sr=44100, duration=30.0)
    return {"y": y, "sr": sr, "duration": len(y) / sr}


@pytest.fixture(scope="module")
def reference_kick_onsets(reference_audio):
    """Extract kick onset times from reference (low frequency transients)."""
    try:
        import librosa
        import numpy as np
    except ImportError:
        pytest.skip("librosa/numpy not installed")

    y, sr = reference_audio["y"], reference_audio["sr"]

    # Focus on low frequencies (kick range: 30-150Hz)
    y_low = librosa.effects.preemphasis(y, coef=-0.97)  # Boost lows

    # Onset detection focused on percussive content
    onset_env = librosa.onset.onset_strength(y=y_low, sr=sr, hop_length=512)
    onsets = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, hop_length=512, backtrack=False, units="time"
    )

    # Filter to likely kick hits (every ~0.44s at 136 BPM)
    beat_duration = 60 / BPM
    kick_onsets = []
    for onset in onsets:
        # Check if onset aligns with quarter note grid (within 50ms tolerance)
        beat_position = onset / beat_duration
        if abs(beat_position - round(beat_position)) < 0.1:  # ~44ms tolerance
            kick_onsets.append(onset)

    return np.array(kick_onsets)


@pytest.fixture(scope="module")
def reference_spectral_centroid(reference_audio):
    """Get spectral centroid of reference (brightness measure)."""
    try:
        import librosa
        import numpy as np
    except ImportError:
        pytest.skip("librosa/numpy not installed")

    y, sr = reference_audio["y"], reference_audio["sr"]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    return np.mean(centroid)


# =============================================================================
# KICK TRACK FIXTURES
# =============================================================================


@pytest.fixture
def kick_track_info(mcp):
    """Get Kick track info (Track 6 = index 5)."""
    return mcp("get_track_info", {"track_index": KICK_TRACK_INDEX})


@pytest.fixture
def kick_clip_notes(mcp):
    """Get MIDI notes from Kick clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": KICK_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# SNARE TRACK FIXTURES
# =============================================================================


@pytest.fixture
def snare_track_info(mcp):
    """Get Snare track info (Track 7 = index 6)."""
    return mcp("get_track_info", {"track_index": SNARE_TRACK_INDEX})


@pytest.fixture
def snare_clip_notes(mcp):
    """Get MIDI notes from Snare clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": SNARE_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# HI-HATS TRACK FIXTURES
# =============================================================================


@pytest.fixture
def hihats_track_info(mcp):
    """Get Hi-hats track info (Track 8 = index 7)."""
    return mcp("get_track_info", {"track_index": HIHATS_TRACK_INDEX})


@pytest.fixture
def hihats_clip_notes(mcp):
    """Get MIDI notes from Hi-hats clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": HIHATS_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# TOMS TRACK FIXTURES
# =============================================================================


@pytest.fixture
def toms_track_info(mcp):
    """Get Toms track info (Track 9 = index 8)."""
    return mcp("get_track_info", {"track_index": TOMS_TRACK_INDEX})


@pytest.fixture
def toms_clip_notes(mcp):
    """Get MIDI notes from Toms clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": TOMS_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# GLITCH TRACK FIXTURES
# =============================================================================


@pytest.fixture
def glitch_track_info(mcp):
    """Get Glitch track info (Track 10 = index 9)."""
    return mcp("get_track_info", {"track_index": GLITCH_TRACK_INDEX})


@pytest.fixture
def glitch_clip_notes(mcp):
    """Get MIDI notes from Glitch clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": GLITCH_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# RIDE TRACK FIXTURES
# =============================================================================


@pytest.fixture
def ride_track_info(mcp):
    """Get Ride track info (Track 11 = index 10)."""
    return mcp("get_track_info", {"track_index": RIDE_TRACK_INDEX})


@pytest.fixture
def ride_clip_notes(mcp):
    """Get MIDI notes from Ride clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": RIDE_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# RUMBLE TRACK FIXTURES
# =============================================================================


@pytest.fixture
def rumble_track_info(mcp):
    """Get Rumble track info (Track 12 = index 11)."""
    return mcp("get_track_info", {"track_index": RUMBLE_TRACK_INDEX})


@pytest.fixture
def rumble_clip_notes(mcp):
    """Get MIDI notes from Rumble clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": RUMBLE_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# ROLLING BASS TRACK FIXTURES
# =============================================================================


@pytest.fixture
def rolling_track_info(mcp):
    """Get Rolling Bass track info (Track 13 = index 12)."""
    return mcp("get_track_info", {"track_index": ROLLING_TRACK_INDEX})


@pytest.fixture
def rolling_clip_notes(mcp):
    """Get MIDI notes from Rolling Bass clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": ROLLING_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# ACID TRACK FIXTURES
# =============================================================================


@pytest.fixture
def acid_track_info(mcp):
    """Get Acid track info (Track 14 = index 13)."""
    return mcp("get_track_info", {"track_index": ACID_TRACK_INDEX})


@pytest.fixture
def acid_clip_notes(mcp):
    """Get MIDI notes from Acid clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": ACID_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# STABS TRACK FIXTURES
# =============================================================================


@pytest.fixture
def stabs_track_info(mcp):
    """Get Stabs track info (Track 15 = index 14)."""
    return mcp("get_track_info", {"track_index": STABS_TRACK_INDEX})


@pytest.fixture
def stabs_clip_notes(mcp):
    """Get MIDI notes from Stabs clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": STABS_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# DRONE TRACK FIXTURES
# =============================================================================


@pytest.fixture
def drone_track_info(mcp):
    """Get Drone track info (Track 16 = index 15)."""
    return mcp("get_track_info", {"track_index": DRONE_TRACK_INDEX})


@pytest.fixture
def drone_clip_notes(mcp):
    """Get MIDI notes from Drone clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": DRONE_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# MAIN VOCAL TRACK FIXTURES
# =============================================================================


@pytest.fixture
def main_vocal_track_info(mcp):
    """Get Main Vocal track info (Track 17 = index 16)."""
    return mcp("get_track_info", {"track_index": MAIN_VOCAL_TRACK_INDEX})


@pytest.fixture
def main_vocal_clip_notes(mcp):
    """Get MIDI notes from Main Vocal clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": MAIN_VOCAL_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# VOCAL FX TRACK FIXTURES
# =============================================================================


@pytest.fixture
def vocal_fx_track_info(mcp):
    """Get Vocal FX track info (Track 18 = index 17)."""
    return mcp("get_track_info", {"track_index": VOCAL_FX_TRACK_INDEX})


@pytest.fixture
def vocal_fx_clip_notes(mcp):
    """Get MIDI notes from Vocal FX clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": VOCAL_FX_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []


# =============================================================================
# RISERS TRACK FIXTURES
# =============================================================================


@pytest.fixture
def risers_track_info(mcp):
    """Get Risers track info (Track 19 = index 18)."""
    return mcp("get_track_info", {"track_index": RISERS_TRACK_INDEX})


@pytest.fixture
def risers_clip_notes(mcp):
    """Get MIDI notes from Risers clip."""
    try:
        result = mcp(
            "get_clip_notes", {"track_index": RISERS_TRACK_INDEX, "clip_index": 0}
        )
        return result.get("notes", [])
    except Exception:
        return []
