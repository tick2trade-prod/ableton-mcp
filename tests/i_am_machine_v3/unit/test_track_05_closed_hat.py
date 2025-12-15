"""
TDD Tests for Track 05: Closed Hat

Spec Reference: Section 3, Track 5 - Tight Closed Hi-Hat
Pattern: 8th notes with velocity variation
Sample: 909 Closed Hat
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track05ClosedHat


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track05ClosedHat(mcp_client, track_index=4)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestClosedHatSample:
    """Sample and sound design tests."""

    def test_drum_sampler_loaded(self, track):
        """H: Drum Sampler loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Drum Sampler"

    def test_closed_hat_sample(self, track):
        """H: 909 Closed Hat sample loaded."""
        assert track.get_sample_name() == "Closed Hat 909.aif"

    def test_decay_short(self, track):
        """H: Decay < 100ms for tight sound."""
        decay = track.get_amplitude_decay()
        assert decay < 100


# =============================================================================
# EFFECTS TESTS
# =============================================================================


class TestClosedHatEffects:
    """Effects chain tests."""

    def test_eq_highpass(self, track):
        """H: High-pass to remove low rumble."""
        eq = track.get_device("EQ Eight")
        hp = eq.get_band(0)
        assert hp["frequency"] >= 200


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestClosedHatMIDI:
    """MIDI pattern tests."""

    def test_eighth_notes(self, track):
        """H: 8th note pattern = 128 notes over 16 bars."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) == 128

    def test_timing_eighth(self, track):
        """H: Notes on every 8th note."""
        notes = track.get_midi_notes(clip_index=0)
        for i, note in enumerate(notes):
            assert note["start_time"] == i * 0.5

    def test_velocity_groove(self, track):
        """H: Velocity variation (accent on 1 and 3)."""
        notes = track.get_midi_notes(clip_index=0)
        # Check that beat 1 and 3 accents are louder
        velocities = [n["velocity"] for n in notes]
        assert max(velocities) >= 100
        assert min(velocities) <= 80


# =============================================================================
# MIX TESTS
# =============================================================================


class TestClosedHatMix:
    """Mix settings tests."""

    def test_volume_minus_18db(self, track):
        """H: Volume at -18dB."""
        volume = track.get_volume_db()
        assert volume == -18.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
