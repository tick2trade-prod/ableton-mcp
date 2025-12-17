---
description: View current MCP tools and backlog
---

## Tools Status

1. List current 28 MCP tools:
// turbo
   ```bash
   just mcp-tools
   ```

2. View full tools documentation:
// turbo
   ```bash
   cat TOOLS.md
   ```

3. Check edition detected:
// turbo
   ```bash
   just doctor
   ```

## Tools Backlog

### P0 (Phase 1 Blockers)
- [ ] `set_sidechain_input` - For Rumble pumping
- [ ] `create_return_track` - For FX buses
- [ ] `load_roar` - Suite saturation device

### P1 (Mixing)
- [ ] `set_send_level` - Send routing
- [ ] `set_track_mute/solo` - Mixing controls

### P2 (Suite Features)
- [ ] `separate_stems` - Reference analysis
- [ ] `load_meld` / `load_drift` - Suite synths

## Add New Tool

```bash
/add-tool
```
