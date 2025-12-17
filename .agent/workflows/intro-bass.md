---
description: Create all bass tracks for intro section (Bars 1-16)
---
// turbo-all

## Intro Bass Lane

Creates 3 bass tracks with sidechain compression for intro section.

### 1. Track 07: Rumble (Sub Bass)
```bash
python scripts/workflows/create_track.py rumble intro --pattern sub_bass --effects hybrid_reverb,roar,eq_eight,compressor
```

### 2. Configure sidechain from Kick to Rumble
```bash
python scripts/workflows/setup_sidechain.py --source kick --target rumble
```

### 3. Track 08: Rolling Bass
```bash
python scripts/workflows/create_track.py rolling_bass intro --pattern fm_bass --silent
```

### 4. Track 09: Acid Line
```bash
python scripts/workflows/create_track.py acid intro --pattern 303 --silent
```

### 5. Verify bass lane
```bash
just test-lane-bass
```

## Expected Result
- 3 bass tracks created
- Rumble has Roar saturation + sidechain from Kick
- Pumping effect audible when Kick plays
- Bass lane tests pass
