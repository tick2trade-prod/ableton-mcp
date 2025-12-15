"""
TDD Tests for Track 16: Impact

Spec Reference: Section 3, Track 16 - Impact Hit
Pattern: Single impact at bar 1 beat 1
Sample: Impact/crash sample
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track16Impact


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track16Impact(mcp_client, track_index=15)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestImpactSample:
    """Sample tests."""

    def test_simpler_loaded(self, track):
        """H: Simpler loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Simpler"

    def test_impact_sample(self, track):
        """H: Impact sample loaded."""
        sample_name = track.get_sample_name()
        assert "Impact" in sample_name or "Crash" in sample_name


# =============================================================================
# EFFECTS TESTS
# =============================================================================


class TestImpactEffects:
    """Effects tests."""

    def test_reverb_loaded(self, track):
        """H: Reverb for decay."""
        devices = track.get_effects_chain()
        assert "Reverb" in [d["name"] for d in devices]


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestImpactMIDI:
    """MIDI pattern tests."""

    def test_single_hit(self, track):
        """H: Single impact hit."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) == 1

    def test_hit_on_downbeat(self, track):
        """H: Hit on beat 1."""
        notes = track.get_midi_notes(clip_index=0)
        assert notes[0]["start_time"] == 0.0

    def test_full_velocity(self, track):
        """H: Full velocity for maximum impact."""
        notes = track.get_midi_notes(clip_index=0)
        assert notes[0]["velocity"] == 127


# =============================================================================
# MIX TESTS
# =============================================================================


class TestImpactMix:
    """Mix settings tests."""

    def test_volume_minus_12db(self, track):
        """H: Volume at -12dB (prominent)."""
        volume = track.get_volume_db()
        assert volume == -12.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
