# Hooks Best Practices

> Source: [https://geminicli.com/docs/hooks/best-practices](https://geminicli.com/docs/hooks/best-practices)

## Security

### Input Validation
```typescript
async beforeRequest(ctx: HookContext) {
  if (!isValidInput(ctx.prompt)) {
    throw new Error('Invalid input');
  }
  return ctx;
}
```

### Sensitive Data
- Don't log prompts with secrets
- Sanitize outputs
- Use environment variables

## Performance

### Async Operations
```typescript
// Good: Non-blocking
async afterResponse(ctx: HookContext) {
  setImmediate(() => logToServer(ctx));
  return ctx;
}
```

### Caching
```typescript
const cache = new Map();

async beforeRequest(ctx: HookContext) {
  const cached = cache.get(ctx.prompt);
  if (cached) {
    ctx.skipRequest = true;
    ctx.response = cached;
  }
  return ctx;
}
```

## Debugging

### Error Handling
```typescript
async beforeRequest(ctx: HookContext) {
  try {
    // Hook logic
  } catch (error) {
    console.error('Hook error:', error);
    // Don't break the chain
  }
  return ctx;
}
```

### Logging
```typescript
const DEBUG = process.env.DEBUG_HOOKS;

async beforeRequest(ctx: HookContext) {
  if (DEBUG) {
    console.log('Hook context:', ctx);
  }
  return ctx;
}
```

## Composability

### Chain-Friendly
Always return context:
```typescript
async beforeRequest(ctx: HookContext) {
  // Modify ctx
  return ctx; // Always return!
}
```

### State Management
Use context for state:
```typescript
async beforeRequest(ctx: HookContext) {
  ctx.metadata.startTime = Date.now();
  return ctx;
}

async afterResponse(ctx: HookContext) {
  const duration = Date.now() - ctx.metadata.startTime;
  console.log(`Duration: ${duration}ms`);
  return ctx;
}
```

## Related Pages

- [Hooks](hooks.md) - Overview
- [Writing Hooks](writing-hooks.md) - Development
