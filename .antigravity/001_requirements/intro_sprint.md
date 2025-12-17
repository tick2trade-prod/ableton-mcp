# Intro Section Sprint Plan

## Goal
Complete all 16 tracks for **Intro (Bars 1-16)** as fast as possible.

---

## Parallelization Strategy

### Why Parallelize?
- 16 tracks are **independent** within a section
- No dependency between Kick and Synth for same bars
- Can run multiple agents/CLIs simultaneously

### Parallel Lanes

```
Lane 1 (Drums)      Lane 2 (Bass)       Lane 3 (Synths)     Lane 4 (Vocals/FX)
─────────────────   ─────────────────   ─────────────────   ─────────────────
Track 01: Kick      Track 07: Rumble    Track 10: Stabs     Track 12: Main Vocal
Track 02: Snare     Track 08: Rolling   Track 11: Drone     Track 13: Vocal FX
Track 03: Hi-hats   Track 09: Acid                          Track 14: Risers
Track 04: Toms                                              Track 15: Return A
Track 05: Glitch                                            Track 16: Return B
Track 06: Ride
```

### Execution Options

| Method | Parallel? | How |
|--------|-----------|-----|
| **4 Terminal tabs** | ✅ Yes | Each runs one lane |
| **DearPyGUI** | ❌ No | Single process |
| **Gemini headless** | ✅ Yes | Multiple instances |
| **Claude CLI** | ⚠️ Limited | One at a time |

---

## Fastest Approach: 4 Parallel Terminals

### Setup
```bash
# Terminal 1: Drums
python scripts/create_intro.py --lane=drums

# Terminal 2: Bass
python scripts/create_intro.py --lane=bass

# Terminal 3: Synths
python scripts/create_intro.py --lane=synths

# Terminal 4: Vocals/FX
python scripts/create_intro.py --lane=vocals
```

### Estimated Time

| Lane | Tracks | Est. per track | Total |
|------|--------|----------------|-------|
| Drums | 6 | 5 min | 30 min |
| Bass | 3 | 8 min | 24 min |
| Synths | 2 | 8 min | 16 min |
| Vocals/FX | 5 | 5 min | 25 min |

**Serial**: ~2.5 hours
**Parallel (4 lanes)**: ~30 min (bottleneck = longest lane)

---

## Track Dependencies

### Order Within Drums Lane
```
1. Kick (first - other drums reference it)
2. Snare/Clap
3. Hi-hats
4. Toms
5. Glitch
6. Ride
```

### Order Within Bass Lane
```
1. Rumble (needs Kick for sidechain reference)
2. Rolling Bass
3. Acid Line
```

### Order Within Synths Lane
```
1. Stabs
2. Drone
```

### Order Within Vocals/FX Lane
```
1. Return A (Reverb) - setup first
2. Return B (Delay) - setup first
3. Risers
4. Main Vocal
5. Vocal FX
```

---

## Intro Track Checklist

### Drums (Lane 1)
- [ ] Track 01: Kick - Intro pattern
- [ ] Track 02: Snare - Intro pattern (sparse or silent?)
- [ ] Track 03: Hi-hats - Intro pattern
- [ ] Track 04: Toms - Intro pattern (none?)
- [ ] Track 05: Glitch - Intro pattern
- [ ] Track 06: Ride - Intro pattern (none?)

### Bass (Lane 2)
- [ ] Track 07: Rumble - Intro pattern
- [ ] Track 08: Rolling Bass - Intro pattern (none?)
- [ ] Track 09: Acid Line - Intro pattern (none?)

### Synths (Lane 3)
- [ ] Track 10: Stabs - Intro pattern (none?)
- [ ] Track 11: Drone - Intro pattern (atmospheric)

### Vocals/FX (Lane 4)
- [ ] Track 12: Main Vocal - Intro (teaser?)
- [ ] Track 13: Vocal FX - Intro (ambient)
- [ ] Track 14: Risers - Intro (buildup texture)
- [ ] Track 15: Return A - Reverb configured
- [ ] Track 16: Return B - Delay configured

---

## What to Build First

### Foundation (Must complete before others)
1. **Tempo/BPM** - Set to 136
2. **Kick** - All other drums/bass reference this
3. **Return A/B** - Sends need to exist

### Then Parallel
- Drums lane can proceed
- Bass lane can proceed (sidechain to Kick)
- Synths lane can proceed
- Vocals/FX lane can proceed

---

## Agent Assignment

| Track | Agent | Notes |
|-------|-------|-------|
| Kick | PercussionAgent | 4-on-floor |
| Snare | PercussionAgent | |
| Hi-hats | PercussionAgent | |
| Toms | PercussionAgent | |
| Glitch | PercussionAgent | |
| Ride | PercussionAgent | |
| Rumble | SynthesizerAgent | Sub bass |
| Rolling Bass | SynthesizerAgent | FM |
| Acid | SynthesizerAgent | 303 |
| Stabs | SynthesizerAgent | Wavetable |
| Drone | SynthesizerAgent | Meld |
| Main Vocal | VocalsAgent | |
| Vocal FX | VocalsAgent | |
| Risers | TransitionAgent | |
| Return A | ReturnTrackAgent | |
| Return B | ReturnTrackAgent | |

---

## Immediate Next Steps

1. **Create `scripts/create_intro.py`** with lane support
2. **Set tempo to 136 BPM** in Ableton
3. **Create Return tracks** first
4. **Run 4 lanes in parallel**
5. **Verify Intro plays correctly**

---

## Decision Needed

**D008: Intro First Strategy**
- **Status**: PENDING APPROVAL
- **Proposal**: Complete Intro (all 16 tracks) before any other section
- **Rationale**:
  - Most setup/learning happens once
  - Remaining sections = duplicate patterns + variations
  - Parallelizable within section
