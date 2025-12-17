# Screenshots

> Source: [https://antigravity.google/docs/screenshots](https://antigravity.google/docs/screenshots)

## Overview

Capture and use screenshots in your development workflow.

## Capturing Screenshots

### Agent Capture
The agent can capture screenshots:
```
USER: Take a screenshot of the current view
AGENT: [Captures screenshot, saves to artifacts]
```

### Browser Screenshot
During browser subagent tasks:
```python
browser_subagent(
    Task="Navigate to page and screenshot the device parameters",
    RecordingName="device_params_screenshot"
)
```

## Using Screenshots

### In Conversations
Reference screenshots to show issues or states.

### In Documentation
Include in walkthroughs and implementation plans.

### For Debugging
Capture UI states for bug reports.

## Screenshots in ableton-mcp

### Capturing Ableton State
Document Ableton Live session states.

### Recording Results
Show test results visually.

### Documentation
Include in track documentation.

## Storage

Screenshots are saved to:
```
.antigravity/artifacts/screenshots/
```

## Related Pages

- [Artifacts](artifacts.md) - Screenshot storage
- [Browser Recordings](browser-recordings.md) - Video recordings
