# Workspaces

> Source: [https://antigravity.google/docs/workspaces](https://antigravity.google/docs/workspaces)

## Overview

Workspaces define project boundaries and configuration for agent interactions.

## Workspace Configuration

A workspace is defined by:
- **Root Directory**: Project location
- **Settings**: Agent configuration
- **MCP Servers**: Available tools
- **Rules**: GEMINI.md content

## ableton-mcp Workspace

### Location
```
/Users/alexzh/ableton-mcp
```

### Structure
```
ableton-mcp/
├── .antigravity/         # IDE configuration
│   ├── docs/             # This documentation
│   └── mcp.json          # MCP server config
├── .agent/               # Agent configuration
│   └── workflows/        # Custom workflows
├── GEMINI.md             # Project rules
├── pyproject.toml        # Dependencies
├── src/                  # Source code
├── tests/                # Test files
├── mcp_servers/          # MCP server code
└── live_set/             # Ableton track scripts
```

### MCP Servers Available
```json
{
  "ableton_codegen": "Ableton code generation",
  "research_mcp": "Web research",
  "sota_researcher_v2": "SOTA research + planning",
  "deepagents": "Multi-agent orchestration"
}
```

## Workspace-Specific Settings

### Agent Behavior
```json
{
  "agent": {
    "mode": "agentic",
    "mcpServers": ["ableton_codegen", "research_mcp"]
  }
}
```

### File Patterns
```json
{
  "files": {
    "include": ["**/*.py", "**/*.md"],
    "exclude": ["**/node_modules", "**/__pycache__"]
  }
}
```

## Multi-Workspace Support

Open multiple workspaces:
1. Open Agent Manager
2. Add Workspace
3. Configure settings
4. Switch between workspaces

## Related Pages

- [Agent Manager](agent-manager.md) - Manager overview
- [Playground](playground.md) - Experimentation
- [Settings](settings.md) - Configuration
