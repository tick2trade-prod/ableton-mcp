"""
TDD Tests for Track 04: Acid

Spec Reference: Section 3, Track 4 - 303-Style Acid Line
Key: F minor, squelchy acid bassline
Synth: Drift (or Wavetable with acid preset)
"""

import pytest

from live_set.lily_palmer.i_am_machine_v3.tracks import Track04Acid


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def track(mcp_client):
    """Create track instance."""
    t = Track04Acid(mcp_client, track_index=3)
    t.create()
    return t


# =============================================================================
# SOUND DESIGN TESTS
# =============================================================================


class TestAcidSynthesis:
    """Acid synth tests."""

    def test_drift_loaded(self, track):
        """H: Drift synth loaded."""
        devices = track.get_effects_chain()
        assert devices[0]["name"] == "Drift"

    def test_saw_waveform(self, track):
        """H: Saw waveform (classic acid)."""
        drift = track.get_device("Drift")
        assert drift.get_parameter("Osc 1 Shape") == "Saw"

    def test_filter_lowpass(self, track):
        """H: Low-pass filter enabled."""
        drift = track.get_device("Drift")
        assert drift.get_parameter("Filter Type") == "Low-pass"

    def test_filter_resonance_high(self, track):
        """H: High resonance for squelch."""
        drift = track.get_device("Drift")
        reso = drift.get_parameter("Filter Resonance")
        assert reso >= 0.7  # 70%+ resonance

    def test_filter_env_decay(self, track):
        """H: Filter envelope with decay."""
        drift = track.get_device("Drift")
        decay = drift.get_parameter("Filter Env Decay")
        assert 100 <= decay <= 400  # ms


# =============================================================================
# EFFECTS CHAIN TESTS
# =============================================================================


class TestAcidEffects:
    """Effects chain tests."""

    def test_overdrive_loaded(self, track):
        """H: Overdrive for grit."""
        devices = track.get_effects_chain()
        assert "Overdrive" in [d["name"] for d in devices]

    def test_delay_loaded(self, track):
        """H: Delay for space."""
        devices = track.get_effects_chain()
        assert "Delay" in [d["name"] for d in devices]

    def test_delay_sync(self, track):
        """H: Delay synced to tempo."""
        delay = track.get_device("Delay")
        assert delay.get_parameter("Sync") is True


# =============================================================================
# MIDI PATTERN TESTS
# =============================================================================


class TestAcidMIDI:
    """MIDI pattern tests."""

    def test_note_count(self, track):
        """H: 16-bar acid pattern with slides."""
        notes = track.get_midi_notes(clip_index=0)
        assert len(notes) >= 64  # At least 1 note per beat

    def test_f_minor_scale(self, track):
        """H: Notes in F minor scale."""
        f_minor = {41, 43, 44, 46, 48, 49, 51, 53}  # F1 and octave
        notes = track.get_midi_notes(clip_index=0)
        pitches = {(n["pitch"] % 12 + 41) % 12 + 41 for n in notes}
        # At least 80% in scale
        in_scale = sum(
            1
            for n in notes
            if n["pitch"] % 12 + 41 in f_minor
            or (n["pitch"] % 12) in {5, 7, 8, 10, 0, 1, 3}
        )
        assert in_scale >= len(notes) * 0.8


# =============================================================================
# MIX TESTS
# =============================================================================


class TestAcidMix:
    """Mix settings tests."""

    def test_volume_minus_18db(self, track):
        """H: Volume at -18dB (background element)."""
        volume = track.get_volume_db()
        assert volume == -18.0

    def test_output_main(self, track):
        """H: Output routed to Main."""
        output = track.get_output_routing()
        assert output == "Main"
