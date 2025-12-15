#!/usr/bin/env python3
"""Base classes for creating a pluggable core for the MCP server."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable
from typing import Any, Optional


class BaseCore(ABC):
    """Abstract Base Class for MCP server core logic.

    This class defines the interface that any "core" logic module should
    implement to be compatible with the generic MCP server.
    """

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the core components.

        This method should be called before any other methods.
        It's responsible for setting up heavy components like models,
        database connections, etc.
        """
        pass

    @abstractmethod
    async def create_agent(
        self,
        agent_name: str,
        description: str,
        system_prompt: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a new agent."""
        pass

    @abstractmethod
    async def run_agent(
        self,
        task: str,
        agent_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """Run a task with an agent."""
        pass

    @abstractmethod
    async def run_agent_stream(
        self,
        task: str,
        agent_name: Optional[str] = None,
        callback: Optional[Callable[[str], Any]] = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Run a task with an agent in streaming mode."""
        yield {}

    @abstractmethod
    async def generate_code_stream(
        self,
        task: str,
        language: str = "python",
        agent_name: Optional[str] = None,
        callback: Optional[Callable[[str], Any]] = None,
        use_structured_output: bool = False,
    ) -> AsyncIterator[dict[str, Any]]:
        """Generate code in streaming mode."""
        yield {}

    @abstractmethod
    async def generate_code_batch(
        self,
        tasks: list[str],
        language: str = "python",
        agent_name: Optional[str] = None,
        max_concurrent: int = 5,
    ) -> list[dict[str, Any]]:
        """Generate code for multiple tasks in a batch."""
        return []

    @abstractmethod
    async def memorize(self, content: str) -> dict[str, Any]:
        """Memorize content."""
        pass

    @abstractmethod
    async def research(self, query: str) -> dict[str, Any]:
        """Research from memory."""
        pass
