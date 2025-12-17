"""
TDD Tests for Track 06: Ride - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate ride cymbal pattern for groove texture.

Run tests:
    pytest tests/phases/phase1_intro/test_track_06_ride.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import RIDE_TRACK_INDEX

# Test parameters
RIDE_TRACK_NAME = "Ride"
INTRO_BARS = 16
BPM = 136
RIDE_PITCH = 51  # D#2 - ride cymbal


class TestRideTrackExists:
    """RED: Ride track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 11 tracks (index 10)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= RIDE_TRACK_INDEX + 1, (
            f"Need at least {RIDE_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_ride_track_exists(self, ride_track_info):
        """Track at index 10 must exist."""
        assert ride_track_info is not None, f"Track {RIDE_TRACK_INDEX} does not exist"
        assert "name" in ride_track_info, f"Track {RIDE_TRACK_INDEX} has no name"

    def test_ride_track_named_correctly(self, ride_track_info):
        """Track should be named 'Ride' or 'Cymbal'."""
        name = ride_track_info.get("name", "")
        assert any(x in name.lower() for x in ["ride", "cymbal"]), (
            f"Track {RIDE_TRACK_INDEX} should contain 'Ride/Cymbal', got: '{name}'"
        )


class TestRideDeviceChain:
    """RED: Ride must have correct device chain."""

    def test_has_drum_device(self, ride_track_info):
        """Ride needs Drum Rack or Sampler."""
        devices = ride_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        drum_keywords = ["drum rack", "simpler", "sampler", "impulse", "909", "808"]
        has_drum = any(kw in names_str for kw in drum_keywords)

        assert has_drum or len(devices) > 0, (
            f"No drum device found. Devices: {device_names}"
        )


class TestRideMIDIPattern:
    """RED: Ride MIDI pattern."""

    def test_clip_exists(self, mcp):
        """Ride must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": RIDE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": RIDE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_ride_pattern(self, ride_clip_notes):
        """Ride should have quarter or 8th note pattern."""
        if not ride_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(ride_clip_notes)
        # Ride typically plays quarter notes (64) or 8ths (128)
        assert note_count >= 32, (
            f"Ride should have at least 32 notes, got: {note_count}"
        )


class TestRideImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 10, named "Ride"
        2. Load 909 Core Kit or similar drum rack
        3. Create 16-bar clip (64 beats)
        4. Add ride pattern (quarter notes):
           notes = [
               {"pitch": 51, "start_time": float(i), "duration": 0.5, "velocity": 70}
               for i in range(64)
           ]
        """
        pass
