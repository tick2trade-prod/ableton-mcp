# Allowlist / Denylist

> Source: [https://antigravity.google/docs/allowlist-denylist](https://antigravity.google/docs/allowlist-denylist)

## Overview

Control which URLs the browser subagent can access.

## Allowlist

URLs the subagent CAN visit:
```json
{
  "browser": {
    "allowlist": [
      "ableton.com",
      "musicradar.com",
      "studiobrootle.com",
      "github.com"
    ]
  }
}
```

## Denylist

URLs the subagent CANNOT visit:
```json
{
  "browser": {
    "denylist": [
      "*.exe",
      "login.*",
      "admin.*"
    ]
  }
}
```

## Configuration for ableton-mcp

### Recommended Allowlist
```json
{
  "browser": {
    "allowlist": [
      "ableton.com",
      "help.ableton.com",
      "musicradar.com",
      "studiobrootle.com",
      "attackmagazine.com",
      "reddit.com/r/ableton",
      "github.com",
      "docs.python.org"
    ]
  }
}
```

### Recommended Denylist
```json
{
  "browser": {
    "denylist": [
      "*.download",
      "login.*",
      "checkout.*",
      "*.torrent"
    ]
  }
}
```

## Precedence

Denylist takes precedence over allowlist.

## Related Pages

- [Browser](browser.md) - Browser overview
- [Browser Subagent](browser-subagent.md) - Automation
- [Secure Mode](secure-mode.md) - Security features
