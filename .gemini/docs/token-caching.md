# Token Caching

> Source: [https://geminicli.com/docs/cli/token-caching](https://geminicli.com/docs/cli/token-caching)

## Overview

Token caching optimizes API usage by caching repeated context.

## How It Works

1. Static context (system prompts, files) is cached
2. Subsequent requests reuse cached tokens
3. Reduces API costs and latency

## Benefits

- **Cost reduction**: Fewer billed tokens
- **Faster responses**: Reduced processing
- **Consistent context**: Reliable behavior

## Configuration

```json
{
  "tokenCaching": {
    "enabled": true,
    "ttl": 3600
  }
}
```

## Cache Management

### Clear Cache
```
/cache clear
```

### View Cache Status
```
/cache status
```

## Best Practices

### Maximize Caching
- Keep system prompts consistent
- Use file references (@file) for context
- Avoid frequent context changes

### For ableton-mcp
```json
{
  "tokenCaching": {
    "enabled": true,
    "includePatterns": [
      "GEMINI.md",
      "pyproject.toml"
    ]
  }
}
```

## Related Pages

- [Configuration](configuration.md) - Settings
- [Quota and Pricing](quota-pricing.md) - Costs
