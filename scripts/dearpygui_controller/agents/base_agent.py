"""Base agent class for all specialized agents."""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger("dearpygui-controller")


@dataclass
class AgentResult:
    """Result from an agent action."""

    success: bool
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class BaseAgent(ABC):
    """Base class for all specialized agents.

    Provides common functionality for agent lifecycle:
    - Initialization with Ollama LLM
    - MCP client connection
    - Progress callback support
    - Error handling
    """

    def __init__(
        self,
        name: str = "BaseAgent",
        verbose: bool = True,
        ollama_model: str = "llama3",
        ollama_base_url: str = "http://localhost:11434",
    ):
        self.name = name
        self.verbose = verbose
        self.ollama_model = ollama_model
        self.ollama_base_url = ollama_base_url
        self._progress_callback: Optional[Callable] = None
        self._log_callback: Optional[Callable] = None
        self._mcp_client = None

    def set_progress_callback(self, callback: Callable) -> None:
        """Set callback for progress updates."""
        self._progress_callback = callback

    def set_log_callback(self, callback: Callable) -> None:
        """Set callback for log messages."""
        self._log_callback = callback

    def log(self, message: str) -> None:
        """Log a message."""
        if self.verbose:
            logger.info(f"[{self.name}] {message}")
        if self._log_callback:
            self._log_callback(f"[{self.name}] {message}")

    def update_progress(self, track_index: int, progress: float) -> None:
        """Update progress for a track (0.0 - 1.0)."""
        if self._progress_callback:
            self._progress_callback(track_index, progress)

    def get_mcp_client(self):
        """Get or create the MCP client."""
        if self._mcp_client is None:
            try:
                # Import here to avoid circular imports
                import sys

                sys.path.insert(0, str(__file__).rsplit("/", 4)[0])
                from live_set.lily_palmer.i_am_machine.ableton_client import (
                    AbletonMCPClient,
                )

                self._mcp_client = AbletonMCPClient()
            except ImportError as e:
                logger.warning(f"Could not import AbletonMCPClient: {e}")
                self._mcp_client = None
        return self._mcp_client

    @abstractmethod
    async def execute(self, **kwargs) -> AgentResult:
        """Execute the agent's main task.

        Returns:
            AgentResult with success status and data
        """
        pass

    @abstractmethod
    def get_role(self) -> str:
        """Return the agent's role description."""
        pass

    @abstractmethod
    def get_goal(self) -> str:
        """Return the agent's goal description."""
        pass
