# Claude Authentication

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## API Key Authentication

### Environment Variable (Recommended)
```bash
export ANTHROPIC_API_KEY=your_api_key
```

### Configuration File
```json
{
  "apiKey": "your_api_key"
}
```

## Getting an API Key

1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create account or sign in
3. Go to API Keys
4. Create new key
5. Copy and store securely

## Verifying Authentication

```bash
claude "Hello"
```

If successful, Claude will respond.

## Security Best Practices

### Use Environment Variables
```bash
# ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY=sk-ant-...
```

### Never Commit Keys
Add to `.gitignore`:
```
.env
**/secrets.*
```

### Rotate Keys Periodically
Replace keys every 90 days.

## Related Pages

- [Installation](installation.md) - Setup
- [Configuration](configuration.md) - Settings
- [Security](security.md) - Security practices
