"""
TDD Tests for Track 14: Vocal FX

Spec Reference: Section 3, Track 14 - Vocal FX
Pattern: Processed vocal textures
Sample: Heavily processed vocals (delay/reverb)
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track14VocalFx


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track14VocalFx(mcp_client, track_index=13)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestVocalFxDevice:
    """Device tests."""

    def test_simpler_loaded(self, track):
        """H: Simpler for vocal playback."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Simpler"


# =============================================================================
# EFFECTS TESTS
# =============================================================================


class TestVocalFxEffects:
    """Effects tests."""

    def test_delay_loaded(self, track):
        """H: Delay for texture."""
        devices = track.get_effects_chain()
        assert "Delay" in [d["name"] for d in devices]

    def test_reverb_loaded(self, track):
        """H: Reverb for space."""
        devices = track.get_effects_chain()
        assert "Reverb" in [d["name"] for d in devices]

    def test_wet_mix(self, track):
        """H: High wet mix (70%+)."""
        reverb = track.get_device("Reverb")
        mix = reverb.get_parameter("Mix")
        assert mix >= 0.7


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestVocalFxMIDI:
    """MIDI pattern tests."""

    def test_sparse_hits(self, track):
        """H: Sparse vocal hits (4-16 per 16 bars)."""
        notes = track.get_midi_notes(clip_index=0)
        assert 4 <= len(notes) <= 16


# =============================================================================
# MIX TESTS
# =============================================================================


class TestVocalFxMix:
    """Mix settings tests."""

    def test_volume_minus_22db(self, track):
        """H: Volume at -22dB (background)."""
        volume = track.get_volume_db()
        assert volume == -22.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
