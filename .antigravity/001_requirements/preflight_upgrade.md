# Pre-Flight: Live 12 Intro → Suite Upgrade

## Current State
- **From**: Live 12.3.1 Intro (Education)
- **To**: Live 12 Suite (Education)

---

## Q1: Uninstall or Upgrade In-Place?

### Recommendation: **Upgrade In-Place** (No Uninstall)

| Approach | Pros | Cons |
|----------|------|------|
| Upgrade in-place | Preserves settings, simpler | Must verify Remote Script |
| Uninstall first | Clean slate | Lose preferences, more work |

**Ableton allows upgrading** without uninstalling. Suite will replace Intro.

---

## Pre-Upgrade Checklist ✅ COMPLETED

### 1. ✅ Backup Remote Script
**Executed**: 2025-12-16 18:07
```bash
cp -r ~/Library/Preferences/Ableton/Live\ 12.3.1/User\ Remote\ Scripts/AbletonMCP \
      ~/Desktop/AbletonMCP_backup_20251216
```
**Result**: `~/Desktop/AbletonMCP_backup_20251216/` created

### 2. ✅ Backup Ableton Preferences
**Executed**: 2025-12-16 18:07
```bash
cp -r ~/Library/Preferences/Ableton/Live\ 12.3.1 \
      ~/Desktop/Ableton_12.3.1_backup_20251216
```
**Result**: `~/Desktop/Ableton_12.3.1_backup_20251216/` created

### 3. ✅ Remote Script Path Documented
```
/Users/alexzh/Library/Preferences/Ableton/Live 12.3.1/User Remote Scripts/AbletonMCP/
```

### 4. Pre-Upgrade Status (Last Known)
- [x] MCP connection working
- [x] Tracks created (with context loss issues)
- [x] Devices loading (limited by Intro edition)
- [ ] Tests passing (partial)

---

## 🔄 INSTALL SUITE NOW

1. Download from: https://www.ableton.com/en/account/
2. Run installer
3. Return here for post-upgrade steps

---

## Post-Upgrade Checklist ✅ COMPLETED

### 1. [x] Verify Remote Script Exists
**Executed**: 2025-12-16 18:34
```bash
./scripts/ableton-mcp/ableton-mcp-install-doctor.sh
```
**Result**: ✅ Remote Script in Ableton prefs

### 2. [x] Enable Control Surface in Ableton
**Status**: Already enabled from previous installation

### 3. [x] Test MCP Connection
**Executed**: 2025-12-16 18:34
```bash
./scripts/ableton-mcp/ableton-mcp-connection-test.sh
```
**Result**:
- ✅ Port 9877 is listening
- ✅ MCP responds to commands

### 4. [ ] Verify Suite-Only Devices
*(Manual testing required)*

| Device | Status |
|--------|--------|
| Roar | [ ] Works |
| Meld | [ ] Works |
| Drift | [ ] Works |
| Wavetable | [ ] Works |
| Operator (full) | [ ] Works |

### 5. [ ] Run Test Suite
```bash
pytest tests/ -v --timeout=300
```

---

## Post-Upgrade Execution Log

| Step | Time | Status | Notes |
|------|------|--------|-------|
| Suite installed | 18:30 | ✅ | Live 12.3 Suite |
| Remote Script verified | 18:34 | ✅ | Via install-doctor |
| Control Surface enabled | 18:34 | ✅ | Already configured |
| MCP connection tested | 18:34 | ✅ | Port 9877 + responds |
| ableton_mcp registered | 18:34 | ✅ | Added to Antigravity |
| Suite devices tested | | ⏳ | Manual needed |
| Full test suite run | | ⏳ | |

---

## Code Migration Considerations

### A001: Device Availability Changes

Previously unavailable devices now work. Check these agents:

| Agent | Devices Used | Action |
|-------|--------------|--------|
| `SynthesizerAgent` | Wavetable, Operator, Meld, Drift | ✅ Now available |
| `EffectsChainAgent` | Roar | ✅ Now available |
| `SoundDesignAgent` | Various | Verify |

### A002: Instrument Paths May Differ

Suite has more instruments. Browser queries may behave differently.

### A003: Running Tests Post-Upgrade
```bash
pytest tests/ -v --timeout=300
pytest tests/ -v -m live
```

---

## Decision Record

**D010: Upgrade Approach**
- **Status**: IN PROGRESS
- **Decision**: Upgrade in-place (no uninstall)
- **Pre-steps**: ✅ Completed 2025-12-16 18:07
- **Post-steps**: ⏳ Pending
