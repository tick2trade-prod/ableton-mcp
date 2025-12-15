"""
TDD Tests for Track 06: Open Hat

Spec Reference: Section 3, Track 6 - Off-beat Open Hi-Hat
Pattern: Off-beat accents (2 and 4)
Sample: 909 Open Hat
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track06OpenHat


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track06OpenHat(mcp_client, track_index=5)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestOpenHatSample:
    """Sample and sound design tests."""

    def test_drum_sampler_loaded(self, track):
        """H: Drum Sampler loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Drum Sampler"

    def test_open_hat_sample(self, track):
        """H: 909 Open Hat sample loaded."""
        assert track.get_sample_name() == "Open Hat 909.aif"

    def test_decay_long(self, track):
        """H: Decay 200-400ms for sustain."""
        decay = track.get_amplitude_decay()
        assert 200 <= decay <= 400


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestOpenHatMIDI:
    """MIDI pattern tests."""

    def test_offbeat_notes(self, track):
        """H: Off-beat pattern = 32 notes over 16 bars."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) == 32

    def test_timing_offbeat(self, track):
        """H: Notes on beats 2 and 4."""
        notes = track.get_midi_notes(clip_index=0)
        for note in notes:
            beat_in_bar = note["start_time"] % 4
            assert beat_in_bar in [1.0, 3.0]  # Off-beats


# =============================================================================
# MIX TESTS
# =============================================================================


class TestOpenHatMix:
    """Mix settings tests."""

    def test_volume_minus_20db(self, track):
        """H: Volume at -20dB."""
        volume = track.get_volume_db()
        assert volume == -20.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
