# Claude Introduction

> Source: [Claude Platform Docs](https://platform.claude.com/docs/en/intro)

## Overview

Claude is Anthropic's AI assistant, designed to be helpful, harmless, and honest. Claude Code brings these capabilities to software development workflows.

## Key Features

### Conversational AI
- Natural language understanding
- Multi-turn conversations
- Context retention

### Tool Use
- Function calling
- MCP integration
- Custom tools

### Code Capabilities
- Code generation
- Code review
- Debugging
- Refactoring

## Claude Models

### Claude 3.5 Sonnet
- Best balance of speed and capability
- Ideal for most development tasks

### Claude 3 Opus
- Most capable model
- Best for complex reasoning

### Claude 3 Haiku
- Fastest responses
- Good for simple queries

## Getting Started

### Install Claude CLI

```bash
npm install -g @anthropic-ai/claude-code
```

### Configure API Key

```bash
export ANTHROPIC_API_KEY=your_api_key
```

### First Run

```bash
# Interactive mode
claude

# Single command
claude "Explain this code" -f main.py
```

## Core Concepts

### Context Window
Claude maintains conversation context up to:
- 100K tokens (Claude 3 Opus)
- 200K tokens (Claude 3.5 Sonnet)

### System Prompts
Customize Claude's behavior with CLAUDE.md files.

### Tool Calling
Claude can call functions/tools you define or expose via MCP.

## ableton-mcp Usage

### Common Tasks

```bash
# Run tests
claude "Run and analyze the tests in tests/test_tools.py"

# Code generation
claude "Create a new MCP tool for tempo detection"

# Debugging
claude "This test times out - help me fix it" -f tests/test_tools.py
```

### With MCP Tools

```bash
# Use Ableton-specific tools
claude "Search the Ableton docs for sidechain compression"
```

## Related Pages

- [Installation](installation.md) - Detailed setup
- [MCP Integration](mcp.md) - Tool development
- [Best Practices](best-practices.md) - Effective usage
