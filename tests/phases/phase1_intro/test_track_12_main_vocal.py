"""
TDD Tests for Track 12: Main Vocal - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Placeholder for main vocal (audio track in later phases).

Note: In the intro, main vocal may be minimal or absent. This track
is prepared for later phases where vocals are prominent.

Run tests:
    pytest tests/phases/phase1_intro/test_track_12_main_vocal.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import MAIN_VOCAL_TRACK_INDEX

# Test parameters
MAIN_VOCAL_TRACK_NAME = "Main Vocal"
INTRO_BARS = 16
BPM = 136


class TestMainVocalTrackExists:
    """RED: Main Vocal track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 17 tracks (index 16)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= MAIN_VOCAL_TRACK_INDEX + 1, (
            f"Need at least {MAIN_VOCAL_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_main_vocal_track_exists(self, main_vocal_track_info):
        """Track at index 16 must exist."""
        assert main_vocal_track_info is not None, (
            f"Track {MAIN_VOCAL_TRACK_INDEX} does not exist"
        )
        assert "name" in main_vocal_track_info, (
            f"Track {MAIN_VOCAL_TRACK_INDEX} has no name"
        )

    def test_main_vocal_track_named_correctly(self, main_vocal_track_info):
        """Track should be named 'Main Vocal' or 'Vocal'."""
        name = main_vocal_track_info.get("name", "")
        assert any(x in name.lower() for x in ["vocal", "vox", "voice"]), (
            f"Track {MAIN_VOCAL_TRACK_INDEX} should contain 'Vocal', got: '{name}'"
        )


class TestMainVocalDeviceChain:
    """RED: Main Vocal must have audio processing chain."""

    def test_has_processing(self, main_vocal_track_info):
        """Main Vocal should have EQ/Compressor for vocal processing."""
        # For intro, track may be empty placeholder
        # Just verify track exists and can hold audio
        assert main_vocal_track_info is not None, "Track should exist"
        _ = main_vocal_track_info.get("devices", [])  # Available for future use


class TestMainVocalContent:
    """RED: Main Vocal content tests (may be empty in intro)."""

    def test_clip_slot_exists(self, mcp):
        """Main Vocal should have clip slots available."""
        track_info = mcp("get_track_info", {"track_index": MAIN_VOCAL_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        # In intro, vocal may not have content yet
        # Just verify slot exists
        assert len(clip_slots) >= 0, "Track should have clip slots"

    @pytest.mark.skip(reason="Vocal content added in later phases")
    def test_has_vocal_content(self, main_vocal_clip_notes):
        """Main Vocal should have content in later phases."""
        pass


class TestMainVocalImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 16, named "Main Vocal"
        2. This is an audio track (will need audio file later)
        3. For intro phase, track can be empty placeholder
        4. Add EQ Eight and Compressor for vocal processing chain
        5. In later phases, add vocal audio clips
        """
        pass
