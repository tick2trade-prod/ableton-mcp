# Extensions Introduction

> Source: [https://geminicli.com/docs/extensions](https://geminicli.com/docs/extensions)

## Overview

Extensions add new functionality to Gemini CLI.

## Types of Extensions

### Tool Extensions
Add new tools to the CLI.

### UI Extensions
Customize the interface.

### Integration Extensions
Connect to external services.

## Extension Discovery

```bash
gemini extensions list
gemini extensions search "audio"
```

## Installation

```bash
gemini extensions install @example/extension
```

## Creating Extensions

See [Getting Started with Extensions](extensions-getting-started.md).

## ableton-mcp Extensions

This project uses MCP servers instead of extensions for:
- Ableton integration
- Research capabilities
- Code generation

MCP provides more flexibility for our use case.

## Related Pages

- [Getting Started with Extensions](extensions-getting-started.md)
- [Extension Releasing](extension-releasing.md)
- [MCP](mcp.md) - Alternative approach
