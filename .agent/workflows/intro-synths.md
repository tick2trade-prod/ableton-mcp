---
description: Create all synth tracks for intro section (Bars 1-16)
---
// turbo-all

## Intro Synths Lane

Creates 2 synth tracks for atmospheric texture.

### 1. Track 10: Synth Stabs
```bash
python scripts/workflows/create_track.py stabs intro --instrument wavetable --pattern silent
```

### 2. Track 11: Atmospheric Drone
```bash
python scripts/workflows/create_track.py drone intro --instrument operator --pattern pad
```

### 3. Verify synths lane
```bash
just test-lane-synths
```

## Expected Result
- 2 synth tracks created
- Drone provides atmospheric texture
- Stabs silent for intro (activated in build/drop)
- Synths lane tests pass
