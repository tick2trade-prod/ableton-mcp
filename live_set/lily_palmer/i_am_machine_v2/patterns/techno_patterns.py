"""Reusable MIDI patterns for techno music production.

Provides standard patterns for common techno elements that can be used
in track configurations.
"""

# Type alias for pattern dictionary
MIDIPattern = list[dict[str, float | int]]


class TechnoPatterns:
    """Collection of techno MIDI patterns."""

    # KICK PATTERNS
    @staticmethod
    def kick_4_on_floor() -> MIDIPattern:
        """4-on-the-floor kick pattern (every quarter note) - 4 bars."""
        return [
            {"pitch": 36, "start_time": float(i), "duration": 0.25, "velocity": 100}
            for i in range(16)  # 16 beats = 4 bars
        ]

    @staticmethod
    def kick_offbeat() -> MIDIPattern:
        """Offbeat kick pattern."""
        return [
            {"pitch": 36, "start_time": 0.5, "duration": 0.25, "velocity": 95},
            {"pitch": 36, "start_time": 1.5, "duration": 0.25, "velocity": 95},
            {"pitch": 36, "start_time": 2.5, "duration": 0.25, "velocity": 95},
            {"pitch": 36, "start_time": 3.5, "duration": 0.25, "velocity": 95},
        ]

    # SNARE/CLAP PATTERNS
    @staticmethod
    def snare_backbeat() -> MIDIPattern:
        """Snare on beats 2 and 4 - 4 bars."""
        return [
            {
                "pitch": 38,
                "start_time": float(i * 4 + 1),
                "duration": 0.125,
                "velocity": 90,
            }
            for bar in range(4)
            for i in [bar]
        ] + [
            {
                "pitch": 38,
                "start_time": float(i * 4 + 3),
                "duration": 0.125,
                "velocity": 90,
            }
            for bar in range(4)
            for i in [bar]
        ]

    @staticmethod
    def clap_backbeat() -> MIDIPattern:
        """Clap on beats 2 and 4."""
        return [
            {"pitch": 39, "start_time": 1.0, "duration": 0.125, "velocity": 85},
            {"pitch": 39, "start_time": 3.0, "duration": 0.125, "velocity": 85},
        ]

    # HI-HAT PATTERNS
    @staticmethod
    def hihat_8th_notes() -> MIDIPattern:
        """8th note hi-hat pattern."""
        return [
            {"pitch": 42, "start_time": i * 0.5, "duration": 0.125, "velocity": 70}
            for i in range(8)
        ]

    @staticmethod
    def hihat_16th_notes() -> MIDIPattern:
        """16th note hi-hat pattern with velocity variation - 4 bars."""
        pattern = []
        for i in range(64):  # 64 16th notes = 4 bars
            velocity = 70 if i % 2 == 0 else 60  # Accent on beat
            pattern.append(
                {
                    "pitch": 42,
                    "start_time": i * 0.25,
                    "duration": 0.125,
                    "velocity": velocity,
                }
            )
        return pattern

    # BASS PATTERNS (E minor)
    @staticmethod
    def bass_e_minor_simple() -> MIDIPattern:
        """Simple E minor bass pattern."""
        return [
            {"pitch": 40, "start_time": 0.0, "duration": 0.5, "velocity": 80},  # E
            {"pitch": 43, "start_time": 0.5, "duration": 0.5, "velocity": 75},  # G
            {"pitch": 40, "start_time": 1.0, "duration": 0.5, "velocity": 80},  # E
            {"pitch": 47, "start_time": 1.5, "duration": 0.5, "velocity": 75},  # B
        ]

    @staticmethod
    def bass_e_minor_rolling() -> MIDIPattern:
        """Rolling E minor bassline."""
        return [
            {"pitch": 40, "start_time": 0.0, "duration": 0.25, "velocity": 85},  # E
            {"pitch": 43, "start_time": 0.25, "duration": 0.25, "velocity": 75},  # G
            {"pitch": 47, "start_time": 0.5, "duration": 0.25, "velocity": 80},  # B
            {"pitch": 43, "start_time": 0.75, "duration": 0.25, "velocity": 70},  # G
            {"pitch": 40, "start_time": 1.0, "duration": 0.25, "velocity": 85},  # E
            {"pitch": 47, "start_time": 1.25, "duration": 0.25, "velocity": 75},  # B
            {"pitch": 52, "start_time": 1.5, "duration": 0.25, "velocity": 80},  # E
            {"pitch": 47, "start_time": 1.75, "duration": 0.25, "velocity": 70},  # B
        ]

    @staticmethod
    def sub_bass_root() -> MIDIPattern:
        """Sub bass on root note."""
        return [
            {"pitch": 28, "start_time": 0.0, "duration": 1.0, "velocity": 90},  # E
            {"pitch": 28, "start_time": 1.0, "duration": 1.0, "velocity": 90},
        ]

    # CHORD PATTERNS
    @staticmethod
    def pad_e_minor_chord() -> MIDIPattern:
        """E minor chord for pads (long sustain)."""
        return [
            {"pitch": 52, "start_time": 0.0, "duration": 4.0, "velocity": 60},  # E
            {"pitch": 55, "start_time": 0.0, "duration": 4.0, "velocity": 55},  # G
            {"pitch": 59, "start_time": 0.0, "duration": 4.0, "velocity": 58},  # B
        ]

    @staticmethod
    def stab_e_minor() -> MIDIPattern:
        """E minor stab chord."""
        return [
            {"pitch": 64, "start_time": 0.0, "duration": 0.125, "velocity": 95},  # E
            {"pitch": 67, "start_time": 0.0, "duration": 0.125, "velocity": 90},  # G
            {"pitch": 71, "start_time": 0.0, "duration": 0.125, "velocity": 92},  # B
        ]

    # LEAD/ARP PATTERNS
    @staticmethod
    def arp_e_minor_16th() -> MIDIPattern:
        """16th note arpeggiated E minor."""
        notes = [64, 67, 71, 64]  # E, G, B, E
        pattern = []
        for i, pitch in enumerate(notes):
            velocity = 75 if i % 2 == 0 else 70
            pattern.append(
                {
                    "pitch": pitch,
                    "start_time": i * 0.125,
                    "duration": 0.125,
                    "velocity": velocity,
                }
            )
        return pattern

    @staticmethod
    def lead_melody() -> MIDIPattern:
        """Simple lead melody in E minor."""
        return [
            {"pitch": 64, "start_time": 0.0, "duration": 0.25, "velocity": 85},  # E
            {"pitch": 67, "start_time": 0.5, "duration": 0.25, "velocity": 80},  # G
            {"pitch": 71, "start_time": 1.0, "duration": 0.5, "velocity": 90},  # B
        ]

    # PERCUSSION PATTERNS
    @staticmethod
    def perc_shaker_8th() -> MIDIPattern:
        """8th note shaker pattern."""
        return [
            {
                "pitch": 50,
                "start_time": i * 0.5,
                "duration": 0.125,
                "velocity": 65 if i % 2 == 0 else 60,
            }
            for i in range(8)
        ]

    @staticmethod
    def perc_conga_syncopated() -> MIDIPattern:
        """Syncopated conga pattern."""
        return [
            {"pitch": 48, "start_time": 0.5, "duration": 0.125, "velocity": 68},
            {"pitch": 48, "start_time": 1.75, "duration": 0.125, "velocity": 65},
            {"pitch": 48, "start_time": 2.5, "duration": 0.125, "velocity": 70},
        ]


# Usage examples
if __name__ == "__main__":
    patterns = TechnoPatterns()

    print("Example Patterns:")
    print(f"Kick 4-on-floor: {len(patterns.kick_4_on_floor())} notes")
    print(f"Hi-hat 16ths: {len(patterns.hihat_16th_notes())} notes")
    print(f"Bass E minor: {len(patterns.bass_e_minor_simple())} notes")
    print(f"Pad chord: {len(patterns.pad_e_minor_chord())} notes")
