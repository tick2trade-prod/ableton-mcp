---
description: Create vocal/FX tracks and return tracks for intro section (Bars 1-16)
---
// turbo-all

## Intro Vocals/FX Lane

Creates vocal, FX, and return tracks.

### 1. Create Return A (Reverb)
```bash
python scripts/workflows/create_return.py reverb --effect hybrid_reverb
```

### 2. Create Return B (Delay)
```bash
python scripts/workflows/create_return.py delay --effect echo
```

### 3. Track 12: Main Vocal
```bash
python scripts/workflows/create_track.py main_vocal intro --type audio --pattern teaser
```

### 4. Track 13: Vocal FX
```bash
python scripts/workflows/create_track.py vocal_fx intro --pattern ambient
```

### 5. Track 14: Risers
```bash
python scripts/workflows/create_track.py risers intro --pattern buildup
```

### 6. Verify vocals/FX lane
```bash
just test-lane-vocals
```

## Expected Result
- 2 return tracks configured (Reverb, Delay)
- 3 vocal/FX tracks created
- Return sends functional
- Vocals lane tests pass
