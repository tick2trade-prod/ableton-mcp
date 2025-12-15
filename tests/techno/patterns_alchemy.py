"""
Musical patterns for I/O Alchemy style techno generation.
Key: G Minor (based on librosa analysis: 129.2 BPM, G Minor)
"""


def get_kick_pattern(length=16.0):
    """4-on-the-floor kick pattern at 129 BPM feel.

    Heavy kick on every beat with accent on 1.
    """
    notes = []
    for i in range(int(length * 4)):  # 4 beats per bar
        notes.append(
            {
                "pitch": 36,  # C1 (Standard kick)
                "start_time": float(i),
                "duration": 0.5,
                "velocity": 127 if i % 4 == 0 else 118,
                "mute": False,
            }
        )
    return notes


def get_sub_bass_pattern(length=16.0):
    """G root sub-bass rumble pattern.

    G1 (31) root with 16th note subdivisions for that I/O rumble.
    """
    notes = []
    pitch = 31  # G1 (Sub-bass root)

    for i in range(int(length * 4)):
        base_time = float(i)
        # 16th note rumble: X.25, X.5, X.75
        for offset, vel in [(0.0, 120), (0.25, 85), (0.5, 100), (0.75, 80)]:
            # Skip on-beat to avoid clash with kick
            if offset == 0.0 and i % 4 == 0:
                continue
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


def get_bass_mid_pattern(length=16.0):
    """Mid-range bass following G Minor root movement.

    G2 (43) with occasional 5th (D) movement for tension.
    """
    notes = []
    # G Minor progression feel
    sequence = [
        (0.0, 43, 110),  # G2
        (0.5, 43, 90),
        (1.0, 43, 100),
        (1.5, 50, 85),  # D2 (5th)
        (2.0, 43, 110),
        (2.5, 43, 85),
        (3.0, 46, 95),  # Bb2 (m3)
        (3.5, 43, 80),
    ]

    for bar in range(int(length / 4)):
        bar_offset = bar * 4.0
        for start, pitch, vel in sequence:
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": bar_offset + start,
                    "duration": 0.3,
                    "velocity": vel,
                    "mute": False,
                }
            )
    return notes


def get_acid_lead_pattern(length=16.0):
    """303-style acid lead in G Minor.

    Uses G Minor scale: G, A, Bb, C, D, Eb, F
    """
    notes = []
    # I/O-style acid motif with slides and accents
    motif = [
        (0.0, 55, 110),  # G3
        (0.5, 55, 80),
        (1.0, 62, 120),  # D4 (5th up)
        (1.5, 58, 95),  # Bb3 (m3)
        (2.0, 55, 100),  # G3
        (2.75, 53, 85),  # F3 (m7)
        (3.0, 50, 110),  # D3 (5th)
        (3.5, 46, 90),  # Bb2
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


def get_arp_pattern(length=16.0):
    """16th note arpeggio in G Minor.

    Ascending/descending G Minor triad pattern.
    """
    notes = []
    # Gm arp: G, Bb, D, G (43, 46, 50, 55)
    arp_notes = [43, 46, 50, 55, 50, 46]

    for beat in range(int(length * 4)):
        base_time = float(beat)
        for i, offset in enumerate([0.0, 0.25, 0.5, 0.75]):
            pitch = arp_notes[i % len(arp_notes)]
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": base_time + offset,
                    "duration": 0.15,
                    "velocity": 95 if i == 0 else 75,
                    "mute": False,
                }
            )
    return notes


def get_pad_pattern(length=16.0):
    """Sustained pad chords: Gm -> Dm -> Cm progression.

    Long notes for atmospheric texture.
    """
    notes = []
    # Chord progression (2 bars each)
    chords = [
        ([55, 58, 62], 0.0),  # Gm: G3, Bb3, D4
        ([55, 58, 62], 8.0),  # Gm
        ([50, 53, 57], 16.0),  # Dm: D3, F3, A3
        ([48, 51, 55], 24.0),  # Cm: C3, Eb3, G3
    ]

    for bar_start in range(0, int(length), 8):
        chord_idx = (bar_start // 8) % len(chords)
        chord_notes, _ = chords[chord_idx]
        for pitch in chord_notes:
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": float(bar_start),
                    "duration": 7.5,
                    "velocity": 80,
                    "mute": False,
                }
            )
    return notes


def get_stab_pattern(length=16.0):
    """Offbeat stab chords for Gm.

    Short, punchy chords on offbeats.
    """
    notes = []
    chord = [55, 58, 62]  # Gm: G3, Bb3, D4

    for beat in range(int(length * 4)):
        # Offbeats only (X.5)
        for pitch in chord:
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": beat + 0.5,
                    "duration": 0.1,
                    "velocity": 90,
                    "mute": False,
                }
            )
    return notes


def get_hihat_pattern(length=16.0):
    """Closed hi-hat 8th notes with accents."""
    notes = []
    for beat in range(int(length * 4)):
        for i, offset in enumerate([0.0, 0.5]):
            notes.append(
                {
                    "pitch": 42,  # F#1 (Closed Hat)
                    "start_time": beat + offset,
                    "duration": 0.1,
                    "velocity": 100 if i == 0 else 75,
                    "mute": False,
                }
            )
    return notes


def get_open_hat_pattern(length=16.0):
    """Open hi-hat on offbeats."""
    notes = []
    for beat in range(int(length * 4)):
        notes.append(
            {
                "pitch": 46,  # A#1 (Open Hat)
                "start_time": beat + 0.5,
                "duration": 0.15,
                "velocity": 85,
                "mute": False,
            }
        )
    return notes


def get_clap_pattern(length=16.0):
    """Clap on 2 and 4."""
    notes = []
    for bar in range(int(length / 4)):
        bar_offset = bar * 4.0
        for beat in [1.0, 3.0]:  # Beats 2 and 4
            notes.append(
                {
                    "pitch": 39,  # D#1 (Clap)
                    "start_time": bar_offset + beat,
                    "duration": 0.2,
                    "velocity": 115,
                    "mute": False,
                }
            )
    return notes


def get_perc_pattern(length=16.0):
    """Shaker/percussion pattern with 16th feel."""
    notes = []
    for beat in range(int(length * 4)):
        for offset in [0.25, 0.75]:
            notes.append(
                {
                    "pitch": 70,  # Maracas/shaker
                    "start_time": beat + offset,
                    "duration": 0.1,
                    "velocity": 65,
                    "mute": False,
                }
            )
    return notes


def get_perc2_pattern(length=16.0):
    """Rim shot pattern on every 2 bars."""
    notes = []
    for bar in range(int(length / 4)):
        if bar % 2 == 1:  # Every other bar
            notes.append(
                {
                    "pitch": 37,  # Side stick / rim
                    "start_time": bar * 4.0,
                    "duration": 0.15,
                    "velocity": 95,
                    "mute": False,
                }
            )
    return notes


def get_riser_pattern(length=16.0):
    """FX riser/sweep for section transitions.

    Rising pitch for build-ups.
    """
    notes = []
    # Riser at bar 12-16 (last 4 bars)
    start_bar = 12
    if length >= 16.0:
        for i in range(16):  # 16 notes rising
            notes.append(
                {
                    "pitch": 48 + i,  # Rising from C3 to D#4
                    "start_time": start_bar + (i * 0.25),
                    "duration": 0.5,
                    "velocity": 60 + (i * 4),
                    "mute": False,
                }
            )
    return notes


def get_impact_pattern(length=16.0):
    """Impact/crash on beat 1 of bar 1."""
    notes = []
    notes.append(
        {
            "pitch": 49,  # Crash cymbal
            "start_time": 0.0,
            "duration": 2.0,
            "velocity": 127,
            "mute": False,
        }
    )
    return notes
