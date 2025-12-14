Research and design a minimal-effort adapter strategy to port my existing **Cursor IDE** configuration/features to **Claude CLI**, **Codex CLI**, and **Gemini CLI**.

## Context (what already exists)

My project currently implements Cursor-style features under `.cursor`, driven by this configuration:

```yaml
# Configuration consumed by scripts/cli/build_cli_adapters.py
cursor_config:
  base_dir: ".cursor"
  paths:
    mcp: "mcp.json"
    rules_dir: "rules"
    commands_dir: "commands/app"
    hooks_dir: "hooks"
    mcp_wrappers_dir: "mcp-wrappers"
cursor_docs:
  commands_url: https://cursor.com/docs/agent/chat/commands
  rules_url: https://cursor.com/docs/context/rules
  hooks_url: https://cursor.com/docs/agent/hooks
  mcp_url: https://cursor.com/docs/context/mcp
```

Expected repository structure (already implemented):

```
.cursor/
  commands/app/
  hooks/
  hooks.json
  mcp.json
  mcp-wrappers/
  rules/*.mdc
```

## Task 1 — Capability research (CLI config surfaces)

For each CLI, identify what local project configuration directories/files are supported and what features they enable:

* **Claude CLI**: `.claude` (claude-cli)
* **Codex CLI**: `.codex` (codex-cli)
* **Gemini CLI**: `.gemini` (gemini-cli)

For each, capture:

* Supported config files/directories and naming conventions
* Supported “rules/system prompts” equivalents (if any)
* Command/shortcut equivalents (if any)
* Hooks / lifecycle events (if any)
* MCP/tooling integration surfaces (if any)
* Recommended/best-practice usage patterns from official docs/examples

## Task 2 — Adapter design (minimal engineering)

Propose the lowest-effort plan to reuse what I already built in `.cursor` by mapping it onto each CLI’s native capabilities first, and only adding glue code where necessary.

Requirements:

* Prefer **native** mechanisms over custom parsing whenever possible
* Reuse existing assets (`rules/*.mdc`, `mcp.json`, wrappers, commands, hooks) with minimal transformation
* Clearly call out any gaps where a CLI has no native equivalent and propose a fallback strategy

## Deliverables (output format)

1. A concise **feature matrix**: `.cursor` vs `.claude` vs `.codex` vs `.gemini` (rules, commands, hooks, MCP/tools, wrappers).
2. Per-CLI **mapping plan** describing how each `.cursor` component will be reused or translated.
3. A recommended **directory/layout** proposal for each CLI (what files to generate and where).
4. A short list of **implementation steps** for `scripts/cli/build_cli_adapters.py` updates (per CLI), emphasizing minimal diffs and maintainability.
5. Links to the most relevant **official documentation** sources used for each CLI capability claim.
