# Intro Synths Workflow - Lane 3

Execute TDD workflow for **Synth** tracks (Bars 1-16 of "I Am Machine" intro section).

## Context

Reference: `assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
Benchmark: Compare against `stems/other.wav`

## Tracks to Create (in order)

| # | Track | Test File | Device | Sound |
|---|-------|-----------|--------|-------|
| 10 | Stabs | `test_intro_stabs.py` | Wavetable | Techno stabs |
| 11 | Drone | `test_intro_drone.py` | Operator | Ambient pad |

## Stabs Track

Techno stabs: short, punchy synth hits on off-beats.

```python
class TestIntroStabs:
    def test_track_exists(self, session):
        tracks = session.get_tracks()
        assert any(t["name"] == "Stabs" for t in tracks)

    def test_wavetable_loaded(self, session):
        track = session.get_track_by_name("Stabs")
        assert any(d["name"] == "Wavetable" for d in track["devices"])

    def test_stab_pattern(self, session):
        """Off-beat stab pattern."""
        clip = session.get_clip(10, 0)
        assert clip["length"] == 64.0  # 16 bars
        # Stabs are typically short duration
        notes = clip["notes"]
        avg_duration = sum(n["duration"] for n in notes) / len(notes)
        assert avg_duration < 0.5  # Short notes

    def test_high_pass_filter(self, session):
        """EQ to avoid low-end clash with bass."""
        track = session.get_track_by_name("Stabs")
        eq = next((d for d in track["devices"] if "EQ" in d["name"]), None)
        assert eq is not None
```

## Drone Track

Ambient drone: long sustained pad providing texture.

```python
class TestIntroDrone:
    def test_track_exists(self, session):
        tracks = session.get_tracks()
        assert any(t["name"] == "Drone" for t in tracks)

    def test_operator_loaded(self, session):
        track = session.get_track_by_name("Drone")
        assert any(d["name"] == "Operator" for d in track["devices"])

    def test_reverb_on_drone(self, session):
        """Drone needs reverb for space."""
        track = session.get_track_by_name("Drone")
        devices = [d["name"] for d in track["devices"]]
        assert any("Reverb" in d for d in devices)

    def test_sustained_notes(self, session):
        """Drone has long sustained notes."""
        clip = session.get_clip(11, 0)
        notes = clip["notes"]
        # Drone notes are long
        avg_duration = sum(n["duration"] for n in notes) / len(notes)
        assert avg_duration >= 4.0  # At least 1 bar duration
```

## Device Chains

### Stabs
1. Wavetable (synth)
2. Auto Filter (movement)
3. EQ Eight (high pass)
4. Compressor (punch)

### Drone
1. Operator (synth)
2. Hybrid Reverb (space)
3. Auto Pan (stereo movement)
4. Utility (volume control)

## Execution Steps

1. Create Stabs track with Wavetable
2. Program off-beat stab pattern
3. Add EQ and effects for punch
4. Create Drone track with Operator
5. Program sustained pad notes
6. Add reverb and spatial effects

## Success Criteria

- [ ] Stabs track with Wavetable and punchy sound
- [ ] Off-beat stab pattern (syncopated)
- [ ] Drone track with Operator and reverb
- [ ] Sustained ambient notes
- [ ] Both tracks have 16-bar intro clips
- [ ] Mix balances with drums and bass
