"""
Tests for audio analysis functionality.

These tests verify the analyze_track.py script can correctly:
- Load and analyze reference audio files
- Extract BPM, key, and mode
- Detect musical sections
- Output valid JSON format
"""

import json
import subprocess
from pathlib import Path

import pytest

# Path to the analysis script
ANALYSIS_SCRIPT = Path(__file__).parent.parent / "analysis" / "analyze_track.py"
ASSETS_DIR = Path(__file__).parent.parent / "assets" / "audio" / "reference"

# Reference tracks for testing
ALCHEMY_TRACK = ASSETS_DIR / "ALCHEMY_I_O.mp3"
TOXIC_TRACK = ASSETS_DIR / "YOURE_TOXIC.mp3"


@pytest.fixture
def reference_tracks():
    """Fixture providing paths to reference tracks."""
    return {"alchemy": ALCHEMY_TRACK, "toxic": TOXIC_TRACK}


def test_analysis_script_exists():
    """Verify the analysis script exists."""
    assert ANALYSIS_SCRIPT.exists(), f"Analysis script not found at {ANALYSIS_SCRIPT}"


def test_reference_tracks_exist(reference_tracks):
    """Verify reference tracks exist."""
    for name, path in reference_tracks.items():
        assert path.exists(), f"Reference track '{name}' not found at {path}"


def test_analyze_alchemy_track_json():
    """Test analyzing ALCHEMY_I_O.mp3 with JSON output."""
    if not ALCHEMY_TRACK.exists():
        pytest.skip(f"Reference track not found: {ALCHEMY_TRACK}")

    result = subprocess.run(
        [".venv/bin/python", str(ANALYSIS_SCRIPT), str(ALCHEMY_TRACK), "--json"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, f"Analysis failed: {result.stderr}"

    # Parse JSON output
    data = json.loads(result.stdout)

    # Verify required fields
    assert "file" in data
    assert "bpm" in data
    assert "key" in data
    assert "mode" in data
    assert "duration_total" in data
    assert "duration_analyzed" in data
    assert "sections" in data

    # Verify data types and ranges
    assert isinstance(data["bpm"], int | float)
    assert 60 <= data["bpm"] <= 200, f"BPM {data['bpm']} outside expected range"
    assert data["key"] in [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    ]
    assert data["mode"] in ["Major", "Minor"]
    assert isinstance(data["sections"], list)


def test_analyze_toxic_track_json():
    """Test analyzing YOURE_TOXIC.mp3 with JSON output."""
    if not TOXIC_TRACK.exists():
        pytest.skip(f"Reference track not found: {TOXIC_TRACK}")

    result = subprocess.run(
        [".venv/bin/python", str(ANALYSIS_SCRIPT), str(TOXIC_TRACK), "--json"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, f"Analysis failed: {result.stderr}"

    # Parse JSON output
    data = json.loads(result.stdout)

    # Verify required fields
    assert "file" in data
    assert "bpm" in data
    assert "key" in data
    assert "mode" in data


def test_analyze_human_readable_output():
    """Test human-readable output format."""
    if not ALCHEMY_TRACK.exists():
        pytest.skip(f"Reference track not found: {ALCHEMY_TRACK}")

    result = subprocess.run(
        [".venv/bin/python", str(ANALYSIS_SCRIPT), str(ALCHEMY_TRACK)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, f"Analysis failed: {result.stderr}"

    # Verify human-readable output contains expected sections
    output = result.stdout
    assert "Analyzing:" in output
    assert "BPM:" in output
    assert "Key:" in output
    assert "To recreate in Ableton:" in output


def test_analyze_nonexistent_file():
    """Test error handling for missing files."""
    nonexistent = "/tmp/nonexistent_audio_file.mp3"

    result = subprocess.run(
        [".venv/bin/python", str(ANALYSIS_SCRIPT), nonexistent, "--json"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Should not crash, but return error in JSON
    data = json.loads(result.stdout)
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_full_track_analysis():
    """Test analyzing full track instead of first 10s."""
    if not ALCHEMY_TRACK.exists():
        pytest.skip(f"Reference track not found: {ALCHEMY_TRACK}")

    result = subprocess.run(
        [
            ".venv/bin/python",
            str(ANALYSIS_SCRIPT),
            str(ALCHEMY_TRACK),
            "--full",
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=120,  # Longer timeout for full track
    )

    assert result.returncode == 0, f"Analysis failed: {result.stderr}"

    data = json.loads(result.stdout)

    # For full track analysis, duration_analyzed should equal duration_total
    assert abs(data["duration_analyzed"] - data["duration_total"]) < 0.5, (
        "Full track analysis should analyze entire duration"
    )


def test_section_detection_format():
    """Test that section detection returns properly formatted data."""
    if not ALCHEMY_TRACK.exists():
        pytest.skip(f"Reference track not found: {ALCHEMY_TRACK}")

    result = subprocess.run(
        [".venv/bin/python", str(ANALYSIS_SCRIPT), str(ALCHEMY_TRACK), "--json"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)

    # Verify sections structure
    for section in data["sections"]:
        assert "type" in section
        assert "time" in section
        assert section["type"] in ["drop", "breakdown", "intro"]
        assert isinstance(section["time"], int | float)
        assert section["time"] >= 0
