# Separate Chrome Profile

> Source: [https://antigravity.google/docs/separate-chrome-profile](https://antigravity.google/docs/separate-chrome-profile)

## Overview

Use a dedicated Chrome profile for Antigravity browser operations.

## Benefits

### Isolation
- Separate cookies
- Separate history
- Separate extensions

### Security
- No cross-contamination with personal browsing
- Protected credentials

### Consistency
- Clean state for automation
- Predictable behavior

## Setup

### Create Profile
1. Open Chrome
2. Profile menu → Add
3. Name: "Antigravity"
4. Create

### Configure in Antigravity
```json
{
  "browser": {
    "chromeProfile": "Antigravity",
    "useIsolatedProfile": true
  }
}
```

## Recommendations for ableton-mcp

### Development Profile
- Install developer extensions
- Configure for testing

### Research Profile
- Clean cookies
- No login sessions
- Ad blocker enabled

## Related Pages

- [Browser](browser.md) - Browser overview
- [Chrome Extension](chrome-extension.md) - Extension setup
