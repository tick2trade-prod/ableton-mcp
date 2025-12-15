"""
TDD Tests for Track 03: Sub Bass

Spec Reference: Section 3, Track 3 - FM Rolling Sub Bass
Key: F minor, 16th note rolling pattern
Synth: Operator (FM synthesis)
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track03SubBass


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track03SubBass(mcp_client, track_index=2)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestSubBassSynthesis:
    """Operator FM synthesis tests."""

    def test_operator_loaded(self, track):
        """H: Operator synth loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Operator"

    def test_fm_algorithm(self, track):
        """H: FM Algorithm 1 (2+3->1)."""
        op = track.get_device("Operator")
        assert op.get_parameter("Algorithm") == 1

    def test_carrier_sine(self, track):
        """H: Operator A = Sine (carrier)."""
        op = track.get_device("Operator")
        assert op.get_parameter("Osc A Wave") == "Sine"

    def test_modulator_sine(self, track):
        """H: Operator B = Sine (modulator)."""
        op = track.get_device("Operator")
        assert op.get_parameter("Osc B Wave") == "Sine"

    def test_modulator_ratio_2(self, track):
        """H: Modulator ratio 2:1 for FM."""
        op = track.get_device("Operator")
        assert op.get_parameter("Osc B Ratio") == 2.0


# =============================================================================
# EFFECTS CHAIN TESTS
# =============================================================================


class TestSubBassEffects:
    """Effects chain tests."""

    def test_saturator_loaded(self, track):
        """H: Saturator for warmth."""
        devices = track.get_effects_chain()
        assert "Saturator" in [d["name"] for d in devices]

    def test_saturator_soft_sine(self, track):
        """H: Soft Sine saturation."""
        sat = track.get_device("Saturator")
        assert sat.get_parameter("Type") == "Soft Sine"

    def test_utility_bass_mono(self, track):
        """H: Bass mono below 120Hz."""
        util = track.get_device("Utility")
        assert util.get_parameter("Bass Mono") is True


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestSubBassMIDI:
    """MIDI pattern tests."""

    def test_note_count(self, track):
        """H: Rolling 16th notes = 256 notes over 16 bars."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) == 256

    def test_root_note_f1(self, track):
        """H: Root note is F1 (MIDI 41)."""
        notes = track.get_midi_notes(clip_index=0)
        # At least half of notes should be root
        root_notes = [n for n in notes if n["pitch"] == 41]
        assert len(root_notes) >= 128

    def test_velocity_variation(self, track):
        """H: Velocity variation for groove."""
        notes = track.get_midi_notes(clip_index=0)
        velocities = {n["velocity"] for n in notes}
        assert len(velocities) >= 2  # Not all same velocity


# =============================================================================
# MIX TESTS
# =============================================================================


class TestSubBassMix:
    """Mix settings tests."""

    def test_volume_minus_15db(self, track):
        """H: Volume at -15dB (below kick)."""
        volume = track.get_volume_db()
        assert volume == -15.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
