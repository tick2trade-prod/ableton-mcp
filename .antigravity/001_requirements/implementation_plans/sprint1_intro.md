# Sprint 1: Intro Section (Bars 1-16)

## Goal
Create 16 tracks for the Intro section using TDD.

**Reference**: `assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`

---

## 4 Parallel Lanes

### Lane 1: Drums (`/intro-drums`)
| # | Track | Device | Status |
|---|-------|--------|--------|
| 1 | Kick | Drum Rack | [ ] |
| 2 | Snare | Drum Rack | [ ] |
| 3 | Hi-hats | Drum Rack | [ ] |
| 4 | Toms | Drum Rack | [ ] |
| 5 | Glitch | Audio Effect Rack | [ ] |
| 6 | Ride | Drum Rack | [ ] |

### Lane 2: Bass (`/intro-bass`)
| # | Track | Device | Status |
|---|-------|--------|--------|
| 7 | Rumble | Roar + Compressor (SC) | [ ] |
| 8 | Rolling Bass | Drift | [ ] |
| 9 | Acid | Analog | [ ] |

### Lane 3: Synths (`/intro-synths`)
| # | Track | Device | Status |
|---|-------|--------|--------|
| 10 | Stabs | Wavetable | [ ] |
| 11 | Drone | Operator | [ ] |

### Lane 4: Vocals/FX (`/intro-vocals`)
| # | Track | Device | Status |
|---|-------|--------|--------|
| 12 | Main Vocal | Sampler | [ ] |
| 13 | Vocal FX | Effects | [ ] |
| 14 | Risers | FX | [ ] |
| 15 | Return A | Reverb | [ ] |
| 16 | Return B | Delay | [ ] |

---

## Key URIs (Suite)

```python
ROAR = "query:AudioFx#Roar"
DRIFT = "query:Synths#Drift"
DRUM_RACK = "query:Synths#Drum%20Rack"
COMPRESSOR = "query:AudioFx#Compressor"
HYBRID_REVERB = "query:AudioFx#Hybrid%20Reverb"
DELAY = "query:AudioFx#Delay"
```

---

## Execution Order

1. **Lane 1**: Kick → Snare → Hi-hats → Toms → Glitch → Ride
2. **Lane 2**: Rumble (P0) → Rolling Bass → Acid
3. **Lane 3**: Stabs → Drone
4. **Lane 4**: Returns → Main Vocal → FX

---

## Definition of Done

- [ ] All 16 tracks created
- [ ] Drum patterns: 4-on-floor kick, offbeat hats
- [ ] Rumble: Roar + sidechain to Kick
- [ ] Returns: Reverb A, Delay B
- [ ] Manual playback verification
