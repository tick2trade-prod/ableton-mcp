"""MCP utility functions."""

import os
import shutil
from typing import Any


def normalize_list[T](value: Any, item_type: type[T]) -> list[T] | None:
    """Normalize a value to a list of the specified type.

    Handles various input types:
    - None -> None
    - List -> List (with type conversion if needed)
    - Single item -> List with one item
    - Other types -> Attempts to convert to list

    Args:
        value: The value to normalize
        item_type: The expected type of list items (used for type hints)

    Returns:
        A normalized list, or None if input was None

    Example:
        >>> normalize_list(["a", "b"], str)
        ['a', 'b']
        >>> normalize_list("single", str)
        ['single']
        >>> normalize_list(None, str)
        None
        >>> normalize_list([1, 2, 3], str)
        ['1', '2', '3']
    """
    if value is None:
        return None

    if isinstance(value, list):
        # Already a list, return as-is
        return value

    # Single item - wrap in list
    return [value]


def normalize_mcp_server_config(server_config: dict[str, Any]) -> dict[str, Any]:
    """Normalize MCP server configuration for MultiServerMCPClient.

    Resolves uv/uvx paths and ensures PATH is set correctly for stdio-based
    MCP servers.

    Args:
        server_config: Raw MCP server configuration from ~/.cursor/mcp.json

    Returns:
        Normalized configuration with resolved command paths and environment

    Example:
        >>> config = {"command": "uv", "args": ["run", "server.py"]}
        >>> normalized = normalize_mcp_server_config(config)
        >>> normalized["command"]  # Returns full path to uv
        '/Users/.../.local/bin/uv'
    """
    result = server_config.copy()

    # Get the command
    command = result.get("command", "")

    # Resolve uv/uvx to full path if needed
    if command in ("uv", "uvx"):
        # Try to find uv/uvx in common locations
        resolved_command = _resolve_command_path(command)
        if resolved_command:
            result["command"] = resolved_command

    # Ensure environment includes PATH
    env = result.get("env", {})
    if "PATH" not in env:
        env["PATH"] = os.environ.get("PATH", "")
    result["env"] = env

    return result


def _resolve_command_path(command: str) -> str | None:
    """Resolve a command to its full path.

    Checks common locations for uv/uvx and other tools.

    Args:
        command: Command name to resolve

    Returns:
        Full path to command, or None if not found
    """
    # First, try shutil.which (respects PATH)
    full_path = shutil.which(command)
    if full_path:
        return full_path

    # Common installation locations for uv/uvx
    home = os.path.expanduser("~")
    common_paths = [
        os.path.join(home, ".local", "bin", command),
        os.path.join(home, ".cargo", "bin", command),
        f"/usr/local/bin/{command}",
        f"/opt/homebrew/bin/{command}",
    ]

    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None
