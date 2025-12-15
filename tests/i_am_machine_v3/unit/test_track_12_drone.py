"""
TDD Tests for Track 12: Drone

Spec Reference: Section 3, Track 12 - Atmospheric Drone
Pattern: Sustained pad/drone
Synth: Wavetable (evolving pad)
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track12Drone


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track12Drone(mcp_client, track_index=11)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestDroneSynth:
    """Synth tests."""

    def test_wavetable_loaded(self, track):
        """H: Wavetable synth loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Wavetable"

    def test_long_attack(self, track):
        """H: Long attack for evolving texture."""
        wt = track.get_device("Wavetable")
        attack = wt.get_parameter("Amp Attack")
        assert attack >= 500  # >= 500ms


# =============================================================================
# EFFECTS TESTS
# =============================================================================


class TestDroneEffects:
    """Effects tests."""

    def test_reverb_loaded(self, track):
        """H: Reverb for space."""
        devices = track.get_effects_chain()
        assert "Reverb" in [d["name"] for d in devices]

    def test_long_reverb(self, track):
        """H: Long reverb decay (3+ seconds)."""
        reverb = track.get_device("Reverb")
        decay = reverb.get_parameter("Decay")
        assert decay >= 3.0


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestDroneMIDI:
    """MIDI pattern tests."""

    def test_sustained_note(self, track):
        """H: Long sustained notes (1-4 per 16 bars)."""
        notes = track.get_midi_notes(clip_index=0)
        assert 1 <= len(notes) <= 8

    def test_long_duration(self, track):
        """H: Notes are long (4+ bars each)."""
        notes = track.get_midi_notes(clip_index=0)
        for note in notes:
            assert note["duration"] >= 16  # 4 bars = 16 beats


# =============================================================================
# MIX TESTS
# =============================================================================


class TestDroneMix:
    """Mix settings tests."""

    def test_volume_minus_24db(self, track):
        """H: Volume at -24dB (background)."""
        volume = track.get_volume_db()
        assert volume == -24.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
