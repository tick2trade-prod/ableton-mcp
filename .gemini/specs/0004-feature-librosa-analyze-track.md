# 0004: Audio Analysis Feature

| Field | Value |
|-------|-------|
| Branch | `feature/0004-librosa-analyze-track` |
| Feature| Audio Signal Analysis Tool |
| Status | ✅ Complete (Phase 1) |

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
2. Runs `make analyze TRACK=assets/audio/reference/ALCHEMY_I_O.mp3`.
3. Script outputs specs (129.2 BPM, G Minor).
4. Runs `make build-techno-clean-i-o` to recreate in Ableton.

---

## Phase 2: Research - External Dependencies

### Objective
Research and integrate additional audio/music libraries to enhance analysis capabilities and enable more sophisticated pattern generation.

### ideoforms Suite (Sound Synthesis & Control)
| Repo | Description | Priority | Status |
|------|-------------|----------|--------|
| [signalflow](https://github.com/ideoforms/signalflow) | Real-time sound synthesis/DSP with Python API, C++ core | High | [ ] Research |
| [isobar](https://github.com/ideoforms/isobar) | Musical pattern generation, MIDI/OSC output | High | [ ] Research |
| [AbletonOSC](https://github.com/ideoforms/AbletonOSC) | Control Ableton Live with OSC | Medium | [ ] Research |
| [pylive](https://github.com/ideoforms/pylive) | Python control of Ableton via AbletonOSC | High | [ ] Research |
| [python-supercollider](https://github.com/ideoforms/python-supercollider) | SuperCollider synthesis from Python | Low | [ ] Research |

### librosa Ecosystem
| Repo | Description | Priority | Status |
|------|-------------|----------|--------|
| [librosa](https://github.com/librosa/librosa) | Core audio analysis (already integrated) | ✅ | Done |
| [librosa/data](https://github.com/librosa/data) | Sample audio datasets | Low | [ ] Research |
| [librosa/tutorial](https://github.com/librosa/tutorial) | Learning resources | Low | [ ] Review |
| [librosa_gallery](https://github.com/librosa/librosa_gallery) | Example notebooks | Low | [ ] Review |

### MIDI & Music Theory
| Repo | Description | Priority | Status |
|------|-------------|----------|--------|
| [pretty-midi](https://github.com/craffel/pretty-midi) | MIDI manipulation library | High | [ ] Research |
| [music21](https://github.com/cuthbertLab/music21) | Music theory / analysis toolkit | Medium | [ ] Research |
| [MIDIUtil](https://github.com/MarkCWirt/MIDIUtil) | MIDI file generation | Medium | [ ] Research |

### Audio Processing
| Repo | Description | Priority | Status |
|------|-------------|----------|--------|
| [pydub](https://github.com/jiaaro/pydub) | Simple audio manipulation | Medium | [ ] Research |
| [essentia](https://github.com/MTG/essentia) | Advanced audio analysis (MTG) | High | [ ] Research |
| [pedalboard](https://github.com/spotify/pedalboard) | Audio effects from Spotify | High | [ ] Research |

---

## Research Tasks

### High Priority
- [ ] **isobar**: Evaluate for pattern generation to replace manual MIDI note arrays
- [ ] **pylive + AbletonOSC**: Compare with current socket-based MCP approach
- [ ] **signalflow**: Assess for real-time audio generation/DSP
- [ ] **pretty-midi**: Evaluate for MIDI file import/export
- [ ] **essentia**: Compare with librosa for advanced analysis (MIR)
- [ ] **pedalboard**: Evaluate for audio effects processing

### Medium Priority
- [ ] **music21**: Evaluate for music theory analysis (chord progressions, voice leading)
- [ ] **pydub**: Evaluate for simple audio slicing/concatenation
- [ ] **MIDIUtil**: Evaluate for MIDI file export

### Low Priority
- [ ] Review librosa tutorials and gallery for advanced techniques
- [ ] Evaluate python-supercollider for alternative synthesis

---

## Gitmodule Integration Plan

### Recommended Structure
```
external/
├── ideoforms/
│   ├── isobar/          # Pattern generation
│   ├── signalflow/      # DSP
│   └── pylive/          # Ableton control
├── audio/
│   ├── librosa/         # Already using via pip
│   ├── essentia/        # Advanced MIR
│   └── pedalboard/      # Effects
└── midi/
    ├── pretty-midi/     # MIDI manipulation
    └── music21/         # Music theory
```

### Integration Priority Order
1. **isobar** - Replace manual pattern arrays with generative sequences
2. **pretty-midi** - Import/export MIDI files
3. **pylive** - Alternative Ableton control method
4. **essentia** - Enhanced audio analysis
5. **pedalboard** - Audio effects chain
