"""Automation Agent for parameter automation and envelopes.

Reference: Ableton Manual Section 4.6 "Working with Automation" (page 116)


Reference: Ableton Manual Section 40.5.1 "Navigating Breakpoints" (page 927)
Reference: Ableton Manual Section 6.1 "Arrangement View" (page 145)
"""

from .base_agent import AgentResult, BaseAgent


class AutomationAgent(BaseAgent):
    """Agent for parameter automation and envelopes.

    Specializes in:
    - Filter cutoff sweeps
    - Parameter automation with breakpoints
    - Envelope curves (linear, exponential, logarithmic)
    """

    def __init__(self, **kwargs):
        super().__init__(name="AutomationAgent", **kwargs)

    def get_role(self) -> str:
        return "Automation and Modulation Engineer"

    def get_goal(self) -> str:
        return "Create parameter automation for dynamics and movement"

    def create_filter_sweep(
        self,
        track_name: str,
        device_index: int = 0,
        start_freq: float = 200,
        end_freq: float = 8000,
        duration_bars: int = 16,
        curve: str = "linear",
    ) -> AgentResult:
        """Create filter cutoff sweep automation.

        Reference: Ableton Manual Section 40.5.1 "Navigating Breakpoints" (page 927)

        Args:
            track_name: Target track name
            device_index: Device index
            start_freq: Starting frequency (Hz)
            end_freq: Ending frequency (Hz)
            duration_bars: Duration in bars
            curve: Curve type ("linear", "exponential", "logarithmic")

        Returns:
            AgentResult with automation details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Filter sweep {track_name} {start_freq}->{end_freq}Hz")
            return AgentResult(
                success=True,
                message="Mock: Created filter sweep",
                data={
                    "track_name": track_name,
                    "start_freq": start_freq,
                    "end_freq": end_freq,
                    "duration_bars": duration_bars,
                },
            )

        try:
            # Normalize frequencies to 0-1 range (assuming 20Hz-20kHz)
            start_norm = (start_freq - 20) / 19980
            end_norm = (end_freq - 20) / 19980

            # Create automation
            auto_result = mcp.create_automation(
                track_name=track_name,
                device_index=device_index,
                parameter="Cutoff",
                start_value=start_norm,
                end_value=end_norm,
                duration_bars=duration_bars,
                curve=curve,
            )
            if not auto_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to create automation: {auto_result.message}",
                )

            self.log(
                f"Created filter sweep {track_name}: "
                f"{start_freq}Hz -> {end_freq}Hz over {duration_bars} bars"
            )
            return AgentResult(
                success=True,
                message="Created filter sweep",
                data={
                    "track_name": track_name,
                    "start_freq": start_freq,
                    "end_freq": end_freq,
                    "duration_bars": duration_bars,
                    "curve": curve,
                },
            )

        except Exception as e:
            self.log(f"Error creating filter sweep: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def create_automation(
        self,
        track_name: str,
        parameter: str,
        breakpoints: list[tuple[float, float]],
        device_index: int = 0,
        curve: str = "linear",
    ) -> AgentResult:
        """Create automation with custom breakpoints.

        Reference: Ableton Manual Section 40.5.1 "Navigating Breakpoints" (page 927)

        Args:
            track_name: Target track name
            parameter: Parameter name (e.g., "Cutoff", "Roar Drive")
            breakpoints: List of (bar_position, value) tuples
            device_index: Device index
            curve: Curve type between breakpoints

        Returns:
            AgentResult with automation details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Automation {track_name}.{parameter}")
            return AgentResult(
                success=True,
                message=f"Mock: Created automation with {len(breakpoints)} breakpoints",
                data={
                    "track_name": track_name,
                    "parameter": parameter,
                    "breakpoints": breakpoints,
                },
            )

        try:
            # Create automation with breakpoints
            auto_result = mcp.create_automation_with_breakpoints(
                track_name=track_name,
                device_index=device_index,
                parameter=parameter,
                breakpoints=breakpoints,
                curve=curve,
            )
            if not auto_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to create automation: {auto_result.message}",
                )

            self.log(
                f"Created automation {track_name}.{parameter} "
                f"with {len(breakpoints)} breakpoints"
            )
            return AgentResult(
                success=True,
                message=f"Created automation with {len(breakpoints)} breakpoints",
                data={
                    "track_name": track_name,
                    "parameter": parameter,
                    "breakpoints": breakpoints,
                    "curve": curve,
                },
            )

        except Exception as e:
            self.log(f"Error creating automation: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(self, **kwargs) -> AgentResult:
        """Execute automation tasks.

        Args:
            filter_sweeps: List of {track, start_freq, end_freq, duration} dicts
            automations: List of {track, parameter, breakpoints} dicts

        Returns:
            AgentResult with all created automations
        """
        filter_sweeps = kwargs.get("filter_sweeps", [])
        automations = kwargs.get("automations", [])
        results = []
        errors = []

        # Create filter sweeps
        for sweep in filter_sweeps:
            result = self.create_filter_sweep(**sweep)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        # Create custom automations
        for auto in automations:
            result = self.create_automation(**auto)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        return AgentResult(
            success=len(errors) == 0,
            message=f"Created {len(results)} automations",
            data={"configurations": results},
            errors=errors,
        )
