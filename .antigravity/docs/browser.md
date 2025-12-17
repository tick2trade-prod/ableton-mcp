# Browser

> Source: [https://antigravity.google/docs/browser](https://antigravity.google/docs/browser)

## Overview

The integrated browser enables web browsing alongside development.

## Features

### Embedded Browser
- Full web browser in IDE
- Navigate to any URL
- Interact with pages

### Agent Integration
- Browser subagent for automation
- Page content extraction
- Screenshot capture

### Session Management
- Multiple tabs
- History
- Bookmarks

## Browser Usage in ableton-mcp

### Research
- View Ableton documentation
- Read tutorials
- Reference Stack Overflow

### Documentation
- Preview markdown
- View generated docs

### API Testing
- View API endpoints
- Test webhooks

## Browser Subagent

For automated browsing, see [Browser Subagent](browser-subagent.md).

```python
browser_subagent(
    Task="Navigate to ableton.com and find Roar documentation",
    RecordingName="roar_docs"
)
```

## Privacy

The browser operates within your local environment:
- No external logging
- Cookies local to IDE
- Session isolated

## Related Pages

- [Browser Subagent](browser-subagent.md) - Automation
- [Chrome Extension](chrome-extension.md) - Chrome integration
- [Allowlist / Denylist](allowlist-denylist.md) - URL filtering
