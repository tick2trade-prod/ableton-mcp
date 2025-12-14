# Tool: Computer Use (Browser Automation)

## Overview

Browser automation (navigate, click, screenshot). This command provides browser automation capabilities from `app/server/tools/computer_tool.py` using Playwright for web interaction, testing, and research.

## Usage

Type `/tool-computer` followed by the browser action.

## Parameters

- `action`: Browser action (navigate, click, type, screenshot, scroll, wait) (required)
- `url`: URL to navigate to (for navigate action)
- `selector`: CSS selector for element (for click/type actions)
- `text`: Text to type (for type action)
- `screenshot_path`: Path to save screenshot (optional)
- `headless`: Run in headless mode (default: true)
- `timeout`: Action timeout in ms (default: 30000)

## Example Usage

### Navigate to URL

```
/tool-computer
Action: navigate
URL: https://docs.python.org/3/library/asyncio.html
```

### Click Element

```
/tool-computer
Action: click
Selector: button#submit
```

### Type Text

```
/tool-computer
Action: type
Selector: input[name="search"]
Text: FastAPI authentication
```

### Take Screenshot

```
/tool-computer
Action: screenshot
Screenshot Path: screenshots/homepage.png
```

### Scroll Page

```
/tool-computer
Action: scroll
Direction: down
Amount: 500
```

### Wait for Element

```
/tool-computer
Action: wait
Selector: div.results
Timeout: 5000
```

## Browser Actions

### Navigate

Navigate to URL and wait for page load.

**Parameters**:
- `url`: Target URL
- `wait_until`: Wait condition (load, domcontentloaded, networkidle)

**Returns**:
```json
{
  "action": "navigate",
  "url": "https://docs.python.org/3/library/asyncio.html",
  "success": true,
  "page_title": "asyncio — Asynchronous I/O — Python 3.12 documentation",
  "final_url": "https://docs.python.org/3/library/asyncio.html",
  "load_time_ms": 1234
}
```

### Click

Click on element matching selector.

**Parameters**:
- `selector`: CSS selector
- `button`: Mouse button (left, right, middle)
- `click_count`: Number of clicks (1 for single, 2 for double)

**Returns**:
```json
{
  "action": "click",
  "selector": "button#submit",
  "success": true,
  "element_text": "Submit Form",
  "clicked_at": {"x": 150, "y": 300}
}
```

### Type

Type text into input element.

**Parameters**:
- `selector`: CSS selector for input
- `text`: Text to type
- `delay`: Delay between keystrokes in ms (default: 0)

**Returns**:
```json
{
  "action": "type",
  "selector": "input[name='search']",
  "text": "FastAPI authentication",
  "success": true,
  "characters_typed": 22
}
```

### Screenshot

Capture page or element screenshot.

**Parameters**:
- `selector`: Element selector (optional, full page if omitted)
- `screenshot_path`: Save path
- `full_page`: Capture full scrollable page

**Returns**:
```json
{
  "action": "screenshot",
  "screenshot_path": "screenshots/homepage.png",
  "success": true,
  "width": 1920,
  "height": 1080,
  "file_size_bytes": 245678
}
```

### Scroll

Scroll page or element.

**Parameters**:
- `direction`: Scroll direction (up, down, left, right)
- `amount`: Scroll amount in pixels
- `selector`: Element selector (optional, scrolls page if omitted)

**Returns**:
```json
{
  "action": "scroll",
  "direction": "down",
  "amount": 500,
  "success": true,
  "scroll_position": {"x": 0, "y": 1500}
}
```

### Wait

Wait for element or condition.

**Parameters**:
- `selector`: Element selector to wait for
- `state`: Element state (visible, hidden, attached, detached)
- `timeout`: Maximum wait time in ms

**Returns**:
```json
{
  "action": "wait",
  "selector": "div.results",
  "state": "visible",
  "success": true,
  "wait_time_ms": 1234
}
```

## Advanced Usage

### Multi-Step Workflow

```
1. /tool-computer
   Action: navigate
   URL: https://github.com/login

2. /tool-computer
   Action: type
   Selector: input#login_field
   Text: username

3. /tool-computer
   Action: type
   Selector: input#password
   Text: password

4. /tool-computer
   Action: click
   Selector: input[type="submit"]

5. /tool-computer
   Action: wait
   Selector: div.dashboard

6. /tool-computer
   Action: screenshot
   Screenshot Path: screenshots/dashboard.png
```

### Extract Page Content

```
/tool-computer
Action: evaluate
Script: |
  document.querySelector('h1').textContent
```

## Error Handling

### Element Not Found

```json
{
  "action": "click",
  "selector": "button#nonexistent",
  "success": false,
  "error": "Element not found: button#nonexistent",
  "timeout_ms": 30000
}
```

### Navigation Failed

```json
{
  "action": "navigate",
  "url": "https://invalid-url.example",
  "success": false,
  "error": "Navigation failed: net::ERR_NAME_NOT_RESOLVED"
}
```

## Best Practices

- Use specific CSS selectors
- Add waits for dynamic content
- Handle errors gracefully
- Take screenshots for debugging
- Use headless mode for automation
- Set appropriate timeouts
- Close browser when done

## Integration

- Used for web research
- Enables UI testing
- Supports data extraction
- Automates repetitive tasks

## Related Commands

- `/deep-research` - Uses browser for research
- `/autonomous-research` - Autonomous web research
- `/research-memory` - Store research findings

## Source

- **File**: `app/server/tools/computer_tool.py`
- **Function**: `browser_action()`, `execute_browser_command()`
- **Technology**: Playwright
- **Layer**: Tools (HOW)
