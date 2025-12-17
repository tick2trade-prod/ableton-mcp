# FAQ

> Source: [https://antigravity.google/docs/faq](https://antigravity.google/docs/faq)

## Frequently Asked Questions

### General

**Q: What is Antigravity?**
A: Antigravity is Google's AI-powered development environment with integrated Gemini models and MCP support.

**Q: How does it differ from other AI coding tools?**
A: Native MCP integration, multi-modal models, and tight Google Cloud integration.

---

### Agent

**Q: How do I start a conversation with the agent?**
A: Press `Cmd+L` or click the agent icon.

**Q: Can the agent run commands automatically?**
A: Yes, if configured in turbo mode or with auto-approve settings.

**Q: How do I give the agent context about my project?**
A: Use `GEMINI.md` for persistent rules, or `@[file]` references in conversations.

---

### MCP

**Q: How do I add a custom MCP server?**
A: Add to `.antigravity/mcp.json` with command and arguments.

**Q: Can MCP tools access external services?**
A: Yes, MCP tools can make network requests (e.g., Redis, Ollama, APIs).

**Q: How do I debug MCP tool issues?**
A: Check MCP server logs and use the terminal to test tool invocations.

---

### Ollama Integration

**Q: Can I use Ollama instead of Gemini?**
A: Ollama can be used through MCP tools for specific tasks, but the main agent uses Gemini.

**Q: How do I configure Ollama?**
A: Set `OLLAMA_BASE_URL` and `OLLAMA_MODEL` environment variables.

**Q: Which Ollama models work best?**
A: `llama3.2` for general tasks, `codellama` for code-specific tasks.

---

### ableton-mcp Specific

**Q: Why do tests fail with timeout?**
A: Ensure Ableton is running and AbletonMCP control surface is enabled. Check port 9877.

**Q: How do I run a single test?**
A: `pytest tests/test_file.py::test_name -v`

**Q: Where are Ableton logs?**
A: `~/Library/Preferences/Ableton/Live 12.3.1/Log.txt`

**Q: How do I use the research MCP?**
A: Use `/research topic` or call `research_and_plan()` tool directly.

---

### Troubleshooting

**Q: Agent is not responding?**
A: Check internet connection and try starting a new conversation.

**Q: MCP server won't start?**
A: Check server logs, ensure dependencies are installed, verify Python path.

**Q: Commands aren't being approved?**
A: Check secure mode settings and command approval configuration.

---

## Getting Help

- Review this documentation
- Check project GEMINI.md
- Search conversation history
- Ask the agent directly

## Related Pages

- [Home](home.md) - Getting started
- [Settings](settings.md) - Configuration
- [Troubleshooting guides in Walkthrough](walkthrough.md)
