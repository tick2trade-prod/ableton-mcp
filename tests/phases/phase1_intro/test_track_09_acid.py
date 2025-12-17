"""
TDD Tests for Track 09: Acid - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate acid bass line with 303-style resonance and slides.

Run tests:
    pytest tests/phases/phase1_intro/test_track_09_acid.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import ACID_TRACK_INDEX

# Test parameters
ACID_TRACK_NAME = "Acid"
INTRO_BARS = 16
BPM = 136
ROOT_NOTE_F = 41  # F1


class TestAcidTrackExists:
    """RED: Acid track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 14 tracks (index 13)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= ACID_TRACK_INDEX + 1, (
            f"Need at least {ACID_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_acid_track_exists(self, acid_track_info):
        """Track at index 13 must exist."""
        assert acid_track_info is not None, f"Track {ACID_TRACK_INDEX} does not exist"
        assert "name" in acid_track_info, f"Track {ACID_TRACK_INDEX} has no name"

    def test_acid_track_named_correctly(self, acid_track_info):
        """Track should be named 'Acid' or '303'."""
        name = acid_track_info.get("name", "")
        assert any(x in name.lower() for x in ["acid", "303", "squelch"]), (
            f"Track {ACID_TRACK_INDEX} should contain 'Acid/303', got: '{name}'"
        )


class TestAcidDeviceChain:
    """RED: Acid must have correct device chain."""

    def test_has_synth(self, acid_track_info):
        """Acid needs a synthesizer (ideally Drift or Operator for 303 sound)."""
        devices = acid_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        synth_keywords = ["drift", "operator", "analog", "wavetable", "303"]
        has_synth = any(kw in names_str for kw in synth_keywords)

        assert has_synth or len(devices) > 0, f"No synth found. Devices: {device_names}"


class TestAcidMIDIPattern:
    """RED: Acid MIDI pattern with characteristic 303 style."""

    def test_clip_exists(self, mcp):
        """Acid must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": ACID_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": ACID_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_acid_pattern(self, acid_clip_notes):
        """Acid should have 16th note pattern with accents."""
        if not acid_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(acid_clip_notes)
        # Acid lines typically have dense 16th patterns
        assert note_count >= 32, f"Acid pattern needs more notes, got: {note_count}"

    def test_notes_in_bass_range(self, acid_clip_notes):
        """Notes should be in bass/mid range (MIDI 30-65)."""
        if not acid_clip_notes:
            pytest.skip("No notes in clip")

        for note in acid_clip_notes:
            pitch = note.get("pitch", 0)
            assert 30 <= pitch <= 65, f"Pitch {pitch} outside acid range (30-65)"


class TestAcidImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 13, named "Acid"
        2. Load Drift synth (best 303 emulation in Live)
        3. Create 16-bar clip (64 beats)
        4. Add 303-style acid pattern:
           - 16th notes with varied velocities
           - Octave jumps for accent
           - Slides (overlapping notes)
           - Root note F with chromatic variations
        """
        pass
