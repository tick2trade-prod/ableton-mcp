---
description: Create all drum tracks for intro section (Bars 1-16)
---
// turbo-all

## Intro Drums Lane

Creates 6 drum tracks for the intro section at 136 BPM.

### 1. Set tempo
```bash
python scripts/workflows/create_track.py --section intro --action set_tempo --bpm 136
```

### 2. Track 01: Kick
```bash
python scripts/workflows/create_track.py kick intro --pattern 4-on-floor
```

### 3. Track 02: Snare
```bash
python scripts/workflows/create_track.py snare intro --pattern sparse
```

### 4. Track 03: Hi-hats
```bash
python scripts/workflows/create_track.py hihats intro --pattern closed_8th
```

### 5. Track 04: Toms
```bash
python scripts/workflows/create_track.py toms intro --pattern minimal
```

### 6. Track 05: Glitch
```bash
python scripts/workflows/create_track.py glitch intro --pattern industrial
```

### 7. Track 06: Ride
```bash
python scripts/workflows/create_track.py ride intro --pattern subtle
```

### 8. Verify drums lane
```bash
just test-lane-drums
```

## Expected Result
- 6 drum tracks created
- Kick has 4-on-floor pattern (Bars 1-16)
- All clips visible in Ableton Session View
- Drumslane tests pass
