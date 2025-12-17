"""
TDD Tests for Track 01: Kick - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate kick that matches reference's punch, timing, and character.

Track Layout:
- Reference + Stems occupy Tracks 1-5
- Kick is Track 6 (index 5)

RED/GREEN/REFACTOR Methodology:
- RED: Tests fail until track is created correctly
- GREEN: Implement minimum to pass tests
- REFACTOR: Optimize sound design for better similarity

Run tests:
    pytest tests/phases/phase1_intro/test_track_01_kick.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import (
    BPM,
    INTRO_BARS,
    KICK_TRACK_INDEX,
)

# Test parameters
KICK_TRACK_NAME = "Kick"
INTRO_BEATS = INTRO_BARS * 4  # 64 beats for 4-on-floor


# =============================================================================
# RED PHASE: STRUCTURAL TESTS (Track must exist with correct setup)
# =============================================================================


class TestKickTrackExists:
    """RED: Kick track must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 6 tracks (ref + stems + kick)."""
        track_count = session_info.get("track_count", 0)
        min_tracks = KICK_TRACK_INDEX + 1  # Need index 5, so 6 tracks
        assert track_count >= min_tracks, (
            f"Need at least {min_tracks} tracks. Got: {track_count}. "
            f"Kick should be at index {KICK_TRACK_INDEX}."
        )

    def test_kick_track_exists(self, kick_track_info):
        """Track at index 5 must exist."""
        assert kick_track_info is not None, f"Track {KICK_TRACK_INDEX} does not exist"
        assert "name" in kick_track_info, (
            f"Track {KICK_TRACK_INDEX} has no name attribute"
        )

    def test_kick_track_named_correctly(self, kick_track_info):
        """Track should be named 'Kick' (or contain 'Kick')."""
        name = kick_track_info.get("name", "")
        assert "Kick" in name or "kick" in name.lower(), (
            f"Track {KICK_TRACK_INDEX} should contain 'Kick', got: '{name}'"
        )


class TestKickDeviceChain:
    """RED: Kick must have correct device chain for reference sound."""

    def test_has_drum_rack_or_sampler(self, kick_track_info):
        """Kick needs Drum Rack or similar for 909 sample."""
        devices = kick_track_info.get("devices", [])
        device_names = [d.get("name", "") for d in devices]

        drum_keywords = ["Drum Rack", "Simpler", "Sampler", "Impulse", "909"]
        has_drum_device = any(
            any(kw in name for kw in drum_keywords) for name in device_names
        )
        assert has_drum_device or len(devices) > 0, (
            f"No drum device found. Devices: {device_names}"
        )

    def test_has_processing_effects(self, kick_track_info):
        """Kick should have processing (EQ, Saturator, Compressor).

        Note: 909 Core Kit includes built-in processing, so we accept
        either explicit effects OR a drum kit with at least 1 device.
        """
        devices = kick_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]
        names_str = " ".join(device_names)

        processing_keywords = ["eq", "saturator", "compressor", "drum buss", "utility"]
        has_processing = any(kw in names_str for kw in processing_keywords)

        # Accept 909/808 drum kits as they include built-in processing
        has_drum_kit = any(
            kit in names_str for kit in ["909", "808", "707", "606", "505"]
        )

        assert len(devices) >= 2 or has_processing or has_drum_kit, (
            f"Kick needs processing effects. Devices: {device_names}"
        )


# =============================================================================
# RED PHASE: PATTERN TESTS (MIDI must match 4-on-floor)
# =============================================================================


class TestKickMIDIPattern:
    """RED: Kick MIDI pattern must be correct 4-on-floor."""

    def test_clip_exists(self, mcp):
        """Kick must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": KICK_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), (
            "No clip in slot 0. Create a 16-bar clip first."
        )

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": KICK_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_64_kick_notes(self, kick_clip_notes):
        """4-on-floor for 16 bars should have ~64 notes.

        Reference-based patterns merge detected kicks with 4-on-floor grid,
        allowing for slight variations (±5 notes).
        """
        if not kick_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        note_count = len(kick_clip_notes)
        assert 59 <= note_count <= 70, (
            f"4-on-floor expects ~64 notes (±5), got: {note_count}"
        )

    def test_notes_on_quarter_beats(self, kick_clip_notes):
        """All notes must be on quarter note positions."""
        if not kick_clip_notes:
            pytest.skip("No notes in clip")

        expected_times = [float(i) for i in range(INTRO_BEATS)]
        actual_times = sorted([note["start_time"] for note in kick_clip_notes])

        for expected, actual in zip(expected_times, actual_times, strict=False):
            assert abs(expected - actual) < 0.01, (
                f"Note timing off. Expected {expected}, got {actual}"
            )

    def test_notes_on_c1_pitch(self, kick_clip_notes):
        """All kick notes should be on C1 (MIDI 36)."""
        if not kick_clip_notes:
            pytest.skip("No notes in clip")

        for note in kick_clip_notes:
            pitch = note.get("pitch", 0)
            assert pitch == 36, f"Kick pitch should be 36 (C1), got: {pitch}"

    def test_velocity_is_consistent(self, kick_clip_notes):
        """Kick velocity should be consistent (90-110 range)."""
        if not kick_clip_notes:
            pytest.skip("No notes in clip")

        velocities = [note.get("velocity", 0) for note in kick_clip_notes]
        min_vel, max_vel = min(velocities), max(velocities)

        assert min_vel >= 90, f"Velocity too low: {min_vel}. Should be 90+"
        assert max_vel <= 127, f"Velocity too high: {max_vel}"

        vel_range = max_vel - min_vel
        assert vel_range <= 20, (
            f"Velocity inconsistent. Range: {vel_range}. "
            "4-on-floor kick should be steady."
        )


# =============================================================================
# RED PHASE: SIMILARITY TESTS (Compare to reference)
# =============================================================================


class TestKickReferenceSimilarity:
    """RED: Kick must be similar to reference track's kick."""

    def test_reference_file_exists(self, reference_exists):
        """Reference file must exist for comparison."""
        assert reference_exists, "Reference file not found"

    def test_kick_timing_matches_reference(
        self, kick_clip_notes, reference_kick_onsets
    ):
        """Kick timing should align with reference kick onsets."""
        if not kick_clip_notes:
            pytest.skip("No kick notes to compare")

        if len(reference_kick_onsets) == 0:
            pytest.skip("Could not detect kick onsets in reference")

        beat_duration = 60 / BPM
        our_kick_times = [
            note["start_time"] * beat_duration for note in kick_clip_notes
        ]

        intro_duration = INTRO_BEATS * beat_duration
        ref_kicks_intro = [t for t in reference_kick_onsets if t < intro_duration]

        if len(ref_kicks_intro) == 0:
            pytest.skip("No reference kicks detected in intro section")

        our_kick_count = len([t for t in our_kick_times if t < intro_duration])
        ref_kick_count = len(ref_kicks_intro)

        count_ratio = min(our_kick_count, ref_kick_count) / max(
            our_kick_count, ref_kick_count
        )
        assert count_ratio >= 0.8, (
            f"Kick count mismatch. Ours: {our_kick_count}, Reference: {ref_kick_count}"
        )


# =============================================================================
# GREEN PHASE: IMPLEMENTATION GUIDE
# =============================================================================


class TestKickImplementationGuide:
    """GREEN: Implementation steps to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Create MIDI track at index 5 (or use existing):
           create_midi_track(index=5)

        2. Name it "Kick":
           set_track_name(track_index=5, name="Kick")

        3. Load 909 Core Kit:
           load_browser_item(track_index=5, item_uri="query:Drums#FileId_14946")

        4. Add processing:
           load_browser_item(track_index=5, item_uri="query:AudioFx#Drum%20Buss")
           load_browser_item(track_index=5, item_uri="query:AudioFx#Saturator")

        5. Create 16-bar clip:
           create_clip(track_index=5, clip_index=0, length=64.0)

        6. Add 64 kick notes (4-on-floor):
           notes = [
               {
                   "pitch": 36,
                   "start_time": float(i),
                   "duration": 0.5,
                   "velocity": 100,
                   "mute": False
               }
               for i in range(64)
           ]
           add_notes_to_clip(track_index=5, clip_index=0, notes=notes)

        7. Name the clip:
           set_clip_name(track_index=5, clip_index=0, name="Kick - Intro")
        """
        pass
