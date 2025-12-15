"""
TDD Tests for Track 09: Glitch

Spec Reference: Section 3, Track 9 - Glitch Percussion
Pattern: Random hits, sparse, glitchy
Synth/Sample: Beat Repeat or sliced percussion
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track09Glitch


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track09Glitch(mcp_client, track_index=8)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestGlitchDevice:
    """Device tests."""

    def test_beat_repeat_loaded(self, track):
        """H: Beat Repeat for glitch effect."""
        devices = track.get_effects_chain()
        assert "Beat Repeat" in [d["name"] for d in devices]

    def test_chance_parameter(self, track):
        """H: Chance parameter for randomness."""
        br = track.get_device("Beat Repeat")
        chance = br.get_parameter("Chance")
        assert 0.2 <= chance <= 0.5  # 20-50% chance


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestGlitchMIDI:
    """MIDI pattern tests."""

    def test_sparse_pattern(self, track):
        """H: Sparse glitch hits (8-32 notes)."""
        notes = track.get_midi_notes(clip_index=0)
        assert 8 <= len(notes) <= 32

    def test_irregular_timing(self, track):
        """H: Notes NOT on regular grid."""
        notes = track.get_midi_notes(clip_index=0)
        # Check that timing varies
        timings = [n["start_time"] % 1 for n in notes]
        unique_timings = set(timings)
        assert len(unique_timings) >= 2  # Not all on beats


# =============================================================================
# MIX TESTS
# =============================================================================


class TestGlitchMix:
    """Mix settings tests."""

    def test_volume_minus_22db(self, track):
        """H: Volume at -22dB (subtle)."""
        volume = track.get_volume_db()
        assert volume == -22.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
