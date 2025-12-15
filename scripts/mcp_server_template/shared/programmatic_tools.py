#!/usr/bin/env python3
"""Programmatic tool calling for autonomous code generation (Claude feature integration).

Enables agents to write code that calls tools programmatically, reducing latency
and token consumption by avoiding model round trips.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class ProgrammaticToolExecutor:
    """Programmatic tool executor for autonomous code generation."""

    def __init__(self):
        """Initialize programmatic tool executor."""
        self.tools: dict[str, Any] = {}

    async def register_tool(self, name: str, tool_func: callable) -> None:
        """Register a tool for programmatic execution.

        Args:
            name: Tool name
            tool_func: Tool function (async or sync)
        """
        self.tools[name] = tool_func

    async def call_tool(self, tool_name: str, tool_input: dict[str, Any]) -> Any:
        """Call tool programmatically.

        Args:
            tool_name: Tool name
            tool_input: Tool input

        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")

        tool = self.tools[tool_name]

        if asyncio.iscoroutinefunction(tool):
            return await tool(**tool_input)
        else:
            return tool(**tool_input)

    async def call_tools_sequence(self, tool_calls: list[dict[str, Any]]) -> list[Any]:
        """Execute sequence of tool calls.

        Args:
            tool_calls: List of tool call dicts with 'tool' and 'input' keys

        Returns:
            List of results
        """
        results = []
        for call in tool_calls:
            result = await self.call_tool(call["tool"], call.get("input", {}))
            results.append(result)
        return results

    async def call_tools_parallel(self, tool_calls: list[dict[str, Any]]) -> list[Any]:
        """Execute tool calls in parallel.

        Args:
            tool_calls: List of tool call dicts with 'tool' and 'input' keys

        Returns:
            List of results
        """
        tasks = [self.call_tool(call["tool"], call.get("input", {})) for call in tool_calls]
        return await asyncio.gather(*tasks, return_exceptions=True)
