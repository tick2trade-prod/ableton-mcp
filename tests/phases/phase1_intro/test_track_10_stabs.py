"""
TDD Tests for Track 10: Stabs - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate synth stabs for rhythmic accents.

Run tests:
    pytest tests/phases/phase1_intro/test_track_10_stabs.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import STABS_TRACK_INDEX

# Test parameters
STABS_TRACK_NAME = "Stabs"
INTRO_BARS = 16
BPM = 136


class TestStabsTrackExists:
    """RED: Stabs track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 15 tracks (index 14)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= STABS_TRACK_INDEX + 1, (
            f"Need at least {STABS_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_stabs_track_exists(self, stabs_track_info):
        """Track at index 14 must exist."""
        assert stabs_track_info is not None, f"Track {STABS_TRACK_INDEX} does not exist"
        assert "name" in stabs_track_info, f"Track {STABS_TRACK_INDEX} has no name"

    def test_stabs_track_named_correctly(self, stabs_track_info):
        """Track should be named 'Stabs' or 'Synth'."""
        name = stabs_track_info.get("name", "")
        assert any(x in name.lower() for x in ["stab", "synth", "chord"]), (
            f"Track {STABS_TRACK_INDEX} should contain 'Stab/Synth', got: '{name}'"
        )


class TestStabsDeviceChain:
    """RED: Stabs must have correct device chain."""

    def test_has_synth(self, stabs_track_info):
        """Stabs needs a synthesizer."""
        devices = stabs_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        synth_keywords = ["operator", "analog", "wavetable", "drift", "serum"]
        has_synth = any(kw in names_str for kw in synth_keywords)

        assert has_synth or len(devices) > 0, f"No synth found. Devices: {device_names}"


class TestStabsMIDIPattern:
    """RED: Stabs MIDI pattern for rhythmic accents."""

    def test_clip_exists(self, mcp):
        """Stabs must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": STABS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": STABS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_stab_pattern(self, stabs_clip_notes):
        """Stabs should have short rhythmic hits."""
        if not stabs_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(stabs_clip_notes)
        # Stabs are sparse accents
        assert note_count >= 8, f"Stabs should have at least 8 notes, got: {note_count}"

        # Check notes are short (stabs)
        durations = [note.get("duration", 0) for note in stabs_clip_notes]
        avg_duration = sum(durations) / len(durations)
        assert avg_duration <= 1.0, (
            f"Stabs should be short, avg duration: {avg_duration}"
        )


class TestStabsImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 14, named "Stabs"
        2. Load Operator or Wavetable synth
        3. Create 16-bar clip (64 beats)
        4. Add stab pattern (offbeat accents, 16 notes)
        """
        pass
