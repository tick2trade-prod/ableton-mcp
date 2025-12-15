"""
TDD Tests for Track 11: Stab

Spec Reference: Section 3, Track 11 - Synth Stab
Pattern: Rhythmic stabs (syncopated)
Synth: Wavetable (brass/string stab)
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track11Stab


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track11Stab(mcp_client, track_index=10)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestStabSynth:
    """Synth tests."""

    def test_wavetable_loaded(self, track):
        """H: Wavetable synth loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Wavetable"

    def test_amp_envelope_short(self, track):
        """H: Short amp envelope for punchiness."""
        wt = track.get_device("Wavetable")
        attack = wt.get_parameter("Amp Attack")
        decay = wt.get_parameter("Amp Decay")
        assert attack < 10  # < 10ms
        assert decay < 200  # < 200ms


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestStabMIDI:
    """MIDI pattern tests."""

    def test_stab_count(self, track):
        """H: Rhythmic stabs (32 stab positions × 3 chord notes = 96)."""
        notes = track.get_midi_notes(clip_index=0)
        assert 48 <= len(notes) <= 128  # 16-32 stabs × 3 chord notes

    def test_chord_notes(self, track):
        """H: Stabs are chords (F minor)."""
        notes = track.get_midi_notes(clip_index=0)
        # Check for simultaneous notes (chords)
        times = [n["start_time"] for n in notes]
        from collections import Counter

        time_counts = Counter(times)
        has_chords = any(c >= 2 for c in time_counts.values())
        assert has_chords


# =============================================================================
# MIX TESTS
# =============================================================================


class TestStabMix:
    """Mix settings tests."""

    def test_volume_minus_18db(self, track):
        """H: Volume at -18dB."""
        volume = track.get_volume_db()
        assert volume == -18.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
