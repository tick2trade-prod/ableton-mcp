"""Mastering Agent for mastering chain and final processing.

Reference: Ableton Manual Section 28.20 "Multiband Dynamics" (page 563)


Reference: Ableton Manual Section 28.26.1 "Dynamics Processing Theory" (page 563)
"""

from .base_agent import AgentResult, BaseAgent


class MasteringAgent(BaseAgent):
    """Agent for master bus processing and loudness optimization.

    Specializes in:
    - Glue Compressor for cohesion
    - Mid/Side EQ for stereo control
    - Roar multiband saturation for warmth
    - Limiting for competitive loudness
    - LUFS targeting (-6 to -8 LUFS)
    """

    def __init__(self, **kwargs):
        super().__init__(name="MasteringAgent", **kwargs)

    def get_role(self) -> str:
        return "Mastering Engineer"

    def get_goal(self) -> str:
        return "Finalize mix with competitive loudness and cohesive glue"

    def get_master_chain(self) -> list[dict]:
        """Get the master bus processing chain.

        Based on spec section 8: Mix Bus and Mastering Chain.
        """
        return [
            {
                "name": "Glue Compressor",
                "params": {
                    "attack": 0.01,  # 10ms
                    "release": 0.1,  # Auto release
                    "ratio": 4.0,
                    "threshold": -12,  # Set to achieve 2-3dB GR
                    "makeup": 2.0,
                    "range": 0,
                    "dry_wet": 1.0,
                },
                "description": "Glues kick and bass with percussion",
            },
            {
                "name": "EQ Eight",
                "params": {
                    "mode": "Mid/Side",
                    # Side channel: cut sub-bass for mono low-end
                    "side_low_cut": 120,
                    "side_low_cut_slope": 48,
                    # Side channel: boost air for width
                    "side_high_shelf_freq": 10000,
                    "side_high_shelf_gain": 1.5,
                    # Mid channel: subtle cuts if needed
                    "mid_notch_freq": 400,
                    "mid_notch_gain": -1.0,
                    "mid_notch_q": 2.0,
                },
                "description": "Mid/Side EQ for stereo control",
            },
            {
                "name": "Roar",
                "fallback": "Saturator",
                "params": {
                    "mode": "Mid/Side",
                    "drive": 2.0,  # Subtle saturation
                    "dry_wet": 0.08,  # 5-10% wet for warmth
                    "feedback": 0.0,
                },
                "description": "Analog warmth and harmonic cohesion",
            },
            {
                "name": "Limiter",
                "params": {
                    "ceiling": -0.3,  # -0.3dB for inter-sample peaks
                    "gain": 6.0,  # Adjust to reach -6 to -8 LUFS
                    "release": 0.05,  # Fast release
                    "lookahead": 0.001,  # 1ms
                    "true_peak": True,  # Enable true peak limiting
                    "stereo_link": 1.0,  # 100% linked
                },
                "description": "Competitive loudness and peak control",
            },
        ]

    def get_reference_targets(self) -> dict:
        """Get mastering reference targets."""
        return {
            "lufs": -7.0,  # Target integrated loudness
            "lufs_range": (-8.0, -6.0),  # Acceptable range
            "true_peak": -0.5,  # Max true peak (dB)
            "dynamic_range": 6.0,  # Target DR (dB)
        }

    async def apply_master_chain(
        self,
        chain: list[dict],
    ) -> tuple[bool, list[str]]:
        """Apply master bus processing chain.

        Args:
            chain: List of device configurations

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        mcp = self.get_mcp_client()

        if not mcp:
            self.log("Mock: Applying master chain")
            for device in chain:
                self.log(f"  - {device['name']}: {device['description']}")
            return True, []

        # Master track is typically the last track or has a special index
        # This depends on MCP implementation
        master_track_index = -1  # Or specific index if known

        for device_spec in chain:
            device_name = device_spec["name"]
            fallback = device_spec.get("fallback")
            params = device_spec.get("params", {})

            self.log(f"Loading {device_name} on master...")

            result = mcp.load_device(
                track_index=master_track_index,
                device_name=device_name,
                fallback=fallback,
            )

            if not result.success:
                errors.append(f"Failed to load {device_name}: {result.message}")
                continue

            # Set parameters
            for param_name, value in params.items():
                param_result = mcp.set_device_parameter(
                    track_index=master_track_index,
                    device_index=-1,
                    parameter_name=param_name,
                    value=value,
                )
                if not param_result.success:
                    errors.append(f"Failed to set {param_name}")

        return len(errors) == 0, errors

    async def analyze_loudness(self) -> dict:
        """Analyze current mix loudness.

        Returns:
            Dictionary with LUFS measurements
        """
        mcp = self.get_mcp_client()

        if not mcp:
            # Return mock values
            return {
                "integrated_lufs": -7.2,
                "true_peak": -0.4,
                "dynamic_range": 6.5,
                "mock": True,
            }

        # If MCP supports loudness analysis
        if hasattr(mcp, "analyze_loudness"):
            result = mcp.analyze_loudness()
            if result.success:
                return result.data

        # Return estimated values
        return {
            "integrated_lufs": None,
            "true_peak": None,
            "dynamic_range": None,
            "error": "Loudness analysis not available",
        }

    def check_loudness_compliance(self, analysis: dict) -> dict:
        """Check if loudness meets targets.

        Args:
            analysis: Loudness analysis results

        Returns:
            Compliance report
        """
        targets = self.get_reference_targets()
        compliance = {}

        if analysis.get("integrated_lufs") is not None:
            lufs = analysis["integrated_lufs"]
            lufs_min, lufs_max = targets["lufs_range"]
            compliance["lufs_ok"] = lufs_min <= lufs <= lufs_max
            compliance["lufs_message"] = (
                f"LUFS: {lufs:.1f} (target: {targets['lufs']:.1f})"
            )
        else:
            compliance["lufs_ok"] = None
            compliance["lufs_message"] = "LUFS measurement unavailable"

        if analysis.get("true_peak") is not None:
            peak = analysis["true_peak"]
            compliance["peak_ok"] = peak <= targets["true_peak"]
            compliance["peak_message"] = (
                f"True Peak: {peak:.2f} dB (max: {targets['true_peak']:.2f})"
            )
        else:
            compliance["peak_ok"] = None
            compliance["peak_message"] = "Peak measurement unavailable"

        return compliance

    def configure_multiband_dynamics(
        self,
        track_index: int,
        num_bands: int = 3,
        crossover_low: float = 120,
        crossover_high: float = 8000,
    ) -> AgentResult:
        """Configure multiband dynamics processing.

        Reference: Ableton Manual Section 28.26.1 "Dynamics Processing Theory" (page 563)

        Args:
            track_index: Track index (typically master)
            num_bands: Number of frequency bands (2 or 3)
            crossover_low: Low band crossover frequency in Hz
            crossover_high: High band crossover frequency in Hz

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Configuring {num_bands}-band dynamics")
            return AgentResult(
                success=True,
                message=f"Mock: Configured {num_bands}-band dynamics",
                data={"num_bands": num_bands},
            )

        try:
            result = mcp.configure_multiband_compressor(
                track_index=track_index,
                num_bands=num_bands,
                crossover_low=crossover_low,
                crossover_high=crossover_high,
            )

            if result.success:
                self.log(f"Configured {num_bands}-band dynamics")

            return result

        except Exception as e:
            self.log(f"Error configuring multiband dynamics: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(
        self,
        analyze_only: bool = False,
        **kwargs,
    ) -> AgentResult:
        """Apply master bus processing and analyze loudness.

        Args:
            analyze_only: If True, only analyze without applying chain

        Returns:
            AgentResult with mastering results
        """
        all_errors = []
        results = {}

        if not analyze_only:
            # Apply master chain
            self.log("Applying master bus processing chain...")
            chain = self.get_master_chain()

            try:
                success, errors = await self.apply_master_chain(chain)
                if success:
                    results["chain_applied"] = True
                    results["devices_count"] = len(chain)
                else:
                    all_errors.extend(errors)
            except Exception as e:
                all_errors.append(f"Master chain error: {e}")

        # Analyze loudness
        self.log("Analyzing loudness...")
        try:
            analysis = await self.analyze_loudness()
            compliance = self.check_loudness_compliance(analysis)

            results["loudness_analysis"] = analysis
            results["compliance"] = compliance

            # Log results
            self.log(compliance.get("lufs_message", ""))
            self.log(compliance.get("peak_message", ""))

        except Exception as e:
            all_errors.append(f"Loudness analysis error: {e}")

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message="Master bus processing complete",
            data=results,
            errors=all_errors,
        )
