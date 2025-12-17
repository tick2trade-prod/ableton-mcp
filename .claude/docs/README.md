# Claude CLI Documentation

> Local documentation for Claude Code CLI features, optimized for agentic workflows and MCP development in the ableton-mcp project.

## Project Context

This documentation is tailored for:
- **Custom MCP Development**: Building Model Context Protocol servers for Ableton Live integration
- **Ollama Integration**: Running local LLM inference alongside Claude
- **Agentic Workflows**: AI-powered automation for music production

## Official Documentation

📖 **Sources**:
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Platform Docs](https://platform.claude.com/docs/en/intro)

---

## Documentation Index

### Getting Started
- [Introduction](intro.md) - Overview of Claude Code
- [Installation](installation.md) - Install Claude CLI
- [Configuration](configuration.md) - Configure Claude settings
- [Authentication](authentication.md) - API keys and auth

### Core Features
- [Agent Mode](agent-mode.md) - Agentic capabilities
- [Tool Use](tool-use.md) - Function calling
- [MCP Integration](mcp.md) ⭐ - **Model Context Protocol**
- [Context Management](context.md) - Managing conversation context
- [Memory](memory.md) - Persistent memory features

### Best Practices
- [Prompt Engineering](prompt-engineering.md) - Effective prompts
- [Multi-Turn Conversations](multi-turn.md) - Conversation patterns
- [Error Handling](error-handling.md) - Handling failures
- [Security](security.md) - Secure usage patterns

### CLI Usage
- [Commands](commands.md) - Available commands
- [Configuration Files](config-files.md) - .claude/ structure
- [Permissions](permissions.md) - Command permissions
- [Custom Instructions](custom-instructions.md) - CLAUDE.md usage

### Integration
- [IDE Integration](ide-integration.md) - Editor connections
- [API Usage](api.md) - Direct API access
- [Streaming](streaming.md) - Response streaming

### Advanced
- [Extended Thinking](extended-thinking.md) - Deep reasoning
- [Vision](vision.md) - Image understanding
- [Artifacts](artifacts.md) - Generated content

---

## Quick Links for ableton-mcp Development

| Feature | Relevance to Project |
|---------|---------------------|
| ⭐ [MCP Integration](mcp.md) | Core integration for Ableton MCP |
| [Tool Use](tool-use.md) | Custom tool development |
| [Permissions](permissions.md) | Safe command execution |
| [Agent Mode](agent-mode.md) | Autonomous task execution |

---

## Project Configuration

### Current Settings
```json
// .claude/settings.local.json
{
  "permissions": {
    "allow": [
      "Bash(uv pip install:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(grep:*)"
    ]
  }
}
```

### Recommended Additions
```json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(make:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)"
    ]
  }
}
```

---

## Claude Code Best Practices

### From Anthropic Engineering

#### 1. Use CLAUDE.md Files
Create a `CLAUDE.md` at project root with:
- Project context and goals
- Code conventions
- Testing requirements
- Security considerations

#### 2. Permission Management
```json
{
  "permissions": {
    "allow": ["safe commands"],
    "deny": ["destructive commands"]
  }
}
```

#### 3. Context Windows
- Be mindful of context limits
- Use file references (`@file`) for focused context
- Start new conversations for unrelated tasks

#### 4. Multi-Turn Patterns
```
USER: Implement feature X
CLAUDE: [implements]
USER: Now add tests
CLAUDE: [adds tests]
USER: Run and fix any failures
CLAUDE: [runs, fixes]
```

---

## Related Documentation

- [Gemini CLI Docs](../.gemini/docs/README.md) - Gemini CLI features
- [Antigravity IDE Docs](../.antigravity/docs/README.md) - IDE features
- [Project README](../../README.md) - Project overview
