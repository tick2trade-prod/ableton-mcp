"""Vocals Agent for vocal processing and effects.

Reference: Ableton Manual Section 28.13 "Corpus" (page 530)
"""

from math import inf

from ..config import TRACKS
from .base_agent import AgentResult, BaseAgent


class VocalsAgent(BaseAgent):
    """Agent for processing vocals with effects chains.

    Specializes in:
    - Main vocal "I Am Machine" processing (Track 13)
    - Vocal FX/glitches and grain clouds (Track 14)
    - Vocoder effects with drum modulation
    - Telephone EQ curves for robotic quality
    - Reverse sweeps and granular synthesis
    """

    def __init__(self, **kwargs):
        super().__init__(name="VocalsAgent", **kwargs)

    def get_role(self) -> str:
        return "Vocal Processing Engineer"

    def get_goal(self) -> str:
        return (
            "Transform vocals into chilling, robotic textures for 'Machine' aesthetic"
        )

    def get_main_vocal_chain(self) -> list[dict]:
        """Get processing chain for Main Vocal (Track 13).

        Creates the "chilling" and "sultry" vocal sound with
        robotic/lo-fi quality suitable for the "Machine" theme.
        """
        return [
            {
                "name": "Gate",
                "params": {
                    "threshold": -40,  # dB
                    "floor": -inf,  # Complete silence when closed
                    "attack": 0.001,
                    "release": 0.05,
                },
            },
            {
                "name": "Compressor",
                "params": {
                    "threshold": -18,  # dB
                    "ratio": 4.0,
                    "attack": 0.003,
                    "release": 0.1,
                    "knee": 0.0,  # Hard knee
                    "makeup_gain": 6.0,
                },
            },
            {
                "name": "Channel EQ",
                "params": {
                    # Telephone-style curve (bandpass 300Hz - 3kHz)
                    "low_cut_freq": 300,
                    "low_cut_slope": 24,  # dB/oct
                    "high_cut_freq": 3000,
                    "high_cut_slope": 24,
                    # Boost presence
                    "mid_freq": 1200,
                    "mid_gain": 3.0,
                    "mid_q": 1.0,
                },
            },
            {
                "name": "Vocoder",
                "params": {
                    "carrier": "External",  # Modulated by drums
                    "modulator_source": "Track 6",  # Open Hats or Glitch
                    "bands": 20,
                    "formant_shift": 0,
                    "attack": 0.01,
                    "release": 0.1,
                    "dry_wet": 0.5,  # Blend with original
                },
            },
            {
                "name": "Reverb",
                "params": {
                    "decay": 0.8,
                    "pre_delay": 0.02,
                    "dry_wet": 0.15,
                },
            },
        ]

    def get_vocal_fx_chain(self) -> list[dict]:
        """Get processing chain for Vocal FX/Glitches (Track 14).

        Creates background textures: whispers, reverse sweeps,
        and granular clouds using heavy processing.
        """
        return [
            {
                "name": "Simpler",
                "params": {
                    "mode": "Slice",  # Slice mode for granular
                    "playback": "Classic",
                    "slice_sensitivity": 0.5,
                },
            },
            {
                "name": "Granulator III",
                "fallback": "Corpus",  # Fallback if Granulator not available
                "params": {
                    "spray": 0.6,
                    "frequency": 80,  # Grain frequency (Hz)
                    "grain_size": 0.05,  # 50ms grains
                    "pitch": -12,  # Octave down
                    "random_pitch": 0.3,
                },
            },
            {
                "name": "Reverb",
                "params": {
                    "decay": 4.0,  # Long reverb
                    "dry_wet": 1.0,  # 100% wet
                    "quality": "High",
                },
            },
            {
                "name": "Auto Pan",
                "params": {
                    "rate": "1/8",
                    "shape": "Triangle",
                    "amount": 0.7,
                    "phase": 0,  # Mono to stereo movement
                },
            },
            {
                "name": "Frequency Shifter",
                "params": {
                    "coarse": -300,  # Hz shift (demonic register)
                    "fine": 0,
                    "mode": "Wide",
                    "dry_wet": 0.6,
                },
            },
        ]

    def configure_vocal_chain(
        self,
        track_index: int,
        eq_enabled: bool = True,
        compressor_enabled: bool = True,
        reverb_amount: float = 0.3,
    ) -> AgentResult:
        """Configure vocal processing chain.

        Reference: Ableton Manual Section 28.13 "Corpus" (page 530)

        Args:
            track_index: Track index
            eq_enabled: Enable EQ in chain
            compressor_enabled: Enable compressor in chain
            reverb_amount: Reverb wet amount (0.0-1.0)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            chain_parts = []
            if eq_enabled:
                chain_parts.append("EQ")
            if compressor_enabled:
                chain_parts.append("Compressor")
            chain_parts.append(f"Reverb@{reverb_amount}")
            self.log(f"Mock: Configuring vocal chain: {', '.join(chain_parts)}")
            return AgentResult(
                success=True,
                message="Mock: Configured vocal chain",
                data={
                    "eq": eq_enabled,
                    "comp": compressor_enabled,
                    "reverb": reverb_amount,
                },
            )

        try:
            devices_loaded = []

            if eq_enabled:
                result = mcp.load_device(
                    track_index=track_index, device_name="Channel EQ"
                )
                if result.success:
                    devices_loaded.append("EQ")

            if compressor_enabled:
                result = mcp.load_device(
                    track_index=track_index, device_name="Compressor"
                )
                if result.success:
                    devices_loaded.append("Compressor")

            result = mcp.load_device(track_index=track_index, device_name="Reverb")
            if result.success:
                devices_loaded.append("Reverb")

            self.log(f"Configured vocal chain: {', '.join(devices_loaded)}")
            return AgentResult(
                success=True,
                message=f"Configured vocal chain ({len(devices_loaded)} devices)",
                data={"devices": devices_loaded},
            )

        except Exception as e:
            self.log(f"Error configuring vocal chain: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def apply_vocal_chain(
        self,
        track_index: int,
        chain: list[dict],
    ) -> tuple[bool, list[str]]:
        """Apply vocal effects chain to a track.

        Args:
            track_index: Track index to process
            chain: List of device configurations

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        track = TRACKS[track_index]
        mcp = self.get_mcp_client()

        if not mcp:
            self.log(f"Mock: Loading {len(chain)} devices for {track.name}")
            return True, []

        for device_spec in chain:
            device_name = device_spec["name"]
            fallback = device_spec.get("fallback")
            params = device_spec.get("params", {})

            self.log(f"Loading {device_name} on {track.name}...")

            # Load device
            result = mcp.load_device(
                track_index=track_index,
                device_name=device_name,
                fallback=fallback,
            )

            if not result.success:
                errors.append(f"Failed to load {device_name}: {result.message}")
                continue

            # Set parameters
            for param_name, value in params.items():
                param_result = mcp.set_device_parameter(
                    track_index=track_index,
                    device_index=-1,  # Last added device
                    parameter_name=param_name,
                    value=value,
                )
                if not param_result.success:
                    errors.append(f"Failed to set {param_name}: {param_result.message}")

        return len(errors) == 0, errors

    async def execute(
        self,
        track_index: int | None = None,
        **kwargs,
    ) -> AgentResult:
        """Process vocal tracks with effects chains.

        Args:
            track_index: Specific track to process (None = all vocal tracks)

        Returns:
            AgentResult with processing results
        """
        vocals_processed = []
        all_errors = []

        # Vocal track configurations
        vocal_configs = {
            12: {  # Track 13: Main Vocal
                "chain": self.get_main_vocal_chain(),
                "type": "Main Vocal",
            },
            13: {  # Track 14: Vocal FX
                "chain": self.get_vocal_fx_chain(),
                "type": "Vocal FX",
            },
        }

        # Get tracks to process
        if track_index is not None:
            if track_index in vocal_configs:
                tracks_to_process = [(track_index, vocal_configs[track_index])]
            else:
                return AgentResult(
                    success=False,
                    message=f"Track {track_index} is not a vocal track",
                    errors=[f"No vocal configuration for track {track_index}"],
                )
        else:
            tracks_to_process = list(vocal_configs.items())

        for idx, config in tracks_to_process:
            track = TRACKS[idx]
            self.log(f"Processing {config['type']}: {track.name}...")

            try:
                success, errors = await self.apply_vocal_chain(
                    idx,
                    config["chain"],
                )

                if success:
                    vocals_processed.append(
                        {
                            "track": track.name,
                            "type": config["type"],
                            "devices": len(config["chain"]),
                        }
                    )
                    self.update_progress(track.index, 0.8)
                else:
                    all_errors.extend(errors)

            except Exception as e:
                all_errors.append(f"{track.name}: {e}")
                self.log(f"Error on {track.name}: {e}")

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Processed {len(vocals_processed)} vocal tracks",
            data={"vocals": vocals_processed},
            errors=all_errors,
        )
