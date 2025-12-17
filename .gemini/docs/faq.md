# FAQ

> Source: [https://geminicli.com/docs/faq](https://geminicli.com/docs/faq)

## General

**Q: What is Gemini CLI?**
A: Command-line interface for interacting with Gemini models.

**Q: Is it free?**
A: Free tier available with usage limits.

**Q: Which models are available?**
A: Gemini 3 Pro, 2.5 Pro, 2.5 Flash, 2.0 Flash.

## Authentication

**Q: How do I authenticate?**
A: `gemini auth login` or set `GOOGLE_API_KEY`.

**Q: Can I use ADC?**
A: Yes, for Google Cloud environments.

## MCP

**Q: What is MCP?**
A: Model Context Protocol for extending AI capabilities.

**Q: How do I add MCP servers?**
A: Configure in `~/.gemini/settings.json`.

**Q: Can I create custom MCP servers?**
A: Yes, see [MCP documentation](mcp.md).

## Tools

**Q: What tools are built-in?**
A: Shell, file system, web fetch, web search, memory, todos.

**Q: How do I trust tools?**
A: Use `trust: true` in MCP config or trusted folders.

## ableton-mcp Specific

**Q: How do I use with this project?**
A: Configure MCP servers, then run `gemini` in project directory.

**Q: Which MCP servers are available?**
A: ableton_codegen, research_mcp, sota_researcher_v2, deepagents.

## Related Pages

- [Troubleshooting](troubleshooting.md) - Problem solving
- [Get Started](get-started.md) - Quick start
