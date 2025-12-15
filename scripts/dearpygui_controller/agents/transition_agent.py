"""Transition Agent for crossfades and transition effects.

Reference: Ableton Manual Section 20.4.2 "Fade and Crossfade Editing" (page 396)
"""

from ..config import TRACKS
from .base_agent import AgentResult, BaseAgent


class TransitionAgent(BaseAgent):
    """Agent for creating transitions and energy changes.

    Specializes in:
    - Risers/White Noise builds (Track 15)
    - Impacts/Downlifters for drops (Track 16)
    - Filter automation for tension/release
    - Stereo width expansion during builds
    - Sidechain pumping for rhythmic intensity
    """

    def __init__(self, **kwargs):
        super().__init__(name="TransitionAgent", **kwargs)

    def get_role(self) -> str:
        return "Transition Designer"

    def get_goal(self) -> str:
        return "Create tension and release transitions for 16-bar phrasing blocks"

    def get_riser_config(self) -> dict:
        """Get configuration for Risers/White Noise (Track 15).

        Creates building tension before a drop using white noise
        with filter automation and stereo widening.
        """
        return {
            "devices": [
                {
                    "name": "Operator",
                    "params": {
                        "osc_a_wave": "White Noise",
                        "osc_a_level": 1.0,
                        "amp_attack": 0.5,
                        "amp_sustain": 1.0,
                        "amp_release": 0.5,
                    },
                },
                {
                    "name": "Auto Filter",
                    "params": {
                        "filter_type": "Bandpass",
                        "frequency": 200,  # Starting point
                        "resonance": 0.5,
                    },
                },
                {
                    "name": "Compressor",
                    "params": {
                        "sidechain": True,
                        "sidechain_source": "Track 0",  # Kick
                        "threshold": -24,
                        "ratio": "Inf:1",
                        "attack": 0.0001,
                        "release": "1/8",  # Synced to tempo
                    },
                },
                {
                    "name": "Utility",
                    "params": {
                        "width": 140,  # Start at 140%
                    },
                },
            ],
            "automation": [
                {
                    "device": "Auto Filter",
                    "parameter": "frequency",
                    "start_value": 200,
                    "end_value": 15000,
                    "duration_bars": 16,  # Over 16 bars
                    "curve": "exponential",
                },
                {
                    "device": "Utility",
                    "parameter": "width",
                    "start_value": 140,
                    "end_value": 200,
                    "duration_bars": 16,
                    "curve": "linear",
                },
            ],
        }

    def get_impact_config(self) -> dict:
        """Get configuration for Impacts/Downlifters (Track 16).

        Creates powerful impact at the drop using heavy industrial
        crash with long reverb tail processed through Roar.
        """
        return {
            "devices": [
                {
                    "name": "Drum Sampler",
                    "params": {
                        "sample": "Crash Heavy",
                        "pitch": -7,  # Lower pitch for weight
                        "decay": 2.0,
                        "transpose": -12,
                    },
                },
                {
                    "name": "Reverb",
                    "params": {
                        "decay": 8.0,  # Very long tail
                        "pre_delay": 0.01,
                        "dry_wet": 0.7,
                    },
                },
                {
                    "name": "Echo",
                    "params": {
                        "time_l": "1/4",
                        "time_r": "1/4D",  # Dotted quarter (ping pong)
                        "feedback": 0.6,
                        "dry_wet": 0.4,
                    },
                },
                {
                    "name": "Roar",
                    "fallback": "Saturator",
                    "params": {
                        "drive": 8.0,
                        "feedback": 0.2,
                        "dry_wet": 0.3,
                    },
                },
            ],
        }

    def generate_riser_clip(self, bars: int = 16) -> dict:
        """Generate a riser clip (sustained note over bars)."""
        return {
            "notes": [
                {
                    "pitch": 60,  # C3
                    "start_time": 0.0,
                    "duration": float(bars * 4),  # Full length
                    "velocity": 100,
                }
            ],
        }

    def generate_impact_clip(self) -> dict:
        """Generate an impact clip (single hit at bar 1)."""
        return {
            "notes": [
                {
                    "pitch": 36,  # C1 (Kick/Crash range)
                    "start_time": 0.0,
                    "duration": 0.1,
                    "velocity": 127,
                }
            ],
        }

    def configure_fade_curve(
        self,
        track_index: int,
        clip_index: int,
        fade_in: float = 0.0,
        fade_out: float = 0.0,
        curve_type: str = "linear",
    ) -> AgentResult:
        """Configure clip fade curves.

        Reference: Ableton Manual Section 20.4.2 "Fade and Crossfade Editing" (page 396)

        Args:
            track_index: Track index
            clip_index: Clip index
            fade_in: Fade in duration in beats
            fade_out: Fade out duration in beats
            curve_type: Curve type (linear, exponential, logarithmic)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(
                f"Mock: Configuring fade for clip {clip_index} on track {track_index}"
            )
            return AgentResult(
                success=True,
                message="Mock: Configured fade curve",
                data={"fade_in": fade_in, "fade_out": fade_out, "curve": curve_type},
            )

        try:
            result = mcp.set_clip_fade(
                track_index=track_index,
                clip_index=clip_index,
                fade_in=fade_in,
                fade_out=fade_out,
                curve_type=curve_type,
            )

            if result.success:
                self.log(f"Configured fade curve: in={fade_in}, out={fade_out}")

            return result

        except Exception as e:
            self.log(f"Error configuring fade curve: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def configure_transition_track(
        self,
        track_index: int,
        config: dict,
    ) -> tuple[bool, list[str]]:
        """Configure a transition track with devices and automation.

        Args:
            track_index: Track to configure
            config: Configuration with devices and automation

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        track = TRACKS[track_index]
        mcp = self.get_mcp_client()

        if not mcp:
            self.log(f"Mock: Configuring transition track {track.name}")
            return True, []

        # Load devices
        for device_spec in config["devices"]:
            device_name = device_spec["name"]
            fallback = device_spec.get("fallback")
            params = device_spec.get("params", {})

            self.log(f"Loading {device_name} on {track.name}...")

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
                    device_index=-1,
                    parameter_name=param_name,
                    value=value,
                )
                if not param_result.success:
                    errors.append(f"Failed to set {param_name}")

        # Create automation (if supported)
        if "automation" in config and hasattr(mcp, "create_automation"):
            for auto in config["automation"]:
                self.log(f"Creating automation for {auto['parameter']}...")
                auto_result = mcp.create_automation(
                    track_index=track_index,
                    device_name=auto["device"],
                    parameter_name=auto["parameter"],
                    start_value=auto["start_value"],
                    end_value=auto["end_value"],
                    duration_bars=auto["duration_bars"],
                    curve=auto.get("curve", "linear"),
                )
                if not auto_result.success:
                    errors.append(f"Failed to create automation: {auto_result.message}")

        return len(errors) == 0, errors

    async def execute(
        self,
        track_index: int | None = None,
        **kwargs,
    ) -> AgentResult:
        """Configure transition tracks with effects and automation.

        Args:
            track_index: Specific track to configure (None = all transition tracks)

        Returns:
            AgentResult with configuration results
        """
        transitions_configured = []
        all_errors = []

        # Transition track configurations
        transition_configs = {
            14: {  # Track 15: Riser
                "config": self.get_riser_config(),
                "clip": self.generate_riser_clip(),
                "type": "Riser",
            },
            15: {  # Track 16: Impact
                "config": self.get_impact_config(),
                "clip": self.generate_impact_clip(),
                "type": "Impact",
            },
        }

        # Get tracks to process
        if track_index is not None:
            if track_index in transition_configs:
                tracks_to_process = [(track_index, transition_configs[track_index])]
            else:
                return AgentResult(
                    success=False,
                    message=f"Track {track_index} is not a transition track",
                    errors=[f"No transition config for track {track_index}"],
                )
        else:
            tracks_to_process = list(transition_configs.items())

        mcp = self.get_mcp_client()

        for idx, config in tracks_to_process:
            track = TRACKS[idx]
            self.log(f"Configuring {config['type']}: {track.name}...")

            try:
                # Configure devices and automation
                success, errors = await self.configure_transition_track(
                    idx,
                    config["config"],
                )

                if not success:
                    all_errors.extend(errors)
                    continue

                # Create clip
                if mcp:
                    clip_data = config["clip"]
                    clip_result = mcp.create_clip(
                        track_index=idx,
                        clip_index=0,
                        length=16.0 if config["type"] == "Riser" else 4.0,
                    )
                    if clip_result.success:
                        notes_result = mcp.add_notes_to_clip(
                            track_index=idx,
                            clip_index=0,
                            notes=clip_data["notes"],
                        )
                        if not notes_result.success:
                            all_errors.append(
                                f"Failed to add notes: {notes_result.message}"
                            )

                transitions_configured.append(
                    {
                        "track": track.name,
                        "type": config["type"],
                        "devices": len(config["config"]["devices"]),
                        "automation_count": len(config["config"].get("automation", [])),
                    }
                )
                self.update_progress(track.index, 0.9)

            except Exception as e:
                all_errors.append(f"{track.name}: {e}")
                self.log(f"Error on {track.name}: {e}")

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Configured {len(transitions_configured)} transition tracks",
            data={"transitions": transitions_configured},
            errors=all_errors,
        )
