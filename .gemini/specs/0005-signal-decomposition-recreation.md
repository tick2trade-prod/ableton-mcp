# 0005: Signal Decomposition & Recreation (build-techno-clean-i-o v3)

| Field | Value |
|-------|-------|
| Branch | `feature/0005-signal-decomposition` |
| Feature | Incremental Signal Decomposition & Ableton Recreation |
| Status | 📝 Planning |
| Reference | [ALCHEMY_I_O.mp3](file:///Users/alexzh/ableton-mcp/assets/audio/reference/ALCHEMY_I_O.mp3) |
| Depends On | 0004-librosa-analyze-track |

---

## Objective

Develop a test-driven pipeline that:
1. **Decomposes** the reference track into isolated audio stems (drums, bass, leads, pads, FX)
2. **Analyzes** each stem for musical parameters (notes, rhythms, timbres)
3. **Recreates** each layer programmatically in Ableton Live
4. **Validates** the recreation by comparing audio similarity to the original

## Reference Track Analysis

| Property | Value |
|----------|-------|
| File | `assets/audio/reference/ALCHEMY_I_O.mp3` |
| Duration | 227.08s (~3:47) |
| BPM | 129.2 |
| Key | G Minor |
| Sections | Drop/breakdown transitions |

---

## Phase 1: Source Separation

### Test: `test_source_separation.py`

#### Dependencies
- [ ] Install `demucs` (Facebook's source separation model)
- [ ] Install `spleeter` (Deezer's source separation)
- [ ] Evaluate which produces better stems for techno

#### Tests
```python
def test_separate_drums():
    """Extract isolated drum stem from reference."""
    # Input: ALCHEMY_I_O.mp3
    # Output: stems/drums.wav
    # Assert: File exists, duration matches original

def test_separate_bass():
    """Extract isolated bass stem from reference."""
    # Output: stems/bass.wav

def test_separate_other():
    """Extract leads/pads/FX stem from reference."""
    # Output: stems/other.wav

def test_separate_vocals():
    """Verify no significant vocal content (techno track)."""
    # Output: stems/vocals.wav
    # Assert: RMS energy below threshold (no vocals expected)
```

### Make Target
```makefile
separate-stems: ## Separate reference track into stems
    @echo "🔬 Separating ALCHEMY_I_O.mp3 into stems..."
    @.venv/bin/python -m demucs assets/audio/reference/ALCHEMY_I_O.mp3 -o assets/audio/stems/
```

---

## Phase 2: Per-Stem Analysis

### Test: `test_stem_analysis.py`

#### Drum Analysis
```python
def test_analyze_kick_pattern():
    """Detect kick pattern from drum stem."""
    # Use onset detection on low frequencies
    # Output: kick_onsets.json with timestamps
    # Assert: ~4 kicks per bar (4-on-floor)

def test_analyze_hihat_pattern():
    """Detect hi-hat pattern from drum stem."""
    # Use onset detection on high frequencies
    # Output: hihat_onsets.json

def test_analyze_clap_snare():
    """Detect clap/snare on beats 2 and 4."""
    # Output: clap_onsets.json
```

#### Bass Analysis
```python
def test_analyze_bass_notes():
    """Extract bass note sequence from bass stem."""
    # Use pitch detection (pyin algorithm)
    # Output: bass_notes.json with pitches and timings
    # Assert: Root note is G (or nearby)

def test_analyze_bass_rhythm():
    """Detect bass rhythmic pattern."""
    # Output: bass_rhythm.json (16th note grid)
```

#### Lead/Pad Analysis
```python
def test_analyze_lead_melody():
    """Extract lead melody from other stem."""
    # Use polyphonic pitch detection
    # Output: lead_notes.json

def test_analyze_pad_chords():
    """Detect sustained chord tones."""
    # Use chroma analysis
    # Output: pad_chords.json (Gm, Dm, Cm progression)
```

---

## Phase 3: Ableton Recreation

### Test: `test_recreation_drums.py`

```python
def test_recreate_kick_from_analysis():
    """Create kick track matching analyzed pattern."""
    # Load kick_onsets.json
    # Create MIDI clip with notes at detected times
    # Load 808 Core Kit on track
    # Assert: Clip contains expected note count

def test_recreate_hihats_from_analysis():
    """Create hi-hat track matching analyzed pattern."""

def test_recreate_clap_from_analysis():
    """Create clap track matching analyzed pattern."""
```

### Test: `test_recreation_bass.py`

```python
def test_recreate_bass_from_analysis():
    """Create bass track matching analyzed notes."""
    # Load bass_notes.json
    # Create MIDI clip with detected pitches
    # Load appropriate bass synth
    # Assert: Notes match detected pitches

def test_bass_timbre_similarity():
    """Verify recreated bass has similar spectral characteristics."""
    # Export recreated audio
    # Compare spectral centroid to original bass stem
    # Assert: Similarity above threshold
```

### Test: `test_recreation_leads.py`

```python
def test_recreate_lead_from_analysis():
    """Create lead track matching analyzed melody."""

def test_recreate_pads_from_analysis():
    """Create pad track matching analyzed chords."""
```

---

## Phase 4: Signal Comparison & Validation

### Test: `test_signal_matching.py`

```python
def test_overall_spectral_similarity():
    """Compare full mix spectrograms."""
    # Export Ableton session as audio
    # Compare spectrogram to original
    # Output: similarity_score (0-1)
    # Assert: similarity > 0.7

def test_drum_pattern_correlation():
    """Compare drum onset times."""
    # Cross-correlate original and recreated drum onsets
    # Assert: correlation > 0.9

def test_harmonic_content_match():
    """Compare chroma features of original and recreation."""
    # Assert: chroma correlation > 0.8

def test_energy_envelope_match():
    """Compare RMS energy curves."""
    # Assert: section transitions align
```

---

## Implementation Roadmap

### Phase 1: Source Separation (Week 1)
- [ ] Add demucs/spleeter to dependencies
- [ ] Create `scripts/separate_stems.py`
- [ ] Add `make separate-stems` target
- [ ] Write stem separation tests
- [ ] Verify stems directory structure

### Phase 2: Stem Analysis (Week 2)
- [ ] Create `analysis/analyze_stems.py`
- [ ] Implement drum onset detection
- [ ] Implement bass pitch detection
- [ ] Implement chord detection
- [ ] Write analysis tests

### Phase 3: Ableton Recreation (Week 3)
- [ ] Create `tests/techno/test_recreation_*.py`
- [ ] Implement pattern-to-MIDI conversion
- [ ] Connect analysis JSON to Ableton MCP
- [ ] Write recreation tests

### Phase 4: Validation (Week 4)
- [ ] Create `analysis/compare_signals.py`
- [ ] Implement spectral similarity metrics
- [ ] Add audio export from Ableton
- [ ] Write validation tests
- [ ] Tune thresholds for passing tests

---

## Make Targets

```makefile
# Phase 1
separate-stems: ## Separate reference into stems
install-separation: ## Install demucs/spleeter

# Phase 2
analyze-stems: ## Analyze each stem for patterns
test-stem-analysis: ## Run stem analysis tests

# Phase 3
build-techno-clean-i-o-v3: ## Recreate from analysis (not manual patterns)
test-recreation: ## Run recreation tests

# Phase 4
compare-signals: ## Compare original vs recreation
test-validation: ## Run signal matching tests

# Full Pipeline
build-techno-matched: separate-stems analyze-stems build-techno-clean-i-o-v3 compare-signals
```

---

## Success Criteria

| Metric | Target | Current |
|--------|--------|---------|
| Drum onset correlation | > 0.9 | - |
| Bass pitch accuracy | > 85% | - |
| Chord progression match | 100% | - |
| Spectral similarity | > 0.7 | - |
| Section alignment | ±0.5 bar | - |
| Tests passing | 100% | 0% |

---

## Dependencies to Research

| Library | Purpose | Priority |
|---------|---------|----------|
| demucs | Source separation (Meta) | High |
| spleeter | Source separation (Deezer) | High |
| madmom | Drum transcription | Medium |
| crepe | Pitch detection | Medium |
| mir_eval | Evaluation metrics | Medium |
