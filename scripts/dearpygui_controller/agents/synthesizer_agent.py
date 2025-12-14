"""Synthesizer Agent for synthesizer device configuration.

Reference: Ableton Manual Section 30.13.2 "Oscillators" (page 742)
Reference: Ableton Manual Section 30.10.8 "The Filter/Global Tab" (page 715)
"""

from ..config import TRACKS, TrackConfig
from .base_agent import AgentResult, BaseAgent


class SynthesizerAgent(BaseAgent):
    """Agent for programming synthesizers with advanced parameters.

    Specializes in:
    - FM synthesis (Operator) for Rolling Bass and Acid lines
    - Wavetable synthesis for Stabs and Leads
    - Drift/Meld for atmospheric drones
    - Filter envelope programming
    - Modulation routing
    """

    def __init__(self, **kwargs):
        super().__init__(name="SynthesizerAgent", **kwargs)

    def get_role(self) -> str:
        return "Synthesis Specialist"

    def get_goal(self) -> str:
        return "Program synths with production-ready parameters for peak-time techno"

    def get_fm_bass_config(self) -> dict:
        """Get Operator config for FM Rolling Bass (Track 3)."""
        return {
            "device": "Operator",
            "params": {
                # Oscillator A (Carrier)
                "osc_a_wave": "Sine",
                "osc_a_level": 1.0,
                "osc_a_decay": 0.6,
                # Oscillator B (Modulator)
                "osc_b_wave": "Sine",
                "osc_b_coarse": 2.0,
                "osc_b_level": 0.7,
                # Algorithm
                "algorithm": 1,  # Vertical stack for series modulation
                # Filter
                "filter_type": "Low-pass 24dB",
                "filter_cutoff": 800,
                "filter_resonance": 0.3,
                "filter_env_amount": 0.4,
                "filter_decay": 0.3,
                # Envelope
                "amp_attack": 0.001,
                "amp_decay": 0.6,
                "amp_sustain": 0.0,
                "amp_release": 0.1,
            },
        }

    def get_acid_config(self) -> dict:
        """Get Drift/Operator config for 303 Acid Line (Track 4)."""
        return {
            "device": "Drift",
            "fallback": "Operator",
            "params": {
                # Oscillator
                "osc_wave": "Sawtooth",
                "drift_amount": 0.2,  # Pitch instability
                # Filter
                "filter_type": "Low-pass 18dB",
                "filter_cutoff": 400,
                "filter_resonance": 0.65,
                # Filter Envelope
                "filter_env_attack": 0.001,
                "filter_env_decay": 0.15,
                "filter_env_sustain": 0.0,
                "filter_env_amount": 0.8,
                # Amp Envelope
                "amp_attack": 0.001,
                "amp_decay": 0.3,
                "amp_sustain": 0.0,
                "amp_release": 0.05,
                # Glide
                "glide_time": 0.08,
                "glide_mode": "Legato",
            },
        }

    def get_synth_stab_config(self) -> dict:
        """Get Wavetable config for Synth Stabs (Track 11)."""
        return {
            "device": "Wavetable",
            "params": {
                # Oscillators
                "osc_1_wavetable": "Distortion",  # Complex harmonics
                "osc_1_position": 0.5,
                "osc_2_wavetable": "Vintage",
                "osc_2_position": 0.3,
                "osc_2_semitones": 7,  # Perfect 5th
                # Filter
                "filter_type": "Low-pass",
                "filter_cutoff": 1200,
                "filter_resonance": 0.2,
                "filter_env_amount": 0.6,
                # Filter Envelope
                "filter_env_attack": 0.01,
                "filter_env_decay": 0.15,
                "filter_env_sustain": 0.0,
                # Amp Envelope
                "amp_attack": 0.01,
                "amp_decay": 0.2,
                "amp_sustain": 0.0,
                "amp_release": 0.1,
                # Unison
                "unison_voices": 2,
                "unison_detune": 0.15,
            },
        }

    def get_drone_config(self) -> dict:
        """Get Meld/Operator config for Atmospheric Drone (Track 12)."""
        return {
            "device": "Meld",
            "fallback": "Operator",
            "params": {
                # Engine A - Sub-harmonic drone
                "engine_a_type": "Sine",
                "engine_a_octave": -1,
                "engine_a_level": 0.7,
                # Engine B - High sparkles/texture
                "engine_b_type": "Noise Loop",
                "engine_b_level": 0.3,
                # Modulation
                "lfo_1_rate": 0.01,  # Very slow (0.01 Hz)
                "lfo_1_waveform": "Random",
                "lfo_1_destination": "Filter Cutoff",
                "lfo_1_amount": 0.4,
                # Scale Awareness
                "scale_aware": True,
                "scale_root": "F",
                "scale_mode": "Minor",
                # Filter
                "filter_type": "Notch",
                "filter_cutoff": 800,
                # Amp
                "amp_attack": 2.0,
                "amp_decay": 0.0,
                "amp_sustain": 1.0,
                "amp_release": 3.0,
            },
        }

    async def configure_synth(
        self,
        track: TrackConfig,
        config: dict,
    ) -> tuple[bool, list[str]]:
        """Apply synth configuration to a track.

        Args:
            track: Track to configure
            config: Configuration dictionary with device and params

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        mcp = self.get_mcp_client()

        if not mcp:
            self.log(f"Mock: Configuring {config['device']} on {track.name}")
            return True, []

        device_name = config["device"]
        fallback = config.get("fallback")
        params = config.get("params", {})

        # Load device
        self.log(f"Loading {device_name} on {track.name}...")
        result = mcp.load_device(
            track_index=track.index,
            device_name=device_name,
            fallback=fallback,
        )

        if not result.success:
            errors.append(f"Failed to load {device_name}: {result.message}")
            return False, errors

        # Set parameters
        self.log(f"Setting {len(params)} parameters...")
        for param_name, value in params.items():
            param_result = mcp.set_device_parameter(
                track_index=track.index,
                device_index=0,  # First device on track
                parameter_name=param_name,
                value=value,
            )
            if not param_result.success:
                errors.append(f"Failed to set {param_name}: {param_result.message}")

        return len(errors) == 0, errors

    def configure_wavetable(
        self,
        track_index: int,
        oscillator_position: float | None = None,
        warp_mode: str | None = None,
        filter_type: str | None = None,
        filter_frequency: float | None = None,
        filter_resonance: float | None = None,
        modulation_source: str | None = None,
        modulation_target: str | None = None,
        modulation_amount: float | None = None,
    ) -> AgentResult:
        """Configure Wavetable synthesizer.

        Reference: Ableton Manual Section 30.13.2 "Oscillators" (page 742)
        Reference: Ableton Manual Section 30.10.8 "The Filter/Global Tab" (page 715)

        Args:
            track_index: Track index
            oscillator_position: Oscillator position (0.0-1.0)
            warp_mode: Warp mode (Bend, FM, Formant, etc.)
            filter_type: Filter type (Lowpass, Highpass, Bandpass, etc.)
            filter_frequency: Filter frequency in Hz
            filter_resonance: Filter resonance (0.0-1.0)
            modulation_source: Modulation source (LFO 1, Envelope, etc.)
            modulation_target: Modulation target parameter
            modulation_amount: Modulation amount (0.0-1.0)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Configuring Wavetable on track {track_index}")
            return AgentResult(
                success=True,
                message="Mock: Configured Wavetable synthesizer",
                data={"track_index": track_index},
            )

        try:
            # Configure oscillator
            if oscillator_position is not None:
                osc_result = mcp.set_device_parameter(
                    track_index=track_index,
                    device_index=0,
                    parameter_name="Osc Position",
                    value=oscillator_position,
                )
                if not osc_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set oscillator position: {osc_result.message}",
                    )

            if warp_mode is not None:
                warp_result = mcp.set_device_parameter(
                    track_index=track_index,
                    device_index=0,
                    parameter_name="Warp Mode",
                    value=warp_mode,
                )
                if not warp_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set warp mode: {warp_result.message}",
                    )

            # Configure filter
            if filter_type is not None:
                filter_result = mcp.set_device_parameter(
                    track_index=track_index,
                    device_index=0,
                    parameter_name="Filter Type",
                    value=filter_type,
                )
                if not filter_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set filter type: {filter_result.message}",
                    )

            if filter_frequency is not None:
                freq_result = mcp.set_device_parameter(
                    track_index=track_index,
                    device_index=0,
                    parameter_name="Filter Frequency",
                    value=filter_frequency,
                )
                if not freq_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set filter frequency: {freq_result.message}",
                    )

            if filter_resonance is not None:
                res_result = mcp.set_device_parameter(
                    track_index=track_index,
                    device_index=0,
                    parameter_name="Filter Resonance",
                    value=filter_resonance,
                )
                if not res_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set filter resonance: {res_result.message}",
                    )

            # Configure modulation
            if all(
                [modulation_source, modulation_target, modulation_amount is not None]
            ):
                mod_result = mcp.set_modulation_routing(
                    track_index=track_index,
                    device_index=0,
                    source=modulation_source,
                    target=modulation_target,
                    amount=modulation_amount,
                )
                if not mod_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set modulation: {mod_result.message}",
                    )

            self.log(f"Configured Wavetable on track {track_index}")
            return AgentResult(
                success=True,
                message="Configured Wavetable synthesizer",
                data={
                    "track_index": track_index,
                    "oscillator_position": oscillator_position,
                    "filter_type": filter_type,
                },
            )

        except Exception as e:
            self.log(f"Error configuring Wavetable: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(
        self,
        track_index: int | None = None,
        **kwargs,
    ) -> AgentResult:
        """Configure synthesizers for tracks.

        Args:
            track_index: Specific track to configure (None = all synth tracks)

        Returns:
            AgentResult with configuration results
        """
        synths_configured = []
        all_errors = []

        # Track-to-config mapping
        synth_configs = {
            2: self.get_fm_bass_config(),  # Track 3: Rolling Bass
            3: self.get_acid_config(),  # Track 4: Acid Line
            10: self.get_synth_stab_config(),  # Track 11: Synth Stabs
            11: self.get_drone_config(),  # Track 12: Atmospheric Drone
        }

        # Get tracks to process
        if track_index is not None:
            if track_index in synth_configs:
                tracks_to_process = [(track_index, TRACKS[track_index])]
            else:
                return AgentResult(
                    success=False,
                    message=f"Track {track_index} is not a synth track",
                    errors=[f"No synth configuration for track {track_index}"],
                )
        else:
            tracks_to_process = [(idx, TRACKS[idx]) for idx in synth_configs]

        for idx, track in tracks_to_process:
            self.log(f"Configuring synthesizer for {track.name}...")

            try:
                config = synth_configs[idx]
                success, errors = await self.configure_synth(track, config)

                if success:
                    synths_configured.append(
                        {
                            "track": track.name,
                            "device": config["device"],
                            "params_count": len(config.get("params", {})),
                        }
                    )
                    self.update_progress(track.index, 0.75)
                else:
                    all_errors.extend(errors)

            except Exception as e:
                all_errors.append(f"{track.name}: {e}")
                self.log(f"Error on {track.name}: {e}")

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Configured {len(synths_configured)} synthesizers",
            data={"synths": synths_configured},
            errors=all_errors,
        )
