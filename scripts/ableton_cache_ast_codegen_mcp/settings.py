#!/usr/bin/env python3
"""Type-safe configuration for Ableton Code Generation MCP server.

All settings can be overridden via environment variables with ABLETON_CODEGEN_ prefix.
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AbletonCodegenSettings(BaseSettings):
    """Configuration for Ableton Code Generation MCP server.

    All settings can be overridden via environment variables with
    ABLETON_CODEGEN_ prefix (e.g., ABLETON_CODEGEN_PDF_PATH=...).
    """

    # PDF Embedding Configuration
    pdf_path: Path = Field(
        default=Path("docs/live12-manual-en.pdf"),
        description="Path to Ableton Live manual PDF",
    )
    chunk_size: int = Field(
        default=1000,
        ge=200,
        le=4000,
        description="Chunk size for PDF embedding (200-4000, default: 1000)",
    )
    chunk_overlap: int = Field(
        default=200,
        ge=50,
        le=500,
        description="Chunk overlap for PDF embedding (50-500, default: 200)",
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence transformer model for embeddings",
    )

    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL",
    )
    redis_index_name: str = Field(
        default="ableton_docs",
        description="Redis index name for document embeddings",
    )

    # Web Search Configuration
    tavily_api_key: str = Field(
        default="",
        description="Tavily API key for web search",
    )
    max_search_results: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum search results (1-50, default: 10)",
    )

    # Code Generation Configuration
    track_scripts_dir: Path = Field(
        default=Path("live_set/lily_palmer/i_am_machine"),
        description="Directory containing track scripts",
    )
    mcp_server_path: Path = Field(
        default=Path("MCP_Server/server.py"),
        description="Path to MCP server file",
    )

    # Summarization Configuration
    use_ollama: bool = Field(
        default=True,
        description="Use Ollama for local summarization",
    )
    ollama_model: str = Field(
        default="llama3.2:latest",
        description="Ollama model for summarization",
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama API base URL",
    )

    model_config = SettingsConfigDict(
        env_prefix="ABLETON_CODEGEN_",
        case_sensitive=False,
        validate_default=True,
        extra="ignore",
    )

    @field_validator("redis_url")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate Redis URL format."""
        if not v.startswith(("redis://", "rediss://")):
            raise ValueError("Redis URL must start with redis:// or rediss://")
        return v

    @field_validator("ollama_base_url")
    @classmethod
    def validate_ollama_url(cls, v: str) -> str:
        """Validate Ollama base URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("Ollama base URL must start with http:// or https://")
        return v.rstrip("/")


# Global settings instance (singleton)
_settings: AbletonCodegenSettings | None = None


def get_settings() -> AbletonCodegenSettings:
    """Get global settings instance (singleton)."""
    global _settings
    if _settings is None:
        _settings = AbletonCodegenSettings()
    return _settings


def reset_settings() -> None:
    """Reset settings singleton (for testing)."""
    global _settings
    _settings = None
