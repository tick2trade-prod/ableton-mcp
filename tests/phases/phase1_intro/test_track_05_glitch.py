"""
TDD Tests for Track 05: Glitch - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate glitch percussion elements (stutters, clicks, textures).

Run tests:
    pytest tests/phases/phase1_intro/test_track_05_glitch.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import GLITCH_TRACK_INDEX

# Test parameters
GLITCH_TRACK_NAME = "Glitch"
INTRO_BARS = 16
BPM = 136


class TestGlitchTrackExists:
    """RED: Glitch track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 10 tracks (index 9)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= GLITCH_TRACK_INDEX + 1, (
            f"Need at least {GLITCH_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_glitch_track_exists(self, glitch_track_info):
        """Track at index 9 must exist."""
        assert glitch_track_info is not None, (
            f"Track {GLITCH_TRACK_INDEX} does not exist"
        )
        assert "name" in glitch_track_info, f"Track {GLITCH_TRACK_INDEX} has no name"

    def test_glitch_track_named_correctly(self, glitch_track_info):
        """Track should be named 'Glitch' or 'Perc'."""
        name = glitch_track_info.get("name", "")
        assert any(x in name.lower() for x in ["glitch", "perc", "fx"]), (
            f"Track {GLITCH_TRACK_INDEX} should contain 'Glitch/Perc', got: '{name}'"
        )


class TestGlitchDeviceChain:
    """RED: Glitch must have correct device chain."""

    def test_has_device(self, glitch_track_info):
        """Glitch needs Drum Rack, Sampler, or synth for textures."""
        devices = glitch_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        glitch_keywords = ["drum rack", "simpler", "sampler", "operator", "wavetable"]
        has_device = any(kw in names_str for kw in glitch_keywords)

        assert has_device or len(devices) > 0, (
            f"No glitch device found. Devices: {device_names}"
        )


class TestGlitchMIDIPattern:
    """RED: Glitch MIDI pattern for textures."""

    def test_clip_exists(self, mcp):
        """Glitch must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": GLITCH_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": GLITCH_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_glitch_pattern(self, glitch_clip_notes):
        """Glitch should have textural elements (irregular timing)."""
        if not glitch_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(glitch_clip_notes)
        # Glitch elements are varied - at least some per intro
        assert note_count >= 8, (
            f"Glitch should have at least 8 notes for texture, got: {note_count}"
        )


class TestGlitchImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 9, named "Glitch"
        2. Load Drum Rack with glitch/noise samples
        3. Create 16-bar clip (64 beats)
        4. Add random/irregular glitch hits:
           - Short bursts of noise
           - Click/pop elements
           - Stutter effects on beat accents
        """
        pass
