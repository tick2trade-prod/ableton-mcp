"""Composer Agent for MIDI patterns and note composition.

Reference: Ableton Manual Section 13.1.4 "Groove Pool" (page 326)


Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)
"""

from ..config import TRACKS, TrackConfig
from .base_agent import AgentResult, BaseAgent


class ComposerAgent(BaseAgent):
    """Agent for composing MIDI patterns.

    Creates patterns appropriate for each track type:
    - 4-on-floor for kicks
    - 16th notes for hi-hats
    - Rolling patterns for bass
    """

    def __init__(self, **kwargs):
        super().__init__(name="ComposerAgent", **kwargs)

    def get_role(self) -> str:
        return "Rhythm Programmer"

    def get_goal(self) -> str:
        return "Create driving 4/4 patterns at 136 BPM in F Minor"

    def generate_kick_pattern(self, bars: int = 4) -> list[dict]:
        """Generate 4-on-floor kick pattern."""
        notes = []
        for bar in range(bars):
            for beat in range(4):
                notes.append(
                    {
                        "pitch": 36,  # C1 (Kick)
                        "start_time": float(bar * 4 + beat),
                        "duration": 0.25,
                        "velocity": 110 if beat in [0, 2] else 100,
                    }
                )
        return notes

    def generate_hihat_pattern(
        self,
        bars: int = 4,
        open_hat: bool = False,
    ) -> list[dict]:
        """Generate hi-hat pattern (16th notes or off-beat)."""
        notes = []
        pitch = 46 if open_hat else 42

        for bar in range(bars):
            for sixteenth in range(16):
                start = bar * 4 + sixteenth * 0.25

                if open_hat:
                    # Off-beat pattern (every 2nd 8th note)
                    if sixteenth % 4 == 2:
                        notes.append(
                            {
                                "pitch": pitch,
                                "start_time": start,
                                "duration": 0.2,
                                "velocity": 85,
                            }
                        )
                else:
                    # 16th note pattern
                    notes.append(
                        {
                            "pitch": pitch,
                            "start_time": start,
                            "duration": 0.1,
                            "velocity": 80 + (10 if sixteenth % 4 == 0 else 0),
                        }
                    )
        return notes

    def generate_clap_pattern(self, bars: int = 4) -> list[dict]:
        """Generate clap on beats 2 and 4."""
        notes = []
        for bar in range(bars):
            for beat in [1, 3]:  # Beats 2 and 4 (0-indexed)
                notes.append(
                    {
                        "pitch": 39,  # Clap
                        "start_time": float(bar * 4 + beat),
                        "duration": 0.25,
                        "velocity": 100,
                    }
                )
        return notes

    def generate_bass_pattern(self, bars: int = 4) -> list[dict]:
        """Generate rolling 16th bass pattern in F Minor."""
        # F Minor scale: F(41), Ab(44), Bb(46), C(48), Eb(51)
        scale = [29, 32, 34, 36, 39]  # F1, Ab1, Bb1, C2, Eb2
        notes = []

        for bar in range(bars):
            for sixteenth in range(16):
                start = bar * 4 + sixteenth * 0.25
                pitch = scale[sixteenth % len(scale)]
                notes.append(
                    {
                        "pitch": pitch,
                        "start_time": start,
                        "duration": 0.2,
                        "velocity": 95 + (10 if sixteenth % 4 == 0 else 0),
                    }
                )
        return notes

    def get_pattern_for_track(self, track: TrackConfig, bars: int = 4) -> list[dict]:
        """Get appropriate pattern for track type."""
        name_lower = track.name.lower()

        if "kick" in name_lower:
            return self.generate_kick_pattern(bars)
        elif "closed" in name_lower and "hat" in name_lower:
            return self.generate_hihat_pattern(bars, open_hat=False)
        elif "open" in name_lower and "hat" in name_lower:
            return self.generate_hihat_pattern(bars, open_hat=True)
        elif "clap" in name_lower or "snare" in name_lower:
            return self.generate_clap_pattern(bars)
        elif "bass" in name_lower:
            return self.generate_bass_pattern(bars)
        else:
            # Default empty pattern
            return []

    def apply_groove(
        self,
        track_index: int,
        clip_index: int,
        groove_name: str,
        groove_amount: float = 0.5,
    ) -> AgentResult:
        """Apply groove to clip for timing and velocity variation.

        Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)

        Args:
            track_index: Track index
            clip_index: Clip index
            groove_name: Groove preset name (e.g., "MPC-60")
            groove_amount: Groove intensity (0.0-1.0)

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Applying groove '{groove_name}' to clip")
            return AgentResult(
                success=True,
                message=f"Mock: Applied groove '{groove_name}'",
                data={"groove_name": groove_name, "amount": groove_amount},
            )

        try:
            result = mcp.set_clip_groove(
                track_index=track_index,
                clip_index=clip_index,
                groove_name=groove_name,
                amount=groove_amount,
            )

            if result.success:
                self.log(f"Applied groove '{groove_name}' with amount {groove_amount}")

            return result

        except Exception as e:
            self.log(f"Error applying groove: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(
        self,
        track_index: int | None = None,
        bars: int = 4,
        **kwargs,
    ) -> AgentResult:
        """Create pattern for one or all tracks.

        Args:
            track_index: Specific track to compose for (None = all)
            bars: Number of bars per pattern

        Returns:
            AgentResult with created patterns
        """
        patterns_created = []
        errors = []

        # Get tracks to process
        if track_index is not None:
            tracks = [TRACKS[track_index]]
        else:
            tracks = [t for t in TRACKS if t.track_type == "midi"]

        mcp = self.get_mcp_client()

        for track in tracks:
            self.log(f"Composing pattern for {track.name}...")

            try:
                # Generate pattern
                notes = self.get_pattern_for_track(track, bars)

                if not notes:
                    self.log(f"No pattern template for {track.name}")
                    continue

                if mcp:
                    # Create clip via MCP
                    clip_result = mcp.create_clip(
                        track_index=track.index,
                        clip_index=0,
                        length=float(bars * 4),
                    )
                    if clip_result.success:
                        # Add notes
                        notes_result = mcp.add_notes_to_clip(
                            track_index=track.index,
                            clip_index=0,
                            notes=notes,
                        )
                        if notes_result.success:
                            patterns_created.append(
                                {
                                    "track": track.name,
                                    "notes_count": len(notes),
                                }
                            )
                            self.update_progress(track.index, 0.5)
                        else:
                            errors.append(f"{track.name}: {notes_result.message}")
                    else:
                        errors.append(f"{track.name}: {clip_result.message}")
                else:
                    # Mock mode
                    patterns_created.append(
                        {
                            "track": track.name,
                            "notes_count": len(notes),
                            "mock": True,
                        }
                    )
                    self.update_progress(track.index, 0.5)

            except Exception as e:
                errors.append(f"{track.name}: {e}")
                self.log(f"Error on {track.name}: {e}")

        success = len(errors) == 0
        return AgentResult(
            success=success,
            message=f"Created {len(patterns_created)} patterns",
            data={"patterns": patterns_created},
            errors=errors,
        )
