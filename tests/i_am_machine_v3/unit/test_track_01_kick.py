"""
TDD Tests for Track 01: Kick

Spec Reference: Section 3, Track 1 - The Anchor Kick
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track01Kick as KickTrack


@pytest.fixture
def mcp_client():
    """Mock MCP client for testing."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def kick_track(mcp_client):
    """Create kick track instance."""
    track = KickTrack(mcp_client, track_index=0)
    track.create()  # Initialize track
    return track


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestKickSoundDesign:
    """Sound design tests per spec."""

    def test_sample_loaded(self, kick_track):
        """H: Kick 909 sample loaded in Drum Sampler."""
        assert kick_track.get_sample_name() == "Kick 909.aif"
        assert kick_track.is_sample_loaded() is True

    def test_pitch_envelope_amount(self, kick_track):
        """H: Pitch envelope +18st creates transient click."""
        envelope = kick_track.get_pitch_envelope()
        assert envelope["amount"] == 18

    def test_pitch_envelope_decay(self, kick_track):
        """H: Pitch envelope 15ms decay."""
        envelope = kick_track.get_pitch_envelope()
        assert envelope["decay"] == 15

    def test_amplitude_decay(self, kick_track):
        """H: Kick decay < 350ms for tight low-end."""
        decay = kick_track.get_amplitude_decay()
        assert decay < 350


# =============================================================================
# EFFECTS CHAIN TESTS
# =============================================================================


class TestKickEffectsChain:
    """Effects chain tests."""

    def test_eq_eight_loaded(self, kick_track):
        """H: EQ Eight in effects chain."""
        effects = kick_track.get_effects_chain()
        assert "EQ Eight" in [e["name"] for e in effects]

    def test_eq_highpass_30hz(self, kick_track):
        """H: High-pass @ 30Hz for headroom."""
        eq = kick_track.get_device("EQ Eight")
        hp = eq.get_band(0)
        assert hp["frequency"] == 30
        assert hp["slope"] == 48

    def test_eq_notch_200hz(self, kick_track):
        """H: Notch @ 200Hz removes boxiness."""
        eq = kick_track.get_device("EQ Eight")
        notch = eq.get_band(2)
        assert notch["frequency"] == 200
        assert notch["type"] == "notch"

    def test_saturator_loaded(self, kick_track):
        """H: Saturator adds harmonics."""
        effects = kick_track.get_effects_chain()
        assert "Saturator" in [e["name"] for e in effects]

    def test_saturator_analog_clip(self, kick_track):
        """H: Analog Clip mode."""
        saturator = kick_track.get_device("Saturator")
        assert saturator.get_parameter("Type") == "Analog Clip"

    def test_saturator_drive_3db(self, kick_track):
        """H: +3dB drive."""
        saturator = kick_track.get_device("Saturator")
        assert saturator.get_parameter("Drive") == 3.0

    def test_utility_bass_mono(self, kick_track):
        """H: Bass mono @ 120Hz."""
        utility = kick_track.get_device("Utility")
        assert utility.get_parameter("Bass Mono") is True
        assert utility.get_parameter("Bass Mono Frequency") == 120


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestKickMIDIPattern:
    """MIDI pattern tests."""

    def test_4_on_floor_64_notes(self, kick_track):
        """H: 4-on-floor for 16 bars = 64 notes."""
        notes = kick_track.get_midi_notes(clip_index=0)
        assert len(notes) == 64

    def test_4_on_floor_timing(self, kick_track):
        """H: Notes on every quarter beat."""
        notes = kick_track.get_midi_notes(clip_index=0)
        expected_times = [float(i) for i in range(64)]
        actual_times = [note["start_time"] for note in notes]
        assert actual_times == expected_times

    def test_kick_pitch_c1(self, kick_track):
        """H: All kicks on C1 (MIDI 36)."""
        notes = kick_track.get_midi_notes(clip_index=0)
        for note in notes:
            assert note["pitch"] == 36

    def test_kick_velocity_100(self, kick_track):
        """H: Velocity 100 for impact."""
        notes = kick_track.get_midi_notes(clip_index=0)
        for note in notes:
            assert note["velocity"] == 100


# =============================================================================
# MIX TESTS
# =============================================================================


class TestKickMix:
    """Mix settings tests."""

    def test_volume_minus_12db(self, kick_track):
        """H: Volume at -12dB for headroom."""
        volume_db = kick_track.get_volume_db()
        assert volume_db == -12.0

    def test_pan_center(self, kick_track):
        """H: Pan centered (mono)."""
        pan = kick_track.get_pan()
        assert pan == 0.0

    def test_fundamental_43hz(self, kick_track):
        """H: Fundamental @ ~43Hz (F1)."""
        spectrum = kick_track.analyze_spectrum()
        fundamental = spectrum.get_peak_frequency(range=(30, 60))
        assert 41 <= fundamental <= 45
