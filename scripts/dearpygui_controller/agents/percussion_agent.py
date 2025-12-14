"""Percussion Agent for drum rack and percussion setup.

Reference: Ableton Manual Section 34.3.1 "Loop Selector" (page 797)
Reference: Ableton Manual Section 24.4.1 "Drum Rack Basics" (page 446)
"""

import random

from ..config import TRACKS, TrackConfig
from .base_agent import AgentResult, BaseAgent


class PercussionAgent(BaseAgent):
    """Agent for creating advanced percussion patterns.

    Specializes in:
    - Low Toms with syncopated tribal rhythms
    - Glitch/Industrial percussion with randomization
    - Ride cymbals with high-energy fills
    - Velocity and timing humanization
    """

    def __init__(self, **kwargs):
        super().__init__(name="PercussionAgent", **kwargs)

    def get_role(self) -> str:
        return "Percussion Programmer"

    def get_goal(self) -> str:
        return "Create syncopated, industrial percussion for peak-time techno energy"

    def generate_tom_pattern(self, bars: int = 4) -> list[dict]:
        """Generate syncopated low tom/tribal pattern (Track 8).

        Creates sparse, syncopated hits that fall on 16th notes
        just before the snare or kick, creating groove tension.
        """
        notes = []
        # Tom pitch (low tom)
        pitch = 45  # A1

        for bar in range(bars):
            # Add sparse syncopated hits
            # Pattern: hits on specific 16th notes for push/pull feel
            syncopated_positions = [
                # Bar subdivision (16th note positions)
                bar * 16 + 3,  # Before beat 2
                bar * 16 + 10,  # Before beat 3
                bar * 16 + 15,  # Before beat 4 (last 16th)
            ]

            # Randomly skip some hits for variation (70% chance to play)
            for pos in syncopated_positions:
                if random.random() < 0.7:
                    notes.append(
                        {
                            "pitch": pitch,
                            "start_time": pos * 0.25,
                            "duration": 0.15,
                            "velocity": random.randint(95, 105),
                        }
                    )

        return notes

    def generate_glitch_pattern(self, bars: int = 4) -> list[dict]:
        """Generate glitch/industrial percussion (Track 9).

        Creates random metallic hits using Meld with pitch
        and timbre randomization for "malfunctioning machine" aesthetic.
        """
        notes = []

        # Glitch pitches (metallic range)
        glitch_pitches = [60, 64, 67, 71, 74]  # C, E, G, B, D

        for bar in range(bars):
            # Random glitch density (4-8 hits per bar)
            hit_count = random.randint(4, 8)

            for _ in range(hit_count):
                # Random position within bar
                position = bar * 16 + random.randint(0, 15)
                start_time = position * 0.25

                notes.append(
                    {
                        "pitch": random.choice(glitch_pitches),
                        "start_time": start_time,
                        "duration": random.uniform(0.05, 0.15),
                        "velocity": random.randint(70, 100),
                    }
                )

        # Sort by time
        notes.sort(key=lambda n: n["start_time"])
        return notes

    def generate_ride_pattern(self, bars: int = 4) -> list[dict]:
        """Generate ride cymbal pattern (Track 10).

        High-energy frequency filler, introduced in main drop
        for maximum intensity. Continuous 8th notes with variation.
        """
        notes = []
        pitch = 51  # Ride cymbal

        for bar in range(bars):
            for eighth in range(8):
                start = bar * 4 + eighth * 0.5

                # Accent every 4th hit
                velocity = 90 if eighth % 4 == 0 else 75

                notes.append(
                    {
                        "pitch": pitch,
                        "start_time": start,
                        "duration": 0.4,
                        "velocity": velocity,
                    }
                )

        return notes

    def get_pattern_for_track(self, track: TrackConfig, bars: int = 4) -> list[dict]:
        """Get appropriate pattern for percussion track."""
        name_lower = track.name.lower()

        if "tom" in name_lower:
            return self.generate_tom_pattern(bars)
        elif "glitch" in name_lower:
            return self.generate_glitch_pattern(bars)
        elif "ride" in name_lower:
            return self.generate_ride_pattern(bars)
        else:
            return []

    def configure_drum_rack(
        self,
        track_index: int,
        pad_layout: str = "4x4",
        choke_groups: dict | None = None,
    ) -> AgentResult:
        """Configure drum rack layout and choke groups.

        Reference: Ableton Manual Section 24.4.1 "Drum Rack Basics" (page 446)

        Args:
            track_index: Track index
            pad_layout: Pad layout ("4x4", "8x8")
            choke_groups: Dict mapping group names to pad lists

        Returns:
            AgentResult with success status
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Configuring drum rack on track {track_index}")
            return AgentResult(
                success=True,
                message="Mock: Configured drum rack",
                data={"track_index": track_index, "pad_layout": pad_layout},
            )

        try:
            # Configure choke groups if provided
            if choke_groups:
                for group_name, pads in choke_groups.items():
                    for pad in pads:
                        choke_result = mcp.set_pad_choke_group(
                            track_index=track_index,
                            pad_index=pad,
                            group_name=group_name,
                        )
                        if not choke_result.success:
                            return AgentResult(
                                success=False,
                                message=f"Failed to set choke group: {choke_result.message}",
                            )

            self.log(f"Configured drum rack on track {track_index}")
            return AgentResult(
                success=True,
                message="Configured drum rack",
                data={
                    "track_index": track_index,
                    "pad_layout": pad_layout,
                    "choke_groups": len(choke_groups) if choke_groups else 0,
                },
            )

        except Exception as e:
            self.log(f"Error configuring drum rack: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(
        self,
        track_index: int | None = None,
        bars: int = 4,
        **kwargs,
    ) -> AgentResult:
        """Create percussion patterns for tracks.

        Args:
            track_index: Specific track to program (None = all percussion tracks)
            bars: Number of bars per pattern

        Returns:
            AgentResult with created patterns
        """
        patterns_created = []
        all_errors = []

        # Percussion tracks: Tom (7), Glitch (8), Ride (9)
        percussion_track_indices = [7, 8, 9]

        # Get tracks to process
        if track_index is not None:
            if track_index in percussion_track_indices:
                tracks = [TRACKS[track_index]]
            else:
                return AgentResult(
                    success=False,
                    message=f"Track {track_index} is not a percussion track",
                    errors=[f"No percussion pattern for track {track_index}"],
                )
        else:
            tracks = [TRACKS[idx] for idx in percussion_track_indices]

        mcp = self.get_mcp_client()

        for track in tracks:
            self.log(f"Creating percussion pattern for {track.name}...")

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
                                    "pattern_type": track.name.split("-")[1],
                                }
                            )
                            self.update_progress(track.index, 0.6)
                        else:
                            all_errors.append(f"{track.name}: {notes_result.message}")
                    else:
                        all_errors.append(f"{track.name}: {clip_result.message}")
                else:
                    # Mock mode
                    patterns_created.append(
                        {
                            "track": track.name,
                            "notes_count": len(notes),
                            "pattern_type": track.name.split("-")[1],
                            "mock": True,
                        }
                    )
                    self.update_progress(track.index, 0.6)

            except Exception as e:
                all_errors.append(f"{track.name}: {e}")
                self.log(f"Error on {track.name}: {e}")

        success = len(all_errors) == 0
        return AgentResult(
            success=success,
            message=f"Created {len(patterns_created)} percussion patterns",
            data={"patterns": patterns_created},
            errors=all_errors,
        )
