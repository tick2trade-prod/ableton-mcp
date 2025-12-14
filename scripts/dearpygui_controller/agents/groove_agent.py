"""Groove Agent for groove templates and quantization.

Reference: Ableton Manual Section 13.1.4 "Groove Pool" (page 326)


Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)
Reference: Ableton Manual Section 10.5.12 "Editing Velocities" (page 258)
"""

from .base_agent import AgentResult, BaseAgent


class GrooveAgent(BaseAgent):
    """Agent for groove templates and quantization.

    Specializes in:
    - Applying swing and groove templates
    - Quantization settings
    - Velocity humanization
    """

    # Common groove templates
    GROOVES = {
        "swing_16_99": "Swing 16-99",
        "swing_8_99": "Swing 8-99",
        "mpc_16": "MPC-16",
        "shuffle_16": "Shuffle 16",
    }

    def __init__(self, **kwargs):
        super().__init__(name="GrooveAgent", **kwargs)

    def get_role(self) -> str:
        return "Groove and Quantization Engineer"

    def get_goal(self) -> str:
        return "Apply groove templates and humanization for realistic feel"

    def apply_groove(
        self,
        track_name: str,
        groove_name: str,
        intensity: float = 0.15,
        timing: float = 1.0,
        velocity: float = 0.0,
    ) -> AgentResult:
        """Apply groove template to track/clip.

        Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)

        Args:
            track_name: Target track name
            groove_name: Groove template name
            intensity: Groove intensity (0.0-1.0, typically 0.10-0.20 for techno)
            timing: Timing adjustment (0.0-1.0)
            velocity: Velocity adjustment (0.0-1.0)

        Returns:
            AgentResult with groove configuration details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Apply groove {groove_name} to {track_name}")
            return AgentResult(
                success=True,
                message=f"Mock: Applied groove {groove_name}",
                data={
                    "track_name": track_name,
                    "groove_name": groove_name,
                    "intensity": intensity,
                },
            )

        try:
            # Apply groove to clips
            groove_result = mcp.apply_groove(
                track_name=track_name,
                groove_name=groove_name,
                intensity=intensity,
            )
            if not groove_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to apply groove: {groove_result.message}",
                )

            # Set timing and velocity adjustments if provided
            if timing != 1.0 or velocity != 0.0:
                timing_result = mcp.set_clip_property(
                    track_name=track_name,
                    clip_index=0,
                    property_name="Groove Amount",
                    value=timing,
                )

            self.log(
                f"Applied groove {groove_name} to {track_name} "
                f"with {intensity * 100:.0f}% intensity"
            )
            return AgentResult(
                success=True,
                message=f"Applied groove {groove_name}",
                data={
                    "track_name": track_name,
                    "groove_name": groove_name,
                    "intensity": intensity,
                    "timing": timing,
                    "velocity": velocity,
                },
            )

        except Exception as e:
            self.log(f"Error applying groove: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def quantize_clip(
        self,
        track_name: str,
        clip_index: int = 0,
        quantize_to: str = "1/16",
        amount: float = 1.0,
    ) -> AgentResult:
        """Quantize clip to specific grid.

        Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)

        Args:
            track_name: Target track name
            clip_index: Clip index
            quantize_to: Quantize grid ("1/4", "1/8", "1/16", "1/32")
            amount: Quantization strength (0.0-1.0)

        Returns:
            AgentResult with quantization details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Quantize {track_name} to {quantize_to}")
            return AgentResult(
                success=True,
                message=f"Mock: Quantized to {quantize_to}",
                data={
                    "track_name": track_name,
                    "quantize_to": quantize_to,
                    "amount": amount,
                },
            )

        try:
            # Set quantization grid
            grid_values = {
                "1/4": 0.25,
                "1/8": 0.5,
                "1/16": 0.75,
                "1/32": 1.0,
            }
            grid_value = grid_values.get(quantize_to, 0.75)

            quant_result = mcp.set_clip_property(
                track_name=track_name,
                clip_index=clip_index,
                property_name="Quantization",
                value=grid_value,
            )

            # Set quantization amount
            amount_result = mcp.set_clip_property(
                track_name=track_name,
                clip_index=clip_index,
                property_name="Quantization Amount",
                value=amount,
            )

            self.log(f"Quantized {track_name} to {quantize_to} grid")
            return AgentResult(
                success=True,
                message=f"Quantized to {quantize_to} grid",
                data={
                    "track_name": track_name,
                    "clip_index": clip_index,
                    "quantize_to": quantize_to,
                    "amount": amount,
                },
            )

        except Exception as e:
            self.log(f"Error quantizing clip: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def humanize_velocities(
        self,
        track_name: str,
        clip_index: int = 0,
        random_amount: float = 0.10,
    ) -> AgentResult:
        """Humanize MIDI note velocities.

        Reference: Ableton Manual Section 10.5.12 "Editing Velocities" (page 258)

        Args:
            track_name: Target track name
            clip_index: Clip index
            random_amount: Randomization amount (0.0-1.0, typically 0.05-0.15)

        Returns:
            AgentResult with humanization details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Humanize velocities on {track_name}")
            return AgentResult(
                success=True,
                message="Mock: Humanized velocities",
                data={
                    "track_name": track_name,
                    "random_amount": random_amount,
                },
            )

        try:
            # Apply velocity randomization
            vel_result = mcp.set_clip_property(
                track_name=track_name,
                clip_index=clip_index,
                property_name="Velocity Random",
                value=random_amount,
            )
            if not vel_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to humanize velocities: {vel_result.message}",
                )

            self.log(
                f"Humanized velocities on {track_name} "
                f"with {random_amount * 100:.0f}% randomization"
            )
            return AgentResult(
                success=True,
                message="Humanized velocities",
                data={
                    "track_name": track_name,
                    "clip_index": clip_index,
                    "random_amount": random_amount,
                },
            )

        except Exception as e:
            self.log(f"Error humanizing velocities: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(self, **kwargs) -> AgentResult:
        """Execute groove and quantization tasks.

        Args:
            grooves: List of {track, groove_name, intensity} dicts
            quantize: List of {track, quantize_to, amount} dicts
            humanize: List of {track, random_amount} dicts

        Returns:
            AgentResult with all applied grooves/quantization
        """
        grooves = kwargs.get("grooves", [])
        quantize = kwargs.get("quantize", [])
        humanize = kwargs.get("humanize", [])
        results = []
        errors = []

        # Apply grooves
        for groove in grooves:
            result = self.apply_groove(**groove)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        # Quantize clips
        for quant in quantize:
            result = self.quantize_clip(**quant)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        # Humanize velocities
        for hum in humanize:
            result = self.humanize_velocities(**hum)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        return AgentResult(
            success=len(errors) == 0,
            message=f"Applied {len(results)} groove/quantization settings",
            data={"configurations": results},
            errors=errors,
        )
