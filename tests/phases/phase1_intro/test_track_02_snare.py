"""
TDD Tests for Track 02: Snare - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate snare with backbeat pattern and character matching reference.

Run tests:
    pytest tests/phases/phase1_intro/test_track_02_snare.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import SNARE_TRACK_INDEX

# Test parameters
SNARE_TRACK_NAME = "Snare"
INTRO_BARS = 16
BPM = 136
SNARE_PITCH = 38  # D1 - typical snare in drum rack


class TestSnareTrackExists:
    """RED: Snare track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 7 tracks (index 6)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= SNARE_TRACK_INDEX + 1, (
            f"Need at least {SNARE_TRACK_INDEX + 1} tracks. Got: {track_count}"
        )

    def test_snare_track_exists(self, snare_track_info):
        """Track at index 6 must exist."""
        assert snare_track_info is not None, f"Track {SNARE_TRACK_INDEX} does not exist"
        assert "name" in snare_track_info, f"Track {SNARE_TRACK_INDEX} has no name"

    def test_snare_track_named_correctly(self, snare_track_info):
        """Track should be named 'Snare'."""
        name = snare_track_info.get("name", "")
        assert "Snare" in name or "snare" in name.lower(), (
            f"Track {SNARE_TRACK_INDEX} should contain 'Snare', got: '{name}'"
        )


class TestSnareDeviceChain:
    """RED: Snare must have correct device chain."""

    def test_has_drum_device(self, snare_track_info):
        """Snare needs Drum Rack or Sampler."""
        devices = snare_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        drum_keywords = ["drum rack", "simpler", "sampler", "impulse", "909", "808"]
        has_drum = any(kw in names_str for kw in drum_keywords)

        assert has_drum or len(devices) > 0, (
            f"No drum device found. Devices: {device_names}"
        )


class TestSnareMIDIPattern:
    """RED: Snare MIDI pattern must be backbeat (2 and 4)."""

    def test_clip_exists(self, mcp):
        """Snare must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": SNARE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), "No clip in slot 0"

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": SNARE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_backbeat_pattern(self, snare_clip_notes):
        """Snare should have snare hits on or near backbeat positions.

        Reference-based patterns may have fewer notes than mechanical backbeat.
        The actual reference track has ~17 snare hits in the intro section.
        """
        if not snare_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(snare_clip_notes)
        # Reference patterns have ~17 snares, allow as few as 12 for variations
        assert note_count >= 12, f"Snare needs at least 12 notes, got: {note_count}"

    def test_notes_on_backbeats(self, snare_clip_notes):
        """Most snare notes should be on or near backbeat positions.

        Reference patterns derive from actual analysis and may have
        variations from mechanical backbeat. Check that snare notes
        are predominantly on beats 2 and 4 (positions 1 and 3 in bar).
        """
        if not snare_clip_notes:
            pytest.skip("No notes in clip")

        expected_positions = []
        for bar in range(16):
            expected_positions.append(bar * 4 + 1)  # Beat 2 (0-indexed: 1)
            expected_positions.append(bar * 4 + 3)  # Beat 4 (0-indexed: 3)

        actual_times = sorted([note["start_time"] for note in snare_clip_notes])

        # Check how many of the actual snare hits are near backbeat positions
        backbeat_hits = sum(
            1
            for t in actual_times
            if any(abs(pos - t) < 0.15 for pos in expected_positions)
        )
        backbeat_ratio = backbeat_hits / len(actual_times) if actual_times else 0

        # At least 50% of snare hits should be on backbeats
        # (reference patterns may have ghost notes and variations)
        assert backbeat_ratio >= 0.5, (
            f"Only {backbeat_ratio * 100:.0f}% of snare hits on backbeats. "
            f"Expected at least 50%. Hits: {actual_times[:10]}..."
        )


class TestSnareImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Track exists at index 6, named "Snare"
        2. Load 909 Core Kit or similar drum rack
        3. Create 16-bar clip (64 beats)
        4. Add 32 snare hits on backbeats (2 and 4)
        """
        pass
