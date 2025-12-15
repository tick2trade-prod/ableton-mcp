# Op: Browser Screenshot

**Rank**: 4 - Atomic Operation Commands

## Overview

Take screenshot of current page or element.

## Usage

```
/op-browser-screenshot filename="screenshot.png" fullpage=true
```

## Parameters

- `filename`: Output filename (required)
- `fullpage`: Full page screenshot (default: false)
- `selector`: CSS selector for element (optional)

## Implementation

```python
from app.server.tools.computer_tool import browser_action
from app.server.protocols.tool_models import BrowserCommand, BrowserAction

command = BrowserCommand(action=BrowserAction.SCREENSHOT)
result = await browser_action(command)
```

## Output

```json
{"filename": "screenshot.png", "size": "1920x1080"}
```
