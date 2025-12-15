"""Modulation Agent for LFO and modulation configuration.

Reference: Ableton Manual Section 30.13.5 "Modulation Matrix" (page 748)
"""

from ..config import TRACKS
from .base_agent import AgentResult, BaseAgent


class ModulationAgent(BaseAgent):
    """Agent for adding modulation and automation for dynamic movement.

    Specializes in:
    - Filter cutoff automation on Acid Line and Synth Stabs
    - LFO routing for evolving textures
    - Reverb send automation during breakdowns
    - Roar distortion automation on Rumble
    - Auto Pan for rhythmic movement
    - Scale-aware pitch modulation
    """

    def __init__(self, **kwargs):
        super().__init__(name="ModulationAgent", **kwargs)

    def get_role(self) -> str:
        return "Modulation Specialist"

    def get_goal(self) -> str:
        return "Add constant timbral evolution and automation to keep listener engaged"

    def get_acid_modulation(self) -> list[dict]:
        """Get modulation/automation for Acid Line (Track 4).

        Constantly automate filter cutoff to build/release tension.
        This is the primary dynamic element in techno.
        """
        return [
            {
                "type": "automation",
                "device": "Drift",
                "parameter": "Filter Cutoff",
                "pattern": "wave",  # Sine wave automation
                "bars": 8,
                "min_value": 200,  # Hz
                "max_value": 1200,
                "phase": 0,
            },
            {
                "type": "lfo",
                "device": "Drift",
                "lfo_shape": "Random S&H",
                "lfo_rate": "1/16",
                "destination": "Filter Resonance",
                "amount": 0.3,
            },
        ]

    def get_stab_modulation(self) -> list[dict]:
        """Get modulation for Synth Stabs (Track 11).

        Filter automation to create tension during builds.
        """
        return [
            {
                "type": "automation",
                "device": "Wavetable",
                "parameter": "Filter Cutoff",
                "pattern": "ramp",  # Linear ramp up
                "bars": 16,
                "start_value": 400,
                "end_value": 4000,
            },
        ]

    def get_rumble_modulation(self) -> list[dict]:
        """Get modulation for Rumble (Track 2).

        Automate Roar drive to change low-end texture over time.
        """
        return [
            {
                "type": "automation",
                "device": "Roar",
                "parameter": "Drive",
                "pattern": "step",  # Stepped changes every 4 bars
                "bars": 16,
                "values": [4.0, 6.0, 8.0, 6.0],  # 4 steps
            },
            {
                "type": "automation",
                "device": "Roar",
                "parameter": "Mix",
                "pattern": "wave",
                "bars": 8,
                "min_value": 0.3,
                "max_value": 0.7,
            },
        ]

    def get_reverb_send_automation(self) -> dict:
        """Get reverb send automation for breakdowns.

        Increase reverb during breakdowns (bars 32-48)
        to create a 'wash', then cut to 0% at the drop.
        """
        return {
            "type": "send_automation",
            "send": "Reverb",
            "tracks": [6, 7, 8, 9],  # Percussion tracks
            "pattern": "envelope",
            "breakpoints": [
                {"bar": 0, "value": 0.0},
                {"bar": 32, "value": 0.0},  # Start of breakdown
                {"bar": 47, "value": 0.8},  # Build to max
                {"bar": 48, "value": 0.0},  # Instant cut at drop
            ],
        }

    def get_auto_pan_config(self) -> list[dict]:
        """Get Auto Pan configuration for hi-hats (Track 5)."""
        return [
            {
                "type": "device_add",
                "device": "Auto Pan",
                "track": 4,  # Closed Hats
                "params": {
                    "phase": 0,  # Tremolo mode
                    "rate": "1/8",
                    "amount": 0.3,
                    "shape": "Sine",
                },
            },
        ]

    def configure_lfo(
        self,
        track_index: int,
        lfo_index: int,
        rate: float,
        shape: str = "Sine",
    ) -> AgentResult:
        """Configure LFO parameters.

        Reference: Ableton Manual Section 30.13.5 "Modulation Matrix" (page 748)

        Args:
            track_index: Track index
            lfo_index: LFO index (0-2)
            rate: LFO rate (0.0-1.0 or Hz)
            shape: LFO shape (Sine, Triangle, Square, etc.)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Configuring LFO {lfo_index} on track {track_index}")
            return AgentResult(
                success=True,
                message=f"Mock: Configured LFO {lfo_index}",
                data={"lfo_index": lfo_index, "rate": rate, "shape": shape},
            )

        try:
            result = mcp.set_lfo_parameter(
                track_index=track_index, lfo_index=lfo_index, rate=rate, shape=shape
            )

            if result.success:
                self.log(f"Configured LFO {lfo_index} with rate {rate}")

            return result

        except Exception as e:
            self.log(f"Error configuring LFO: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def apply_modulation(
        self,
        track_index: int,
        modulations: list[dict],
    ) -> tuple[bool, list[str]]:
        """Apply modulation to a track.

        Args:
            track_index: Track to apply modulation to
            modulations: List of modulation configurations

        Returns:
            Tuple of (success, error_messages)
        """
        errors = []
        track = TRACKS[track_index]
        mcp = self.get_mcp_client()

        if not mcp:
            self.log(f"Mock: Applying {len(modulations)} modulations to {track.name}")
            return True, []

        for mod in modulations:
            mod_type = mod.get("type")

            if mod_type == "automation":
                # Create parameter automation
                self.log(f"Creating automation for {mod['parameter']}...")

                if hasattr(mcp, "create_automation"):
                    result = mcp.create_automation(
                        track_index=track_index,
                        device_name=mod["device"],
                        parameter_name=mod["parameter"],
                        pattern=mod.get("pattern", "linear"),
                        **{
                            k: v
                            for k, v in mod.items()
                            if k not in ["type", "device", "parameter", "pattern"]
                        },
                    )
                    if not result.success:
                        errors.append(f"Failed to create automation: {result.message}")
                else:
                    self.log("Automation not supported by MCP client")

            elif mod_type == "lfo":
                # Route LFO
                self.log(f"Routing LFO to {mod['destination']}...")
                # This would require device-specific LFO routing
                # Implementation depends on MCP capabilities

            elif mod_type == "device_add":
                # Add modulation device
                device_name = mod["device"]
                params = mod.get("params", {})

                result = mcp.load_device(
                    track_index=track_index,
                    device_name=device_name,
                )
                if not result.success:
                    errors.append(f"Failed to load {device_name}")

        return len(errors) == 0, errors

    async def execute(
        self,
        track_index: int | None = None,
        **kwargs,
    ) -> AgentResult:
        """Apply modulation and automation to tracks.

        Args:
            track_index: Specific track (None = all modulation targets)

        Returns:
            AgentResult with modulation results
        """
        modulations_applied = []
        all_errors = []

        # Modulation configurations per track
        mod_configs = {
            3: self.get_acid_modulation(),  # Acid Line
            10: self.get_stab_modulation(),  # Synth Stabs
            1: self.get_rumble_modulation(),  # Rumble
        }

        # Get tracks to process
        if track_index is not None:
            if track_index in mod_configs:
                tracks_to_process = [(track_index, mod_configs[track_index])]
            else:
                return AgentResult(
                    success=False,
                    message=f"Track {track_index} has no modulation config",
                    errors=[f"No modulation for track {track_index}"],
                )
        else:
            tracks_to_process = list(mod_configs.items())

        # Apply per-track modulation
        for idx, mods in tracks_to_process:
            track = TRACKS[idx]
            self.log(f"Applying modulation to {track.name}...")

            try:
                success, errors = await self.apply_modulation(idx, mods)

                if success:
                    modulations_applied.append(
                        {
                            "track": track.name,
                            "modulation_count": len(mods),
                        }
                    )
                    self.update_progress(track.index, 0.85)
                else:
                    all_errors.extend(errors)

            except Exception as e:
                all_errors.append(f"{track.name}: {e}")
                self.log(f"Error on {track.name}: {e}")

        # Apply global modulation (reverb sends, etc.)
        # This would be implemented based on MCP capabilities

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Applied modulation to {len(modulations_applied)} tracks",
            data={"modulations": modulations_applied},
            errors=all_errors,
        )
