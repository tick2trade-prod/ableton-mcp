# Gemini CLI Documentation

> Local documentation for Gemini CLI features, optimized for agentic workflows and MCP development in the ableton-mcp project.

## Project Context

This documentation is tailored for:
- **Custom MCP Development**: Building Model Context Protocol servers for Ableton Live integration
- **Ollama Integration**: Running local LLM inference alongside Gemini CLI
- **Agentic Workflows**: Command-line AI automation for music production

## Official Documentation

📖 **Source**: [https://geminicli.com/docs/](https://geminicli.com/docs/)

---

## Documentation Index

### Overview
- [Architecture](architecture.md) - High-level design and components
- [Contribution Guide](https://github.com/google-gemini/gemini-cli/blob/main/CONTRIBUTING.md) - Setup, building, testing

### Get Started
- [Quickstart](get-started.md) - Getting started with Gemini CLI
- [Gemini 3 Pro](gemini-3.md) - Enable and use Gemini 3
- [Authentication](authentication.md) - Authenticate to Gemini CLI
- [Configuration](configuration.md) - Configure the CLI
- [Installation](installation.md) - Install and run Gemini CLI
- [Examples](examples.md) - Example usage

### CLI
- [CLI Introduction](cli-reference.md) ✓ - Command-line interface overview
- [Commands](commands.md) - Available CLI commands
- [Checkpointing](checkpointing.md) ✓ - Checkpointing feature
- [Custom Commands](custom-commands.md) - Create your own commands
- [Enterprise](enterprise.md) - Enterprise features
- [Headless Mode](headless.md) - Scripting and automation
- [Keyboard Shortcuts](keyboard-shortcuts.md) - Workflow shortcuts
- [Model Selection](model-selection.md) - Select processing model
- [Sandbox](sandbox.md) - Containerized tool execution
- [Settings](settings.md) - CLI behavior configuration
- [Telemetry](telemetry.md) - Telemetry overview
- [Themes](themes.md) - CLI themes
- [Token Caching](token-caching.md) - Token optimization
- [Trusted Folders](trusted-folders.md) - Security feature
- [Tutorials](tutorials.md) - Gemini CLI tutorials
- [Uninstall](uninstall.md) - Uninstall methods

### Core
- [Core Introduction](core.md) - Gemini CLI core information
- [Memport](memport.md) - Memory Import Processor
- [Tools API](tools-api.md) - Core tool management
- [Policy Engine](policy-engine.md) - Fine-grained tool control

### Tools
- [Tools Introduction](tools.md) - Gemini CLI tools overview
- [File System Tools](file-system.md) - read_file, write_file
- [Shell Tool](shell.md) - run_shell_command
- [Web Fetch Tool](web-fetch.md) - web_fetch tool
- [Web Search Tool](web-search.md) - google_web_search
- [Memory Tool](memory.md) - save_memory tool
- [Todo Tool](todos.md) - write_todos tool
- [MCP Servers](mcp.md) ✓ - **MCP integration** ⭐

### Extensions
- [Extensions Introduction](extensions.md) - Extend CLI functionality
- [Getting Started with Extensions](extensions-getting-started.md) - Build extensions
- [Extension Releasing](extension-releasing.md) - Release extensions

### Hooks
- [Hooks](hooks.md) ✓ - CLI behavior customization
- [Writing Hooks](writing-hooks.md) - Create hooks
- [Best Practices](hooks-best-practices.md) - Security and performance

### IDE Integration
- [IDE Integration](ide-integration.md) - Connect CLI to editor
- [IDE Companion Spec](ide-companion-spec.md) - Build companion extensions

### Development
- [NPM](npm.md) - Package structure
- [Releases](releases.md) - Deployment cadence
- [Changelog](changelog.md) - Notable changes
- [Integration Tests](integration-tests.md) - Testing framework
- [Issue and PR Automation](issue-pr-automation.md) - Automation processes

### Support
- [FAQ](faq.md) - Frequently asked questions
- [Troubleshooting](troubleshooting.md) - Common problems
- [Quota and Pricing](quota-pricing.md) - Free tier and paid options
- [Terms of Service](tos-privacy.md) - Legal information

---

## Quick Links for ableton-mcp Development

| Feature | Relevance to Project |
|---------|---------------------|
| ⭐ [MCP Servers](mcp.md) | Core integration for Ableton MCP |
| [Slash Commands](slash-commands.md) ✓ | Custom command workflows |
| [Hooks](hooks.md) ✓ | Customize CLI behavior |
| [Headless Mode](headless.md) | Scripting automation |
| [Interactive Mode](interactive-mode.md) ✓ | REPL development |

✓ = Already documented locally

---

## Project-Specific Configuration

### MCP Servers in This Project
```json
// ~/.gemini/settings.json
{
  "mcpServers": {
    "ableton_codegen": {
      "command": "python",
      "args": ["-m", "mcp_servers.ableton_codegen.server"]
    },
    "research_mcp": {
      "command": "python",
      "args": ["-m", "mcp_servers.research_mcp.server"]
    }
  }
}
```

### Ollama Integration
```bash
# Use Gemini CLI with Ollama for specific tasks
gemini "Summarize this with local Ollama" --model ollama:llama3.2
```

---

## Related Documentation

- [Antigravity IDE Docs](../.antigravity/docs/README.md) - IDE features
- [Claude CLI Docs](../.claude/docs/README.md) - Claude Code usage
- [Project GEMINI.md](../GEMINI.md) - Project rules
