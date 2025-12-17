# Intro Vocals/FX Workflow - Lane 4

Execute TDD workflow for **Vocals and FX** tracks (Bars 1-16 of "I Am Machine" intro section).

## Context

Reference: `assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
Benchmark: Compare against `stems/vocals.wav`

## Tracks to Create (in order)

| # | Track | Test File | Type | Purpose |
|---|-------|-----------|------|---------|
| 12 | Main Vocal | `test_intro_vocal.py` | Audio/Sampler | Lead vocal |
| 13 | Vocal FX | `test_intro_vocal_fx.py` | Effects | Vocal processing |
| 14 | Risers | `test_intro_risers.py` | FX | Build tension |
| 15 | Return A | `test_intro_return_a.py` | Return | Reverb send |
| 16 | Return B | `test_intro_return_b.py` | Return | Delay send |

## Main Vocal Track

```python
class TestIntroVocal:
    def test_track_exists(self, session):
        tracks = session.get_tracks()
        assert any(t["name"] == "Main Vocal" for t in tracks)

    def test_sampler_or_audio(self, session):
        """Vocal can be Sampler or audio clip."""
        track = session.get_track_by_name("Main Vocal")
        # Either has Sampler device or is audio track
        has_sampler = any(d["name"] == "Sampler" for d in track.get("devices", []))
        is_audio = track.get("type") == "audio"
        assert has_sampler or is_audio

    def test_vocal_processing(self, session):
        """Vocal needs EQ and compression."""
        track = session.get_track_by_name("Main Vocal")
        devices = [d["name"] for d in track.get("devices", [])]
        assert any("EQ" in d for d in devices)
        assert any("Compressor" in d or "Glue" in d for d in devices)
```

## Vocal FX Track

```python
class TestIntroVocalFX:
    def test_track_exists(self, session):
        tracks = session.get_tracks()
        assert any(t["name"] == "Vocal FX" for t in tracks)

    def test_creative_effects(self, session):
        """Has creative vocal effects."""
        track = session.get_track_by_name("Vocal FX")
        devices = [d["name"].lower() for d in track.get("devices", [])]
        # Should have at least one creative effect
        creative = ["vocoder", "grain", "shifter", "delay", "reverb", "echo"]
        assert any(c in " ".join(devices) for c in creative)
```

## Risers Track

```python
class TestIntroRisers:
    def test_track_exists(self, session):
        tracks = session.get_tracks()
        assert any(t["name"] == "Risers" for t in tracks)

    def test_riser_device(self, session):
        """Risers use Wavetable or audio."""
        track = session.get_track_by_name("Risers")
        has_wavetable = any(d["name"] == "Wavetable" for d in track.get("devices", []))
        is_audio = track.get("type") == "audio"
        assert has_wavetable or is_audio

    def test_automation_for_build(self, session):
        """Risers should have filter/volume automation."""
        # Note: This may require checking automation lanes
        pass  # Implementation depends on MCP capabilities
```

## Return Tracks

```python
class TestIntroReturnA:
    def test_return_exists(self, session):
        returns = session.get_return_tracks()
        assert any(r["name"] == "Reverb" or r["name"] == "Return A" for r in returns)

    def test_reverb_loaded(self, session):
        returns = session.get_return_tracks()
        reverb_return = next(r for r in returns if "Reverb" in r["name"] or r["index"] == 0)
        devices = [d["name"] for d in reverb_return.get("devices", [])]
        assert any("Reverb" in d for d in devices)

class TestIntroReturnB:
    def test_return_exists(self, session):
        returns = session.get_return_tracks()
        assert any(r["name"] == "Delay" or r["name"] == "Return B" for r in returns)

    def test_delay_loaded(self, session):
        returns = session.get_return_tracks()
        delay_return = next(r for r in returns if "Delay" in r["name"] or r["index"] == 1)
        devices = [d["name"] for d in delay_return.get("devices", [])]
        assert any("Delay" in d or "Echo" in d for d in devices)
```

## Device Chains

### Main Vocal
1. Sampler (if using samples) or Audio clip
2. EQ Eight (remove mud)
3. Compressor (dynamics)
4. De-esser (optional)

### Vocal FX
1. Vocoder or Grain Delay
2. Reverb (big space)
3. Delay (rhythmic)

### Risers
1. Wavetable (sweep sound)
2. Auto Filter (movement)
3. Utility (volume automation target)

### Return A (Reverb)
1. Hybrid Reverb or Reverb
2. EQ Eight (high pass the reverb)

### Return B (Delay)
1. Echo or Delay
2. Auto Filter (filter the delays)

## Execution Steps

1. Create Return tracks first (A=Reverb, B=Delay)
2. Create Main Vocal track with processing chain
3. Create Vocal FX track with creative effects
4. Create Risers track for tension builds
5. Set up sends from vocal tracks to returns

## P0 Tool Required

This lane requires `create_return_track` tool from Sprint 0:

```python
def test_create_return_track():
    result = mcp.create_return_track(name="Reverb")
    assert result["status"] == "success"
    assert "index" in result["result"]
```

## Success Criteria

- [ ] Return A has Reverb loaded
- [ ] Return B has Delay loaded
- [ ] Main Vocal has EQ + Compression
- [ ] Vocal FX has creative processing
- [ ] Risers ready for build sections
- [ ] All tracks sending to returns appropriately
- [ ] Intro vocal elements present (if applicable)
