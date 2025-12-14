# Implementation Plan (P3): Full 16-Track Scaffold + Verifier + “Run All”

**Status**: Active
**Version**: 2.0.0
**Last Updated**: 2025-12-14
**Depends On**: `specs/active/imp_plan_p2.md`, `specs/active/005.md`, `specs/active/006.md`

## 1. Outcome (What P3 Delivers)

By the end of P3, the system can:

- build *all 16 tracks* to a consistent scaffold
- run a deterministic “Run All” pipeline (with section gates)
- produce a machine-readable verification report covering the MVP acceptance criteria

P3 focuses on completeness + verification, not “perfect sound”.

## 2. Expand Recipes to Tracks 10–16

### 2.1 Bass (Track 10)

- create 4‑bar rolling bass pattern (F minor constraint)
- load stock instrument (Operator/Wavetable) with a safe preset
- apply basic EQ/sidechain (optional scaffold)

### 2.2 Main Synth (Track 11)

- create motif clip placeholders (MVP may start with 1–2 note motif scaffold)
- load a saw-based synth (Wavetable)
- add distortion + delay/reverb scaffold

### 2.3 Vocal Main / Vocal FX (Tracks 12–13)

- create tracks and routing scaffold
- **do not** require copyrighted samples; provide “user drop zone” workflow:
  - user loads a licensed sample into the track manually
  - GUI marks track as “Ready for processing”
- Vocal FX chain scaffold: delay/reverb/filters

### 2.4 FX (Tracks 14–16)

- add riser/impact placeholders (sample slots or synth noise)
- add atmosphere pad/drone scaffold

## 3. Verifier (Critical P3 Component)

### 3.1 Verifier Output Format

Verifier must output:

- `checks`: map of boolean checks (AC‑001…)
- `score`: numeric summary
- `missing_tools`: list of checks that cannot yet be automated due to tool gaps
- `recommendations`: next actions

### 3.2 Required New Tooling (If Missing)

To fully automate verification, P3 may require extending the tool surface to include:

- clip note inspection (e.g., `get_clip_notes(track_index, clip_index)`)
- nested device/rack chain inspection (e.g., `get_device_tree(track_index)`)
- parameter addressing by name (e.g., `set_device_param_by_name(...)`)

If these tools are not implemented, P3 must still:

- detect the gap
- surface it in `missing_tools`
- allow manual verification steps in the GUI

## 4. “Run All” Pipeline

### 4.1 Section Ordering

Recommended order:

1. Bootstrap + naming
2. Kick + Rumble
3. Drums (03–09)
4. Bass + Synth
5. Vocals
6. FX + Atmosphere
7. Verify (full)

### 4.2 Gates

After each section, require:

- verify subset checks
- pause for HITL approval if failures exist

## 5. UX Completion in DearPyGUI

Add:

- “Run All” / “Pause” / “Stop” buttons
- per-section progress (not just per-track)
- a “Failures” panel with actionable items

## 6. Tests & Release Gate

### 6.1 Unit Tests

- pattern generators for bass/synth must validate note ranges + scale constraints
- verifier report schema validation

### 6.2 Live Gates

- **P3-G1**: “Run All” completes without crashing Ableton
- **P3-G2**: basic acceptance criteria pass (tempo, 16 tracks, key track scaffolds)
- **P3-G3**: verifier produces non-empty report and logs missing automation tools explicitly

## 7. Acceptance Criteria (P3 Done)

- P3-AC1: From a blank Live Set, “Run All” produces a 16-track scaffold with correct names.
- P3-AC2: Verifier runs and produces a report aligned to PRD §9.
- P3-AC3: The system is safe to re-run (idempotent ensures; no runaway duplication).
