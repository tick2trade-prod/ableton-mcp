# Troubleshooting

> Source: [https://geminicli.com/docs/troubleshooting](https://geminicli.com/docs/troubleshooting)

## Common Issues

### Authentication Failed

**Symptoms**: "Not authenticated" error

**Solutions**:
1. Run `gemini auth login`
2. Check API key: `echo $GOOGLE_API_KEY`
3. Verify network connection

### MCP Server Won't Connect

**Symptoms**: Server shows `DISCONNECTED`

**Solutions**:
1. Verify server command: Run manually
2. Check dependencies: Install requirements
3. Review logs: `gemini --debug`
4. Check path: Ensure command is accessible

### No Tools Discovered

**Symptoms**: MCP connected but no tools

**Solutions**:
1. Verify server implements tool listing
2. Check `includeTools` / `excludeTools`
3. Review server stderr

### Commands Timing Out

**Symptoms**: Tool calls hang

**Solutions**:
1. Increase timeout in config
2. Check server performance
3. Test server independently

### Rate Limiting

**Symptoms**: "Rate limit exceeded" error

**Solutions**:
1. Wait and retry
2. Reduce request frequency
3. Use Flash models for quick tasks

## Debug Mode

```bash
gemini --debug
```

Shows:
- API requests/responses
- MCP communication
- Tool execution logs

## Log Files

Check `~/.gemini/logs/` for detailed logs.

## ableton-mcp Specific

### Ableton Connection Issues
1. Verify Ableton is running
2. Check port: `make check-port`
3. Test connection: `make test-connection`
4. Review Ableton logs

### MCP Server Errors
1. Check Redis: `docker ps`
2. Verify environment variables
3. Test server directly

## Getting Help

- Check [FAQ](faq.md)
- Search GitHub issues
- Ask in discussions

## Related Pages

- [FAQ](faq.md) - Common questions
- [MCP](mcp.md) - MCP troubleshooting
