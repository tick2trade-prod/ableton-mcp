# Gemini CLI Hooks

This document provides an overview of how to use hooks in Gemini CLI to customize its behavior.

## What are Hooks?

Hooks are scripts or programs that the Gemini CLI executes at specific points within its agentic loop. They allow you to intercept and customize the CLI's behavior without altering its source code.

With hooks, you can perform various actions, including:

*   **Adding context**: Injecting relevant information before a model processes a request.
*   **Validating actions**: Reviewing and potentially blocking dangerous operations.
*   **Enforcing policies**: Implementing security and compliance requirements.
*   **Logging interactions**: Tracking tool usage and model responses.
*   **Optimizing behavior**: Dynamically adjusting tool selection or model parameters.

Hooks run synchronously as part of the agent loop, meaning the Gemini CLI waits for all matching hooks to complete before proceeding.

## Key Hook Events

Hooks are triggered by specific events in Gemini CLI's lifecycle:

*   `SessionStart`: Fires when a session begins.
*   `SessionEnd`: Fires when a session ends.
*   `BeforeAgent`: Occurs after a user submits a prompt but before planning.
*   `AfterAgent`: Fires when the agent loop ends.
*   `BeforeModel`: Executes before sending a request to the Large Language Model (LLM).
*   `AfterModel`: Fires after receiving a response from the LLM.
*   `BeforeToolSelection`: Occurs before the LLM selects tools.
*   `BeforeTool`: Executes before a tool runs.
*   `AfterTool`: Fires after a tool executes.
*   `PreCompress`: Occurs before context compression.
*   `Notification`: Triggers when a notification occurs.

## Configuration

Hooks are defined in `settings.json` files. The configuration supports matchers for tool-related events, allowing you to filter which tools trigger a hook using exact matches, regex, or wildcards.

## Input/Output

Hooks receive JSON data via stdin and use exit codes and stdout/stderr to communicate back to the CLI.

*   **Exit code 0**: Success.
*   **Exit code 2**: Blocking error.
*   **Other exit codes**: Non-blocking warnings.

Input JSON contains common fields like `session_id`, `cwd`, `hook_event_name`, and `timestamp`, along with event-specific fields.

## Migrating from Claude Code

Gemini CLI provides a command to migrate hooks from Claude Code:

```bash
gemini hooks migrate --from-claude
```

This command helps in mapping event and tool names from a Claude Code environment to Gemini CLI.

For more detailed information, refer to the [official Gemini CLI hooks documentation](https://geminicli.com/docs/hooks/).
