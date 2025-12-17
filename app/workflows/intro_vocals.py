"""Intro Vocals/FX Workflow - Lane 4.

TDD workflow for creating vocal and FX tracks:
- Main Vocal (lead vocal, audio or sampler)
- Vocal FX (creative processing)
- Risers (tension builders)
- Return A (Reverb send)
- Return B (Delay send)

P0 Blocker: Requires create_return_track tool.
"""

from .base import BaseWorkflow, TrackSpec


class IntroVocalsWorkflow(BaseWorkflow):
    """Lane 4: Vocals and FX workflow for intro section."""

    @property
    def name(self) -> str:
        return "Intro Vocals/FX"

    @property
    def lane(self) -> int:
        return 4

    def define_tracks(self) -> list[TrackSpec]:
        """Define vocal and FX tracks for intro section.

        Note: Returns are special - they use create_return_track tool.
        """
        return [
            # Return tracks first (dependencies for sends)
            TrackSpec(
                name="Return A - Reverb",
                index=-1,  # Return track, index determined by create_return_track
                device="Hybrid Reverb",
                device_uri="query:AudioFx#Hybrid%20Reverb",
                pattern_type="return",
                effects=[
                    {"name": "EQ Eight", "uri": "query:AudioFx#EQ%20Eight"},
                ],
                test_file="test_intro_return_a.py",
            ),
            TrackSpec(
                name="Return B - Delay",
                index=-1,  # Return track
                device="Echo",
                device_uri="query:AudioFx#Echo",
                pattern_type="return",
                effects=[
                    {"name": "Auto Filter", "uri": "query:AudioFx#Auto%20Filter"},
                ],
                test_file="test_intro_return_b.py",
            ),
            # Regular tracks
            TrackSpec(
                name="Main Vocal",
                index=12,
                device="Sampler",
                device_uri="query:Instruments#Sampler",
                pattern_type="vocal",
                effects=[
                    {"name": "EQ Eight", "uri": "query:AudioFx#EQ%20Eight"},
                    {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
                ],
                test_file="test_intro_vocal.py",
            ),
            TrackSpec(
                name="Vocal FX",
                index=13,
                device="Vocoder",
                device_uri="query:AudioFx#Vocoder",
                pattern_type="vocal_fx",
                effects=[
                    {"name": "Reverb", "uri": "query:AudioFx#Reverb"},
                    {"name": "Delay", "uri": "query:AudioFx#Delay"},
                ],
                test_file="test_intro_vocal_fx.py",
            ),
            TrackSpec(
                name="Risers",
                index=14,
                device="Wavetable",
                device_uri="query:Synths#Wavetable",
                pattern_type="riser",
                effects=[
                    {"name": "Auto Filter", "uri": "query:AudioFx#Auto%20Filter"},
                    {"name": "Utility", "uri": "query:AudioFx#Utility"},
                ],
                test_file="test_intro_risers.py",
            ),
        ]

    async def execute_red(self, track: TrackSpec) -> bool:
        """RED: Verify test fails.

        For vocal/FX tracks, verify:
        1. Track/return doesn't exist
        2. Track exists but device not loaded
        3. For returns: verify send routing not configured
        """
        # TODO: Implement actual test execution using track spec
        del track  # Unused in stub
        return True

    async def execute_green(self, track: TrackSpec) -> bool:
        """GREEN: Create track to pass test.

        For return tracks:
        1. Use create_return_track (P0 tool)
        2. Load effect (Reverb/Delay)
        3. Add EQ/Filter

        For regular tracks:
        1. Create MIDI/audio track
        2. Load device
        3. Load effects
        4. Configure sends to returns
        """
        # TODO: Implement using MCP client with track spec
        # Example for return track:
        # if track.pattern_type == "return":
        #     result = mcp.create_return_track(name=track.name)
        #     track.index = result["result"]["index"]
        #     mcp.load_browser_item(f"return_{track.index}", track.device_uri)
        del track  # Unused in stub
        return True

    async def execute_refactor(self, track: TrackSpec) -> bool:
        """REFACTOR: Verify and clean up.

        Checks:
        - Returns: Effect tails appropriate
        - Vocals: Not clashing with main elements
        - Risers: Automation ready for builds
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

        if track.pattern_type == "vocal":
            # Main vocal: sparse intro phrases
            # For intro, might just be atmospheric samples
            # This would typically be audio, not MIDI
            pass

        elif track.pattern_type == "vocal_fx":
            # Processed vocal bits
            pass

        elif track.pattern_type == "riser":
            # Riser: ascending pitch for build
            # For intro, we might have a subtle riser
            for step in range(64):  # 64 steps over 16 bars
                # Ascending pitch
                pitch = 36 + (step // 4)  # Slowly rising
                notes.append({
                    "pitch": min(pitch, 72),  # Cap at C4
                    "start_time": step,
                    "duration": 0.9,
                    "velocity": 40 + (step // 2),  # Building velocity
                })

        return notes
