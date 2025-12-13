# Backlog: Project Structure Refactor

## Objective
Adopt a standard project structure similar to `redis-mcp` to improve maintainability and discoverability, while supporting Antigravity agent workflows.

## Proposed Structure

```
/
  src/
    ableton_mcp/            # Main package (formerly MCP_Server)
    remote_script/          # Remote Script code
  app/                      # Application layer (Agent-facing logic)
  tests/                    # Test suite
    config.py               # Test configuration loader
  examples/                 # Example scripts/clients
  scripts/                  # DevOps and setup scripts
  assets/                   # Binary assets (audio/midi)
  external/                 # External dependencies/references (submodules)
  config.yaml               # Global Env Config (OS=MACOS, IDE=ANTIGRAVITY)
  pyproject.toml
  gemini-extension.json     # Gemini CLI configuration
  Makefile                  # Build & Run commands
```

## Detailed Changes

1.  **Move Source Code**:
    *   `MCP_Server` -> `src/ableton_mcp`
    *   `AbletonMCP_Remote_Script` -> `src/remote_script` (symlinked if needed).
2.  **Configuration**:
    *   Utilize `config.yaml` for environment flags (OS, IDE, MODEL).
    *   Utilize `tests/config.py` for test-specific constants.
3.  **Docker Integration**:
    *   Implement `make build-docker-local` with build arguments:
        ```bash
        make build-docker-local OS=MACOS IDE=ANTIGRAVITY MODEL=GEMINI
        ```
    *   Dockerfile should consume these args to configure the image.

## Antigravity & Agents
*   Research best practices for "Antigravity Agents" within this repo.
*   Ensure `gemini-extension.json` exposes tools correctly for agent discovery.
*   Keep workflows "stupid simple" for agent interaction.

## References
*   [redis-mcp](https://github.com/redis/mcp-redis) (Structure Reference)


 https://antigravity.google/docs/mcp


https://antigravity.google/docs/artifacts


https://antigravity.google/docs/task-list


https://antigravity.google/docs/implementation-plan


https://antigravity.google/docs/knowledge


https://antigravity.google/docs/agent-manager


https://antigravity.google/docs/workspaces

https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-system-instructions.json
