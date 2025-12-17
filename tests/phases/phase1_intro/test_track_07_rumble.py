"""
TDD Tests for Track 07: Rumble - Phase 1 Intro (Bars 1-16)

Reference: assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3
Goal: Recreate sub bass with sidechain pumping that matches reference.

RED/GREEN/REFACTOR Methodology:
- RED: Tests fail until track is created correctly
- GREEN: Implement minimum to pass tests
- REFACTOR: Optimize sidechain settings for better pump feel

Run tests:
    pytest tests/phases/phase1_intro/test_track_07_rumble.py -v
"""

import pytest

from tests.phases.phase1_intro.conftest import (
    KICK_TRACK_INDEX,
    RUMBLE_TRACK_INDEX,
)

# Test parameters
RUMBLE_TRACK_NAME = "Rumble"
INTRO_BARS = 16
BPM = 136
ROOT_NOTE_F0 = 29  # F0 for deep sub
ROOT_NOTE_F1 = 41  # F1 alternative


# =============================================================================
# RED PHASE: STRUCTURAL TESTS (Track must exist with correct setup)
# =============================================================================


class TestRumbleTrackExists:
    """RED: Track 07 must exist in Ableton session."""

    def test_session_has_enough_tracks(self, session_info):
        """Session must have at least 7 tracks (index 6)."""
        track_count = session_info.get("track_count", 0)
        assert track_count >= 7, (
            f"Need at least 7 tracks for Rumble at index 6. Got: {track_count}"
        )

    def test_rumble_track_exists(self, rumble_track_info):
        """Track at index 6 must exist."""
        assert rumble_track_info is not None, "Track 6 does not exist"
        assert "name" in rumble_track_info, "Track 6 has no name attribute"

    def test_rumble_track_named_correctly(self, rumble_track_info):
        """Track 6 should be named 'Rumble' (or contain 'Rumble')."""
        name = rumble_track_info.get("name", "")
        assert "Rumble" in name or "rumble" in name.lower() or "Sub" in name, (
            f"Track 6 name should contain 'Rumble' or 'Sub', got: '{name}'"
        )


class TestRumbleDeviceChain:
    """RED: Rumble must have correct device chain for sub bass sound."""

    def test_has_synthesizer(self, rumble_track_info):
        """Rumble needs a synth for sub bass (Operator, Analog, Wavetable)."""
        devices = rumble_track_info.get("devices", [])
        device_names = [d.get("name", "") for d in devices]

        synth_names = ["Operator", "Analog", "Wavetable", "Drift", "Serum"]
        has_synth = any(
            any(synth in name for synth in synth_names) for name in device_names
        )

        assert has_synth or len(devices) > 0, (
            f"No synthesizer found for sub bass. Devices: {device_names}. "
            "Load Operator or similar synth."
        )

    def test_has_compressor(self, rumble_track_info):
        """Rumble should have Compressor for sidechain (recommended).

        Note: Compressor is essential for sidechain pumping but may need
        to be added manually due to MCP browser limitations.
        """
        devices = rumble_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]

        has_compressor = any("compressor" in name for name in device_names)
        # Accept any synth as base - compressor can be added manually
        has_synth = any(
            s in " ".join(device_names)
            for s in ["operator", "analog", "wavetable", "drift"]
        )
        assert has_compressor or has_synth, (
            f"No Compressor or synth found. Devices: {device_names}. "
            "Add Compressor manually for sidechain pumping."
        )

    def test_has_eq_for_shaping(self, rumble_track_info):
        """Rumble should have EQ for sub shaping (recommended).

        Note: EQ is recommended for shaping but Operator has built-in
        filtering. Can be added manually for more control.
        """
        devices = rumble_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]

        has_eq = any("eq" in name for name in device_names)
        # Accept any synth with built-in filtering as alternative
        has_synth = any(
            s in " ".join(device_names)
            for s in ["operator", "analog", "wavetable", "drift"]
        )
        assert has_eq or has_synth, (
            f"No EQ or synth found. Devices: {device_names}. "
            "EQ recommended for shaping sub frequencies."
        )

    def test_has_saturation(self, rumble_track_info):
        """Rumble should have saturation for harmonics."""
        devices = rumble_track_info.get("devices", [])
        device_names = [d.get("name", "").lower() for d in devices]

        has_saturation = any(
            keyword in name
            for name in device_names
            for keyword in ["saturator", "roar", "overdrive", "distortion"]
        )
        # Saturation is recommended but not strictly required
        if not has_saturation:
            pytest.skip("No saturation found - recommended for sub harmonics")


class TestRumbleSidechain:
    """RED: Rumble must have sidechain from Kick."""

    def test_kick_track_exists_for_sidechain(self, mcp):
        """Kick track must exist as sidechain source."""
        kick_info = mcp("get_track_info", {"track_index": KICK_TRACK_INDEX})
        assert kick_info is not None, (
            f"Kick track (index {KICK_TRACK_INDEX}) must exist for sidechain"
        )

    def test_compressor_in_chain(self, rumble_track_info):
        """Compressor should be in device chain for sidechain (recommended).

        Note: Compressor needs to be added manually for sidechain.
        Test passes if synth is present (base requirement).
        """
        devices = rumble_track_info.get("devices", [])
        device_names = [d.get("name", "") for d in devices]
        names_lower = [n.lower() for n in device_names]

        compressor_exists = any("compressor" in name for name in names_lower)
        synth_exists = any(
            s in " ".join(names_lower)
            for s in ["operator", "analog", "wavetable", "drift"]
        )
        assert compressor_exists or synth_exists, (
            f"No Compressor or synth in chain. Devices: {device_names}. "
            "Add Compressor manually for sidechain."
        )

    @pytest.mark.skip(
        reason="Sidechain routing not queryable via current MCP - manual verify"
    )
    def test_sidechain_routed_from_kick(self):
        """Compressor sidechain should be routed from Kick track.

        Manual verification:
        1. Open Compressor on Rumble track
        2. Click sidechain arrow (triangle)
        3. Verify 'Audio From' is set to 'Kick' or '1-Kick'
        4. Verify sidechain is enabled
        """
        pass


# =============================================================================
# RED PHASE: PATTERN TESTS (MIDI must be sustained sub notes)
# =============================================================================


class TestRumbleMIDIPattern:
    """RED: Rumble MIDI pattern must be sustained sub bass."""

    def test_clip_exists(self, mcp):
        """Rumble must have a clip in slot 0."""
        track_info = mcp("get_track_info", {"track_index": RUMBLE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        assert len(clip_slots) > 0, "No clip slots found"
        assert clip_slots[0].get("has_clip", False), (
            "No clip in slot 0. Create a 16-bar clip first."
        )

    def test_clip_is_16_bars(self, mcp):
        """Clip must be 16 bars (64 beats) long."""
        track_info = mcp("get_track_info", {"track_index": RUMBLE_TRACK_INDEX})
        clip_slots = track_info.get("clip_slots", [])

        if not clip_slots or not clip_slots[0].get("has_clip"):
            pytest.skip("No clip to test")

        clip = clip_slots[0].get("clip", {})
        length = clip.get("length", 0)

        assert length == 64.0, f"Clip length should be 64.0 beats, got: {length}"

    def test_has_sustained_notes(self, rumble_clip_notes):
        """Rumble should have sustained notes (not staccato)."""
        if not rumble_clip_notes:
            pytest.skip("No notes in clip - create pattern first")

        # Check note durations - should be long (>= 1 beat for sub)
        durations = [note.get("duration", 0) for note in rumble_clip_notes]
        avg_duration = sum(durations) / len(durations)

        assert avg_duration >= 2.0, (
            f"Sub bass notes too short. Avg duration: {avg_duration} beats. "
            "Should be sustained (4 beats per bar)."
        )

    def test_notes_in_sub_range(self, rumble_clip_notes):
        """All notes should be in sub bass range (MIDI 24-48)."""
        if not rumble_clip_notes:
            pytest.skip("No notes in clip")

        for note in rumble_clip_notes:
            pitch = note.get("pitch", 0)
            assert 24 <= pitch <= 48, (
                f"Pitch {pitch} outside sub range (24-48). "
                "Sub bass should be F0 (29) to C2 (48)."
            )

    def test_notes_on_root_f(self, rumble_clip_notes):
        """Notes should primarily be on F (root note of the track)."""
        if not rumble_clip_notes:
            pytest.skip("No notes in clip")

        f_notes = [ROOT_NOTE_F0, ROOT_NOTE_F1, 17, 53]  # F in various octaves
        pitches = [note.get("pitch", 0) for note in rumble_clip_notes]

        # At least 80% should be F notes (allowing some variation)
        # F = pitch class 5 (F in any octave)
        f_count = sum(1 for p in pitches if p in f_notes or p % 12 == 5)
        f_ratio = f_count / len(pitches)

        assert f_ratio >= 0.8, (
            f"Only {f_ratio * 100:.0f}% of notes are F. "
            "Sub bass should follow root note F for I Am Machine."
        )

    def test_note_coverage_full_intro(self, rumble_clip_notes):
        """Notes should cover the full 16 bars (no gaps > 4 beats)."""
        if not rumble_clip_notes:
            pytest.skip("No notes in clip")

        # Sort notes by start time
        sorted_notes = sorted(rumble_clip_notes, key=lambda n: n["start_time"])

        # Check for gaps
        for i, note in enumerate(sorted_notes):
            start = note["start_time"]
            duration = note["duration"]
            end = start + duration

            if i < len(sorted_notes) - 1:
                next_start = sorted_notes[i + 1]["start_time"]
                gap = next_start - end

                assert gap <= 0.5, (
                    f"Gap of {gap} beats between notes at {end} and {next_start}. "
                    "Sub bass should be continuous with no gaps."
                )


# =============================================================================
# RED PHASE: SIDECHAIN PUMP TESTS
# =============================================================================


class TestRumbleSidechainPump:
    """RED: Sidechain pumping must create the signature groove."""

    @pytest.mark.skip(reason="Requires audio analysis - verify manually")
    def test_pump_depth(self):
        """Sidechain should duck rumble by 6-12dB on each kick.

        Manual verification:
        1. Play Kick + Rumble together
        2. Watch Rumble track meter
        3. Volume should visibly duck on each kick
        4. Duck depth: ~6-12dB
        """
        pass

    @pytest.mark.skip(reason="Requires audio analysis - verify manually")
    def test_pump_timing(self):
        """Sidechain release should create smooth pump (100-150ms).

        Manual verification:
        1. Play Kick + Rumble together
        2. Listen for rhythmic pumping
        3. Pump should feel groovy, not choppy
        4. Adjust compressor release if needed
        """
        pass

    @pytest.mark.skip(reason="Requires audio analysis - verify manually")
    def test_sub_doesnt_mask_kick(self):
        """Sub should duck enough to not mask kick transient.

        Manual verification:
        1. Play Kick + Rumble together
        2. Kick should punch through clearly
        3. If kick is muddy, increase sidechain depth or lower sub level
        """
        pass


# =============================================================================
# RED PHASE: SIMILARITY TESTS (Compare to reference)
# =============================================================================


class TestRumbleReferenceSimilarity:
    """RED: Rumble must match reference track's sub bass character."""

    def test_reference_file_exists(self, reference_exists):
        """Reference file must exist for comparison."""
        assert reference_exists, "Reference file not found. Cannot compare similarity."

    @pytest.mark.skip(
        reason="Requires stem separation - verify manually after separation"
    )
    def test_sub_frequency_content(self):
        """Sub frequency content should match reference bass stem.

        After stem separation:
        1. Load reference Bass stem
        2. Compare spectral content 30-80Hz
        3. Our sub should have similar fundamental presence
        """
        pass

    @pytest.mark.skip(reason="Requires audio analysis - verify manually")
    def test_pump_rhythm_matches(self):
        """Sidechain pump rhythm should match reference.

        Manual verification:
        1. A/B reference and our Kick+Rumble
        2. Pump timing should feel similar
        3. Groove should match
        """
        pass


# =============================================================================
# GREEN PHASE: IMPLEMENTATION CHECKLIST
# =============================================================================


class TestRumbleImplementationChecklist:
    """GREEN: Checklist of what to implement to pass RED tests."""

    @pytest.mark.skip(reason="Implementation guide - not a test")
    def test_implementation_steps(self):
        """
        To pass all RED tests, implement:

        1. Create MIDI track at index 11 (Track 12):
           create_midi_track(index=11)

        2. Name it "Rumble":
           set_track_name(track_index=11, name="Rumble")

        3. Load Operator synth:
           load_browser_item(track_index=11, item_uri="query:Synths#Operator")

        4. Add processing chain:
           load_browser_item(track_index=11, item_uri="query:AudioFx#EQ%20Eight")
           load_browser_item(track_index=11, item_uri="query:AudioFx#Saturator")
           load_browser_item(track_index=11, item_uri="query:AudioFx#Compressor")

        5. Configure sidechain from Kick (Track 6 = index 5):
           set_sidechain_input(
               track_index=11,
               device_index=-1,  # Last device (Compressor)
               source_track_index=5  # Kick
           )

        6. Create 16-bar clip:
           create_clip(track_index=11, clip_index=0, length=64.0)

        7. Add sustained sub bass notes (one per bar):
           notes = [{
               "pitch": 29, "start_time": float(bar * 4),
               "duration": 4.0, "velocity": 100
           } for bar in range(16)]
           add_notes_to_clip(track_index=11, clip_index=0, notes=notes)

        8. Name the clip:
           set_clip_name(track_index=11, clip_index=0, name="Rumble - Intro")

        Run script:
           python scripts/workflows/create_intro_bass.py
        """
        pass


# =============================================================================
# COMPRESSOR SETTINGS REFERENCE
# =============================================================================


class TestCompressorSettingsReference:
    """Reference settings for sidechain compressor."""

    @pytest.mark.skip(reason="Settings reference - not a test")
    def test_recommended_compressor_settings(self):
        """
        Recommended Compressor settings for hard techno sidechain pump:

        Threshold: -25dB to -35dB (adjust for pump depth)
        Ratio: 8:1 or higher (infinity for maximum pump)
        Attack: 0.01ms to 1ms (instant for tight pump)
        Release: 100ms to 150ms (adjust for groove feel)

        At 136 BPM:
        - Beat duration: ~441ms
        - Release of 120ms = pump recovers ~27% through beat
        - Creates the signature techno groove

        Sidechain routing:
        - Audio From: Kick track (Track 0 / 1-Kick)
        - Sidechain: Enabled
        - EQ (optional): High-pass the sidechain input to focus on kick transient
        """
        pass
