# Core Introduction

> Source: [https://geminicli.com/docs/core](https://geminicli.com/docs/core)

## Overview

The Core package (`packages/core`) is the heart of Gemini CLI, managing API communication, tools, and MCP integration.

## Components

### API Client
Communicates with Gemini API:
- Request formatting
- Response handling
- Error management
- Streaming support

### Tool Registry
Manages available tools:
- Built-in tools
- MCP-discovered tools
- Tool execution

### MCP Client
Handles MCP server connections:
- Server discovery
- Tool listing
- Resource management

### Context Manager
Manages conversation state:
- Message history
- File context
- Tool results

## Architecture

```
┌──────────────────────────────────────┐
│           Core Package               │
│  ┌────────────┐  ┌──────────────┐   │
│  │ API Client │  │ MCP Client   │   │
│  └────────────┘  └──────────────┘   │
│  ┌────────────┐  ┌──────────────┐   │
│  │ Tool Reg.  │  │ Context Mgr  │   │
│  └────────────┘  └──────────────┘   │
└──────────────────────────────────────┘
```

## Key Files

| File | Purpose |
|------|---------|
| `mcp-client.ts` | MCP server connections |
| `mcp-tool.ts` | MCP tool wrappers |
| `tools/` | Built-in tools |
| `context/` | Context management |

## Related Pages

- [Architecture](architecture.md) - Overall design
- [Tools API](tools-api.md) - Tool management
- [MCP](mcp.md) - MCP integration
