# Track 01: Kick - I Am Machine Recreation

Create the kick drum track optimized for "I Am Machine" by Lilly Palmer.

## Reference Analysis

**Source**: `/Users/alexzh/ableton-mcp/assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`
**Style**: Hard Techno / Industrial Techno
**BPM**: 136
**Key Characteristics**:
- Punchy, distorted 909-style kick
- Heavy low-end with sub presence
- Saturated/driven character
- 4-on-floor pattern with slight variations

## Sound Design Target

### Drum Kit
- **Primary**: 909 Core Kit (bundled with Live)
- **URI**: `query:Drums#FileId_14946`
- **Alternative**: Drum Rack with custom 909 sample

### Processing Chain
1. **Drum Buss** - Glue and punch
   - Drive: 30-40%
   - Crunch: Medium
   - Boom: Adjust for sub weight
2. **Saturator** - Harmonic warmth
   - Drive: Soft clip
   - Output: -3dB compensation
3. **EQ Eight** - Shape
   - High-pass: 30Hz (clean sub)
   - Boost: 60-80Hz (punch)
   - Cut: 200-400Hz (mud removal)
   - Presence: 3-5kHz (click)
4. **Compressor** - Punch
   - Ratio: 4:1
   - Attack: 10ms
   - Release: Auto

## Intro Pattern (Bars 1-16)

### MIDI Notes
```
4-on-floor: Every beat (quarter notes)
Pitch: 36 (C1 - standard kick)
Velocity: 100-110 (consistent power)
Duration: 0.5 beats (short, punchy)
```

### Python Pattern Generator
```python
def kick_intro_pattern():
    """Kick pattern for Intro (Bars 1-16)."""
    notes = []
    bars = 16
    beats_per_bar = 4

    for bar in range(bars):
        for beat in range(beats_per_bar):
            notes.append({
                "pitch": 36,
                "start_time": float(bar * 4 + beat),
                "duration": 0.5,
                "velocity": 105,
                "mute": False,
            })
    return notes
```

## Execution Steps

### Step 1: Create Track
```python
# MCP calls
create_midi_track(index=0)
set_track_name(track_index=0, name="Kick")
```

### Step 2: Load 909 Kit
```python
load_browser_item(track_index=0, item_uri="query:Drums#FileId_14946")
```

### Step 3: Add Processing
```python
# Drum Buss
load_browser_item(track_index=0, item_uri="query:AudioFx#Drum%20Buss")

# Saturator
load_browser_item(track_index=0, item_uri="query:AudioFx#Saturator")

# EQ Eight
load_browser_item(track_index=0, item_uri="query:AudioFx#EQ%20Eight")

# Compressor
load_browser_item(track_index=0, item_uri="query:AudioFx#Compressor")
```

### Step 4: Create Clip & Add Notes
```python
create_clip(track_index=0, clip_index=0, length=64.0)  # 16 bars
add_notes_to_clip(track_index=0, clip_index=0, notes=kick_intro_pattern())
set_clip_name(track_index=0, clip_index=0, name="Kick - Intro")
```

### Step 5: Preview
```python
fire_clip(track_index=0, clip_index=0)
start_playback()
```

## Run Script

```bash
python scripts/workflows/create_intro_drums.py
```

This script creates all 6 drum tracks including kick with 909 kit loaded.

## Validation

- [ ] Track 0 named "Kick"
- [ ] 909 Core Kit loaded
- [ ] Processing chain: Drum Buss > Saturator > EQ Eight > Compressor
- [ ] 16-bar clip with 64 kick notes (4-on-floor)
- [ ] Punchy, distorted sound matching reference
- [ ] Sidechain source for Rumble track

## Reference Comparison

After creation, compare with reference:
1. Solo the kick track
2. Play reference in parallel
3. A/B compare for:
   - Low-end weight (sub presence)
   - Punch (transient attack)
   - Saturation character
   - Overall level

## Log File

Execution logged to: `scripts/workflows/intro_drums.log`

---

## TDD: Red/Green/Refactor

### Test Location
```
tests/phases/phase1_intro/test_track_01_kick.py
```

### Run Tests (RED Phase)
```bash
# Run all kick tests - expect failures until implemented
pytest tests/phases/phase1_intro/test_track_01_kick.py -v

# Run specific test class
pytest tests/phases/phase1_intro/test_track_01_kick.py::TestKickTrackExists -v
pytest tests/phases/phase1_intro/test_track_01_kick.py::TestKickDeviceChain -v
pytest tests/phases/phase1_intro/test_track_01_kick.py::TestKickMIDIPattern -v
```

### Test Categories

| Test Class | What It Tests | Pass Criteria |
|------------|---------------|---------------|
| `TestKickTrackExists` | Track 0 exists, named "Kick" | Track visible in Ableton |
| `TestKickDeviceChain` | 909 kit + processing loaded | Devices in chain |
| `TestKickMIDIPattern` | 64 notes, 4-on-floor, C1 | Correct MIDI |
| `TestKickReferenceSimilarity` | Timing matches reference | Onset alignment |

### RED → GREEN → REFACTOR Cycle

**RED Phase** (Tests Fail):
```bash
pytest tests/phases/phase1_intro/test_track_01_kick.py -v
# Expected: FAILED - track doesn't exist yet
```

**GREEN Phase** (Implement to Pass):
```bash
# Run the creation script
python scripts/workflows/create_intro_drums.py

# Re-run tests
pytest tests/phases/phase1_intro/test_track_01_kick.py -v
# Expected: PASSED - track now exists with correct setup
```

**REFACTOR Phase** (Optimize Sound):
1. A/B compare with reference
2. Adjust EQ, saturation, compression
3. Re-run similarity tests
4. Iterate until satisfied

### Similarity Metrics

The tests measure:
- **Structural**: Track exists with correct name and devices
- **Pattern**: 64 notes on quarter beats at C1
- **Timing**: Kick onsets align with reference (within 50ms)
- **Spectral**: (Manual) Frequency content matches reference

### Manual Verification

After tests pass, manually verify:
1. Play reference first 30 seconds
2. Solo your kick track
3. A/B compare for:
   - [ ] Punch (transient attack)
   - [ ] Low-end weight (sub content)
   - [ ] Saturation character
   - [ ] Overall level balance

---

## Next Track

After kick: `/track-07-rumble` (needs kick for sidechain)
