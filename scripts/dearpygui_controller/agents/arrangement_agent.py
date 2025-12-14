"""Arrangement Agent for clip and scene management in session view.

Reference: Ableton Manual Section 16.1 "The Launch Controls" (page 340)
Reference: Ableton Manual Section 7.4.3 "Editing Scenes" (page 176)
"""

from ..config import TRACKS
from .base_agent import AgentResult, BaseAgent


class ArrangementAgent(BaseAgent):
    """Agent for arranging track structure and energy flow.

    Specializes in:
    - 16-bar phrasing block structure
    - Intro/Development/Breakdown/Drop sections
    - Track muting/unmuting for arrangement
    - Energy management throughout track
    - DJ-friendly mixing intro/outro
    """

    def __init__(self, **kwargs):
        super().__init__(name="ArrangementAgent", **kwargs)

    def get_role(self) -> str:
        return "Arrangement Architect"

    def get_goal(self) -> str:
        return "Structure track with functional DJ-friendly arrangement"

    def get_arrangement_structure(self) -> dict:
        """Get the arrangement structure based on spec.

        Returns timeline structure with sections and active tracks.
        """
        return {
            "bpm": 136,
            "total_bars": 140,  # ~6 minutes
            "sections": [
                {
                    "name": "Intro",
                    "start_bar": 0,
                    "end_bar": 16,
                    "description": (
                        "Stripped back for mixing - Kick, Rumble, Closed Hats"
                    ),
                    "active_tracks": [0, 1, 4],  # Kick, Rumble, Closed Hats
                    "energy": "contained",
                },
                {
                    "name": "Development",
                    "start_bar": 16,
                    "end_bar": 48,
                    "description": (
                        "Introduce Rolling Bass, Percussion, Vocal fragments"
                    ),
                    "active_tracks": [0, 1, 2, 4, 5, 7, 8, 13],
                    "energy": "building",
                },
                {
                    "name": "Breakdown 1",
                    "start_bar": 48,
                    "end_bar": 64,
                    "description": (
                        "Energy reset - Remove kick, filter bass, "
                        "intro main vocal and drone"
                    ),
                    "active_tracks": [
                        2,
                        4,
                        10,
                        11,
                        12,
                        14,
                    ],  # Bass, Hats, Stabs, Drone, Vocal, Riser
                    "energy": "tension",
                },
                {
                    "name": "Drop 1",
                    "start_bar": 64,
                    "end_bar": 96,
                    "description": "Full energy - All elements firing",
                    "active_tracks": [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 15],
                    "energy": "peak",
                },
                {
                    "name": "Bridge/Breakdown 2",
                    "start_bar": 96,
                    "end_bar": 112,
                    "description": "Minimal - Focus on Acid modulation and Glitch",
                    "active_tracks": [3, 4, 8, 11],  # Acid, Hats, Glitch, Drone
                    "energy": "minimal",
                },
                {
                    "name": "Main Drop",
                    "start_bar": 112,
                    "end_bar": 128,
                    "description": "Maximum intensity - All tracks",
                    "active_tracks": list(range(16)),  # All tracks
                    "energy": "maximum",
                },
                {
                    "name": "Outro",
                    "start_bar": 128,
                    "end_bar": 140,
                    "description": "Strip elements - Kick and Rumble last for DJ mixout",
                    "active_tracks": [0, 1],
                    "energy": "outro",
                },
            ],
        }

    def get_clip_positions(self, section: dict) -> dict:
        """Get clip positions for all tracks in a section.

        Args:
            section: Section configuration

        Returns:
            Dictionary mapping track indices to clip start positions
        """
        positions = {}

        for track_idx in section["active_tracks"]:
            positions[track_idx] = {
                "clip_slot": 0,  # Scene 0
                "length_bars": (section["end_bar"] - section["start_bar"]),
            }

        return positions

    async def create_arrangement_markers(
        self,
        structure: dict,
    ) -> tuple[bool, list[str]]:
        """Create arrangement locator markers in Ableton.

        Args:
            structure: Arrangement structure

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        mcp = self.get_mcp_client()

        if not mcp:
            self.log("Mock: Creating arrangement markers")
            return True, []

        for section in structure["sections"]:
            self.log(f"Creating marker for {section['name']}...")

            # Create locator if MCP supports it
            if hasattr(mcp, "create_locator"):
                result = mcp.create_locator(
                    name=f"{section['name']} ({section['energy']})",
                    bar=section["start_bar"],
                )
                if not result.success:
                    errors.append(f"Failed to create marker: {result.message}")
            else:
                self.log("Locator creation not supported")

        return len(errors) == 0, errors

    async def apply_section_automation(
        self,
        section: dict,
    ) -> tuple[bool, list[str]]:
        """Apply track muting/unmuting for a section.

        Args:
            section: Section configuration

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        mcp = self.get_mcp_client()

        if not mcp:
            self.log(f"Mock: Applying automation for {section['name']}")
            return True, []

        # Get all track indices
        all_tracks = set(range(len(TRACKS)))
        active_tracks = set(section["active_tracks"])
        muted_tracks = all_tracks - active_tracks

        # Unmute active tracks
        for track_idx in active_tracks:
            if hasattr(mcp, "set_track_mute"):
                result = mcp.set_track_mute(
                    track_index=track_idx,
                    muted=False,
                )
                if not result.success:
                    errors.append(f"Failed to unmute track {track_idx}")

        # Mute inactive tracks
        for track_idx in muted_tracks:
            if hasattr(mcp, "set_track_mute"):
                result = mcp.set_track_mute(
                    track_index=track_idx,
                    muted=True,
                )
                if not result.success:
                    errors.append(f"Failed to mute track {track_idx}")

        return len(errors) == 0, errors

    def configure_clip_launch_settings(
        self,
        track_index: int,
        clip_index: int,
        launch_mode: str,
        quantization: str | None = None,
        follow_action_a: str | None = None,
        follow_action_time: float | None = None,
    ) -> AgentResult:
        """Configure clip launch settings.

        Reference: Ableton Manual Section 16.1 "The Launch Controls" (page 340)

        Args:
            track_index: Track index
            clip_index: Clip index
            launch_mode: Launch mode (trigger, gate, toggle, repeat)
            quantization: Optional quantization setting (e.g., "1 Bar", "1 Beat")
            follow_action_a: Optional follow action (e.g., "Next", "Previous", "Stop")
            follow_action_time: Optional follow action time in bars

        Returns:
            AgentResult with success status
        """
        # Validate launch mode
        valid_modes = ["trigger", "gate", "toggle", "repeat"]
        if launch_mode not in valid_modes:
            return AgentResult(
                success=False,
                message=f"Invalid launch mode: {launch_mode}. Must be one of {valid_modes}",
            )

        mcp = self.get_mcp_client()
        if not mcp:
            self.log(
                f"Mock: Configuring clip launch settings for track "
                f"{track_index}, clip {clip_index}"
            )
            return AgentResult(
                success=True,
                message=f"Mock: Configured clip launch mode to {launch_mode}",
                data={
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "launch_mode": launch_mode,
                },
            )

        try:
            # Set launch mode
            result = mcp.set_clip_launch_mode(
                track_index=track_index, clip_index=clip_index, mode=launch_mode
            )

            if not result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to set launch mode: {result.message}",
                )

            # Set quantization if provided
            if quantization:
                quant_result = mcp.set_clip_quantization(
                    track_index=track_index,
                    clip_index=clip_index,
                    quantization=quantization,
                )
                if not quant_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set quantization: {quant_result.message}",
                    )

            # Set follow action if provided
            if follow_action_a:
                follow_result = mcp.set_follow_action(
                    track_index=track_index,
                    clip_index=clip_index,
                    action_a=follow_action_a,
                    time=follow_action_time or 4.0,
                )
                if not follow_result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to set follow action: {follow_result.message}",
                    )

            self.log(
                f"Configured clip launch mode to {launch_mode} for track "
                f"{track_index}, clip {clip_index}"
            )
            return AgentResult(
                success=True,
                message=f"Configured clip launch mode to {launch_mode}",
                data={
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "launch_mode": launch_mode,
                    "quantization": quantization,
                    "follow_action": follow_action_a,
                },
            )

        except Exception as e:
            self.log(f"Error configuring clip launch settings: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def configure_scene_launch(
        self, scene_index: int, launch_mode: str = "immediate"
    ) -> AgentResult:
        """Configure scene launch behavior.

        Reference: Ableton Manual Section 7.4.3 "Editing Scenes" (page 176)

        Args:
            scene_index: Scene index
            launch_mode: Launch mode (immediate, quantized)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Configuring scene {scene_index} launch mode")
            return AgentResult(
                success=True,
                message=(
                    f"Mock: Configured scene {scene_index} launch mode to {launch_mode}"
                ),
            )

        try:
            result = mcp.set_scene_launch_mode(
                scene_index=scene_index, mode=launch_mode
            )

            if result.success:
                self.log(f"Configured scene {scene_index} launch mode to {launch_mode}")

            return result

        except Exception as e:
            self.log(f"Error configuring scene launch: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(
        self,
        mode: str = "full",
        **kwargs,
    ) -> AgentResult:
        """Create arrangement structure.

        Args:
            mode: "markers" (just markers), "automation" (just muting), "full" (both)

        Returns:
            AgentResult with arrangement results
        """
        arrangement_created = []
        all_errors = []

        structure = self.get_arrangement_structure()

        self.log(f"Creating {len(structure['sections'])} section arrangement...")

        # Create markers
        if mode in ["markers", "full"]:
            try:
                success, errors = await self.create_arrangement_markers(structure)
                if success:
                    arrangement_created.append(
                        {
                            "type": "markers",
                            "count": len(structure["sections"]),
                        }
                    )
                else:
                    all_errors.extend(errors)
            except Exception as e:
                all_errors.append(f"Marker creation error: {e}")

        # Apply section automation
        if mode in ["automation", "full"]:
            for section in structure["sections"]:
                try:
                    success, errors = await self.apply_section_automation(section)
                    if success:
                        arrangement_created.append(
                            {
                                "type": "section",
                                "name": section["name"],
                                "tracks": len(section["active_tracks"]),
                                "energy": section["energy"],
                            }
                        )
                    else:
                        all_errors.extend(errors)
                except Exception as e:
                    all_errors.append(f"Section automation error: {e}")

        # Generate summary
        summary = {
            "total_bars": structure["total_bars"],
            "sections": len(structure["sections"]),
            "bpm": structure["bpm"],
            "duration_minutes": (structure["total_bars"] * 4 / structure["bpm"])
            * 60
            / 4,
        }

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Created arrangement with {len(structure['sections'])} sections",
            data={
                "arrangement": arrangement_created,
                "summary": summary,
            },
            errors=all_errors,
        )
