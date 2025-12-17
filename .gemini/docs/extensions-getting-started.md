# Getting Started with Extensions

> Source: [https://geminicli.com/docs/extensions/getting-started-extensions](https://geminicli.com/docs/extensions/getting-started-extensions)

## Creating an Extension

### 1. Initialize Project
```bash
mkdir my-extension
cd my-extension
npm init
```

### 2. Create Extension
```typescript
// index.ts
import { Extension, Tool } from '@google/gemini-cli-sdk';

export default class MyExtension implements Extension {
  name = 'my-extension';

  tools: Tool[] = [
    {
      name: 'my_tool',
      description: 'Does something useful',
      inputSchema: {...},
      execute: async (params) => {
        return { result: 'Success' };
      }
    }
  ];
}
```

### 3. Build
```bash
npm run build
```

### 4. Test Locally
```bash
gemini --extension ./dist
```

## Extension Structure

```
my-extension/
├── src/
│   ├── index.ts
│   └── tools/
├── package.json
└── tsconfig.json
```

## vs MCP Servers

For ableton-mcp, we use MCP servers instead:
- Python-native (matches project)
- More flexible
- Easier debugging

## Related Pages

- [Extensions](extensions.md) - Overview
- [Extension Releasing](extension-releasing.md) - Publishing
- [MCP](mcp.md) - Alternative approach
