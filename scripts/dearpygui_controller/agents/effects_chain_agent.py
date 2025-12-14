"""Effects Chain Agent for audio effects and rack configuration.

Reference: Ableton Manual Section 24.4 "Chain List" (page 445)
Reference: Ableton Manual Section 17.5.2 "Making Use of Internal Routing" (page 363)
Reference: Ableton Manual Section 24.7.3 "Macro Control Variations" (page 457)
"""

from ..config import TRACKS
from .base_agent import AgentResult, BaseAgent


class EffectsChainAgent(BaseAgent):
    """Agent for complex multi-band processing and routing.

    Specializes in:
    - Sidechain compression routing (kick to rumble, bass, etc.)
    - Multi-band saturation with Roar
    - Send/Return effects configuration
    - Mid/Side processing for stereo control
    - Parallel compression setups
    """

    def __init__(self, **kwargs):
        super().__init__(name="EffectsChainAgent", **kwargs)

    def get_role(self) -> str:
        return "Signal Processing Engineer"

    def get_goal(self) -> str:
        return "Configure advanced signal routing and multi-band processing"

    def get_sidechain_targets(self) -> list[dict]:
        """Get tracks that need sidechain compression to the kick.

        Critical for the genre-defining pumping rhythm.
        """
        return [
            {
                "track_index": 1,  # Rumble
                "name": "Rumble Sidechain",
                "params": {
                    "threshold": -24,
                    "ratio": "Inf:1",  # Full ducking
                    "attack": 0.0001,
                    "release": "1/8",  # Synced to tempo
                    "sidechain_source": 0,  # Kick track
                },
            },
            {
                "track_index": 2,  # Rolling Bass
                "name": "Bass Sidechain",
                "params": {
                    "threshold": -18,
                    "ratio": "8:1",
                    "attack": 0.001,
                    "release": "1/8",
                    "sidechain_source": 0,
                },
            },
            {
                "track_index": 3,  # Acid Line
                "name": "Acid Sidechain",
                "params": {
                    "threshold": -15,
                    "ratio": "4:1",
                    "attack": 0.001,
                    "release": "1/16",
                    "sidechain_source": 0,
                },
            },
            {
                "track_index": 9,  # Ride
                "name": "Ride Sidechain",
                "params": {
                    "threshold": -20,
                    "ratio": "3:1",  # Gentle pump
                    "attack": 0.005,
                    "release": "1/8",
                    "sidechain_source": 0,
                },
            },
        ]

    def get_return_tracks(self) -> list[dict]:
        """Get return track configurations for send effects."""
        return [
            {
                "name": "A-Reverb",
                "devices": [
                    {
                        "name": "Reverb",
                        "params": {
                            "decay": 2.5,
                            "pre_delay": 0.02,
                            "diffusion": 0.8,
                            "quality": "High",
                        },
                    },
                    {
                        "name": "Channel EQ",
                        "params": {
                            "low_cut": 200,  # Keep reverb out of low-end
                            "high_cut": 12000,
                        },
                    },
                ],
            },
            {
                "name": "B-Delay",
                "devices": [
                    {
                        "name": "Echo",
                        "params": {
                            "time_l": "1/4",
                            "time_r": "1/4D",
                            "feedback": 0.4,
                            "filter_on": True,
                            "filter_freq": 2000,
                        },
                    },
                ],
            },
            {
                "name": "C-Parallel Compression",
                "devices": [
                    {
                        "name": "Glue Compressor",
                        "params": {
                            "threshold": -30,
                            "ratio": "10:1",
                            "attack": 0.01,
                            "release": 0.3,
                            "makeup": 10.0,
                        },
                    },
                    {
                        "name": "Saturator",
                        "params": {
                            "drive": 6.0,
                        },
                    },
                ],
            },
        ]

    def create_effect_rack(
        self,
        track_index: int,
        rack_name: str,
        num_chains: int = 1,
    ) -> AgentResult:
        """Create an effect rack with parallel chains.

        Reference: Ableton Manual Section 24.4 "Chain List" (page 445)

        Args:
            track_index: Track index
            rack_name: Name for the rack
            num_chains: Number of parallel chains to create (default: 1)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Creating effect rack '{rack_name}' on track {track_index}")
            return AgentResult(
                success=True,
                message=(
                    f"Mock: Created effect rack '{rack_name}' with {num_chains} chains"
                ),
                data={
                    "track_index": track_index,
                    "rack_name": rack_name,
                    "num_chains": num_chains,
                },
            )

        try:
            # Create the rack
            result = mcp.create_effect_rack(track_index=track_index, name=rack_name)

            if not result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to create effect rack: {result.message}",
                )

            # Add additional chains if requested
            for i in range(num_chains):
                chain_result = mcp.add_chain_to_rack(
                    track_index=track_index,
                    rack_index=-1,  # Last rack
                    chain_name=f"Chain {i + 1}",
                )
                if not chain_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to add chain {i + 1}: {chain_result.message}",
                    )

            self.log(f"Created effect rack '{rack_name}' with {num_chains} chains")
            return AgentResult(
                success=True,
                message=f"Created effect rack '{rack_name}' with {num_chains} chains",
                data={
                    "track_index": track_index,
                    "rack_name": rack_name,
                    "num_chains": num_chains,
                },
            )

        except Exception as e:
            self.log(f"Error creating effect rack: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def configure_chain_selector(
        self,
        track_index: int,
        rack_index: int,
        chain_index: int,
        zone_min: int,
        zone_max: int,
    ) -> AgentResult:
        """Configure chain selector zones.

        Reference: Ableton Manual Section 24.4 "Chain List" (page 445)

        Args:
            track_index: Track index
            rack_index: Rack index
            chain_index: Chain index
            zone_min: Minimum zone value (0-127)
            zone_max: Maximum zone value (0-127)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Configuring chain selector zone {zone_min}-{zone_max}")
            return AgentResult(
                success=True, message="Mock: Configured chain selector zone"
            )

        try:
            result = mcp.set_chain_selector_zone(
                track_index=track_index,
                rack_index=rack_index,
                chain_index=chain_index,
                zone_min=zone_min,
                zone_max=zone_max,
            )

            if result.success:
                self.log(f"Configured chain selector zone {zone_min}-{zone_max}")

            return result

        except Exception as e:
            self.log(f"Error configuring chain selector: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def map_macro_control(
        self,
        track_index: int,
        rack_index: int,
        macro_index: int,
        device_index: int,
        parameter_name: str,
    ) -> AgentResult:
        """Map a device parameter to a macro control.

        Reference: Ableton Manual Section 24.7.3 "Macro Control Variations" (page 457)

        Args:
            track_index: Track index
            rack_index: Rack index
            macro_index: Macro control index (0-7)
            device_index: Device index within rack
            parameter_name: Parameter name to map

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Mapping {parameter_name} to macro {macro_index}")
            return AgentResult(
                success=True,
                message=f"Mock: Mapped {parameter_name} to macro {macro_index}",
            )

        try:
            result = mcp.map_to_macro(
                track_index=track_index,
                rack_index=rack_index,
                macro_index=macro_index,
                device_index=device_index,
                parameter_name=parameter_name,
            )

            if result.success:
                self.log(f"Mapped {parameter_name} to macro {macro_index}")

            return result

        except Exception as e:
            self.log(f"Error mapping macro control: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def configure_chain_routing(
        self,
        track_index: int,
        rack_index: int,
        chain_index: int,
        routing_point: str,
    ) -> AgentResult:
        """Configure chain routing points.

        Reference: Ableton Manual Section 17.5.2 "Making Use of Internal Routing" (page 363)

        Args:
            track_index: Track index
            rack_index: Rack index
            chain_index: Chain index
            routing_point: Routing point ("Pre FX", "Post FX", "Post Mixer")

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Configuring chain routing to {routing_point}")
            return AgentResult(
                success=True,
                message=f"Mock: Configured chain routing to {routing_point}",
            )

        try:
            result = mcp.set_chain_routing(
                track_index=track_index,
                rack_index=rack_index,
                chain_index=chain_index,
                routing_point=routing_point,
            )

            if result.success:
                self.log(f"Configured chain routing to {routing_point}")

            return result

        except Exception as e:
            self.log(f"Error configuring chain routing: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def get_bass_mono_config(self) -> list[dict]:
        """Get bass mono configuration for tracks.

        Ensures low-end is mono below 120Hz for phase coherence.
        """
        return [
            {"track_index": 0, "cutoff": 120},  # Kick
            {"track_index": 1, "cutoff": 100},  # Rumble
            {"track_index": 2, "cutoff": 120},  # Rolling Bass
            {"track_index": 3, "cutoff": 150},  # Acid (higher cutoff)
        ]

    async def configure_sidechain(
        self,
        config: dict,
    ) -> tuple[bool, list[str]]:
        """Configure sidechain compression on a track.

        Args:
            config: Sidechain configuration

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        track_index = config["track_index"]
        track = TRACKS[track_index]
        mcp = self.get_mcp_client()

        if not mcp:
            self.log(f"Mock: Configuring sidechain on {track.name}")
            return True, []

        self.log(f"Setting up sidechain on {track.name}...")

        # Load compressor
        result = mcp.load_device(
            track_index=track_index,
            device_name="Compressor",
        )

        if not result.success:
            errors.append(f"Failed to load Compressor: {result.message}")
            return False, errors

        # Set compressor parameters
        params = config["params"]
        for param_name, value in params.items():
            param_result = mcp.set_device_parameter(
                track_index=track_index,
                device_index=-1,  # Last device
                parameter_name=param_name,
                value=value,
            )
            if not param_result.success:
                errors.append(f"Failed to set {param_name}")

        return len(errors) == 0, errors

    async def configure_bass_mono(
        self,
        config: dict,
    ) -> tuple[bool, list[str]]:
        """Configure bass mono on a track using Utility.

        Args:
            config: Bass mono configuration

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        track_index = config["track_index"]
        track = TRACKS[track_index]
        mcp = self.get_mcp_client()

        if not mcp:
            self.log(f"Mock: Enabling bass mono on {track.name}")
            return True, []

        self.log(f"Enabling bass mono on {track.name}...")

        result = mcp.load_device(
            track_index=track_index,
            device_name="Utility",
        )

        if not result.success:
            errors.append(f"Failed to load Utility: {result.message}")
            return False, errors

        # Enable bass mono
        param_result = mcp.set_device_parameter(
            track_index=track_index,
            device_index=-1,
            parameter_name="bass_mono",
            value=True,
        )
        if param_result.success:
            # Set cutoff frequency
            freq_result = mcp.set_device_parameter(
                track_index=track_index,
                device_index=-1,
                parameter_name="bass_mono_freq",
                value=config["cutoff"],
            )
            if not freq_result.success:
                errors.append("Failed to set bass mono frequency")

        return len(errors) == 0, errors

    async def execute(
        self,
        mode: str = "all",
        **kwargs,
    ) -> AgentResult:
        """Configure advanced effects routing.

        Args:
            mode: What to configure ("sidechain", "bass_mono", "returns", "all")

        Returns:
            AgentResult with configuration results
        """
        configured = []
        all_errors = []

        # Configure sidechain compression
        if mode in ["sidechain", "all"]:
            sidechain_targets = self.get_sidechain_targets()

            for sc_config in sidechain_targets:
                try:
                    success, errors = await self.configure_sidechain(sc_config)
                    if success:
                        configured.append(
                            {
                                "type": "sidechain",
                                "name": sc_config["name"],
                            }
                        )
                    else:
                        all_errors.extend(errors)
                except Exception as e:
                    all_errors.append(f"Sidechain error: {e}")

        # Configure bass mono
        if mode in ["bass_mono", "all"]:
            bass_mono_configs = self.get_bass_mono_config()

            for bm_config in bass_mono_configs:
                try:
                    success, errors = await self.configure_bass_mono(bm_config)
                    if success:
                        track = TRACKS[bm_config["track_index"]]
                        configured.append(
                            {
                                "type": "bass_mono",
                                "track": track.name,
                                "cutoff": bm_config["cutoff"],
                            }
                        )
                    else:
                        all_errors.extend(errors)
                except Exception as e:
                    all_errors.append(f"Bass mono error: {e}")

        # Configure return tracks
        if mode in ["returns", "all"]:
            # Return track configuration would go here
            # This depends on MCP return track capabilities
            self.log("Return track configuration not yet implemented")

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Configured {len(configured)} effect routings",
            data={"configurations": configured},
            errors=all_errors,
        )
