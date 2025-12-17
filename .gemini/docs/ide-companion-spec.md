# IDE Companion Extension Spec

> Source: [https://geminicli.com/docs/ide-integration/ide-companion-spec](https://geminicli.com/docs/ide-integration/ide-companion-spec)

## Overview

Specification for building IDE companion extensions.

## Protocol

### Connection
Extensions connect to Gemini CLI via:
- WebSocket
- IPC
- HTTP

### Messages

```typescript
interface Message {
  type: 'request' | 'response' | 'event';
  id: string;
  payload: any;
}
```

## Commands

### Send Prompt
```json
{
  "type": "request",
  "id": "1",
  "payload": {
    "action": "prompt",
    "text": "Explain this code",
    "context": {
      "file": "main.py",
      "selection": "lines 10-20"
    }
  }
}
```

### Get Status
```json
{
  "type": "request",
  "id": "2",
  "payload": {
    "action": "status"
  }
}
```

## Events

### Response Stream
```json
{
  "type": "event",
  "id": "1",
  "payload": {
    "event": "response",
    "data": "..."
  }
}
```

## Implementation

See examples in:
- VS Code extension
- JetBrains plugin

## Related Pages

- [IDE Integration](ide-integration.md) - Overview
- [Extensions](extensions.md) - Extension development
