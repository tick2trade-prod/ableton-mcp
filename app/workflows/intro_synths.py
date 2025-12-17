"""Intro Synths Workflow - Lane 3.

TDD workflow for creating synth tracks:
- Stabs (techno stabs, off-beat)
- Drone (ambient pad)
"""

from .base import BaseWorkflow, TrackSpec


class IntroSynthsWorkflow(BaseWorkflow):
    """Lane 3: Synths workflow for intro section."""

    @property
    def name(self) -> str:
        return "Intro Synths"

    @property
    def lane(self) -> int:
        return 3

    def define_tracks(self) -> list[TrackSpec]:
        """Define synth tracks for intro section."""
        return [
            TrackSpec(
                name="Stabs",
                index=10,
                device="Wavetable",
                device_uri="query:Synths#Wavetable",
                pattern_type="stabs",
                effects=[
                    {"name": "Auto Filter", "uri": "query:AudioFx#Auto%20Filter"},
                    {"name": "EQ Eight", "uri": "query:AudioFx#EQ%20Eight"},
                    {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
                ],
                test_file="test_intro_stabs.py",
            ),
            TrackSpec(
                name="Drone",
                index=11,
                device="Operator",
                device_uri="query:Synths#Operator",
                pattern_type="drone",
                effects=[
                    {"name": "Hybrid Reverb", "uri": "query:AudioFx#Hybrid%20Reverb"},
                    {"name": "Auto Pan", "uri": "query:AudioFx#Auto%20Pan"},
                    {"name": "Utility", "uri": "query:AudioFx#Utility"},
                ],
                test_file="test_intro_drone.py",
            ),
        ]

    async def execute_red(self, track: TrackSpec) -> bool:
        """RED: Verify test fails.

        For synth tracks, verify:
        1. Track doesn't exist
        2. Track exists but no synth loaded
        3. Track exists but no clip
        """
        # TODO: Implement actual test execution using track.name, track.device
        del track  # Unused in stub
        return True

    async def execute_green(self, track: TrackSpec) -> bool:
        """GREEN: Create track to pass test.

        Steps:
        1. Create MIDI track
        2. Load synth (Wavetable/Operator)
        3. Load effects chain
        4. Create 16-bar clip
        5. Add appropriate pattern
        """
        # TODO: Implement using MCP client with track spec
        del track  # Unused in stub
        return True

    async def execute_refactor(self, track: TrackSpec) -> bool:
        """REFACTOR: Verify and clean up.

        Checks:
        - Stabs: EQ high-pass to avoid low-end clash
        - Drone: Reverb amount appropriate
        - Both: Mix level balanced
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

        if track.pattern_type == "stabs":
            # Techno stabs: short, punchy, off-beat
            # Chord: Fm (F, Ab, C)
            chord = [53, 56, 60]  # F3, Ab3, C4
            for bar in range(16):
                # Off-beat stabs (& of 1, & of 3)
                for beat_offset in [0.5, 2.5]:
                    for pitch in chord:
                        notes.append({
                            "pitch": pitch,
                            "start_time": bar * 4 + beat_offset,
                            "duration": 0.2,  # Short stab
                            "velocity": 85,
                        })

        elif track.pattern_type == "drone":
            # Ambient drone: long sustained chord
            # Using Fm7 (F, Ab, C, Eb)
            chord = [41, 44, 48, 51]  # F2, Ab2, C3, Eb3
            for bar in range(4):  # 4 long notes covering 16 bars
                for pitch in chord:
                    notes.append({
                        "pitch": pitch,
                        "start_time": bar * 16,  # Every 4 bars
                        "duration": 16.0,  # 4 bars each
                        "velocity": 60,  # Soft
                    })

        return notes
