"""Return Track Agent for return track and send management.

Reference: Ableton Manual Section 18.4 "Return Tracks" (page 381)
Reference: Ableton Manual Section 18.1 "The Live Mixer - Sends" (page 376)
"""

from .base_agent import AgentResult, BaseAgent


class ReturnTrackAgent(BaseAgent):
    """Agent for return track and send management.

    Specializes in:
    - Creating reverb/delay return tracks
    - Setting send levels
    - Automating sends for transitions
    """

    def __init__(self, **kwargs):
        super().__init__(name="ReturnTrackAgent", **kwargs)

    def get_role(self) -> str:
        return "Return Track and Send Engineer"

    def get_goal(self) -> str:
        return "Configure return tracks and send routing for spatial effects"

    def create_return_track(
        self,
        name: str,
        device: str = "Reverb",
        preset: str | None = None,
    ) -> AgentResult:
        """Create return track with specified effect device.

        Reference: Ableton Manual Section 18.4 "Return Tracks" (page 381)

        Args:
            name: Return track name
            device: Effect device to load
            preset: Device preset name (optional)

        Returns:
            AgentResult with return track details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Create return track {name} with {device}")
            return AgentResult(
                success=True,
                message=f"Mock: Created return track {name}",
                data={"name": name, "device": device, "preset": preset},
            )

        try:
            # Create return track
            create_result = mcp.create_return_track(name=name)
            if not create_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to create return track: {create_result.message}",
                )

            # Load effect device
            device_result = mcp.load_device(track_name=name, device_name=device)
            if not device_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to load {device}: {device_result.message}",
                )

            # Load preset if specified
            if preset:
                preset_result = mcp.load_preset(
                    track_name=name, device_index=0, preset_name=preset
                )
                if not preset_result.success:
                    self.log(f"Warning: Failed to load preset: {preset_result.message}")

            self.log(f"Created return track {name} with {device}")
            return AgentResult(
                success=True,
                message=f"Created return track {name}",
                data={"name": name, "device": device, "preset": preset},
            )

        except Exception as e:
            self.log(f"Error creating return track: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def set_send_level(
        self,
        track_name: str,
        return_track: str,
        send_level: float = 0.5,
    ) -> AgentResult:
        """Set send level from track to return track.

        Reference: Ableton Manual Section 18.1 "The Live Mixer - Sends" (page 376)

        Args:
            track_name: Source track name
            return_track: Return track name or index
            send_level: Send level (0.0-1.0)

        Returns:
            AgentResult with send configuration
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Set send {track_name} → {return_track}")
            return AgentResult(
                success=True,
                message=f"Mock: Set send level to {send_level}",
                data={
                    "track_name": track_name,
                    "return_track": return_track,
                    "send_level": send_level,
                },
            )

        try:
            # Set send level
            send_result = mcp.set_send_level(
                track_name=track_name,
                return_track=return_track,
                level=send_level,
            )
            if not send_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to set send level: {send_result.message}",
                )

            self.log(f"Set send {track_name} → {return_track}: {send_level * 100:.0f}%")
            return AgentResult(
                success=True,
                message=f"Set send level to {send_level}",
                data={
                    "track_name": track_name,
                    "return_track": return_track,
                    "send_level": send_level,
                },
            )

        except Exception as e:
            self.log(f"Error setting send level: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def automate_send(
        self,
        track_name: str,
        return_track: str,
        start_value: float = 0.0,
        end_value: float = 1.0,
        duration_bars: int = 8,
    ) -> AgentResult:
        """Automate send level over time for transitions.

        Reference: Ableton Manual Section 18.1 "The Live Mixer - Sends" (page 376)

        Args:
            track_name: Source track name
            return_track: Return track name
            start_value: Starting send level (0.0-1.0)
            end_value: Ending send level (0.0-1.0)
            duration_bars: Duration in bars

        Returns:
            AgentResult with automation details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Automate send {track_name} → {return_track}")
            return AgentResult(
                success=True,
                message=f"Mock: Automated send {start_value} → {end_value}",
                data={
                    "track_name": track_name,
                    "return_track": return_track,
                    "start_value": start_value,
                    "end_value": end_value,
                    "duration_bars": duration_bars,
                },
            )

        try:
            # Create automation envelope
            automation_result = mcp.create_automation(
                track_name=track_name,
                parameter=f"Send {return_track}",
                start_value=start_value,
                end_value=end_value,
                duration_bars=duration_bars,
            )
            if not automation_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to create automation: {automation_result.message}",
                )

            self.log(
                f"Automated send {track_name} → {return_track} "
                f"over {duration_bars} bars"
            )
            return AgentResult(
                success=True,
                message=f"Automated send over {duration_bars} bars",
                data={
                    "track_name": track_name,
                    "return_track": return_track,
                    "start_value": start_value,
                    "end_value": end_value,
                    "duration_bars": duration_bars,
                },
            )

        except Exception as e:
            self.log(f"Error automating send: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(self, **kwargs) -> AgentResult:
        """Execute return track and send configuration tasks.

        Args:
            return_tracks: List of {name, device, preset} dicts
            sends: List of {track, return_track, level} dicts
            automations: List of {track, return_track, start, end, duration} dicts

        Returns:
            AgentResult with all configurations
        """
        return_tracks = kwargs.get("return_tracks", [])
        sends = kwargs.get("sends", [])
        automations = kwargs.get("automations", [])
        results = []
        errors = []

        # Create return tracks
        for rt in return_tracks:
            result = self.create_return_track(**rt)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        # Set send levels
        for send in sends:
            result = self.set_send_level(**send)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        # Create send automations
        for auto in automations:
            result = self.automate_send(**auto)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        return AgentResult(
            success=len(errors) == 0,
            message=f"Configured {len(results)} return tracks/sends",
            data={"configurations": results},
            errors=errors,
        )
