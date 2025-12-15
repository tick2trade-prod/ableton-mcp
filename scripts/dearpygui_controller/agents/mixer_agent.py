"""Mixer Agent for mixer routing and level management.

Reference: Ableton Manual Section 17.7 "Monitoring" (page 366)
"""

from ..config import TRACKS, TrackConfig
from .base_agent import AgentResult, BaseAgent

# Device chains per track type
DEVICE_CHAINS: dict[str, list[dict]] = {
    "kick": [
        {"name": "Drum Sampler", "params": {}},
        {"name": "Channel EQ", "params": {}},
        {"name": "Saturator", "params": {"drive": 3.0}},
    ],
    "rumble": [
        {"name": "Reverb", "params": {"decay": 0.6, "dry_wet": 1.0}},
        {"name": "Roar", "params": {"drive": 6.0}, "fallback": "Saturator"},
        {"name": "EQ Eight", "params": {"high_cut": 150}},
        {"name": "Compressor", "params": {"sidechain": True}},
    ],
    "bass": [
        {"name": "Operator", "params": {}},
        {"name": "Channel EQ", "params": {}},
        {"name": "Compressor", "params": {"ratio": 4.0}},
    ],
    "hihat": [
        {"name": "Drum Sampler", "params": {}},
        {"name": "Channel EQ", "params": {}},
    ],
    "clap": [
        {"name": "Drum Sampler", "params": {}},
        {"name": "Reverb", "params": {"decay": 0.3}},
    ],
    "synth": [
        {"name": "Wavetable", "params": {}},
        {"name": "Echo", "params": {}},
        {"name": "Reverb", "params": {}},
    ],
    "fx": [
        {"name": "Operator", "params": {}},
        {"name": "Auto Filter", "params": {}},
    ],
}

# Volume levels per track (in dB)
VOLUME_LEVELS: dict[str, float] = {
    "kick": -6.0,
    "rumble": -12.0,
    "bass": -9.0,
    "hihat": -18.0,
    "clap": -12.0,
    "synth": -15.0,
    "fx": -18.0,
}


class MixerAgent(BaseAgent):
    """Agent for mixing and applying effects.

    Loads device chains and sets volume levels
    appropriate for Peak Time Techno.
    """

    def __init__(self, **kwargs):
        super().__init__(name="MixerAgent", **kwargs)

    def get_role(self) -> str:
        return "Mix Engineer"

    def get_goal(self) -> str:
        return "Balance levels and apply effects chains"

    def get_chain_for_track(self, track: TrackConfig) -> list[dict]:
        """Get device chain for track type."""
        name_lower = track.name.lower()

        if "kick" in name_lower:
            return DEVICE_CHAINS.get("kick", [])
        elif "rumble" in name_lower:
            return DEVICE_CHAINS.get("rumble", [])
        elif "bass" in name_lower:
            return DEVICE_CHAINS.get("bass", [])
        elif "hat" in name_lower:
            return DEVICE_CHAINS.get("hihat", [])
        elif "clap" in name_lower or "snare" in name_lower:
            return DEVICE_CHAINS.get("clap", [])
        elif "synth" in name_lower or "drone" in name_lower:
            return DEVICE_CHAINS.get("synth", [])
        elif "riser" in name_lower or "impact" in name_lower:
            return DEVICE_CHAINS.get("fx", [])
        else:
            return []

    def get_volume_for_track(self, track: TrackConfig) -> float:
        """Get volume level for track type."""
        name_lower = track.name.lower()

        if "kick" in name_lower:
            return VOLUME_LEVELS.get("kick", -6.0)
        elif "rumble" in name_lower:
            return VOLUME_LEVELS.get("rumble", -12.0)
        elif "bass" in name_lower:
            return VOLUME_LEVELS.get("bass", -9.0)
        elif "hat" in name_lower:
            return VOLUME_LEVELS.get("hihat", -18.0)
        elif "clap" in name_lower:
            return VOLUME_LEVELS.get("clap", -12.0)
        elif "synth" in name_lower:
            return VOLUME_LEVELS.get("synth", -15.0)
        else:
            return VOLUME_LEVELS.get("fx", -18.0)

    async def apply_chain_to_track(
        self,
        track: TrackConfig,
    ) -> tuple[bool, list[str]]:
        """Apply device chain to a single track.

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        chain = self.get_chain_for_track(track)

        if not chain:
            return True, []  # No chain needed

        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Loading {len(chain)} devices for {track.name}")
            return True, []

        for device_spec in chain:
            device_name = device_spec["name"]
            fallback = device_spec.get("fallback")

            self.log(f"Loading {device_name} on {track.name}...")

            result = mcp.load_device(
                track_index=track.index,
                device_name=device_name,
                fallback=fallback,
            )

            if not result.success:
                errors.append(f"Failed to load {device_name}: {result.message}")

        return len(errors) == 0, errors

    def configure_submix_routing(
        self,
        source_tracks: list[int],
        group_track_index: int,
    ) -> AgentResult:
        """Configure submix/group track routing.

        Reference: Ableton Manual Section 17.7 "Monitoring" (page 366)

        Args:
            source_tracks: List of source track indices
            group_track_index: Group/submix track index

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(
                f"Mock: Routing {len(source_tracks)} tracks to group {group_track_index}"
            )
            return AgentResult(
                success=True,
                message="Mock: Configured submix routing",
                data={"source_tracks": source_tracks, "group": group_track_index},
            )

        try:
            for track_idx in source_tracks:
                result = mcp.set_track_routing(
                    track_index=track_idx, output_target=group_track_index
                )
                if not result.success:
                    return AgentResult(
                        success=False,
                        message=f"Failed to route track {track_idx}: {result.message}",
                    )

            self.log(f"Routed {len(source_tracks)} tracks to group {group_track_index}")
            return AgentResult(
                success=True,
                message="Configured submix routing",
                data={"source_tracks": source_tracks, "group": group_track_index},
            )

        except Exception as e:
            self.log(f"Error configuring submix routing: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(
        self,
        track_index: int | None = None,
        **kwargs,
    ) -> AgentResult:
        """Apply effects and mixing to tracks.

        Args:
            track_index: Specific track to mix (None = all)

        Returns:
            AgentResult with mixing results
        """
        tracks_mixed = []
        all_errors = []

        # Get tracks to process
        if track_index is not None:
            tracks = [TRACKS[track_index]]
        else:
            tracks = TRACKS

        for track in tracks:
            self.log(f"Mixing {track.name}...")

            try:
                success, errors = await self.apply_chain_to_track(track)

                if success:
                    tracks_mixed.append(
                        {
                            "track": track.name,
                            "devices": len(self.get_chain_for_track(track)),
                            "volume_db": self.get_volume_for_track(track),
                        }
                    )
                    self.update_progress(track.index, 1.0)
                else:
                    all_errors.extend(errors)

            except Exception as e:
                all_errors.append(f"{track.name}: {e}")
                self.log(f"Error on {track.name}: {e}")

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Mixed {len(tracks_mixed)} tracks",
            data={"tracks": tracks_mixed},
            errors=all_errors,
        )
