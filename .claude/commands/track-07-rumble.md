# Track 07: Rumble - I Am Machine Recreation

Create the sub bass / rumble track optimized for "I Am Machine" by Lilly Palmer.

## Reference Analysis

**Source**: `/Users/alexzh/ableton-mcp/assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
**Style**: Hard Techno sub bass with aggressive sidechain pumping
**BPM**: 136
**Key**: F minor
**Key Characteristics**:
- Deep sub bass foundation (30-60Hz)
- Heavy sidechain compression from kick
- Saturated/distorted harmonic content
- Creates the "breathing" pump effect

## Sound Design Target

### Synthesizer
- **Primary**: Operator (FM synthesis for sub)
- **URI**: `query:Synths#Operator`
- **Alternative**: Analog or Wavetable

### Operator Settings
- **Algorithm**: 1 (single carrier)
- **Oscillator A**: Sine wave
- **Coarse**: 0 (fundamental only)
- **Level**: Max
- **Filter**: Off (pure sub)

### Processing Chain (Order Matters!)
1. **EQ Eight** - Shape sub
   - High-pass: 25Hz (remove rumble)
   - Low shelf boost: +3dB at 40Hz
   - Cut: 100-200Hz (clean separation from kick)

2. **Saturator** - Harmonic content
   - Type: Analog Clip
   - Drive: 6-10dB
   - Output: Compensate

3. **Compressor** - Sidechain from Kick
   - Sidechain: Track 0 (Kick)
   - Ratio: 8:1 or higher
   - Attack: 0.1ms (instant)
   - Release: 100-150ms (pumping)
   - Threshold: -20dB to -30dB

4. **Utility** - Level control
   - Gain: Adjust to taste

## Intro Pattern (Bars 1-16)

### MIDI Notes
```
Sustained sub bass: F0 (29) or F1 (41)
Each bar = one long note
Velocity: 100 (consistent)
Duration: 4 beats (full bar)
```

### Python Pattern Generator
```python
def rumble_intro_pattern():
    """Rumble sub bass for Intro (Bars 1-16)."""
    notes = []
    bars = 16

    for bar in range(bars):
        notes.append({
            "pitch": 29,  # F0 - deep sub
            "start_time": float(bar * 4),
            "duration": 4.0,  # Full bar sustained
            "velocity": 100,
            "mute": False,
        })
    return notes
```

## Execution Steps

### Step 1: Create Track
```python
# MCP calls
create_midi_track(index=6)
set_track_name(track_index=6, name="Rumble")
```

### Step 2: Load Operator
```python
load_browser_item(track_index=6, item_uri="query:Synths#Operator")
```

### Step 3: Add Processing Chain
```python
# EQ Eight - shape sub
load_browser_item(track_index=6, item_uri="query:AudioFx#EQ%20Eight")

# Saturator - harmonics
load_browser_item(track_index=6, item_uri="query:AudioFx#Saturator")

# Compressor - SIDECHAIN
load_browser_item(track_index=6, item_uri="query:AudioFx#Compressor")
```

### Step 4: Configure Sidechain
```python
# Set compressor sidechain input to Kick (Track 0)
set_sidechain_input(
    track_index=6,
    device_index=-1,  # Last device (Compressor)
    source_track_index=0  # Kick
)
```

### Step 5: Create Clip & Add Notes
```python
create_clip(track_index=6, clip_index=0, length=64.0)  # 16 bars
add_notes_to_clip(track_index=6, clip_index=0, notes=rumble_intro_pattern())
set_clip_name(track_index=6, clip_index=0, name="Rumble - Intro")
```

### Step 6: Preview with Kick
```python
# Fire both clips to hear sidechain pumping
fire_clip(track_index=0, clip_index=0)  # Kick
fire_clip(track_index=6, clip_index=0)  # Rumble
start_playback()
```

## Run Script

```bash
python scripts/workflows/create_intro_bass.py
```

This creates Rumble, Rolling Bass, and Acid tracks with sidechain configured.

## Sidechain Pumping Effect

The signature "pump" comes from:
- **Fast attack** (0.1ms): Instantly ducks when kick hits
- **Medium release** (100-150ms): Smooth return between kicks
- **High ratio** (8:1+): Deep ducking
- **Low threshold**: Ensures every kick triggers

At 136 BPM:
- Beat duration = 441ms
- Optimal release = 100-150ms
- Creates rhythmic breathing effect

## Validation

- [ ] Track 6 named "Rumble"
- [ ] Operator loaded with sine sub
- [ ] Processing chain: EQ > Saturator > Compressor
- [ ] Sidechain routed from Track 0 (Kick)
- [ ] 16-bar clip with sustained F0 notes
- [ ] Audible pumping effect when kick plays
- [ ] Sub doesn't conflict with kick (EQ separation)

## Reference Comparison

After creation, compare with reference:
1. Play kick + rumble together
2. Listen for the pump rhythm
3. A/B compare for:
   - Pump depth (how much the sub ducks)
   - Release timing (smooth vs choppy)
   - Sub weight vs kick clarity
   - Overall groove feel

## Troubleshooting

### No Sidechain Effect
- Check compressor sidechain input is set to Kick
- Verify threshold is low enough
- Ensure kick is playing

### Sub Too Muddy
- Increase EQ high-pass (try 40Hz)
- Cut more at 100-200Hz
- Reduce saturation drive

### Pump Too Aggressive
- Increase release time (150-200ms)
- Raise threshold
- Lower ratio

## Log File

Execution logged to: `scripts/workflows/intro_bass.log`

## Dependencies

- Requires Track 01 (Kick) to be created first for sidechain source

---

## TDD: Red/Green/Refactor

### Test Location
```
tests/phases/phase1_intro/test_track_07_rumble.py
```

### Run Tests (RED Phase)
```bash
# Run all rumble tests - expect failures until implemented
pytest tests/phases/phase1_intro/test_track_07_rumble.py -v

# Run specific test class
pytest tests/phases/phase1_intro/test_track_07_rumble.py::TestRumbleTrackExists -v
pytest tests/phases/phase1_intro/test_track_07_rumble.py::TestRumbleDeviceChain -v
pytest tests/phases/phase1_intro/test_track_07_rumble.py::TestRumbleMIDIPattern -v
pytest tests/phases/phase1_intro/test_track_07_rumble.py::TestRumbleSidechain -v
```

### Test Categories

| Test Class | What It Tests | Pass Criteria |
|------------|---------------|---------------|
| `TestRumbleTrackExists` | Track 6 exists, named "Rumble" | Track visible |
| `TestRumbleDeviceChain` | Operator + EQ + Compressor | Devices loaded |
| `TestRumbleSidechain` | Compressor sidechained to Kick | Routing verified |
| `TestRumbleMIDIPattern` | Sustained F notes, 16 bars | Correct MIDI |
| `TestRumbleSidechainPump` | Pump depth and timing | Manual verify |

### RED → GREEN → REFACTOR Cycle

**RED Phase** (Tests Fail):
```bash
pytest tests/phases/phase1_intro/test_track_07_rumble.py -v
# Expected: FAILED - track doesn't exist yet
```

**GREEN Phase** (Implement to Pass):
```bash
# Create kick first (sidechain source)
python scripts/workflows/create_intro_drums.py

# Then create rumble
python scripts/workflows/create_intro_bass.py

# Re-run tests
pytest tests/phases/phase1_intro/test_track_07_rumble.py -v
# Expected: PASSED (except manual verification tests)
```

**REFACTOR Phase** (Optimize Pump):
1. Play Kick + Rumble together
2. Adjust compressor threshold (-25dB to -35dB)
3. Adjust release time (100-150ms for groove)
4. A/B compare with reference
5. Iterate until pump feels right

### Sidechain Verification

Tests can verify compressor exists but **sidechain routing must be manually verified**:

1. Open Compressor on Rumble track
2. Click sidechain arrow (triangle icon)
3. Verify settings:
   - **Audio From**: "Kick" or "1-Kick"
   - **Sidechain**: Enabled (lit)

### Similarity Metrics

The tests measure:
- **Structural**: Track 6 exists with Operator + Compressor
- **Pattern**: Sustained F notes covering 16 bars
- **Routing**: Compressor in chain (sidechain manual)
- **Pump**: (Manual) Duck depth and release feel

### Manual Verification Checklist

After tests pass:
1. [ ] Play Kick + Rumble together
2. [ ] Verify audible pumping on each kick
3. [ ] Kick punches through clearly (not muddy)
4. [ ] Sub returns smoothly between kicks
5. [ ] A/B with reference - groove feels similar

### Compressor Quick Reference

```
Threshold: -30dB (adjust for pump depth)
Ratio: 8:1 to inf:1
Attack: 0.1ms (instant)
Release: 120ms (adjust for 136 BPM groove)
```

---

## Next Tracks

After rumble:
- Track 08: Rolling Bass
- Track 09: Acid Line
