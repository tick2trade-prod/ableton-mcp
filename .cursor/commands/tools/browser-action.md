# Browser Action

## Overview

Execute browser automation using Playwright for web research, testing, and interaction. Enables "Computer Use" capabilities similar to Claude.

> **Layer**: HOW (Execution Primitives)
> **Rank**: 2 - Layer-Based Command

## Usage

Type `/browser-action` followed by action and parameters.

## Parameters

- `action`: Action to perform (navigate, click, type, screenshot, scroll) (required)
- `url`: URL to navigate to (for navigate action)
- `selector`: CSS selector for element (for click, type actions)
- `text`: Text to type (for type action)
- `output_path`: Screenshot path (for screenshot action)

## Example Usage

### Navigate to URL

```
/browser-action
Action: navigate
URL: https://docs.python.org
```

### Click Element

```
/browser-action
Action: click
Selector: button.search-button
```

### Type Text

```
/browser-action
Action: type
Selector: input[name="search"]
Text: FastAPI async patterns
```

### Take Screenshot

```
/browser-action
Action: screenshot
Output Path: screenshots/page.png
```

### Scroll Page

```
/browser-action
Action: scroll
Direction: down
Amount: 500
```

## Workflow

1. **Browser Initialization**:
   - Call `app.server.tools.computer_tool.browser_action()`
   - Launch headless Chromium via Playwright
   - Set viewport size (1280x720 default)

2. **Action Execution**:
   - Execute requested action
   - Wait for page load/element
   - Handle timeouts gracefully

3. **Result Capture**:
   - Capture action result
   - Extract relevant data (title, text, screenshot)
   - Handle errors

4. **Cleanup**:
   - Close browser context
   - Return result

## Implementation

This command uses:
- **Computer Tool**: `app.server.tools.computer_tool`
- **Playwright**: Browser automation library
- **Protocol Models**: `app.server.protocols.tool_models.BrowserCommand`

## Supported Actions

### NAVIGATE
Navigate to a URL and wait for page load.

```json
{
  "action": "NAVIGATE",
  "url": "https://example.com"
}
```

### CLICK
Click an element by CSS selector.

```json
{
  "action": "CLICK",
  "selector": "button#submit"
}
```

### TYPE
Type text into an input field.

```json
{
  "action": "TYPE",
  "selector": "input[name='email']",
  "text": "user@example.com"
}
```

### SCREENSHOT
Capture page or element screenshot.

```json
{
  "action": "SCREENSHOT",
  "selector": "div.content",
  "output_path": "screenshots/content.png"
}
```

### SCROLL
Scroll page up or down.

```json
{
  "action": "SCROLL",
  "direction": "down",
  "amount": 500
}
```

## Output Format

```json
{
  "success": true,
  "action": "navigate",
  "data": {
    "title": "Python Documentation",
    "url": "https://docs.python.org",
    "status": 200
  },
  "screenshot_path": null,
  "error": null
}
```

## Error Handling

```json
{
  "success": false,
  "action": "click",
  "data": null,
  "error": "Element not found: button.nonexistent",
  "suggestion": "Check selector or wait for page load"
}
```

## Best Practices

- Wait for page load before interacting
- Use specific CSS selectors
- Handle timeouts gracefully
- Take screenshots for debugging
- Close browser after use
- Use headless mode for CI/CD
- Respect robots.txt and rate limits

## Use Cases

1. **Research**: Navigate docs, extract information
2. **Testing**: Automated UI testing
3. **Data Extraction**: Scrape structured data
4. **Validation**: Check deployed features
5. **Screenshots**: Visual documentation

## Related Commands

- `/deep-research` - Web research workflow
- `/execute-qa-skill` - Testing with browser validation
- `/create-custom-agent` - Custom agent with browser tool

## Requirements

- Playwright installed: `uv add playwright`
- Chromium installed: `uv run playwright install chromium`
- Headless mode supported (for CI/CD)
