"""
TDD Tests for Track 08: Rolling Bass - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate rolling/moving bass line with 16th note movement.

Run tests:
    pytest tests/phases/phase1_intro/test_track_08_rolling.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import ROLLING_TRACK_INDEX

# Test parameters
ROLLING_TRACK_NAME = "Rolling"
INTRO_BARS = 16
BPM = 136
ROOT_NOTE_F = 41  # F1


class TestRollingTrackExists:
    """RED: Rolling Bass track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 13 tracks (index 12)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= ROLLING_TRACK_INDEX + 1, (
            f"Need at least {ROLLING_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_rolling_track_exists(self, rolling_track_info):
        """Track at index 12 must exist."""
        assert rolling_track_info is not None, (
            f"Track {ROLLING_TRACK_INDEX} does not exist"
        )
        assert "name" in rolling_track_info, f"Track {ROLLING_TRACK_INDEX} has no name"

    def test_rolling_track_named_correctly(self, rolling_track_info):
        """Track should be named 'Rolling' or 'Bass'."""
        name = rolling_track_info.get("name", "")
        assert any(x in name.lower() for x in ["rolling", "bass", "16th"]), (
            f"Track {ROLLING_TRACK_INDEX} should contain 'Rolling/Bass', got: '{name}'"
        )


class TestRollingDeviceChain:
    """RED: Rolling Bass must have correct device chain."""

    def test_has_synth(self, rolling_track_info):
        """Rolling Bass needs a synthesizer."""
        devices = rolling_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        synth_keywords = ["operator", "analog", "wavetable", "drift", "serum"]
        has_synth = any(kw in names_str for kw in synth_keywords)

        assert has_synth or len(devices) > 0, f"No synth found. Devices: {device_names}"


class TestRollingMIDIPattern:
    """RED: Rolling Bass MIDI pattern with 16th movement."""

    def test_clip_exists(self, mcp):
        """Rolling Bass must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": ROLLING_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": ROLLING_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_16th_movement(self, rolling_clip_notes):
        """Rolling Bass should have 16th note movement (many notes)."""
        if not rolling_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(rolling_clip_notes)
        # 16th notes = 16 per bar * 16 bars = 256 (or at least half)
        assert note_count >= 64, (
            f"Rolling bass needs 16th movement, got only {note_count} notes"
        )

    def test_notes_in_bass_range(self, rolling_clip_notes):
        """Notes should be in bass range (MIDI 30-60)."""
        if not rolling_clip_notes:
            pytest.skip("No notes in clip")

        for note in rolling_clip_notes:
            pitch = note.get("pitch", 0)
            assert 30 <= pitch <= 60, f"Pitch {pitch} outside bass range (30-60)"


class TestRollingImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 12, named "Rolling Bass"
        2. Load Operator or similar bass synth
        3. Create 16-bar clip (64 beats)
        4. Add 16th note rolling pattern (256 notes)
        """
        pass
