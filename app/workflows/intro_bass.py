"""Intro Bass Workflow - Lane 2.

TDD workflow for creating bass tracks:
- Rumble (sub bass with sidechain)
- Rolling Bass (acid pattern)
- Acid (303 sound)

P0 Blocker: Rumble requires sidechain routing from Kick.
"""

from .base import BaseWorkflow, TrackSpec


class IntroBassWorkflow(BaseWorkflow):
    """Lane 2: Bass workflow for intro section."""

    @property
    def name(self) -> str:
        return "Intro Bass"

    @property
    def lane(self) -> int:
        return 2

    def define_tracks(self) -> list[TrackSpec]:
        """Define bass tracks for intro section."""
        return [
            TrackSpec(
                name="Rumble",
                index=6,
                device="Operator",
                device_uri="query:Synths#Operator",
                pattern_type="sub_bass",
                needs_sidechain=True,
                sidechain_source="Kick",
                effects=[
                    {"name": "Hybrid Reverb", "uri": "query:AudioFx#Hybrid%20Reverb"},
                    {"name": "Roar", "uri": "query:AudioFx#Roar"},
                    {"name": "EQ Eight", "uri": "query:AudioFx#EQ%20Eight"},
                    {"name": "Compressor", "uri": "query:AudioFx#Compressor"},
                ],
                test_file="test_intro_rumble.py",
            ),
            TrackSpec(
                name="Rolling Bass",
                index=7,
                device="Wavetable",
                device_uri="query:Synths#Wavetable",
                pattern_type="acid",
                test_file="test_intro_rolling_bass.py",
            ),
            TrackSpec(
                name="Acid",
                index=8,
                device="Drift",
                device_uri="query:Synths#Drift",
                pattern_type="303",
                test_file="test_intro_acid.py",
            ),
        ]

    async def execute_red(self, track: TrackSpec) -> bool:
        """RED: Verify test fails (track doesn't exist yet).

        For bass tracks, we verify:
        1. Track does not exist OR
        2. Track exists but has no synth OR
        3. Track exists but effects chain incomplete OR
        4. For Rumble: sidechain not configured
        """
        # TODO: Implement actual test execution using track spec
        del track  # Unused in stub
        return True

    async def execute_green(self, track: TrackSpec) -> bool:
        """GREEN: Create track to pass test.

        Steps for Rumble (P0):
        1. Create MIDI track with name
        2. Load Operator
        3. Load effects chain (Hybrid Reverb, Roar, EQ Eight, Compressor)
        4. Configure sidechain on Compressor to Kick
        5. Create 16-bar clip with sub bass notes

        Steps for Rolling Bass / Acid:
        1. Create MIDI track
        2. Load synth (Wavetable/Drift)
        3. Create 16-bar clip with acid pattern
        """
        # TODO: Implement using MCP client
        # Example for Rumble:
        # mcp.create_midi_track(name=track.name)
        # mcp.load_browser_item(track.index, track.device_uri)
        # for effect in track.effects:
        #     mcp.load_browser_item(track.index, effect["uri"])
        # mcp.set_sidechain_input(track.index, -1, "Kick")  # P0 tool
        # mcp.create_clip(track.index, 0, 64.0)
        # mcp.add_notes_to_clip(track.index, 0, self._generate_pattern(track))
        del track  # Unused in stub
        return True

    async def execute_refactor(self, track: TrackSpec) -> bool:
        """REFACTOR: Verify and clean up.

        For Rumble specifically:
        1. Verify sidechain pumping is audible
        2. Check low-end balance with Kick
        3. Adjust EQ if needed
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

        if track.pattern_type == "sub_bass":
            # Rumble: sustained low notes, follows root note
            # Assuming key of F minor (common in techno)
            for bar in range(16):
                notes.append({
                    "pitch": 29,  # F0 - sub bass
                    "start_time": float(bar * 4),
                    "duration": 4.0,  # Whole bar
                    "velocity": 100,
                })

        elif track.pattern_type == "acid":
            # Acid: 16th note pattern with accent variations
            # F1, F1, Ab1, F1, Bb1, F1, C2, F1
            pitches = [36, 36, 39, 36, 41, 36, 43, 36]
            for bar in range(16):
                for step in range(16):
                    pitch = pitches[step % len(pitches)]
                    notes.append({
                        "pitch": pitch,
                        "start_time": bar * 4 + step * 0.25,
                        "duration": 0.2,
                        "velocity": 100 if step % 4 == 0 else 70,
                    })

        elif track.pattern_type == "303":
            # 303: Similar to acid but with slides
            # Slides are implemented via overlapping notes
            base_pitches = [36, 41, 36, 43]  # F1, Bb1, F1, C2
            for bar in range(16):
                for beat in range(4):
                    pitch = base_pitches[beat]
                    # Add slide by extending duration
                    notes.append({
                        "pitch": pitch,
                        "start_time": bar * 4 + beat,
                        "duration": 1.1,  # Slight overlap for slide
                        "velocity": 90,
                    })

        return notes
