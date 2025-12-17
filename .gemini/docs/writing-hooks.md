# Writing Hooks

> Source: [https://geminicli.com/docs/hooks/writing-hooks](https://geminicli.com/docs/hooks/writing-hooks)

## Hook Structure

```typescript
import { Hook, HookContext } from '@google/gemini-cli-sdk';

export default class MyHook implements Hook {
  name = 'my-hook';

  async beforeRequest(ctx: HookContext) {
    // Modify request
    return ctx;
  }

  async afterResponse(ctx: HookContext) {
    // Process response
    return ctx;
  }
}
```

## Available Hooks

| Hook | Timing |
|------|--------|
| `beforeRequest` | Before API call |
| `afterResponse` | After response |
| `beforeToolCall` | Before tool execution |
| `afterToolCall` | After tool execution |
| `onError` | On error |

## Example: Logging Hook

```typescript
export default class LoggingHook implements Hook {
  name = 'logging';

  async beforeRequest(ctx: HookContext) {
    console.log(`Request: ${ctx.prompt}`);
    return ctx;
  }

  async afterResponse(ctx: HookContext) {
    console.log(`Response: ${ctx.response.length} chars`);
    return ctx;
  }
}
```

## Example: Cost Tracking

```typescript
export default class CostHook implements Hook {
  name = 'cost-tracker';

  async afterResponse(ctx: HookContext) {
    const tokens = ctx.usage.totalTokens;
    console.log(`Tokens used: ${tokens}`);
    return ctx;
  }
}
```

## Configuration

```json
{
  "hooks": [
    "./my-hook.js",
    "@example/hook-package"
  ]
}
```

## Related Pages

- [Hooks](hooks.md) - Overview
- [Best Practices](hooks-best-practices.md) - Guidelines
