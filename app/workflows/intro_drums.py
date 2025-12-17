"""Intro Drums Workflow - Lane 1.

TDD workflow for creating drum tracks:
- Kick (4-on-floor)
- Snare (off-beat)
- Hi-hats (16th notes)
- Toms (fills)
- Glitch (stutter)
- Ride (cymbal)
"""

from .base import BaseWorkflow, TrackSpec


class IntroDrumsWorkflow(BaseWorkflow):
    """Lane 1: Drums workflow for intro section."""

    @property
    def name(self) -> str:
        return "Intro Drums"

    @property
    def lane(self) -> int:
        return 1

    def define_tracks(self) -> list[TrackSpec]:
        """Define drum tracks for intro section."""
        return [
            TrackSpec(
                name="Kick",
                index=0,
                device="Drum Rack",
                device_uri="query:Drums#Drum%20Rack",
                pattern_type="4-on-floor",
                test_file="test_intro_kick.py",
            ),
            TrackSpec(
                name="Snare",
                index=1,
                device="Drum Rack",
                device_uri="query:Drums#Drum%20Rack",
                pattern_type="off-beat",
                test_file="test_intro_snare.py",
            ),
            TrackSpec(
                name="Hi-hats",
                index=2,
                device="Drum Rack",
                device_uri="query:Drums#Drum%20Rack",
                pattern_type="16th-notes",
                test_file="test_intro_hihats.py",
            ),
            TrackSpec(
                name="Toms",
                index=3,
                device="Drum Rack",
                device_uri="query:Drums#Drum%20Rack",
                pattern_type="fills",
                test_file="test_intro_toms.py",
            ),
            TrackSpec(
                name="Glitch",
                index=4,
                device="Drum Rack",
                device_uri="query:Drums#Drum%20Rack",
                pattern_type="stutter",
                test_file="test_intro_glitch.py",
            ),
            TrackSpec(
                name="Ride",
                index=5,
                device="Drum Rack",
                device_uri="query:Drums#Drum%20Rack",
                pattern_type="cymbal",
                test_file="test_intro_ride.py",
            ),
        ]

    async def execute_red(self, track: TrackSpec) -> bool:
        """RED: Verify test fails (track doesn't exist yet).

        For drums, we verify:
        1. Track does not exist OR
        2. Track exists but has no Drum Rack OR
        3. Track exists but has no clip
        """
        # In TDD, RED means the test should fail
        # We return True if the test correctly fails
        # (i.e., track doesn't exist or isn't complete)
        # TODO: Implement actual test execution using track spec
        del track  # Unused in stub
        return True

    async def execute_green(self, track: TrackSpec) -> bool:
        """GREEN: Create track to pass test.

        Steps:
        1. Create MIDI track with name
        2. Load Drum Rack
        3. Create 16-bar clip
        4. Add notes based on pattern_type
        """
        # TODO: Implement using MCP client with track spec
        # Example:
        # mcp.create_midi_track(name=track.name)
        # mcp.load_browser_item(track.index, track.device_uri)
        # mcp.create_clip(track.index, 0, 64.0)  # 16 bars
        # mcp.add_notes_to_clip(track.index, 0, self._generate_pattern(track))
        del track  # Unused in stub
        return True

    async def execute_refactor(self, track: TrackSpec) -> bool:
        """REFACTOR: Verify and clean up.

        Steps:
        1. Run test again to verify pass
        2. Check audio output
        3. Adjust velocity/timing if needed
        """
        # TODO: Implement verification using track spec
        del track  # Unused in stub
        return True

    def _generate_pattern(self, track: TrackSpec) -> list[dict]:
        """Generate MIDI notes based on pattern type.

        Args:
            track: Track specification

        Returns:
            List of note dicts for MCP
        """
        notes = []

        if track.pattern_type == "4-on-floor":
            # Kick on every beat: 64 beats in 16 bars
            for beat in range(64):
                notes.append({
                    "pitch": 36,  # C1 - standard kick
                    "start_time": float(beat),
                    "duration": 0.5,
                    "velocity": 100,
                })

        elif track.pattern_type == "off-beat":
            # Snare on beats 2 and 4
            for bar in range(16):
                for beat in [1, 3]:  # 2nd and 4th beat (0-indexed)
                    notes.append({
                        "pitch": 38,  # D1 - standard snare
                        "start_time": float(bar * 4 + beat),
                        "duration": 0.25,
                        "velocity": 90,
                    })

        elif track.pattern_type == "16th-notes":
            # Hi-hats on every 16th note
            for step in range(256):  # 16 * 16 = 256 16th notes
                notes.append({
                    "pitch": 42,  # F#1 - closed hi-hat
                    "start_time": step * 0.25,
                    "duration": 0.125,
                    "velocity": 70 if step % 4 == 0 else 50,
                })

        # Add more patterns as needed

        return notes
