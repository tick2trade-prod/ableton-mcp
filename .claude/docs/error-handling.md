# Claude Error Handling

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Handling Claude Errors

### API Errors
```
Error: Rate limit exceeded
Solution: Wait and retry, or reduce request frequency
```

### Tool Errors
```
Error: Command failed with exit code 1
Solution: Review output, fix issue, retry
```

### Context Errors
```
Error: Context too long
Solution: Start new conversation, reduce file context
```

## Providing Error Context

### Include Full Error
```
The test failed with this error:
```
ConnectionError: Socket timeout after 10 seconds
  at src/client.py:45
  at tests/test_tools.py:23
```
Help me debug this.
```

### Include Recent Changes
```
I just modified src/client.py to add timeout handling.
Now the tests fail with:
[error message]
```

### Describe Expected Behavior
```
Expected: Track creates in < 5 seconds
Actual: Timeout after 30 seconds
```

## Recovery Patterns

### Retry Logic
Claude will suggest retry mechanisms:
```python
for attempt in range(3):
    try:
        result = await connect()
        break
    except TimeoutError:
        await asyncio.sleep(2 ** attempt)
```

### Graceful Degradation
```python
try:
    detailed_info = await get_full_info()
except APIError:
    detailed_info = get_cached_info()
```

### Rollback
```bash
git checkout -- src/client.py
```

## ableton-mcp Common Errors

### Socket Timeout
```
Issue: ConnectionError: Socket timeout
Solution: Verify Ableton is running, check port 9877

Check: make check-port
Verify: make test-connection
```

### MCP Server Not Found
```
Issue: MCP server disconnected
Solution: Check server command, verify Python path
```

## Related Pages

- [Best Practices](best-practices.md) - Prevention
- [Troubleshooting](troubleshooting.md) - Problem solving
- [Agent Mode](agent-mode.md) - Automated recovery
