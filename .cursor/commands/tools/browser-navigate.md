# Op: Browser Navigate

**Rank**: 4 - Atomic Operation Commands

## Overview

Navigate browser to URL.

## Usage

```
/op-browser-navigate url="https://docs.python.org"
```

## Parameters

- `url`: URL to navigate (required)
- `wait_for`: Wait for selector (optional)
- `timeout`: Timeout in ms (default: 30000)

## Implementation

```python
from app.server.tools.computer_tool import browser_action
from app.server.protocols.tool_models import BrowserCommand, BrowserAction

command = BrowserCommand(action=BrowserAction.NAVIGATE, url=url)
result = await browser_action(command)
```

## Output

```json
{"title": "Python Documentation", "url": "..."}
```
