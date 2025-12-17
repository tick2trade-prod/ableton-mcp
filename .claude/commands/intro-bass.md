# Intro Bass Workflow - Lane 2

Execute TDD workflow for **Bass** tracks (Bars 1-16 of "I Am Machine" intro section).

## Context

Reference: `assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
Benchmark: Compare against `stems/bass.wav`

## Tracks to Create (in order)

| # | Track | Test File | Device | Special |
|---|-------|-----------|--------|---------|
| 7 | Rumble | `test_intro_rumble.py` | Operator + Roar | Sidechain to Kick |
| 8 | Rolling Bass | `test_intro_rolling_bass.py` | Wavetable | Acid pattern |
| 9 | Acid | `test_intro_acid.py` | Drift | 303 sound |

## P0 Blocker: Rumble Track

The Rumble track requires:
1. **Roar** saturation effect (Suite only)
2. **Compressor** with sidechain input from Kick

### Rumble TDD Tests

```python
class TestIntroRumble:
    def test_track_exists(self, session):
        tracks = session.get_tracks()
        assert any(t["name"] == "Rumble" for t in tracks)

    def test_operator_loaded(self, session):
        track = session.get_track_by_name("Rumble")
        assert any(d["name"] == "Operator" for d in track["devices"])

    @pytest.mark.suite  # Only run on Ableton Suite
    def test_roar_loaded(self, session):
        """Suite-only: Roar saturation."""
        track = session.get_track_by_name("Rumble")
        devices = [d["name"] for d in track["devices"]]
        assert "Roar" in devices

    def test_sidechain_to_kick(self, session):
        """Compressor sidechained to Kick."""
        track = session.get_track_by_name("Rumble")
        compressor = next(d for d in track["devices"] if d["name"] == "Compressor")
        assert compressor["sidechain_source"] == "Kick"

    def test_clip_has_notes(self, session):
        clip = session.get_clip(6, 0)  # Track 6, clip 0
        assert clip["length"] == 64.0  # 16 bars
        # Sub bass: sustained low notes
        assert all(n["pitch"] <= 48 for n in clip["notes"])
```

## Device Chain for Rumble

Per `state/tracks/rumble.json`:
1. Operator (synth)
2. Hybrid Reverb
3. Roar (saturation)
4. EQ Eight
5. Compressor (with sidechain)

## Rolling Bass / Acid Pattern

```python
class TestIntroRollingBass:
    def test_wavetable_loaded(self, session):
        track = session.get_track_by_name("Rolling Bass")
        assert any(d["name"] == "Wavetable" for d in track["devices"])

    def test_acid_pattern(self, session):
        """16th note acid pattern with slides."""
        clip = session.get_clip(7, 0)
        notes = clip["notes"]
        # Check for characteristic acid slides
        assert len(notes) >= 32  # 16th notes over 16 bars
```

## Execution Steps

1. Ensure Kick track exists (Lane 1 dependency)
2. Create Rumble track with full device chain
3. Set up sidechain routing from Kick to Rumble's Compressor
4. Create Rolling Bass and Acid tracks
5. Program intro patterns for each

## State Files

- `state/tracks/rumble.json` - Rumble spec with effects chain
- `state/tracks/rolling_bass.json` - Rolling bass spec
- `state/tracks/acid.json` - Acid bass spec

## Success Criteria

- [ ] Rumble has Operator + Roar + sidechained Compressor
- [ ] Sidechain pumping is audible
- [ ] Rolling Bass has acid pattern
- [ ] All bass tracks have 16-bar intro clips
- [ ] Low end sits well with Kick (no mud)
