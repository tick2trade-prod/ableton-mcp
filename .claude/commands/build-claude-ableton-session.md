# Build Claude Ableton Session

Build, validate, and ensure the ableton-mcp codebase is ready for track creation.

## Reference

- Build workflow: `.agent/workflows/build.md`
- Commands: `justfile`

## Build Commands

### Initial Setup (if needed)
```bash
just setup
```
Creates `config.yaml` from template if it doesn't exist.

### Install Dependencies
```bash
just install
```
Runs `uv sync --all-groups --upgrade`.

### Full Initialization
```bash
just init
```
Installs deps, creates config, sets up pre-commit hooks.

## Validation Commands

### Quick Validation (No Ableton)
```bash
just quick
```

### Full CI Pipeline
```bash
just ci
```
Runs: lint → test → doctor-quick

### CI with Live Ableton
```bash
just ci-live
```
Runs: lint → test → doctor (requires Ableton running)

### Pre-Merge Check
```bash
just pre-merge
```

## Build Verification

### Check MCP Server Syntax
```bash
python3 -m py_compile MCP_Server/server.py
```

### Check Remote Script Syntax
```bash
python3 -m py_compile AbletonMCP_Remote_Script/__init__.py
```

### Build MCP (Auto-detect Edition)
```bash
just build
```

### Build for Specific Edition
```bash
just build-edition suite
```

## MCP Verification

### List Available Tools
```bash
just mcp-tools
```
Expected: **32 tools** available

### Test MCP Connection
```bash
just mcp-test
```
Requires Ableton with AbletonMCP Control Surface enabled.

### Run Doctor
```bash
just doctor
```
Expected: **4/4 checks pass**

## Deploy Remote Script

```bash
just deploy
```
Copies Remote Script to Ableton's User Remote Scripts folder.

### After Deployment: Reload in Ableton

After `just deploy`, you must reload the Remote Script:

1. **Option A - Restart Ableton**: Close and reopen Ableton Live
2. **Option B - Reload Control Surface** (faster):
   - Preferences → Link/Tempo/MIDI
   - Control Surface: Set AbletonMCP to "None"
   - Wait 2 seconds
   - Set back to "AbletonMCP"
   - Click OK

The reload is required because Ableton caches the Remote Script on startup.

## Run MCP Server

```bash
just run
```
Or for specific edition:
```bash
just run-suite
```

## Lint & Format

```bash
just lint
just format
```

## Test Commands

### All Tests
```bash
just test
```

### Specific Test
```bash
just test-one <test_name>
```

### Live Ableton Tests
```bash
just test-live
```

## Expected Build State

After successful build:
- [ ] `just ci` passes
- [ ] 32 MCP tools available
- [ ] Doctor shows 4/4 checks
- [ ] Port 9877 listening (when Ableton running)
- [ ] Remote Script deployed

## If Build Fails

### Syntax Error in server.py
1. Check the error line
2. Fix the Python syntax
3. Re-run `python3 -m py_compile MCP_Server/server.py`

### Syntax Error in __init__.py
1. Check the error line
2. Fix the Python syntax
3. Re-run `python3 -m py_compile AbletonMCP_Remote_Script/__init__.py`

### Missing Dependencies
```bash
just install
```

### Lint Failures
```bash
just format
```

### Test Failures
```bash
just test-one <failing_test>
```

## Adding New Tools

If a tool is missing for track creation:
1. Use `/add-tool` command for workflow
2. Add to `MCP_Server/server.py`
3. Add handler to `AbletonMCP_Remote_Script/__init__.py`
4. Run `just build` to verify
5. Run `just mcp-tools` to confirm tool appears
6. Update `TOOLS.md`

## Related Commands

- `/start-claude-ableton-session` - Start a new session
- `/validate` - Quick validation
- `/add-tool` - Add new MCP tool
