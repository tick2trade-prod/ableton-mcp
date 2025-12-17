# Integration Tests

> Source: [https://geminicli.com/docs/integration-tests](https://geminicli.com/docs/integration-tests)

## Overview

Information about the integration testing framework used in Gemini CLI.

## Running Tests

For contributors:
```bash
npm run test:integration
```

## Test Categories

### CLI Tests
- Command parsing
- Output formatting
- Session management

### Tool Tests
- File operations
- Shell execution
- Web tools

### MCP Tests
- Server connection
- Tool discovery
- Execution

## Writing Tests

```typescript
describe('MCP Integration', () => {
  it('should connect to server', async () => {
    const client = new MCPClient(config);
    const result = await client.connect();
    expect(result.status).toBe('connected');
  });
});
```

## ableton-mcp Testing

Our project uses similar patterns:
- pytest for integration tests
- Live Ableton connection
- MCP tool verification

See `tests/` directory.

## Related Pages

- [Architecture](architecture.md) - System design
- [Contributing](https://github.com/google-gemini/gemini-cli/blob/main/CONTRIBUTING.md)
