# Implementation Plan (P2): Rhythm Section Recipes + CrewAI Agents (Ollama) — Kick → Rumble → Drums

**Status**: Active
**Version**: 2.0.0
**Last Updated**: 2025-12-14
**Depends On**: `specs/active/imp_plan_pt1.rmd`, `specs/active/005.md`, `specs/active/006.md`

## 1. Outcome (What P2 Delivers)

By the end of P2, the system can build and verify the **rhythm section** using deterministic recipes, optionally assisted by CrewAI agents (Ollama):

- 01‑Kick: clip scaffold + basic device chain
- 02‑Rumble: rumble processing chain derived from the kick
- 03‑LowTom / 04‑ClosedHat / 05‑OpenHat / 06‑Ride / 07‑ClapSnare
- 08‑PercLoop1 / 09‑PercLoop2 (sample placeholder + FX scaffold)

The DearPyGUI controller can run:

- “Build Kick”
- “Build Rumble”
- “Build Drums (03–09)”
- “Verify Rhythm Section”

## 2. Principle: Recipes First, Agents Second

Agents can decide **what** to do next and help choose parameters, but **how** to implement the change is encoded as recipes.

This prevents:

- invalid MIDI note dicts
- wrong tool arguments
- runaway device insertion

## 3. Recipe Contracts (Code-Owned, Deterministic)

### 3.1 Kick Recipe (Track 01)

Minimum build steps:

1. Ensure track exists and named `01-Kick` (MIDI).
2. Ensure clip in slot 0 (length 16 beats).
3. Add notes (4‑on‑the‑floor):
   - pitch 36 (C1) on beats 0, 1, 2, 3… for 4 bars
4. Load a kick instrument (Ableton stock; URI resolved per machine).
5. Apply basic EQ/saturation if available (optional in P2, but scaffold chain).

### 3.2 Rumble Recipe (Track 02)

Minimum build steps:

1. Ensure `02-Rumble` exists (Audio).
2. Route audio-from kick (or use an audio effect rack receiving kick, depending on current tool support).
3. Create rumble chain:
   - Reverb (100% wet inside rumble path)
   - Distortion/saturation (Roar or Saturator)
   - Filter/EQ to limit rumble band
   - Sidechain compressor keyed to kick

**Note**: If nested chain inspection is not yet supported, P2 must at least create the rack/chain and verify top-level device presence, and log “needs deep inspection tool” for P3.

### 3.3 Drum Recipes (Tracks 03–09)

These recipes can be simple scaffolds in P2:

- create track + clip(s)
- apply a placeholder drum rack / simpler
- add minimal patterns (closed hats 16ths, open hats off-beat, clap on 2&4, tom fills)

## 4. CrewAI Integration (Ollama)

### 4.1 Why CrewAI in P2

- helpful for “parameter selection” and “variation generation” while staying inside recipe guardrails
- helpful for multi-track drum programming prompts (“make hats more driving but leave kick untouched”)

### 4.2 CrewAI Roles (Minimum)

- **Rhythm Programmer**: suggests MIDI variations within constraints
- **Sound Designer**: suggests device chain parameter settings (no tool calls directly)
- **Verifier**: interprets verification results and proposes adjustments

### 4.3 Tool Wiring Rule

CrewAI tools must call the same adapter built in PT1 (no duplicated DAW control logic).

## 5. DearPyGUI Wiring

Add buttons and progress mapping:

- “Build Kick” → sets Track 01 progress to 1.0 on success
- “Build Rumble” → sets Track 02 progress to 1.0 on success
- “Build Drums (03–09)” → updates tracks 03–09 progressively
- “Verify Rhythm Section” → shows boolean report and score

Include a “HITL Confirm” modal for any action that:

- replaces existing devices
- empties clip slots
- changes routing

## 6. Tests & Gates

### 6.1 Unit Tests

- kick pattern generator returns exactly 16 notes (4 bars * 4 beats) with valid note dicts
- rumble chain spec validates against schema (no empty device names)

### 6.2 Live Integration Gates

- **P2-G1**: “Build Kick” creates a clip in slot 0 and does not error.
- **P2-G2**: “Build Rumble” creates at least the top-level rumble rack/device chain without freezing Ableton.
- **P2-G3**: “Verify Rhythm Section” returns a report with no missing required fields.

## 7. Acceptance Criteria (P2 Done)

- P2-AC1: Kick + Rumble can be created from a blank set via GUI.
- P2-AC2: Drum scaffold for tracks 03–09 exists (tracks named, clips created).
- P2-AC3: All tool calls and outcomes are logged to `events.jsonl`.
