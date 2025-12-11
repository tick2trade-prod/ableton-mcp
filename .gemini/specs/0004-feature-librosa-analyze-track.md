# 0004: Audio Analysis Feature

| Field | Value |
|-------|-------|
| Branch | `feature/0004-audio-analysis` (Proposed) |
| Feature| Audio Signal Analysis Tool |
| Status | 📝 Planning |

---

## Objective
Develop a robust CLI tool using `librosa` to analyze reference audio tracks and extract musical features (BPM, Key, Sections) to guide programmatic reproduction in Ableton Live.

## Prerequisites
- [x] Python environment with `uv`
- [ ] `ffmpeg` installed (for mp3 support)
- [ ] Dependencies: `librosa`, `numpy`, `scipy`

## Requirements

### 1. Analysis Script (`analysis/analyze_track.py`)
- [ ] **Robust Loading**: Handle various formats (mp3, wav, aif).
- [ ] **Feature Extraction**:
    - **Tempo**: Extract BPM (scalar).
    - **Key**: Detect root note and mode (Major/Minor).
    - **Structure**: (Optional) Detect drop/breakdown using RMS energy.
- [ ] **Output**:
    - Print human-readable summary.
    - (Future) Generate JSON for test consumption.

### 2. Integration
- [ ] `install-analysis` Make target.
- [ ] Error handling for missing backends (`NoBackendError`).

## Workflow
1. User adds reference track to `assets/audio/reference/`.
2. Runs `make analyze TRACK=assets/audio/reference/paramore.mp3`.
3. Script outputs specs.
4. User updates Test Specs (e.g., 0002) with detected values.
