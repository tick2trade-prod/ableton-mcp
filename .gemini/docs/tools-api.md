# Tools API

> Source: [https://geminicli.com/docs/core/tools-api](https://geminicli.com/docs/core/tools-api)

## Overview

The Tools API manages tool registration, discovery, and execution in Gemini CLI.

## Tool Registration

### Built-in Tools
Registered automatically:
```typescript
registry.register(new ShellTool());
registry.register(new FileSystemTool());
registry.register(new WebFetchTool());
```

### MCP Tools
Discovered from configured servers:
```typescript
const tools = await mcpClient.listTools();
for (const tool of tools) {
  registry.register(new MCPToolWrapper(tool));
}
```

## Tool Interface

```typescript
interface Tool {
  name: string;
  description: string;
  inputSchema: JSONSchema;

  execute(params: object): Promise<ToolResult>;
  requiresConfirmation(): boolean;
}
```

## Tool Execution Flow

1. Model generates function call
2. Registry locates tool
3. Confirmation requested (if needed)
4. Tool executes
5. Result returned to model

## Creating Custom Tools

### Extension Pattern
```typescript
export class CustomTool implements Tool {
  name = "custom_tool";
  description = "Does something custom";

  inputSchema = {
    type: "object",
    properties: {
      input: { type: "string" }
    }
  };

  async execute(params: { input: string }) {
    return { result: `Processed: ${params.input}` };
  }
}
```

### MCP Pattern
```python
@server.tool()
async def custom_tool(input: str) -> dict:
    """Does something custom."""
    return {"result": f"Processed: {input}"}
```

## Tool Naming

- Alphanumeric, underscore, dot, hyphen only
- Maximum 63 characters
- Conflicts resolved via prefixing

## Related Pages

- [Tools](tools.md) - Available tools
- [MCP](mcp.md) - MCP tool integration
- [Policy Engine](policy-engine.md) - Execution control
