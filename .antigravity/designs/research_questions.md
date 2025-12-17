# Research Questions & Open Items

## Categorized Research Backlog

> Date: 2025-12-16

---

## 🔴 Critical (Blocks MVP)

### RQ-001: Stem Separation API Access
**Question**: Can Ableton's stem separation be triggered via Remote Script?

**Context**: The stem separation UI is accessed via right-click menu. We need programmatic access.

**Research Actions**:
- [ ] Review Ableton Remote Script API documentation
- [ ] Search AbletonMCP control surface code for similar UI triggers
- [ ] Test via `browser.get_item()` or similar
- [ ] Check if stems can be pre-extracted and used as files

**Fallback**: Manual extraction, use WAV files directly

---

### RQ-002: Audio Export API
**Question**: How do we export audio from a specific track via MCP?

**Context**: Need to compare recreated track audio against original stem.

**Research Actions**:
- [ ] Check current MCP tools for export capability
- [ ] Review Ableton export_audio() Python API
- [ ] Consider render-in-place as alternative
- [ ] Check if we can read from arrangement view

**Workaround**: Solo track + bounce to disk (manual)

---

### RQ-003: Spectral Comparison Accuracy
**Question**: Does spectral similarity correlate with perceptual similarity?

**Context**: We're using FFT-based comparison, but humans hear differently.

**Research Actions**:
- [ ] Benchmark librosa spectral comparison on known similar tracks
- [ ] Research perceptual audio codecs (e.g., psychoacoustic models)
- [ ] Test with intentionally different mixes
- [ ] Define acceptable false positive/negative rates

---

## 🟡 Important (Affects Quality)

### RQ-004: Ollama Model Selection
**Question**: Is llama3 the best model for music production suggestions?

**Context**: Current agents default to llama3 (8B). May need larger or specialized model.

**Research Actions**:
- [ ] Test llama3 with music production prompts
- [ ] Compare llama3:70b if resources allow
- [ ] Explore music-specific models (if any exist)
- [ ] Benchmark response quality and latency

**Options**:
| Model | Size | Speed | Music Knowledge |
|-------|------|-------|-----------------|
| llama3 | 8B | Fast | Unknown |
| llama3:70b | 70B | Slow | Unknown |
| mixtral | 8x7B | Medium | Unknown |
| codellama | 34B | Medium | Code focus |

---

### RQ-005: Similarity Threshold
**Question**: Is 80% the right target? What does 80% mean perceptually?

**Context**: Arbitrary threshold chosen. Need validation.

**Research Actions**:
- [ ] Create test set of known similar/different audio pairs
- [ ] Compute similarity scores for each
- [ ] Have human listeners rate similarity
- [ ] Correlate scores with ratings

**Hypothesis**: 80% spectral similarity ≈ "recognizably the same" perceptually

---

### RQ-006: Agent Subset for MVP
**Question**: Which of 22 agents are actually needed for MVP?

**Context**: Migrating all 22 agents is expensive. Need minimum viable set.

**Research Actions**:
- [ ] Map each agent to stem coverage
- [ ] Identify critical path agents
- [ ] Flag agents with placeholder implementations

**Initial Analysis**:
| Priority | Agents | Reason |
|----------|--------|--------|
| Must Have | PercussionAgent, SynthesizerAgent, EffectsChainAgent, VerifierAgent | Core recreation |
| Should Have | VocalsAgent, MixerAgent, SidechainAgent | Polish |
| Nice to Have | All others | Future enhancement |

---

## 🟢 Nice to Know

### RQ-007: FastMCP Cloud Deployment
**Question**: Should we deploy MCP server to FastMCP Cloud?

**Context**: Currently running locally. Cloud could enable remote access.

**Research Actions**:
- [ ] Review FastMCP Cloud features
- [ ] Evaluate latency for Ableton control (needs local)
- [ ] Consider hybrid: cloud for research tools, local for Ableton

**Likely Answer**: Local only for Ableton tools (latency sensitive)

---

### RQ-008: DearPyGUI Alternative
**Question**: Is DearPyGUI the best GUI framework for this use case?

**Context**: Currently using DearPyGUI for agent control panel.

**Research Actions**:
- [ ] Evaluate Streamlit for quick prototyping
- [ ] Consider Gradio for ML-native interface
- [ ] Check if we even need a GUI (CLI first?)

---

### RQ-009: CrewAI vs Custom Orchestration
**Question**: Should we use CrewAI for agent orchestration?

**Context**: pyproject.toml includes `crewai>=0.51.0`. Currently using custom orchestration.

**Research Actions**:
- [ ] Review current `workflow_orchestrator.py`
- [ ] Compare to CrewAI patterns
- [ ] Evaluate migration effort
- [ ] Check CrewAI + Ollama compatibility

---

## Research Templates

### For Technical Feasibility

```markdown
## RQ-XXX: [Question]

**Question**: [Clear, specific question]

**Context**: [Why this matters]

**Research Actions**:
- [ ] Action 1
- [ ] Action 2
- [ ] Action 3

**Expected Output**: [What we'll learn]

**Decision Deadline**: [Date]
```

### For Technology Choice

```markdown
## TC-XXX: [Technology Decision]

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| A | ... | ... |
| B | ... | ... |

**Evaluation Criteria**:
1. Criteria 1 (weight)
2. Criteria 2 (weight)

**Recommendation**: [Choice with rationale]
```

---

## Research Priority Queue

| Priority | ID | Question | ETA |
|----------|-----|----------|-----|
| 1 | RQ-001 | Stem separation API | 2 days |
| 2 | RQ-002 | Audio export API | 2 days |
| 3 | RQ-003 | Spectral comparison | 3 days |
| 4 | RQ-006 | Agent subset | 1 day |
| 5 | RQ-004 | Ollama model | 2 days |
| 6 | RQ-005 | Similarity threshold | 3 days |

---

## Answered Questions

*(Move items here as they're resolved)*

### AQ-001: FastMCP Project Structure
**Answer**: See `research_fastmcp.md` - decorator-based tools with `@mcp.tool` pattern.

### AQ-002: Agent Inventory
**Answer**: See `agent_inventory.md` - 22 agents, all extend BaseAgent with Ollama integration.
