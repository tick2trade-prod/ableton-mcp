"""
TDD Tests for Track 15: Riser

Spec Reference: Section 3, Track 15 - Riser/Sweep
Pattern: Building riser at end of 16 bars
Synth: Wavetable (noise + filtered sweep)
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track15Riser


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track15Riser(mcp_client, track_index=14)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestRiserSynth:
    """Synth tests."""

    def test_wavetable_loaded(self, track):
        """H: Wavetable synth loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Wavetable"

    def test_noise_oscillator(self, track):
        """H: Noise oscillator for texture."""
        wt = track.get_device("Wavetable")
        noise = wt.get_parameter("Osc 2 Wave")
        assert "Noise" in noise


# =============================================================================
# EFFECTS TESTS
# =============================================================================


class TestRiserEffects:
    """Effects tests."""

    def test_auto_filter_loaded(self, track):
        """H: Auto Filter for sweep."""
        devices = track.get_effects_chain()
        assert "Auto Filter" in [d["name"] for d in devices]

    def test_filter_sweep_up(self, track):
        """H: Filter sweeps up."""
        af = track.get_device("Auto Filter")
        lfo_amount = af.get_parameter("LFO Amount")
        assert lfo_amount > 0


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestRiserMIDI:
    """MIDI pattern tests."""

    def test_riser_note(self, track):
        """H: Single long riser note."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) == 1

    def test_riser_at_end(self, track):
        """H: Riser starts in last 4 bars."""
        notes = track.get_midi_notes(clip_index=0)
        assert notes[0]["start_time"] >= 48  # Bar 13+

    def test_riser_long_duration(self, track):
        """H: Riser is 4 bars long."""
        notes = track.get_midi_notes(clip_index=0)
        assert notes[0]["duration"] >= 16  # 4 bars


# =============================================================================
# MIX TESTS
# =============================================================================


class TestRiserMix:
    """Mix settings tests."""

    def test_volume_minus_15db(self, track):
        """H: Volume at -15dB."""
        volume = track.get_volume_db()
        assert volume == -15.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
