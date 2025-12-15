"""
TDD Tests for Track 07: Clap

Spec Reference: Section 3, Track 7 - Layered Clap
Pattern: Beats 2 and 4
Sample: 909 Clap with layered reverb
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track07Clap


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track07Clap(mcp_client, track_index=6)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestClapSample:
    """Sample and sound design tests."""

    def test_drum_sampler_loaded(self, track):
        """H: Drum Sampler loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Drum Sampler"

    def test_clap_sample(self, track):
        """H: 909 Clap sample loaded."""
        assert track.get_sample_name() == "Clap 909.aif"


# =============================================================================
# EFFECTS TESTS
# =============================================================================


class TestClapEffects:
    """Effects chain tests."""

    def test_reverb_loaded(self, track):
        """H: Reverb for space."""
        devices = track.get_effects_chain()
        assert "Reverb" in [d["name"] for d in devices]

    def test_reverb_short_decay(self, track):
        """H: Short reverb decay (0.5-1s)."""
        reverb = track.get_device("Reverb")
        decay = reverb.get_parameter("Decay")
        assert 0.5 <= decay <= 1.0


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestClapMIDI:
    """MIDI pattern tests."""

    def test_backbeat_notes(self, track):
        """H: Backbeat pattern = 32 notes over 16 bars."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) == 32

    def test_timing_backbeat(self, track):
        """H: Notes on beats 2 and 4."""
        notes = track.get_midi_notes(clip_index=0)
        for note in notes:
            beat_in_bar = note["start_time"] % 4
            assert beat_in_bar in [1.0, 3.0]

    def test_velocity_100(self, track):
        """H: Full velocity for impact."""
        notes = track.get_midi_notes(clip_index=0)
        for note in notes:
            assert note["velocity"] == 100


# =============================================================================
# MIX TESTS
# =============================================================================


class TestClapMix:
    """Mix settings tests."""

    def test_volume_minus_15db(self, track):
        """H: Volume at -15dB."""
        volume = track.get_volume_db()
        assert volume == -15.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
