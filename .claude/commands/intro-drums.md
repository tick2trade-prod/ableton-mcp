# Intro Drums Workflow - Lane 1

Execute TDD workflow for **Drums** tracks (Bars 1-16 of "I Am Machine" intro section).

## Context

Reference: `assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
Benchmark: Compare against `stems/drums.wav`

## Tracks to Create (in order)

| # | Track | Test File | Device | Pattern |
|---|-------|-----------|--------|---------|
| 1 | Kick | `test_intro_kick.py` | Drum Rack | 4-on-floor |
| 2 | Snare | `test_intro_snare.py` | Drum Rack | Off-beat hits |
| 3 | Hi-hats | `test_intro_hihats.py` | Drum Rack | 16th notes |
| 4 | Toms | `test_intro_toms.py` | Drum Rack | Fills |
| 5 | Glitch | `test_intro_glitch.py` | Drum Rack | Stutter/glitch |
| 6 | Ride | `test_intro_ride.py` | Drum Rack | Cymbal pattern |

## TDD Pattern (per track)

```
RED    -> Write failing test in tests/phases/test_intro_{track}.py
GREEN  -> Implement minimum code to pass via MCP tools
REFACTOR -> Clean up, verify clip plays correctly
```

## Test Structure Template

```python
class TestIntro{Track}:
    """RED/GREEN/REFACTOR for {Track} track."""

    def test_track_exists(self, session):
        """RED: Track must exist."""
        tracks = session.get_tracks()
        assert any(t["name"] == "{Track}" for t in tracks)

    def test_drum_rack_loaded(self, session):
        """RED: Drum Rack on track."""
        track = session.get_track_info({index})
        assert track["devices"][0]["name"] == "Drum Rack"

    def test_clip_has_notes(self, session):
        """RED: 16-bar clip with correct pattern."""
        clip = session.get_clip({index}, 0)
        assert clip["length"] == 64.0  # 16 bars
```

## Execution Steps

1. Create test file for each track (RED phase)
2. Run `just test-phase1` to see failures
3. Use MCP tools to create track, load Drum Rack, add notes (GREEN phase)
4. Verify each track via `just tdd track={name}`
5. Move to next track

## State Files

Track specs in: `state/tracks/`
- `kick.json` - Kick drum spec
- `snare.json` - Snare spec
- etc.

## Success Criteria

- [ ] All 6 drum tracks exist
- [ ] Each has Drum Rack loaded
- [ ] Each has 16-bar intro clip
- [ ] Notes match reference pattern
- [ ] Plays in sync with Ableton session
