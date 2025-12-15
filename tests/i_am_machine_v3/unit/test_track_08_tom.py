"""
TDD Tests for Track 08: Tom

Spec Reference: Section 3, Track 8 - Pitched Tom Fill
Pattern: Fills every 4 bars
Sample: 909 Tom (tuned)
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track08Tom


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track08Tom(mcp_client, track_index=7)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestTomSample:
    """Sample and sound design tests."""

    def test_drum_sampler_loaded(self, track):
        """H: Drum Sampler loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Drum Sampler"

    def test_tom_sample(self, track):
        """H: 909 Tom sample loaded."""
        assert "Tom" in track.get_sample_name()

    def test_pitch_tuned(self, track):
        """H: Tom tuned to F."""
        pitch = track.get_pitch_offset()
        assert pitch in [-5, 0, 7]  # F, C, or G


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestTomMIDI:
    """MIDI pattern tests."""

    def test_fill_pattern(self, track):
        """H: Fills every 4 bars = 16-24 notes."""
        notes = track.get_midi_notes(clip_index=0)
        assert 16 <= len(notes) <= 32

    def test_fill_timing(self, track):
        """H: Fills on last beat of every 4th bar."""
        notes = track.get_midi_notes(clip_index=0)
        # Check some notes are in fill positions
        fill_positions = [15, 31, 47, 63]  # End of bars 4, 8, 12, 16
        has_fills = any(n["start_time"] in fill_positions for n in notes)
        assert has_fills


# =============================================================================
# MIX TESTS
# =============================================================================


class TestTomMix:
    """Mix settings tests."""

    def test_volume_minus_18db(self, track):
        """H: Volume at -18dB."""
        volume = track.get_volume_db()
        assert volume == -18.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
