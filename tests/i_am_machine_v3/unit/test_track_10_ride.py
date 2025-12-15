"""
TDD Tests for Track 10: Ride

Spec Reference: Section 3, Track 10 - Ride Cymbal
Pattern: Every 2 beats (half notes)
Sample: 909 Ride
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track10Ride


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track10Ride(mcp_client, track_index=9)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestRideSample:
    """Sample tests."""

    def test_drum_sampler_loaded(self, track):
        """H: Drum Sampler loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Drum Sampler"

    def test_ride_sample(self, track):
        """H: 909 Ride sample loaded."""
        assert "Ride" in track.get_sample_name()


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestRideMIDI:
    """MIDI pattern tests."""

    def test_half_note_pattern(self, track):
        """H: Half note pattern = 32 notes over 16 bars."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) == 32

    def test_timing_half_notes(self, track):
        """H: Notes every 2 beats."""
        notes = track.get_midi_notes(clip_index=0)
        for i, note in enumerate(notes):
            assert note["start_time"] == i * 2.0


# =============================================================================
# MIX TESTS
# =============================================================================


class TestRideMix:
    """Mix settings tests."""

    def test_volume_minus_22db(self, track):
        """H: Volume at -22dB."""
        volume = track.get_volume_db()
        assert volume == -22.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
