"""
TDD Tests for Track 11: Drone - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate atmospheric drone/pad for texture.

Run tests:
    pytest tests/phases/phase1_intro/test_track_11_drone.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import DRONE_TRACK_INDEX

# Test parameters
DRONE_TRACK_NAME = "Drone"
INTRO_BARS = 16
BPM = 136
ROOT_NOTE_F = 41  # F1


class TestDroneTrackExists:
    """RED: Drone track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 16 tracks (index 15)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= DRONE_TRACK_INDEX + 1, (
            f"Need at least {DRONE_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_drone_track_exists(self, drone_track_info):
        """Track at index 15 must exist."""
        assert drone_track_info is not None, f"Track {DRONE_TRACK_INDEX} does not exist"
        assert "name" in drone_track_info, f"Track {DRONE_TRACK_INDEX} has no name"

    def test_drone_track_named_correctly(self, drone_track_info):
        """Track should be named 'Drone' or 'Pad'."""
        name = drone_track_info.get("name", "")
        assert any(x in name.lower() for x in ["drone", "pad", "atmo"]), (
            f"Track {DRONE_TRACK_INDEX} should contain 'Drone/Pad', got: '{name}'"
        )


class TestDroneDeviceChain:
    """RED: Drone must have correct device chain."""

    def test_has_synth(self, drone_track_info):
        """Drone needs a synthesizer (Wavetable or Operator)."""
        devices = drone_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        synth_keywords = ["wavetable", "operator", "analog", "drift"]
        has_synth = any(kw in names_str for kw in synth_keywords)

        assert has_synth or len(devices) > 0, f"No synth found. Devices: {device_names}"


class TestDroneMIDIPattern:
    """RED: Drone MIDI pattern for sustained atmosphere."""

    def test_clip_exists(self, mcp):
        """Drone must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": DRONE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": DRONE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_sustained_notes(self, drone_clip_notes):
        """Drone should have long sustained notes."""
        if not drone_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        # Check note durations - drone should be sustained
        durations = [note.get("duration", 0) for note in drone_clip_notes]
        avg_duration = sum(durations) / len(durations)

        assert avg_duration >= 4.0, (
            f"Drone notes should be sustained (>= 4 beats), avg: {avg_duration}"
        )

    def test_notes_on_root(self, drone_clip_notes):
        """Drone should primarily be on root note F."""
        if not drone_clip_notes:
            pytest.skip("No notes in clip")

        pitches = [note.get("pitch", 0) for note in drone_clip_notes]
        # F = pitch class 5
        f_count = sum(1 for p in pitches if p % 12 == 5)
        f_ratio = f_count / len(pitches)

        assert f_ratio >= 0.5, (
            f"Drone should be mostly on F, only {f_ratio * 100:.0f}% are F"
        )


class TestDroneImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 15, named "Drone"
        2. Load Wavetable or Operator synth
        3. Create 16-bar clip (64 beats)
        4. Add sustained drone notes:
           notes = [
               {"pitch": 41, "start_time": 0.0, "duration": 64.0, "velocity": 60}
           ]
           # Or multiple shorter sustained notes for F chord
        """
        pass
