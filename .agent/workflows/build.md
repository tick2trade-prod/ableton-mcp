---
description: Run build, CI, and validation commands using Justfile
---
// turbo-all

## Build Workflow

1. Setup config if needed:
   ```bash
   just setup
   ```

2. Run quick validation:
   ```bash
   just quick
   ```

3. Run full CI (no Ableton needed):
   ```bash
   just ci
   ```

4. Run doctor with live Ableton:
   ```bash
   just doctor
   ```

5. List available MCP tools:
   ```bash
   just mcp-tools
   ```

## Expected Result
- All doctor checks pass (4/4)
- MCP tools listed (28 available)
- Ready for Phase 1 track creation
