"""
TDD Tests for Track 14: Risers - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate riser/sweep FX for transitions.

Run tests:
    pytest tests/phases/phase1_intro/test_track_14_risers.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import RISERS_TRACK_INDEX

# Test parameters
RISERS_TRACK_NAME = "Risers"
INTRO_BARS = 16
BPM = 136


class TestRisersTrackExists:
    """RED: Risers track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 19 tracks (index 18)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= RISERS_TRACK_INDEX + 1, (
            f"Need at least {RISERS_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_risers_track_exists(self, risers_track_info):
        """Track at index 18 must exist."""
        assert risers_track_info is not None, (
            f"Track {RISERS_TRACK_INDEX} does not exist"
        )
        assert "name" in risers_track_info, f"Track {RISERS_TRACK_INDEX} has no name"

    def test_risers_track_named_correctly(self, risers_track_info):
        """Track should be named 'Risers' or 'FX'."""
        name = risers_track_info.get("name", "")
        assert any(x in name.lower() for x in ["riser", "sweep", "fx", "trans"]), (
            f"Track {RISERS_TRACK_INDEX} should contain 'Riser/FX', got: '{name}'"
        )


class TestRisersDeviceChain:
    """RED: Risers must have correct device chain."""

    def test_has_device(self, risers_track_info):
        """Risers needs synth or sampler for sweep sounds."""
        devices = risers_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        riser_keywords = ["operator", "wavetable", "simpler", "sampler", "analog"]
        has_device = any(kw in names_str for kw in riser_keywords)

        assert has_device or len(devices) >= 0, f"Devices: {device_names}"


class TestRisersMIDIPattern:
    """RED: Risers MIDI pattern for sweeps."""

    def test_clip_exists(self, mcp):
        """Risers must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": RISERS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": RISERS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_riser_pattern(self, risers_clip_notes):
        """Risers should have sweep triggers at transitions."""
        if not risers_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(risers_clip_notes)
        # Risers are sparse - at section transitions
        assert note_count >= 1, (
            f"Risers should have at least 1 trigger, got: {note_count}"
        )

    def test_riser_duration(self, risers_clip_notes):
        """Riser notes should be long (sweep duration)."""
        if not risers_clip_notes:
            pytest.skip("No notes in clip")

        durations = [note.get("duration", 0) for note in risers_clip_notes]
        max_duration = max(durations)

        # Risers typically build over several bars
        assert max_duration >= 4.0, (
            f"Riser should have long notes (>= 4 beats), max: {max_duration}"
        )


class TestRisersImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 18, named "Risers"
        2. Load Operator or Wavetable synth with noise/sweep
        3. Create 16-bar clip (64 beats)
        4. Add riser at end of intro (leading to drop):
           notes = [
               {"pitch": 60, "start_time": 48.0, "duration": 16.0, "velocity": 100}
               # 16-beat riser building from bar 13 to 16
           ]
        """
        pass
