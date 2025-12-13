"""
Musical patterns for i_o style techno generation.
Key: E Minor (Alchemy style)
Tempo: 130 BPM
"""


def get_kick_pattern(length=4.0):
    """4-on-the-floor kick pattern."""
    notes = []
    # 16 beats (4 bars)
    for i in range(int(length * 4)):
        notes.append(
            {
                "pitch": 36,  # C1 (Standard kick map)
                "start_time": float(i),
                "duration": 0.5,
                "velocity": 127 if i % 4 == 0 else 115,
                "mute": False,
            }
        )
    return notes


def get_bass_pattern(length=4.0):
    """Rolling E Minor rumble."""
    notes = []
    # Root note E1 (28)
    pitch = 28
    for i in range(int(length * 4)):
        base_time = float(i)
        # 16th note rumble pattern: X.25, X.50, X.75
        for offset, vel in [(0.25, 95), (0.5, 110), (0.75, 90)]:
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": base_time + offset,
                    "duration": 0.2,
                    "velocity": vel,
                    "mute": False,
                }
            )
    return notes


def get_lead_pattern(length=4.0):
    """303-style Acid Lead in E Minor."""
    # E Minor: E, F#, G, A, B
    notes = []
    motif = [
        (0.0, 40, 100),  # E2
        (0.75, 40, 80),
        (1.5, 52, 110),  # E3 (Octave)
        (2.0, 47, 90),  # B2 (Fifth)
        (2.5, 43, 95),  # G2 (Minor Third)
        (3.25, 40, 100),  # E2
    ]

    for bar in range(int(length / 4)):
        bar_offset = bar * 4.0
        for start, pitch, vel in motif:
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": bar_offset + start,
                    "duration": 0.25,
                    "velocity": vel,
                    "mute": False,
                }
            )
    return notes


def get_stab_pattern(length=4.0):
    """Offbeat Dub Techno Stabs."""
    notes = []
    # E Minor Chord (E, G, B) -> MIDI 52, 55, 59
    chord = [52, 55, 59]

    for i in range(int(length * 4)):  # Per beat
        # Place on the "and": X.5
        for pitch in chord:
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": i + 0.5,
                    "duration": 0.15,
                    "velocity": 85,
                    "mute": False,
                }
            )
    return notes


def get_hihat_pattern(length=4.0):
    """Open hats on offbeat."""
    notes = []
    for i in range(int(length * 4)):  # For each beat
        notes.append(
            {
                "pitch": 46,  # Open Hat (Alchemy style)
                "start_time": i + 0.5,
                "duration": 0.1,
                "velocity": 90,
                "mute": False,
            }
        )
    return notes


def get_perc_pattern(length=4.0):
    """Clap/Snare pattern on 2 and 4."""
    notes = []
    # D#1 (39) is usually Clap in Ableton 909 Kit

    # Let's align with existing loop structure
    for i in range(int(length * 4)):
        if i % 2 == 1:  # Beats 2, 4, 6, 8...
            notes.append(
                {
                    "pitch": 39,  # D#1 Clap
                    "start_time": float(i),
                    "duration": 0.2,
                    "velocity": 110,
                    "mute": False,
                }
            )
    return notes


def get_rumble_pattern(length=4.0):
    """Sub-bass rumble pattern (mirrors kick with lower pitch)."""
    notes = []
    # E0 (16) - Very low sub-bass
    for i in range(int(length * 4)):
        notes.append(
            {
                "pitch": 16,  # E0 (Sub-bass)
                "start_time": float(i),
                "duration": 0.5,
                "velocity": 120 if i % 4 == 0 else 105,
                "mute": False,
            }
        )
    return notes
