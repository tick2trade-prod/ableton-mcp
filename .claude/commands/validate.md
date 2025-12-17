# Validate

Run CI, linting, and validation checks.

## Quick Validation (No Ableton)

```bash
just quick
```

## Full CI Pipeline

```bash
just ci
```

## CI with Live Ableton Connection

```bash
just ci-live
```

## Individual Checks

### Lint
```bash
just lint
```

### Tests
```bash
just test
```

### Doctor (Full)
```bash
just doctor
```

### Doctor (Quick)
```bash
just doctor-quick
```

### MCP Tools Check
```bash
just mcp-tools
```

### MCP Connection Test
```bash
just mcp-test
```

## Pre-Merge Checklist

```bash
just pre-merge
```

## Expected Results

- Lint: All files pass
- Tests: All tests pass
- Doctor: 4/4 checks pass
- MCP Tools: 32 tools available

## Troubleshooting

### Port 9877 Not Listening
1. Open Ableton Live
2. Enable AbletonMCP in Preferences > Link, Tempo & MIDI > Control Surface

### Remote Script Not Found
```bash
just deploy
```

### Tests Failing
```bash
just test-one <test_name>
```
