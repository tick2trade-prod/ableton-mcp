# Backlog: Project Structure Refactor

## Objective
Adopt a standard project structure similar to `redis-mcp` to improve maintainability and discoverability.

## Proposed Structure

```
/
  src/
    ableton_mcp/            # Main package (formerly MCP_Server)
    remote_script/          # Remote Script code
  tests/                    # Test suite
  examples/                 # Example scripts/clients
  assets/                   # Binary assets (audio/midi)
  external/                 # External dependencies/references (submodules)
  pyproject.toml
  gemini-extension.json     # Gemini CLI configuration
```

## detailed Changes

1.  **Move Source Code**:
    *   `MCP_Server` -> `src/ableton_mcp`
    *   `AbletonMCP_Remote_Script` -> `src/remote_script` (or kept at root if Ableton requires hard path, but symlinking is better).
2.  **Create `gemini-extension.json`**:
    *   Standardize entry point for agents.
3.  **Examples**:
    *   Move ad-hoc scripts to `examples/`.

## References
*   [redis-mcp](https://github.com/redis/mcp-redis) (Added as submodule in `external/redis-mcp`)
