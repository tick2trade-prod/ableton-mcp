"""Tests for newly implemented specialized agents."""

import pytest


class TestSynthesizerAgent:
    """Test SynthesizerAgent synth programming."""

    def test_fm_bass_config(self):
        """Verify FM bass configuration."""
        from dearpygui_controller.agents.synthesizer_agent import SynthesizerAgent

        agent = SynthesizerAgent(verbose=False)
        config = agent.get_fm_bass_config()

        assert config["device"] == "Operator"
        assert "params" in config
        assert config["params"]["algorithm"] == 1

    def test_acid_config(self):
        """Verify acid line configuration."""
        from dearpygui_controller.agents.synthesizer_agent import SynthesizerAgent

        agent = SynthesizerAgent(verbose=False)
        config = agent.get_acid_config()

        assert config["device"] == "Drift"
        assert config["fallback"] == "Operator"
        assert config["params"]["filter_resonance"] >= 0.6  # High resonance

    def test_synth_stab_config(self):
        """Verify synth stab configuration."""
        from dearpygui_controller.agents.synthesizer_agent import SynthesizerAgent

        agent = SynthesizerAgent(verbose=False)
        config = agent.get_synth_stab_config()

        assert config["device"] == "Wavetable"
        assert "osc_1_wavetable" in config["params"]

    def test_drone_config(self):
        """Verify drone configuration."""
        from dearpygui_controller.agents.synthesizer_agent import SynthesizerAgent

        agent = SynthesizerAgent(verbose=False)
        config = agent.get_drone_config()

        assert config["device"] == "Meld"
        assert config["fallback"] == "Operator"
        assert config["params"]["scale_aware"] is True
        assert config["params"]["scale_root"] == "F"

    @pytest.mark.asyncio
    async def test_execute_all_synths(self):
        """Verify execute processes all synth tracks."""
        from dearpygui_controller.agents.synthesizer_agent import SynthesizerAgent

        agent = SynthesizerAgent(verbose=False)
        result = await agent.execute()

        assert result.success
        assert "synths" in result.data
        assert len(result.data["synths"]) == 4  # 4 synth tracks


class TestPercussionAgent:
    """Test PercussionAgent pattern generation."""

    def test_tom_pattern_syncopation(self):
        """Verify tom pattern has syncopation."""
        from dearpygui_controller.agents.percussion_agent import PercussionAgent

        agent = PercussionAgent(verbose=False)
        notes = agent.generate_tom_pattern(bars=1)

        # Should have sparse hits (not all 16ths)
        assert len(notes) < 16

    def test_glitch_pattern_randomness(self):
        """Verify glitch pattern has randomness."""
        from dearpygui_controller.agents.percussion_agent import PercussionAgent

        agent = PercussionAgent(verbose=False)

        # Generate two patterns
        notes1 = agent.generate_glitch_pattern(bars=1)
        notes2 = agent.generate_glitch_pattern(bars=1)

        # Should have variable hit counts (4-8 per bar)
        assert 4 <= len(notes1) <= 8
        assert 4 <= len(notes2) <= 8

        # Patterns should be sorted by time
        for i in range(len(notes1) - 1):
            assert notes1[i]["start_time"] <= notes1[i + 1]["start_time"]

    def test_ride_pattern_continuous(self):
        """Verify ride pattern is continuous 8th notes."""
        from dearpygui_controller.agents.percussion_agent import PercussionAgent

        agent = PercussionAgent(verbose=False)
        notes = agent.generate_ride_pattern(bars=1)

        assert len(notes) == 8  # 8 eighth notes per bar

        # Check timing (every 0.5 beats)
        for i, note in enumerate(notes):
            assert note["start_time"] == i * 0.5

    def test_get_pattern_for_track(self):
        """Verify pattern selection by track name."""
        from dearpygui_controller.agents.percussion_agent import PercussionAgent
        from dearpygui_controller.config import TRACKS

        agent = PercussionAgent(verbose=False)

        # Tom track
        tom = TRACKS[7]  # 08-LowTom
        pattern = agent.get_pattern_for_track(tom, bars=1)
        assert len(pattern) > 0

        # Ride track
        ride = TRACKS[9]  # 10-Ride
        pattern = agent.get_pattern_for_track(ride, bars=1)
        assert len(pattern) == 8

    @pytest.mark.asyncio
    async def test_execute_all_percussion(self):
        """Verify execute processes all percussion tracks."""
        from dearpygui_controller.agents.percussion_agent import PercussionAgent

        agent = PercussionAgent(verbose=False)
        result = await agent.execute()

        assert result.success
        assert "patterns" in result.data
        assert len(result.data["patterns"]) == 3  # 3 percussion tracks


class TestVocalsAgent:
    """Test VocalsAgent vocal processing."""

    def test_main_vocal_chain(self):
        """Verify main vocal processing chain."""
        from dearpygui_controller.agents.vocals_agent import VocalsAgent

        agent = VocalsAgent(verbose=False)
        chain = agent.get_main_vocal_chain()

        device_names = [d["name"] for d in chain]
        assert "Gate" in device_names
        assert "Compressor" in device_names
        assert "Channel EQ" in device_names
        assert "Vocoder" in device_names

    def test_vocal_fx_chain(self):
        """Verify vocal FX chain."""
        from dearpygui_controller.agents.vocals_agent import VocalsAgent

        agent = VocalsAgent(verbose=False)
        chain = agent.get_vocal_fx_chain()

        device_names = [d["name"] for d in chain]
        assert "Simpler" in device_names or "Granulator III" in device_names
        assert "Reverb" in device_names
        assert "Frequency Shifter" in device_names

    @pytest.mark.asyncio
    async def test_execute_all_vocals(self):
        """Verify execute processes all vocal tracks."""
        from dearpygui_controller.agents.vocals_agent import VocalsAgent

        agent = VocalsAgent(verbose=False)
        result = await agent.execute()

        assert result.success
        assert "vocals" in result.data
        assert len(result.data["vocals"]) == 2  # 2 vocal tracks


class TestTransitionAgent:
    """Test TransitionAgent for risers and impacts."""

    def test_riser_config(self):
        """Verify riser configuration."""
        from dearpygui_controller.agents.transition_agent import TransitionAgent

        agent = TransitionAgent(verbose=False)
        config = agent.get_riser_config()

        assert "devices" in config
        assert "automation" in config

        device_names = [d["name"] for d in config["devices"]]
        assert "Auto Filter" in device_names
        assert "Compressor" in device_names

    def test_impact_config(self):
        """Verify impact configuration."""
        from dearpygui_controller.agents.transition_agent import TransitionAgent

        agent = TransitionAgent(verbose=False)
        config = agent.get_impact_config()

        device_names = [d["name"] for d in config["devices"]]
        assert "Drum Sampler" in device_names
        assert "Reverb" in device_names
        assert "Echo" in device_names

    def test_riser_clip(self):
        """Verify riser clip is sustained note."""
        from dearpygui_controller.agents.transition_agent import TransitionAgent

        agent = TransitionAgent(verbose=False)
        clip = agent.generate_riser_clip(bars=16)

        assert len(clip["notes"]) == 1  # Single sustained note
        assert clip["notes"][0]["duration"] == 64.0  # 16 bars = 64 beats

    def test_impact_clip(self):
        """Verify impact clip is single hit."""
        from dearpygui_controller.agents.transition_agent import TransitionAgent

        agent = TransitionAgent(verbose=False)
        clip = agent.generate_impact_clip()

        assert len(clip["notes"]) == 1  # Single hit
        assert clip["notes"][0]["velocity"] == 127  # Maximum velocity

    @pytest.mark.asyncio
    async def test_execute_all_transitions(self):
        """Verify execute processes all transition tracks."""
        from dearpygui_controller.agents.transition_agent import TransitionAgent

        agent = TransitionAgent(verbose=False)
        result = await agent.execute()

        assert result.success
        assert "transitions" in result.data
        assert len(result.data["transitions"]) == 2  # 2 transition tracks


class TestModulationAgent:
    """Test ModulationAgent for automation."""

    def test_acid_modulation(self):
        """Verify acid modulation configuration."""
        from dearpygui_controller.agents.modulation_agent import ModulationAgent

        agent = ModulationAgent(verbose=False)
        mods = agent.get_acid_modulation()

        assert len(mods) > 0
        assert any(m["type"] == "automation" for m in mods)

    def test_stab_modulation(self):
        """Verify stab modulation configuration."""
        from dearpygui_controller.agents.modulation_agent import ModulationAgent

        agent = ModulationAgent(verbose=False)
        mods = agent.get_stab_modulation()

        assert len(mods) > 0
        # Should automate filter cutoff
        assert any("Filter Cutoff" in m.get("parameter", "") for m in mods)

    def test_rumble_modulation(self):
        """Verify rumble modulation configuration."""
        from dearpygui_controller.agents.modulation_agent import ModulationAgent

        agent = ModulationAgent(verbose=False)
        mods = agent.get_rumble_modulation()

        assert len(mods) > 0
        # Should modulate Roar parameters
        assert any("Roar" in m.get("device", "") for m in mods)

    @pytest.mark.asyncio
    async def test_execute_modulation(self):
        """Verify execute applies modulation."""
        from dearpygui_controller.agents.modulation_agent import ModulationAgent

        agent = ModulationAgent(verbose=False)
        result = await agent.execute()

        assert result.success
        assert "modulations" in result.data


class TestEffectsChainAgent:
    """Test EffectsChainAgent for signal processing."""

    def test_sidechain_targets(self):
        """Verify sidechain compression targets."""
        from dearpygui_controller.agents.effects_chain_agent import EffectsChainAgent

        agent = EffectsChainAgent(verbose=False)
        targets = agent.get_sidechain_targets()

        assert len(targets) > 0
        # Should include rumble and bass
        track_indices = [t["track_index"] for t in targets]
        assert 1 in track_indices  # Rumble
        assert 2 in track_indices  # Rolling Bass

    def test_return_tracks(self):
        """Verify return track configurations."""
        from dearpygui_controller.agents.effects_chain_agent import EffectsChainAgent

        agent = EffectsChainAgent(verbose=False)
        returns = agent.get_return_tracks()

        assert len(returns) > 0
        names = [r["name"] for r in returns]
        assert any("Reverb" in n for n in names)

    def test_bass_mono_config(self):
        """Verify bass mono configuration."""
        from dearpygui_controller.agents.effects_chain_agent import EffectsChainAgent

        agent = EffectsChainAgent(verbose=False)
        configs = agent.get_bass_mono_config()

        assert len(configs) > 0
        # Should include kick, rumble, bass
        track_indices = [c["track_index"] for c in configs]
        assert 0 in track_indices  # Kick
        assert 1 in track_indices  # Rumble

        # Check cutoff frequencies are reasonable
        for config in configs:
            assert 100 <= config["cutoff"] <= 200

    @pytest.mark.asyncio
    async def test_execute_sidechain_mode(self):
        """Verify execute in sidechain mode."""
        from dearpygui_controller.agents.effects_chain_agent import EffectsChainAgent

        agent = EffectsChainAgent(verbose=False)
        result = await agent.execute(mode="sidechain")

        assert result.success
        assert "configurations" in result.data

    @pytest.mark.asyncio
    async def test_execute_bass_mono_mode(self):
        """Verify execute in bass mono mode."""
        from dearpygui_controller.agents.effects_chain_agent import EffectsChainAgent

        agent = EffectsChainAgent(verbose=False)
        result = await agent.execute(mode="bass_mono")

        assert result.success
        assert "configurations" in result.data


class TestArrangementAgent:
    """Test ArrangementAgent for timeline structure."""

    def test_arrangement_structure(self):
        """Verify arrangement structure."""
        from dearpygui_controller.agents.arrangement_agent import ArrangementAgent

        agent = ArrangementAgent(verbose=False)
        structure = agent.get_arrangement_structure()

        assert structure["bpm"] == 136
        assert structure["total_bars"] > 0
        assert len(structure["sections"]) == 7  # 7 sections

    def test_section_names(self):
        """Verify section names."""
        from dearpygui_controller.agents.arrangement_agent import ArrangementAgent

        agent = ArrangementAgent(verbose=False)
        structure = agent.get_arrangement_structure()

        section_names = [s["name"] for s in structure["sections"]]
        assert "Intro" in section_names
        assert "Development" in section_names
        assert "Drop 1" in section_names
        assert "Main Drop" in section_names
        assert "Outro" in section_names

    def test_section_energy_levels(self):
        """Verify section energy levels."""
        from dearpygui_controller.agents.arrangement_agent import ArrangementAgent

        agent = ArrangementAgent(verbose=False)
        structure = agent.get_arrangement_structure()

        # Check energy progression
        for section in structure["sections"]:
            assert "energy" in section
            assert section["energy"] in [
                "contained",
                "building",
                "tension",
                "peak",
                "minimal",
                "maximum",
                "outro",
            ]

    def test_track_activation(self):
        """Verify track activation per section."""
        from dearpygui_controller.agents.arrangement_agent import ArrangementAgent

        agent = ArrangementAgent(verbose=False)
        structure = agent.get_arrangement_structure()

        for section in structure["sections"]:
            assert "active_tracks" in section
            assert len(section["active_tracks"]) > 0

            # Intro should be minimal (kick, rumble, hats)
            if section["name"] == "Intro":
                assert len(section["active_tracks"]) <= 3

            # Main drop should have all tracks
            if section["name"] == "Main Drop":
                assert len(section["active_tracks"]) == 16

    @pytest.mark.asyncio
    async def test_execute_markers_mode(self):
        """Verify execute in markers mode."""
        from dearpygui_controller.agents.arrangement_agent import ArrangementAgent

        agent = ArrangementAgent(verbose=False)
        result = await agent.execute(mode="markers")

        assert result.success
        assert "arrangement" in result.data
        assert "summary" in result.data


class TestMasteringAgent:
    """Test MasteringAgent for master bus processing."""

    def test_master_chain(self):
        """Verify master chain configuration."""
        from dearpygui_controller.agents.mastering_agent import MasteringAgent

        agent = MasteringAgent(verbose=False)
        chain = agent.get_master_chain()

        device_names = [d["name"] for d in chain]
        assert "Glue Compressor" in device_names
        assert "EQ Eight" in device_names
        assert "Limiter" in device_names

    def test_reference_targets(self):
        """Verify mastering reference targets."""
        from dearpygui_controller.agents.mastering_agent import MasteringAgent

        agent = MasteringAgent(verbose=False)
        targets = agent.get_reference_targets()

        assert "lufs" in targets
        assert "true_peak" in targets
        assert -10 <= targets["lufs"] <= -5  # Reasonable LUFS range
        assert targets["true_peak"] < 0  # Below 0dB

    def test_loudness_compliance(self):
        """Verify loudness compliance checking."""
        from dearpygui_controller.agents.mastering_agent import MasteringAgent

        agent = MasteringAgent(verbose=False)

        # Test with good values
        analysis = {"integrated_lufs": -7.0, "true_peak": -0.5}
        compliance = agent.check_loudness_compliance(analysis)

        assert "lufs_ok" in compliance
        assert "peak_ok" in compliance

    @pytest.mark.asyncio
    async def test_execute_analyze_only(self):
        """Verify execute in analyze mode."""
        from dearpygui_controller.agents.mastering_agent import MasteringAgent

        agent = MasteringAgent(verbose=False)
        result = await agent.execute(analyze_only=True)

        assert result.success
        assert "loudness_analysis" in result.data

    @pytest.mark.asyncio
    async def test_execute_full_mastering(self):
        """Verify full mastering execute."""
        from dearpygui_controller.agents.mastering_agent import MasteringAgent

        agent = MasteringAgent(verbose=False)
        result = await agent.execute(analyze_only=False)

        assert result.success
        assert "loudness_analysis" in result.data
        assert "compliance" in result.data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
