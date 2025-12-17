# Browser Subagent View

> Source: [https://antigravity.google/docs/browser-subagent-view](https://antigravity.google/docs/browser-subagent-view)

## Overview

The Browser Subagent View provides a visual interface for monitoring browser automation tasks.

## Features

### Live Preview
- See browser actions in real-time
- Visual feedback on navigation

### Action Log
- Step-by-step action list
- Status of each action
- Error messages

### Recording Playback
- View recorded sessions
- Review completed tasks

## Interface Elements

### Browser Window
Shows current page state:
- URL bar
- Page content
- Interactive elements

### Action Panel
Lists actions:
```
1. ✓ Navigate to ableton.com
2. ✓ Click "Manual"
3. ⧖ Search for "Compressor"
4. ○ Extract content
```

### Status Bar
- Task name
- Progress
- Elapsed time

## Using Browser Subagent View

### During Execution
1. Start browser subagent task
2. View opens automatically
3. Watch progress in real-time
4. Review results when complete

### After Execution
1. Open recording from artifacts
2. Review actions taken
3. Verify extracted data

## Browser Tasks in ableton-mcp

### Research Tasks
```
Task: Research rumble bass techniques
Status: In Progress

Actions:
✓ Navigate to musicradar.com
✓ Search "techno rumble bass"
⧖ Reading article 1 of 3
○ Extract technique details
○ Return summary
```

### Documentation Tasks
```
Task: Find Roar device parameters
Status: Complete

Actions:
✓ Navigate to ableton.com/manual
✓ Search "Roar"
✓ Navigate to device chapter
✓ Extract parameter list
✓ Return with 12 parameters
```

## Troubleshooting

### Task Fails
Review action log to see where it stopped.

### Wrong Data Extracted
Check page state at extraction point.

### Timeout
Increase task timeout or break into smaller tasks.

## Related Pages

- [Browser Subagent](browser-subagent.md) - Subagent overview
- [Browser](browser.md) - Browser features
- [Artifacts](artifacts.md) - Recordings storage
