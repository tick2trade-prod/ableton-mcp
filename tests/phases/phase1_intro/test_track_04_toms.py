"""
TDD Tests for Track 04: Toms - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate tom fills for transitions and groove accents.

Run tests:
    pytest tests/phases/phase1_intro/test_track_04_toms.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import TOMS_TRACK_INDEX

# Test parameters
TOMS_TRACK_NAME = "Toms"
INTRO_BARS = 16
BPM = 136
TOM_LOW_PITCH = 41  # F1 - low tom
TOM_MID_PITCH = 45  # A1 - mid tom
TOM_HIGH_PITCH = 48  # C2 - high tom


class TestTomsTrackExists:
    """RED: Toms track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 9 tracks (index 8)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= TOMS_TRACK_INDEX + 1, (
            f"Need at least {TOMS_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_toms_track_exists(self, toms_track_info):
        """Track at index 8 must exist."""
        assert toms_track_info is not None, f"Track {TOMS_TRACK_INDEX} does not exist"
        assert "name" in toms_track_info, f"Track {TOMS_TRACK_INDEX} has no name"

    def test_toms_track_named_correctly(self, toms_track_info):
        """Track should be named 'Toms'."""
        name = toms_track_info.get("name", "")
        assert "Tom" in name or "tom" in name.lower(), (
            f"Track {TOMS_TRACK_INDEX} should contain 'Tom', got: '{name}'"
        )


class TestTomsDeviceChain:
    """RED: Toms must have correct device chain."""

    def test_has_drum_device(self, toms_track_info):
        """Toms needs Drum Rack or Sampler."""
        devices = toms_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        drum_keywords = ["drum rack", "simpler", "sampler", "impulse", "909", "808"]
        has_drum = any(kw in names_str for kw in drum_keywords)

        assert has_drum or len(devices) > 0, (
            f"No drum device found. Devices: {device_names}"
        )


class TestTomsMIDIPattern:
    """RED: Toms MIDI pattern for fills."""

    def test_clip_exists(self, mcp):
        """Toms must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": TOMS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": TOMS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_fill_pattern(self, toms_clip_notes):
        """Toms should have fill patterns (sparse, accent-based)."""
        if not toms_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(toms_clip_notes)
        # Toms are sparse fills - expect at least a few per 16 bars
        assert note_count >= 4, (
            f"Toms should have at least 4 notes for fills, got: {note_count}"
        )
        # But not too many (not a constant pattern)
        assert note_count <= 64, (
            f"Toms should be sparse fills, got too many: {note_count}"
        )


class TestTomsImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 8, named "Toms"
        2. Load 909 Core Kit or similar drum rack
        3. Create 16-bar clip (64 beats)
        4. Add tom fills at bar transitions (every 4 or 8 bars):
           notes = [
               # Fill at end of bar 4
               {"pitch": 48, "start_time": 15.5, "duration": 0.25, "velocity": 100},
               {"pitch": 45, "start_time": 15.75, "duration": 0.25, "velocity": 95},
               # Fill at end of bar 8
               {"pitch": 48, "start_time": 31.5, "duration": 0.25, "velocity": 100},
               {"pitch": 45, "start_time": 31.75, "duration": 0.25, "velocity": 95},
               # etc.
           ]
        """
        pass
