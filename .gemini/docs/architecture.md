# Gemini CLI Architecture

> Source: [https://geminicli.com/docs/architecture](https://geminicli.com/docs/architecture)

## Overview

Gemini CLI brings Gemini models to your terminal in an interactive REPL environment.

## Components

### CLI Package (`packages/cli`)
- User interface
- Command parsing
- Input/output handling
- Session management

### Core Package (`packages/core`)
- API communication
- Tool management
- MCP integration
- Context management

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│                  User                        │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              CLI (packages/cli)              │
│  ┌─────────┐ ┌─────────┐ ┌─────────────┐   │
│  │ Commands│ │ REPL    │ │ Formatting  │   │
│  └─────────┘ └─────────┘ └─────────────┘   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│             Core (packages/core)             │
│  ┌─────────┐ ┌─────────┐ ┌─────────────┐   │
│  │ Gemini  │ │ Tools   │ │ MCP Client  │   │
│  │ API     │ │ Registry│ │             │   │
│  └─────────┘ └─────────┘ └─────────────┘   │
└─────┬───────────────┬───────────────┬───────┘
      │               │               │
      ▼               ▼               ▼
┌─────────┐    ┌──────────┐    ┌──────────┐
│ Gemini  │    │ Built-in │    │ MCP      │
│ API     │    │ Tools    │    │ Servers  │
└─────────┘    └──────────┘    └──────────┘
```

## Key Subsystems

### Tool Registry
Central registry for all tools:
- Built-in tools (shell, file system, web)
- MCP-discovered tools
- Custom tools

### MCP Client
Handles MCP server connections:
- Discovery
- Tool listing
- Tool execution
- Resource access

### Context Manager
Manages conversation context:
- Message history
- File context
- Tool results

## Data Flow

1. **User Input** → CLI parses command
2. **Context Building** → Core gathers relevant context
3. **API Request** → Sent to Gemini API
4. **Tool Execution** → If tools needed
5. **Response** → Formatted and displayed

## Configuration Flow

```
~/.gemini/settings.json
        │
        ▼
    Settings Loader
        │
        ▼
    MCP Discovery
        │
        ▼
    Tool Registry
        │
        ▼
    Ready for Use
```

## Related Pages

- [Tools](tools.md) - Built-in tools
- [MCP](mcp.md) - MCP integration
- [Core](core.md) - Core package details
