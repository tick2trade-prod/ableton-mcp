# Model Selection

> Source: [https://geminicli.com/docs/cli/model](https://geminicli.com/docs/cli/model)

## Available Models

| Model | Speed | Capability | Context |
|-------|-------|------------|---------|
| `gemini-3-pro` | Medium | Highest | 1M |
| `gemini-2.5-pro` | Medium | Very High | 1M |
| `gemini-2.5-flash` | Fast | High | 1M |
| `gemini-2.0-flash` | Fastest | Good | 128K |

## Selecting Models

### Configuration
```json
{
  "model": "gemini-2.5-pro"
}
```

### Command Line
```bash
gemini --model gemini-2.5-flash "Quick question"
```

### Slash Command
```
/model gemini-3-pro
```

## Model Recommendations

### For ableton-mcp

| Task | Recommended Model |
|------|-------------------|
| Complex MCP development | gemini-3-pro |
| Track script generation | gemini-2.5-pro |
| Quick queries | gemini-2.5-flash |
| Test analysis | gemini-2.5-pro |
| Research | gemini-2.5-pro |

### By Task Type

| Task Type | Model |
|-----------|-------|
| Complex reasoning | gemini-3-pro |
| Code generation | gemini-2.5-pro |
| Quick edits | gemini-2.5-flash |
| Large codebase | gemini-3-pro |

## Switching Models Mid-Session

```
> [Using gemini-2.5-flash]
> I need to do something complex
/model gemini-3-pro
> Now help with complex refactoring
```

## Cost Considerations

More capable models cost more per token:
- gemini-3-pro: Highest
- gemini-2.5-pro: Medium
- gemini-2.5-flash: Lower
- gemini-2.0-flash: Lowest

## Related Pages

- [Gemini 3](gemini-3.md) - Gemini 3 features
- [Configuration](configuration.md) - Settings
- [Quota and Pricing](quota-pricing.md) - Costs
