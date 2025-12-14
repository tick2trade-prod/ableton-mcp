"""Tests for DearPyGUI controller agents."""

import pytest


class TestConfig:
    """Test configuration module."""

    def test_tracks_count(self):
        """Verify 16 tracks defined."""
        from dearpygui_controller.config import TRACKS

        assert len(TRACKS) == 16

    def test_track_indices(self):
        """Verify track indices are 0-15."""
        from dearpygui_controller.config import TRACKS

        indices = [t.index for t in TRACKS]
        assert indices == list(range(16))

    def test_track_names(self):
        """Verify track names follow convention."""
        from dearpygui_controller.config import TRACKS

        for track in TRACKS:
            assert track.name.startswith(f"{track.index + 1:02d}-")

    def test_config_singleton(self):
        """Verify config singleton works."""
        from dearpygui_controller.config import get_config, reset_config

        reset_config()
        c1 = get_config()
        c2 = get_config()
        assert c1 is c2

    def test_config_defaults(self):
        """Verify config defaults."""
        from dearpygui_controller.config import ControllerConfig

        config = ControllerConfig()
        assert config.tempo == 136.0
        assert config.key == "F"
        assert config.scale == "minor"
        assert config.track_count == 16


class TestComposerAgent:
    """Test composer agent pattern generation."""

    def test_kick_pattern_length(self):
        """Verify kick pattern has correct note count."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        notes = agent.generate_kick_pattern(bars=4)
        assert len(notes) == 16  # 4 bars * 4 beats

    def test_kick_pattern_pitch(self):
        """Verify all kick notes are C1 (MIDI 36)."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        notes = agent.generate_kick_pattern(bars=4)
        assert all(n["pitch"] == 36 for n in notes)

    def test_kick_pattern_timing(self):
        """Verify kick notes are on beats."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        notes = agent.generate_kick_pattern(bars=2)
        starts = [n["start_time"] for n in notes]
        expected = [0, 1, 2, 3, 4, 5, 6, 7]
        assert starts == expected

    def test_hihat_pattern_16ths(self):
        """Verify closed hi-hat pattern is 16th notes."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        notes = agent.generate_hihat_pattern(bars=1, open_hat=False)
        assert len(notes) == 16  # 16 16ths per bar

    def test_hihat_open_pattern(self):
        """Verify open hi-hat pattern is off-beat."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        notes = agent.generate_hihat_pattern(bars=1, open_hat=True)
        # Off-beat: every 2nd 8th note = positions 2, 6, 10, 14
        assert len(notes) == 4

    def test_clap_pattern(self):
        """Verify clap on beats 2 and 4."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        notes = agent.generate_clap_pattern(bars=2)
        assert len(notes) == 4  # 2 bars * 2 claps
        starts = [n["start_time"] for n in notes]
        assert starts == [1, 3, 5, 7]

    def test_bass_pattern_scale(self):
        """Verify bass uses F Minor notes."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        notes = agent.generate_bass_pattern(bars=1)
        pitches = set(n["pitch"] for n in notes)
        f_minor = {29, 32, 34, 36, 39}  # F1, Ab1, Bb1, C2, Eb2
        assert pitches.issubset(f_minor)

    def test_get_pattern_for_track(self):
        """Verify pattern selection by track type."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent
        from dearpygui_controller.config import TRACKS

        agent = ComposerAgent(verbose=False)

        # Kick track
        kick = TRACKS[0]
        pattern = agent.get_pattern_for_track(kick, bars=1)
        assert len(pattern) == 4  # 4-on-floor

        # Hi-hat track
        hihat = TRACKS[4]  # 05-ClosedHats
        pattern = agent.get_pattern_for_track(hihat, bars=1)
        assert len(pattern) == 16  # 16th notes


class TestMixerAgent:
    """Test mixer agent device chains."""

    def test_kick_chain(self):
        """Verify kick device chain."""
        from dearpygui_controller.agents.mixer_agent import MixerAgent
        from dearpygui_controller.config import TRACKS

        agent = MixerAgent(verbose=False)
        chain = agent.get_chain_for_track(TRACKS[0])
        names = [d["name"] for d in chain]
        assert "Drum Sampler" in names or "Saturator" in names

    def test_rumble_chain(self):
        """Verify rumble device chain has Reverb."""
        from dearpygui_controller.agents.mixer_agent import MixerAgent
        from dearpygui_controller.config import TRACKS

        agent = MixerAgent(verbose=False)
        chain = agent.get_chain_for_track(TRACKS[1])
        names = [d["name"] for d in chain]
        assert "Reverb" in names
        assert "Compressor" in names

    def test_volume_levels(self):
        """Verify volume levels for different tracks."""
        from dearpygui_controller.agents.mixer_agent import MixerAgent
        from dearpygui_controller.config import TRACKS

        agent = MixerAgent(verbose=False)

        kick_vol = agent.get_volume_for_track(TRACKS[0])
        rumble_vol = agent.get_volume_for_track(TRACKS[1])

        assert kick_vol > rumble_vol  # Kick should be louder


class TestVerifierAgent:
    """Test verifier agent checks."""

    @pytest.mark.asyncio
    async def test_format_report(self):
        """Verify report formatting."""
        from dearpygui_controller.agents.verifier_agent import (
            VerificationResult,
            VerifierAgent,
        )

        agent = VerifierAgent(verbose=False)
        results = [
            VerificationResult("TEST_1", True, "Passed"),
            VerificationResult("TEST_2", False, "Failed"),
        ]

        report = agent.format_report(results)
        assert "TEST_1" in report
        assert "TEST_2" in report
        assert "1/2" in report
        assert "50%" in report

    @pytest.mark.asyncio
    async def test_execute_returns_results(self):
        """Verify execute returns results."""
        from dearpygui_controller.agents.verifier_agent import VerifierAgent

        agent = VerifierAgent(verbose=False)
        result = await agent.execute()

        assert "results" in result.data
        assert "report" in result.data
        assert len(result.data["results"]) == 7  # 7 checks


class TestBaseAgent:
    """Test base agent functionality."""

    def test_log_callback(self):
        """Verify log callback is called."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        logs = []
        agent = ComposerAgent(verbose=True)
        agent.set_log_callback(lambda msg: logs.append(msg))
        agent.log("Test message")

        assert any("Test message" in log for log in logs)

    def test_progress_callback(self):
        """Verify progress callback is called."""
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        progress_updates = []
        agent = ComposerAgent(verbose=False)
        agent.set_progress_callback(
            lambda idx, prog: progress_updates.append((idx, prog))
        )
        agent.update_progress(0, 0.5)

        assert (0, 0.5) in progress_updates


class TestLogPanel:
    """Test log panel functionality."""

    def test_log_buffer(self):
        """Verify log buffer works."""
        from dearpygui_controller.layouts.log_panel import (
            clear_log,
            get_log_buffer,
            log_message,
        )

        clear_log()
        log_message("Test 1")
        log_message("Test 2")

        buffer = get_log_buffer()
        assert len(buffer) == 2
        assert any("Test 1" in msg for msg in buffer)


class TestArrangerAgent:
    """Test arranger agent functionality."""

    @pytest.mark.asyncio
    async def test_execute_structure(self):
        """Verify execute accepts structure."""
        from dearpygui_controller.agents.arranger_agent import ArrangerAgent

        agent = ArrangerAgent(verbose=False)
        result = await agent.execute(structure="techno_basic")

        assert result.success
        assert "techno_basic" in result.message


class TestSoundDesignAgent:
    """Test sound design agent functionality."""

    @pytest.mark.asyncio
    async def test_execute_runs(self):
        """Verify execute runs successfuly."""
        from dearpygui_controller.agents.sound_design_agent import SoundDesignAgent

        agent = SoundDesignAgent(verbose=False)
        result = await agent.execute()

        assert result.success
        assert "Configured" in result.message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
