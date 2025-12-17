# Inbox

> Source: [https://antigravity.google/docs/inbox](https://antigravity.google/docs/inbox)

## Overview

The Inbox collects notifications and alerts from agent activities.

## Notification Types

### Task Completion
- Completed tasks
- Failed tasks
- Pending approvals

### Agent Activity
- Background task results
- MCP tool outputs
- Error alerts

### System Notifications
- Updates
- Configuration changes
- Workspace events

## Inbox Usage

### Checking Notifications
1. Click inbox icon
2. View unread items
3. Mark as read/dismiss

### Acting on Notifications
- Click notification to view details
- Jump to related file/conversation
- Approve pending actions

## Notifications in ableton-mcp

### Common Notifications
```
✓ Test suite completed: 27/27 passed
⚠ MCP server disconnected: ableton_codegen
ℹ New conversation started
○ Command pending approval: git push
```

### Background Task Results
```
✓ Research completed: sidechain techniques
  → View results
  → Open artifact
```

### Error Alerts
```
✗ Test failed: test_create_track
  → View error log
  → Jump to test
```

## Configuration

```json
{
  "notifications": {
    "taskCompletion": true,
    "errors": true,
    "info": false
  }
}
```

## Related Pages

- [Agent Manager](agent-manager.md) - Overview
- [Task List](task-list.md) - Task notifications
