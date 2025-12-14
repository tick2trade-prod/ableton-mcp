# AbletonLite

SQLite + Ollama + FastMCP agent orchestration layer.

## Quick Start

```bash
# Install dependencies
uv sync

# Run the MCP server
uv run python -m ableton_lite.server

# Run tests
uv run pytest tests/ -v
```

## Features

- **FastMCP Server**: Exposes SQLite CRUD tools via MCP
- **Ollama Integration**: Natural language → SQL translation
- **MindsDB-Inspired**: `CREATE AGENT`, jobs, triggers (V2)

## Schema

| Table | Purpose |
|-------|---------|
| `agents` | Agent definitions |
| `tasks` | Task queue and results |
| `knowledge_base` | Embeddings and documents |
