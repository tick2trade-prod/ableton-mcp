# Agent Investigation Findings

**Date:** 2025-12-16
**Objective:** Determine how agents can improve tracks to match reference
**Reference:** `assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`

---

## Executive Summary

The current agent architecture **cannot produce reference-accurate patterns** because:
1. Agents use **hardcoded patterns** (not reference-based)
2. Agents **do not access** the pre-computed stem analysis
3. The hardcoded key is **WRONG** (F minor vs G in reference)

**Validated improvement potential:** Switching from F-minor to G-based scale improves pitch accuracy from **21.1% → 44.6%** (2x improvement).

---

## Validated Findings

### 1. Agent Invocation ✅

**Finding:** Agents CAN be invoked via CLI.

```bash
python scripts/dearpygui_controller/run_agent.py composer
```

**Result:** Agents execute, but produce hardcoded output.

---

### 2. Reference Analysis Data ✅

**Finding:** Pre-computed stem analysis EXISTS and contains usable data.

| Data | Count | Source |
|------|-------|--------|
| Drum onsets | 1,292 | `stem_analysis.json` |
| Bass notes | 1,231 | `stem_analysis.json` |
| Intro drum onsets | 207 | First 16 bars |
| Intro bass notes | 204 | First 16 bars |

---

### 3. Agents Do NOT Access Reference ❌

**Finding:** Zero agents reference `stem_analysis.json`.

```bash
grep -r "stem_analysis\|analysis.json" scripts/dearpygui_controller/agents/
# Result: No matches
```

**Implication:** Agents hallucinate generic patterns instead of matching reference.

---

### 4. Current Agent Uses WRONG Key ❌

**Finding:** Reference track is in **G**, not F.

| Metric | Current Agent | Reference |
|--------|---------------|-----------|
| Root note | F1 (MIDI 29) | G1 (MIDI 31) |
| Scale | F minor | G-based |
| Pitch accuracy | 21.1% | — |
| Improved (G-based) | 44.6% | — |

**Test validation:**
```python
# test_agent_reference_accuracy.py
test_detect_root_note → PASSED (G1 detected)
test_current_agent_uses_wrong_key → PASSED (confirms F usage)
test_pitch_accuracy_baseline → PASSED (21.1% → 44.6%)
```

---

### 5. Note Density Mismatch ⚠️

| Metric | Current Agent | Reference |
|--------|---------------|-----------|
| Notes per bar | 16.0 | 12.8 |
| Style | Mechanical 16ths | Syncopated |

---

### 6. Ollama Capability ⚠️

**Finding:** Ollama (llama3.1:8b) can provide recommendations when given data, but:
- Does not output reliable machine-readable patterns
- Quality varies
- Needs careful prompting

**Tested prompt:**
```
Based on bass analysis: G1 most common (39 notes), G#1 (23), A1 (18)...
Provide 3 SPECIFIC changes to match reference.
```

**Result:** Partial recommendations (some correct, some wrong).

---

## Validated Test Suite

Created: `tests/phases/phase1_intro/test_agent_reference_accuracy.py`

| Test | Result |
|------|--------|
| `test_analysis_file_exists` | ✅ PASS |
| `test_has_drum_data` | ✅ PASS |
| `test_has_bass_data` | ✅ PASS |
| `test_detect_root_note` | ✅ PASS |
| `test_current_agent_uses_wrong_key` | ✅ PASS |
| `test_pitch_accuracy_baseline` | ✅ PASS |
| `test_note_density_baseline` | ✅ PASS |
| `test_analysis_path_accessible` | ✅ PASS |
| `test_agent_uses_reference_data` | SKIPPED (not implemented) |

---

## Recommendations

### Priority 1: Add Reference Data Access to Agents

The simplest, highest-impact change:

```python
# In BaseAgent or specific agents
class ReferenceAwareAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analysis = self._load_analysis()

    def _load_analysis(self):
        path = Path(__file__).parent.parent.parent.parent / "assets/analysis/stem_analysis.json"
        with open(path) as f:
            return json.load(f)

    def get_intro_bass_notes(self):
        """Get bass notes for intro section."""
        intro_duration = 16 * 4 * (60/136)  # 28.2 seconds
        return [n for n in self.analysis["bass"]["notes"] if n["start"] < intro_duration]
```

### Priority 2: Fix Hardcoded Key

Change ComposerAgent from F minor to G-based:

```python
# Current (WRONG)
scale = [29, 32, 34, 36, 39]  # F1, Ab1, Bb1, C2, Eb2

# Improved (reference-based)
scale = [31, 32, 33, 34]  # G1, G#1, A1, A#1 (from analysis)
```

### Priority 3: Ollama Integration (Lower Priority)

Ollama can assist with:
- Interpreting analysis data
- Suggesting parameter values
- Validating patterns

But NOT reliably:
- Generating machine-readable patterns directly
- Making decisions without reference data

---

## Conclusion

**The path forward is clear:**

1. **Immediate:** Make agents load `stem_analysis.json`
2. **Quick win:** Fix the key from F to G
3. **Later:** Enhance with ollama for interpretation

**Do NOT rely on ollama to generate patterns** - it should assist with interpretation of reference data, not replace it.

---

## Files Created

- `tests/phases/phase1_intro/test_agent_reference_accuracy.py` - Validation tests
- `.antigravity/001_requirements/agent_investigation_findings.md` - This document
