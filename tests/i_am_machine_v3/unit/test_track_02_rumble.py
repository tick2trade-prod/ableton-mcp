"""
TDD Tests for Track 02: Rumble

Spec Reference: Section 3, Track 2 - The Industrial Rumble
Critical: Roar multiband + infinite sidechain to kick
"""

import pytest
from live_set.lily_palmer.i_am_machine_v3.tracks.low_end.rumble_track import RumbleTrack


@pytest.fixture
def mcp_client():
    """Mock MCP client."""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def rumble_track(mcp_client):
    """Create rumble track."""
    track = RumbleTrack(mcp_client, track_index=1)
    track.create()
    return track


# =============================================================================
# SIGNAL ROUTING TESTS
# =============================================================================


class TestRumbleSignalRouting:
    """Signal routing tests."""

    def test_receives_from_kick(self, rumble_track):
        """H: Audio input from Track 1 (Kick)."""
        input_source = rumble_track.get_audio_input()
        assert input_source == "Track 1 - Kick"

    def test_receives_post_fx(self, rumble_track):
        """H: Receives Post FX from kick."""
        mode = rumble_track.get_input_mode()
        assert mode == "Post FX"


# =============================================================================
# HYBRID REVERB TESTS
# =============================================================================


class TestRumbleHybridReverb:
    """Hybrid Reverb tests."""

    def test_hybrid_reverb_loaded(self, rumble_track):
        """H: Hybrid Reverb first in chain."""
        effects = rumble_track.get_effects_chain()
        assert effects[0]["name"] == "Hybrid Reverb"

    def test_convolution_engine(self, rumble_track):
        """H: Convolution engine used."""
        reverb = rumble_track.get_device("Hybrid Reverb")
        assert reverb.get_parameter("Engine") == "Convolution"

    def test_dark_hall_ir(self, rumble_track):
        """H: Dark Hall impulse response."""
        reverb = rumble_track.get_device("Hybrid Reverb")
        assert reverb.get_parameter("IR") == "Dark Hall"

    def test_decay_1_2_seconds(self, rumble_track):
        """H: Decay 1.2s."""
        reverb = rumble_track.get_device("Hybrid Reverb")
        assert reverb.get_parameter("Decay") == 1.2

    def test_predelay_10ms(self, rumble_track):
        """H: Pre-delay 10ms."""
        reverb = rumble_track.get_device("Hybrid Reverb")
        assert reverb.get_parameter("Pre-delay") == 0.01

    def test_mix_100_wet(self, rumble_track):
        """H: Mix 100% wet."""
        reverb = rumble_track.get_device("Hybrid Reverb")
        assert reverb.get_parameter("Mix") == 1.0


# =============================================================================
# ROAR MULTIBAND SATURATION TESTS (CRITICAL!)
# =============================================================================


class TestRumbleRoarSaturation:
    """Roar multiband saturation tests."""

    def test_roar_loaded(self, rumble_track):
        """H: Roar device loaded."""
        effects = rumble_track.get_effects_chain()
        assert "Roar" in [e["name"] for e in effects]

    def test_roar_low_band_tube(self, rumble_track):
        """H: Low band (<150Hz) uses Tube saturation."""
        roar = rumble_track.get_device("Roar")
        assert roar.get_band_saturation("low") == "Tube"

    def test_roar_mid_band_diode(self, rumble_track):
        """H: Mid band (150Hz-1kHz) uses Diode clipping."""
        roar = rumble_track.get_device("Roar")
        assert roar.get_band_saturation("mid") == "Diode"

    def test_roar_feedback_15_percent(self, rumble_track):
        """H: Feedback 15% for metallic texture."""
        roar = rumble_track.get_device("Roar")
        assert roar.get_parameter("Feedback") == 0.15


# =============================================================================
# LOWPASS FILTER TESTS
# =============================================================================


class TestRumbleLowpass:
    """Lowpass filter tests."""

    def test_eq_eight_lowpass(self, rumble_track):
        """H: EQ Eight for lowpass."""
        effects = rumble_track.get_effects_chain()
        assert "EQ Eight" in [e["name"] for e in effects]

    def test_lowpass_150hz(self, rumble_track):
        """H: Lowpass @ 150Hz."""
        eq = rumble_track.get_device("EQ Eight")
        lp = eq.get_lowpass()
        assert lp["frequency"] == 150


# =============================================================================
# SIDECHAIN COMPRESSION TESTS (CRITICAL!)
# =============================================================================


class TestRumbleSidechain:
    """Sidechain compression tests."""

    def test_compressor_loaded(self, rumble_track):
        """H: Compressor loaded."""
        effects = rumble_track.get_effects_chain()
        assert "Compressor" in [e["name"] for e in effects]

    def test_sidechain_source_kick(self, rumble_track):
        """H: Sidechain source is Track 1 (Kick)."""
        comp = rumble_track.get_device("Compressor")
        source = comp.get_sidechain_source()
        assert source == "Track 1 - Kick"

    def test_sidechain_ratio_infinite(self, rumble_track):
        """H: Infinite ratio for complete ducking."""
        comp = rumble_track.get_device("Compressor")
        ratio = comp.get_parameter("Ratio")
        assert ratio == float("inf")

    def test_sidechain_attack_0_1ms(self, rumble_track):
        """H: Attack 0.1ms for instant ducking."""
        comp = rumble_track.get_device("Compressor")
        attack = comp.get_parameter("Attack")
        assert attack == 0.1

    def test_sidechain_release_synced(self, rumble_track):
        """H: Release synced to tempo."""
        comp = rumble_track.get_device("Compressor")
        release_mode = comp.get_parameter("Release Mode")
        assert release_mode == "Sync"

    def test_sidechain_release_1_8th(self, rumble_track):
        """H: Release time 1/8 note."""
        comp = rumble_track.get_device("Compressor")
        release = comp.get_parameter("Release Time")
        assert release == "1/8"


# =============================================================================
# MIX TESTS
# =============================================================================


class TestRumbleMix:
    """Mix settings tests."""

    def test_volume_minus_12db(self, rumble_track):
        """H: Volume -12dB."""
        volume = rumble_track.get_volume_db()
        assert volume == -12.0

    def test_contains_below_150hz(self, rumble_track):
        """H: Rumble contained below 150Hz."""
        spectrum = rumble_track.analyze_spectrum()
        energy_above_150 = spectrum.get_energy(range=(150, 20000))
        assert energy_above_150 < 0.1  # Minimal energy above 150Hz
