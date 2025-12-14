"""Sidechain Agent for compression routing.

Reference: Ableton Manual Section 28.9.2 "Compressor Tips" (page 521)
Reference: Ableton Manual Section 17.5.2 "Internal Routing" (page 363)
"""

from .base_agent import AgentResult, BaseAgent


class SidechainAgent(BaseAgent):
    """Agent for sidechain compression routing.

    Specializes in:
    - Rumble pumping (infinite:1 sidechain to kick)
    - Rhythmic ducking for pads/leads
    - Preset sidechain patterns
    """

    # Preset configurations
    PRESETS = {
        "kick_pump": {
            "ratio": "infinite:1",
            "attack_ms": 0.1,
            "release": "1/8n",
            "threshold_db": -20,
        },
        "rhythmic_duck": {
            "ratio": "4:1",
            "attack_ms": 5,
            "release": "1/16n",
            "threshold_db": -15,
        },
        "gentle_pump": {
            "ratio": "2:1",
            "attack_ms": 10,
            "release": "1/4n",
            "threshold_db": -10,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(name="SidechainAgent", **kwargs)

    def get_role(self) -> str:
        return "Sidechain Compression Engineer"

    def get_goal(self) -> str:
        return "Configure sidechain compression for techno pumping effect"

    def setup_sidechain(
        self,
        source_track: str,
        target_track: str,
        preset: str | None = None,
        ratio: str | None = None,
        attack_ms: float | None = None,
        release: str | None = None,
        threshold_db: float = -20,
    ) -> AgentResult:
        """Setup sidechain compression routing.

        Reference: Ableton Manual Section 28.9.2 "Compressor Tips" (page 521)

        Args:
            source_track: Track triggering sidechain (e.g., "01 - Kick")
            target_track: Track being sidechained (e.g., "02 - Rumble")
            preset: Preset pattern ("kick_pump", "rhythmic_duck", "gentle_pump")
            ratio: Compression ratio (or "infinite:1")
            attack_ms: Attack time in milliseconds
            release: Release time (tempo-synced, e.g., "1/8n", "1/16n")
            threshold_db: Threshold in dB

        Returns:
            AgentResult with configuration details
        """
        # Use preset if provided
        if preset and preset in self.PRESETS:
            config = self.PRESETS[preset]
            ratio = ratio or config["ratio"]
            attack_ms = attack_ms or config["attack_ms"]
            release = release or config["release"]
            threshold_db = threshold_db or config["threshold_db"]

        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Sidechain {target_track} → {source_track}")
            return AgentResult(
                success=True,
                message=f"Mock: Configured sidechain {target_track} → {source_track}",
                data={
                    "source_track": source_track,
                    "target_track": target_track,
                    "ratio": ratio,
                    "attack_ms": attack_ms,
                    "release": release,
                },
            )

        try:
            # Load Compressor on target track
            load_result = mcp.load_device(
                track_name=target_track, device_name="Compressor"
            )
            if not load_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to load Compressor: {load_result.message}",
                )

            # Set sidechain input
            sidechain_result = mcp.set_sidechain_input(
                target_track=target_track,
                device_index=0,  # Compressor just loaded
                source_track=source_track,
            )
            if not sidechain_result.success:
                return AgentResult(
                    success=False,
                    message=(
                        f"Failed to set sidechain input: {sidechain_result.message}"
                    ),
                )

            # Configure compressor parameters
            params_to_set = [
                ("Ratio", self._ratio_to_value(ratio)),
                ("Attack", attack_ms),
                ("Release", self._release_to_value(release)),
                ("Threshold", threshold_db),
            ]

            for param_name, value in params_to_set:
                param_result = mcp.set_device_parameter(
                    track_name=target_track,
                    device_index=0,
                    parameter_name=param_name,
                    value=value,
                )
                if not param_result.success:
                    self.log(
                        f"Warning: Failed to set {param_name}: {param_result.message}"
                    )

            self.log(f"Configured sidechain: {target_track} → {source_track}")
            return AgentResult(
                success=True,
                message="Configured sidechain compression",
                data={
                    "source_track": source_track,
                    "target_track": target_track,
                    "ratio": ratio,
                    "attack_ms": attack_ms,
                    "release": release,
                    "threshold_db": threshold_db,
                },
            )

        except Exception as e:
            self.log(f"Error setting up sidechain: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def _ratio_to_value(self, ratio: str) -> float:
        """Convert ratio string to parameter value."""
        if ratio == "infinite:1":
            return 1.0  # Max ratio
        # Parse "4:1" format
        try:
            numerator = float(ratio.split(":")[0])
            return min(numerator / 20.0, 1.0)  # Normalize to 0-1
        except Exception:
            return 0.5  # Default mid ratio

    def _release_to_value(self, release: str) -> float:
        """Convert tempo-synced release to parameter value."""
        release_map = {
            "1/4n": 0.25,
            "1/8n": 0.5,
            "1/16n": 0.75,
            "1/32n": 0.9,
        }
        return release_map.get(release, 0.5)

    async def execute(self, **kwargs) -> AgentResult:
        """Execute sidechain setup for multiple tracks.

        Args:
            sidechains: List of {source, target, preset/params} dicts

        Returns:
            AgentResult with all configured sidechains
        """
        sidechains = kwargs.get("sidechains", [])
        results = []
        errors = []

        for sc in sidechains:
            result = self.setup_sidechain(**sc)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        return AgentResult(
            success=len(errors) == 0,
            message=f"Configured {len(results)} sidechains",
            data={"sidechains": results},
            errors=errors,
        )
