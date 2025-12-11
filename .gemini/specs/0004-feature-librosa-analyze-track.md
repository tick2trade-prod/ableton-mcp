# 0004: Audio Analysis Feature

| Field | Value |
|-------|-------|
| Branch | `feature/0004-audio-analysis` (Proposed) |
| Feature| Audio Signal Analysis Tool |
| Status | ✅ Complete |

---

## Objective
Develop a robust CLI tool using `librosa` to analyze reference audio tracks and extract musical features (BPM, Key, Sections) to guide programmatic reproduction in Ableton Live.

## Prerequisites
- [x] Python environment with `uv`
- [x] `ffmpeg` installed (for mp3 support)
- [x] Dependencies: `librosa`, `numpy`, `scipy`

## Requirements

### 1. Analysis Script (`analysis/analyze_track.py`)
- [x] **Robust Loading**: Handle various formats (mp3, wav, aif).
- [x] **Feature Extraction**:
    - **Tempo**: Extract BPM (scalar).
    - **Key**: Detect root note and mode (Major/Minor).
    - **Structure**: Detect drop/breakdown using RMS energy.
- [x] **Output**:
    - Print human-readable summary.
    - Generate JSON for programmatic consumption.

### 2. Integration
- [x] `install-analysis` Make target.
- [x] `check-ffmpeg` Make target.
- [x] `analyze` Make target.
- [x] Error handling for missing backends (`NoBackendError`).

### 3. Testing
- [x] Comprehensive pytest suite (`tests/test_analysis.py`).
- [x] 8 tests covering all functionality.
- [x] All tests passing.

## Workflow
1. User adds reference track to `assets/audio/reference/`.
2. Runs `make analyze TRACK=assets/audio/reference/paramore.mp3`.
3. Script outputs specs.
4. User updates Test Specs (e.g., 0002) with detected values.
