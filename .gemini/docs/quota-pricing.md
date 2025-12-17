# Quota and Pricing

> Source: [https://geminicli.com/docs/quota-and-pricing](https://geminicli.com/docs/quota-and-pricing)

## Free Tier

Gemini CLI includes free usage:
- Limited requests per minute
- Limited tokens per day
- Access to all models

## Paid Options

### API Key Billing
Pay-as-you-go with Google Cloud:
```bash
export GOOGLE_API_KEY=your_billing_enabled_key
```

### Enterprise
Custom pricing for organizations.

## Token Pricing

| Model | Input | Output |
|-------|-------|--------|
| Gemini 3 Pro | Higher | Higher |
| Gemini 2.5 Pro | Medium | Medium |
| Gemini 2.5 Flash | Lower | Lower |

## Optimization Tips

### Use Token Caching
```json
{
  "tokenCaching": {
    "enabled": true
  }
}
```

### Choose Right Model
- Simple tasks: Flash models
- Complex tasks: Pro models

### Manage Context
- Keep conversations focused
- Start fresh for new topics

## Monitoring Usage

```
/usage
```

Shows:
- Tokens used today
- Requests count
- Rate limit status

## Related Pages

- [Token Caching](token-caching.md) - Reduce costs
- [Model Selection](model-selection.md) - Model costs
- [Settings](settings.md) - Configuration
