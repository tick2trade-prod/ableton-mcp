# Decisions & Assumptions Log

> Tracking all decisions made during "I Am Machine" recreation project

---

## Assumptions

### A001: Song Structure
- **Assumed**: ~136 BPM, ~224 bars, 9 sections
- **Needs verification**: Actual song analysis

### A002: Track Count
- **Assumed**: 16 tracks sufficient
- **Basis**: Standard techno arrangement

### A003: MCP Works
- **Assumed**: Existing MCP connection to Ableton is functional
- **Basis**: User says "tracks start creating"

### A004: Agents Exist
- **Assumed**: 22 agents in `scripts/dearpygui_controller/agents/` are reusable
- **Note**: User says we can redesign if needed

---

## Decisions

### D001: Project Approach
- **Status**: PENDING
- **Options**: A (fork), B (continue), C (new FastMCP)
- **Recommendation**: B (continue current repo)
- **Rationale**: Agents/MCP already exist, problem is workflow not codebase

### D002: Packages to Add
- **Status**: APPROVED
- **Decision**: Add `isobar`, `pretty-midi`, `midiutil` to pyproject.toml
- **Rationale**: Pattern generation is 10x faster than manual note programming

### D003: Packages to Skip
- **Status**: APPROVED
- **Skipped**:
  - signalflow (Ableton does synthesis)
  - pylive (have MCP)
  - AbletonOSC (have MCP)
  - essentia (have librosa)
  - basic-pitch (not doing audio-to-MIDI)
  - note-seq (too heavy)
- **Rationale**: Already covered by Ableton or existing packages

### D004: Work Unit Size
- **Status**: APPROVED
- **Decision**: Work in 16-bar increments per section
- **Rationale**: Prevents context loss, enables checkpointing

### D005: DearPyGUI Role
- **Status**: APPROVED
- **Decision**: Use as "Task Master" for visual progress tracking
- **Rationale**: User wants GUI to manage tasks/agents

---

## Open Decisions

### D006: Workflow Tool
- **Status**: PENDING
- **Options**:
  - Antigravity workflows (`.agent/workflows/`)
  - Gemini CLI headless
  - Claude CLI agent mode
  - Direct Python scripts
- **Question**: Which combination is fastest?

### D007: Agent Architecture
- **Status**: PENDING
- **Options**:
  - Keep existing 22 agents
  - Simplify to fewer agents
  - Hybrid (keep some, merge others)
- **Depends on**: Testing existing agents first

---

### A005: Remote Script Location
- **Assumed**: `/Users/<USER>/Library/Preferences/Ableton/Live 12.3.1/User Remote Scripts/`
- **Action**: Verify after upgrade

### A006: Suite Device Availability
- **Assumed**: Roar, Meld, Drift, Wavetable now fully available
- **Basis**: Suite includes all devices

### A007: Upgrade Preserves Settings
- **Assumed**: Ableton preserves preferences on upgrade
- **Risk**: Remote Script may need re-copying

---

## Change Log

| Date | ID | Change |
|------|-----|--------|
| 2025-12-16 | D002 | Approved: Add isobar, pretty-midi, midiutil |
| 2025-12-16 | D003 | Approved: Skip signalflow, pylive, etc. |
| 2025-12-16 | D004 | Approved: 16-bar work units |
| 2025-12-16 | D005 | Approved: DearPyGUI as task master |
| 2025-12-16 | D008 | Proposed: Intro-first strategy with 4-lane parallelization |
| 2025-12-16 | D009 | Proposed: Hybrid execution (Gemini headless + Antigravity + Claude) |
| 2025-12-16 | D010 | Proposed: Upgrade in-place (no uninstall) |
| 2025-12-16 | D011 | COMPLETED: Register ableton_mcp in Antigravity config |
| 2025-12-16 | D012 | APPROVED: Edition-aware build system with Justfile |
| 2025-12-16 | D013 | COMPLETED: Antigravity workflows /build, /add-tool, /ci |
| 2025-12-16 | D014 | COMPLETED: Tools documentation in TOOLS.md with backlog |
