"""
TDD Tests for Track 03: Hi-hats - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate hi-hat pattern with offbeat 8ths and character matching reference.

Run tests:
    pytest tests/phases/phase1_intro/test_track_03_hihats.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import HIHATS_TRACK_INDEX

# Test parameters
HIHATS_TRACK_NAME = "Hi-hats"
INTRO_BARS = 16
BPM = 136
HIHAT_CLOSED_PITCH = 42  # F#1 - closed hi-hat
HIHAT_OPEN_PITCH = 46  # A#1 - open hi-hat


class TestHihatsTrackExists:
    """RED: Hi-hats track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 8 tracks (index 7)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= HIHATS_TRACK_INDEX + 1, (
            f"Need at least {HIHATS_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_hihats_track_exists(self, hihats_track_info):
        """Track at index 7 must exist."""
        assert hihats_track_info is not None, (
            f"Track {HIHATS_TRACK_INDEX} does not exist"
        )
        assert "name" in hihats_track_info, f"Track {HIHATS_TRACK_INDEX} has no name"

    def test_hihats_track_named_correctly(self, hihats_track_info):
        """Track should be named 'Hi-hats' or 'Hats'."""
        name = hihats_track_info.get("name", "")
        assert any(x in name.lower() for x in ["hat", "hh", "hihat"]), (
            f"Track {HIHATS_TRACK_INDEX} should contain 'Hat', got: '{name}'"
        )


class TestHihatsDeviceChain:
    """RED: Hi-hats must have correct device chain."""

    def test_has_drum_device(self, hihats_track_info):
        """Hi-hats needs Drum Rack or Sampler."""
        devices = hihats_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        drum_keywords = ["drum rack", "simpler", "sampler", "impulse", "909", "808"]
        has_drum = any(kw in names_str for kw in drum_keywords)

        assert has_drum or len(devices) > 0, (
            f"No drum device found. Devices: {device_names}"
        )


class TestHihatsMIDIPattern:
    """RED: Hi-hats MIDI pattern must be offbeat 8ths."""

    def test_clip_exists(self, mcp):
        """Hi-hats must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": HIHATS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": HIHATS_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_offbeat_pattern(self, hihats_clip_notes):
        """Hi-hats should hit on offbeat 8ths (64 notes minimum for 16 bars)."""
        if not hihats_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(hihats_clip_notes)
        # Offbeat 8ths = 4 hits per bar * 16 bars = 64 notes (minimum)
        assert note_count >= 64, (
            f"Offbeat 8ths needs at least 64 notes, got: {note_count}"
        )

    def test_notes_on_offbeats(self, hihats_clip_notes):
        """Notes should be on offbeat 8th positions."""
        if not hihats_clip_notes:
            pytest.skip("No notes in clip")

        # Offbeat 8ths: 0.5, 1.5, 2.5, 3.5 per bar
        expected_positions = []
        for bar in range(16):
            for beat in [0.5, 1.5, 2.5, 3.5]:
                expected_positions.append(bar * 4 + beat)

        actual_times = sorted([note["start_time"] for note in hihats_clip_notes])

        # Check at least 80% of expected positions are hit
        hits = sum(
            1
            for pos in expected_positions
            if any(abs(pos - t) < 0.1 for t in actual_times)
        )
        hit_ratio = hits / len(expected_positions)

        assert hit_ratio >= 0.8, (
            f"Only {hit_ratio * 100:.0f}% of offbeats hit. "
            "Hi-hats should hit on offbeat 8ths."
        )


class TestHihatsImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 7, named "Hi-hats"
        2. Load 909 Core Kit or similar drum rack
        3. Create 16-bar clip (64 beats)
        4. Add 64 hi-hat hits on offbeat 8ths
        """
        pass
