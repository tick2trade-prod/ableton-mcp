"""Configuration management for AbletonLite."""

import os
from pathlib import Path

from pydantic import BaseModel, Field


class Config(BaseModel):
    """AbletonLite configuration."""

    # Database
    db_path: Path = Field(
        default_factory=lambda: Path.home() / ".ableton_lite" / "ableton_lite.db"
    )

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_enabled: bool = True

    # Server
    server_name: str = "ableton_lite"

    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment variables."""
        return cls(
            db_path=Path(
                os.getenv(
                    "ABLETON_LITE_DB",
                    str(Path.home() / ".ableton_lite" / "ableton_lite.db"),
                )
            ),
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            ollama_enabled=os.getenv("OLLAMA_ENABLED", "true").lower() == "true",
        )

    def ensure_db_dir(self) -> None:
        """Ensure database directory exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
