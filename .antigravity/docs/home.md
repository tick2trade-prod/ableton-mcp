# Home

> Source: [https://antigravity.google/docs/home](https://antigravity.google/docs/home)

## Overview

Antigravity is Google's AI-powered development environment that combines the power of Gemini models with a complete IDE experience. It's designed for building software with AI assistance at every step.

## Key Features for ableton-mcp

### 🤖 Agentic Development
- AI agents that understand your codebase
- Automatic code generation and refactoring
- Test-driven development support

### 🔌 MCP Integration
- Native support for Model Context Protocol servers
- Connect external tools and data sources
- Build custom MCPs for specialized workflows

### 🏠 Local Development
- Works with local projects and repositories
- Integrates with local tools like Ollama
- Maintains privacy for sensitive code

## Relevance to This Project

For the **ableton-mcp** project, Antigravity provides:

1. **MCP Server Development**: Build and test custom MCP servers
2. **Ableton Integration**: AI-assisted music production automation
3. **Research Workflows**: Use SOTA researcher for production techniques
4. **Local LLM Support**: Run Ollama for local inference

## Getting Started

See [Getting Started](get-started.md) for initial setup.

## Project-Specific Configuration

This project uses:
```yaml
# From GEMINI.md
Primary Objective: Write pytest integration tests for Ableton MCP tools
Key Principles:
  - No mocks - All tests run against real Ableton Live
  - Incremental testing - Test one tool at a time
  - Live verification - Confirm changes in DAW
```
