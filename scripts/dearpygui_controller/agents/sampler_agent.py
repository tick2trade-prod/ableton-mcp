"""Sampler Agent for sample manipulation and granular synthesis.

Reference: Ableton Manual Section 30.4.2 "Drum Sampler Playback" (page 660)
Reference: Ableton Manual Section 28.31 "Granulator III" (page 579)
"""

from .base_agent import AgentResult, BaseAgent


class SamplerAgent(BaseAgent):
    """Agent for sample manipulation and granular synthesis.

    Specializes in:
    - Sample slicing for vocal chops (Track 14)
    - Random slice triggering for glitch percussion
    - Granular synthesis for vocal FX
    """

    def __init__(self, **kwargs):
        super().__init__(name="SamplerAgent", **kwargs)

    def get_role(self) -> str:
        return "Sample Manipulation Engineer"

    def get_goal(self) -> str:
        return "Configure advanced sample playback and granular synthesis"

    def load_sample(
        self,
        track_name: str,
        sample_path: str,
        mode: str = "classic",
        slice_count: int = 16,
        device_type: str = "Simpler",
    ) -> AgentResult:
        """Load sample into Simpler/Sampler with specified playback mode.

        Reference: Ableton Manual Section 30.4.2 "Drum Sampler Playback"
        (page 660)

        Args:
            track_name: Target track name
            sample_path: Path to sample file
            mode: Playback mode ("classic", "slice", "1-shot")
            slice_count: Number of slices (if mode="slice")
            device_type: Device to use ("Simpler", "Sampler", "Drum Sampler")

        Returns:
            AgentResult with sample configuration details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Load sample {sample_path} on {track_name}")
            return AgentResult(
                success=True,
                message=f"Mock: Loaded sample in {mode} mode",
                data={
                    "track_name": track_name,
                    "sample_path": sample_path,
                    "mode": mode,
                    "slice_count": slice_count,
                },
            )

        try:
            # Load Simpler/Sampler device
            load_result = mcp.load_device(
                track_name=track_name, device_name=device_type
            )
            if not load_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to load {device_type}: {load_result.message}",
                )

            # Load sample
            sample_result = mcp.load_sample(
                track_name=track_name, device_index=0, sample_path=sample_path
            )
            if not sample_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to load sample: {sample_result.message}",
                )

            # Set playback mode
            mode_param = "Playback Mode" if device_type == "Simpler" else "Mode"
            mode_value = {"classic": 0.0, "slice": 0.5, "1-shot": 1.0}.get(mode, 0.0)

            mode_result = mcp.set_device_parameter(
                track_name=track_name,
                device_index=0,
                parameter_name=mode_param,
                value=mode_value,
            )

            # If slice mode, set slice count
            if mode == "slice" and mode_result.success:
                slice_result = mcp.set_device_parameter(
                    track_name=track_name,
                    device_index=0,
                    parameter_name="Slices",
                    value=slice_count,
                )
                if not slice_result.success:
                    self.log(f"Warning: Failed to set slices: {slice_result.message}")

            self.log(f"Loaded sample {sample_path} on {track_name} in {mode} mode")
            return AgentResult(
                success=True,
                message=f"Loaded sample in {mode} mode",
                data={
                    "track_name": track_name,
                    "sample_path": sample_path,
                    "mode": mode,
                    "slice_count": slice_count,
                },
            )

        except Exception as e:
            self.log(f"Error loading sample: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def setup_random_slicing(
        self,
        track_name: str,
        slice_count: int = 16,
        randomize: bool = True,
    ) -> AgentResult:
        """Setup random slice triggering for glitch effects.

        Reference: Ableton Manual Section 30.4.2 "Drum Sampler Playback"
        (page 660)

        Args:
            track_name: Target track name
            slice_count: Number of slices
            randomize: Enable random slice triggering

        Returns:
            AgentResult with configuration details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Random slicing on {track_name}")
            return AgentResult(
                success=True,
                message="Mock: Configured random slicing",
                data={
                    "track_name": track_name,
                    "slice_count": slice_count,
                    "randomize": randomize,
                },
            )

        try:
            # Set slice mode
            mode_result = mcp.set_device_parameter(
                track_name=track_name,
                device_index=0,
                parameter_name="Playback Mode",
                value=0.5,  # Slice mode
            )

            # Set slice count
            slice_result = mcp.set_device_parameter(
                track_name=track_name,
                device_index=0,
                parameter_name="Slices",
                value=slice_count,
            )

            # Enable randomization if requested
            if randomize:
                random_result = mcp.set_device_parameter(
                    track_name=track_name,
                    device_index=0,
                    parameter_name="Random",
                    value=1.0,
                )
                if not random_result.success:
                    self.log(
                        f"Warning: Failed to enable random: {random_result.message}"
                    )

            self.log(f"Configured random slicing on {track_name}")
            return AgentResult(
                success=True,
                message="Configured random slicing",
                data={
                    "track_name": track_name,
                    "slice_count": slice_count,
                    "randomize": randomize,
                },
            )

        except Exception as e:
            self.log(f"Error setting up random slicing: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def setup_granular(
        self,
        track_name: str,
        grain_size_ms: float = 50,
        density: float = 0.7,
        randomize_pitch: bool = True,
        spray: float = 0.0,
    ) -> AgentResult:
        """Setup granular synthesis using Granulator III.

        Reference: Ableton Manual Section 28.31 "Granulator III" (page 579)

        Args:
            track_name: Target track name
            grain_size_ms: Grain size in milliseconds
            density: Grain density (0.0-1.0)
            randomize_pitch: Enable pitch randomization
            spray: Spray amount (0.0-1.0)

        Returns:
            AgentResult with granular configuration details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Granular synthesis on {track_name}")
            return AgentResult(
                success=True,
                message="Mock: Configured granular synthesis",
                data={
                    "track_name": track_name,
                    "grain_size_ms": grain_size_ms,
                    "density": density,
                    "randomize_pitch": randomize_pitch,
                },
            )

        try:
            # Load Granulator III
            load_result = mcp.load_device(
                track_name=track_name, device_name="Granulator III"
            )
            if not load_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to load Granulator III: {load_result.message}",
                )

            # Configure grain size (normalized to 0-1)
            grain_normalized = min(grain_size_ms / 200.0, 1.0)
            grain_result = mcp.set_device_parameter(
                track_name=track_name,
                device_index=0,
                parameter_name="Grain Size",
                value=grain_normalized,
            )

            # Configure density
            density_result = mcp.set_device_parameter(
                track_name=track_name,
                device_index=0,
                parameter_name="Spray",
                value=density,
            )

            # Configure pitch randomization
            if randomize_pitch:
                pitch_result = mcp.set_device_parameter(
                    track_name=track_name,
                    device_index=0,
                    parameter_name="Pitch",
                    value=0.5,  # Center detune
                )
                pitch_random_result = mcp.set_device_parameter(
                    track_name=track_name,
                    device_index=0,
                    parameter_name="Pitch Random",
                    value=0.3,  # 30% randomization
                )

            self.log(
                f"Configured granular synthesis on {track_name}: "
                f"grain={grain_size_ms}ms, density={density}"
            )
            return AgentResult(
                success=True,
                message="Configured granular synthesis",
                data={
                    "track_name": track_name,
                    "grain_size_ms": grain_size_ms,
                    "density": density,
                    "randomize_pitch": randomize_pitch,
                    "spray": spray,
                },
            )

        except Exception as e:
            self.log(f"Error setting up granular synthesis: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(self, **kwargs) -> AgentResult:
        """Execute sample manipulation tasks.

        Args:
            samples: List of {track, sample_path, mode, slice_count} dicts
            granular_tracks: List of {track, grain_size, density} dicts

        Returns:
            AgentResult with all configured samples/granular tracks
        """
        samples = kwargs.get("samples", [])
        granular_tracks = kwargs.get("granular_tracks", [])
        results = []
        errors = []

        # Load samples
        for sample in samples:
            result = self.load_sample(**sample)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        # Setup granular synthesis
        for granular in granular_tracks:
            result = self.setup_granular(**granular)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        return AgentResult(
            success=len(errors) == 0,
            message=f"Configured {len(results)} sample/granular tracks",
            data={"configurations": results},
            errors=errors,
        )
