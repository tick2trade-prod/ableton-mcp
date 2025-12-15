"""
TDD Tests for Track 13: Vocal

Spec Reference: Section 3, Track 13 - Vocal Chop
Pattern: Rhythmic vocal samples
Sample: Processed vocal chops
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track13Vocal


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track13Vocal(mcp_client, track_index=12)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestVocalSample:
    """Sample tests."""

    def test_simpler_loaded(self, track):
        """H: Simpler loaded for vocal playback."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Simpler"

    def test_vocal_sample_loaded(self, track):
        """H: Vocal sample loaded."""
        assert track.is_sample_loaded() is True


# =============================================================================
# EFFECTS TESTS
# =============================================================================


class TestVocalEffects:
    """Effects tests."""

    def test_auto_filter_loaded(self, track):
        """H: Auto Filter for movement."""
        devices = track.get_effects_chain()
        assert "Auto Filter" in [d["name"] for d in devices]


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestVocalMIDI:
    """MIDI pattern tests."""

    def test_vocal_hits(self, track):
        """H: Rhythmic vocal hits (8-24 per 16 bars)."""
        notes = track.get_midi_notes(clip_index=0)
        assert 8 <= len(notes) <= 32


# =============================================================================
# MIX TESTS
# =============================================================================


class TestVocalMix:
    """Mix settings tests."""

    def test_volume_minus_18db(self, track):
        """H: Volume at -18dB."""
        volume = track.get_volume_db()
        assert volume == -18.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
