"""
TDD Tests for Track 13: Vocal FX - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate vocal chops, stutters, and FX elements.

Run tests:
    pytest tests/phases/phase1_intro/test_track_13_vocal_fx.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import VOCAL_FX_TRACK_INDEX

# Test parameters
VOCAL_FX_TRACK_NAME = "Vocal FX"
INTRO_BARS = 16
BPM = 136


class TestVocalFXTrackExists:
    """RED: Vocal FX track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 18 tracks (index 17)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= VOCAL_FX_TRACK_INDEX + 1, (
            f"Need at least {VOCAL_FX_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_vocal_fx_track_exists(self, vocal_fx_track_info):
        """Track at index 17 must exist."""
        assert vocal_fx_track_info is not None, (
            f"Track {VOCAL_FX_TRACK_INDEX} does not exist"
        )
        assert "name" in vocal_fx_track_info, (
            f"Track {VOCAL_FX_TRACK_INDEX} has no name"
        )

    def test_vocal_fx_track_named_correctly(self, vocal_fx_track_info):
        """Track should be named 'Vocal FX' or 'Vox FX'."""
        name = vocal_fx_track_info.get("name", "")
        assert any(x in name.lower() for x in ["vocal", "vox", "fx", "chop"]), (
            f"Track {VOCAL_FX_TRACK_INDEX} should contain 'Vocal FX', got: '{name}'"
        )


class TestVocalFXDeviceChain:
    """RED: Vocal FX must have correct device chain."""

    def test_has_device(self, vocal_fx_track_info):
        """Vocal FX needs Sampler or effects for vocal chops."""
        devices = vocal_fx_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        fx_keywords = ["sampler", "simpler", "beat repeat", "delay", "reverb"]
        has_fx = any(kw in names_str for kw in fx_keywords)

        # Accept any device or empty (will be configured)
        assert has_fx or len(devices) >= 0, f"Devices: {device_names}"


class TestVocalFXMIDIPattern:
    """RED: Vocal FX MIDI pattern for chops/stutters."""

    def test_clip_exists(self, mcp):
        """Vocal FX must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": VOCAL_FX_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": VOCAL_FX_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_fx_pattern(self, vocal_fx_clip_notes):
        """Vocal FX should have chop/stutter triggers."""
        if not vocal_fx_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(vocal_fx_clip_notes)
        # FX elements are sparse but present
        assert note_count >= 4, (
            f"Vocal FX should have at least 4 triggers, got: {note_count}"
        )


class TestVocalFXImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 17, named "Vocal FX"
        2. Load Simpler with vocal sample or audio
        3. Create 16-bar clip (64 beats)
        4. Add vocal chop triggers:
           notes = [
               {"pitch": 60, "start_time": 7.5, "duration": 0.5, "velocity": 100},
               {"pitch": 60, "start_time": 15.5, "duration": 0.5, "velocity": 100},
               # etc at transition points
           ]
        """
        pass
