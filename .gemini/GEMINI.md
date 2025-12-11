# Ableton MCP - Gemini Configuration

## Primary Objective
Write pytest integration tests for `feature/rack-chain-tools` branch to verify all MCP tools work with a **live Ableton DAW**.

## Key Principles
- **No mocks** - All tests run against real Ableton Live instance
- **Incremental testing** - Test one tool at a time, fix issues, then proceed
- **Live verification** - Confirm changes in Ableton DAW after each test

## Prerequisites
- Ableton Live running with AbletonMCP control surface enabled
- Port 9877 listening: `make check-port`
- Test connection: `make test-connection`

## Testing Workflow
1. Run single test: `pytest tests/test_tools.py::test_<tool_name> -v`
2. Check Ableton state manually if needed
3. Fix issues and re-run until passing
4. Proceed to next tool

## Log Location
```
/Users/$(USER)/Library/Preferences/Ableton/Live 12.3.1/Log.txt
```

## Conventions

### Conventional Commits
```
test: add test for get_session_info
feat: add new tool for X
fix: resolve connection timeout issue
docs: update README with setup steps
refactor: simplify socket handling
```

### Branch Naming
```
feature/<name>     # New features
test/<tool-name>   # Test additions
fix/<issue>        # Bug fixes
```

### PR Template
```
## Summary
Brief description of changes

## Tests
- [ ] All 27 tool tests pass
- [ ] Tested against live Ableton
```
