#!/usr/bin/env python3
"""Type-safe configuration for Research MCP server using pydantic-settings.

Provides centralized configuration management with validation and type safety.
All settings can be overridden via environment variables with RESEARCH_MCP_ prefix.
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ResearchMCPSettings(BaseSettings):
    """Type-safe configuration for Research MCP server.

    All settings can be overridden via environment variables with
    RESEARCH_MCP_ prefix (e.g., RESEARCH_MCP_MAX_RESULTS=20).
    """

    # API Keys
    tavily_api_key: str = Field(
        default="",
        description="Tavily API key for web search (free tier: 1000 queries/month)",
    )

    # Research Configuration
    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum search results to return (1-50, default: 10)",
    )
    cache_ttl_seconds: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Cache TTL in seconds (60-86400, default: 3600 = 1 hour)",
    )
    timeout_seconds: int = Field(
        default=60,
        ge=5,
        le=300,
        description="Request timeout in seconds (5-300, default: 60)",
    )

    # Summarization Configuration
    use_ollama: bool = Field(
        default=True,
        description="Use Ollama for local summarization (default: true)",
    )
    ollama_model: str = Field(
        default="llama3.2:latest",
        description="Ollama model for summarization (default: llama3.2:latest)",
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama API base URL (default: http://localhost:11434)",
    )

    # Caching Configuration
    use_redis: bool = Field(
        default=False,
        description="Use Redis for distributed caching (default: false)",
    )
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL (default: redis://localhost:6379)",
    )
    cache_dir: Path = Field(
        default=Path.home() / ".cache" / "research_mcp",
        description="Local cache directory (default: ~/.cache/research_mcp)",
    )

    # Validation
    require_validation: bool = Field(
        default=False,
        description="Require API validation before use (default: false)",
    )

    model_config = SettingsConfigDict(
        env_prefix="RESEARCH_MCP_",
        case_sensitive=False,
        validate_default=True,
        extra="ignore",
    )

    @field_validator("ollama_base_url")
    @classmethod
    def validate_ollama_url(cls, v: str) -> str:
        """Validate Ollama base URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("Ollama base URL must start with http:// or https://")
        return v.rstrip("/")

    @field_validator("redis_url")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate Redis URL format."""
        if not v.startswith(("redis://", "rediss://")):
            raise ValueError("Redis URL must start with redis:// or rediss://")
        return v

    @field_validator("cache_dir")
    @classmethod
    def validate_cache_dir(cls, v: Path) -> Path:
        """Ensure cache directory exists."""
        v = Path(v)
        v.mkdir(parents=True, exist_ok=True)
        return v


# Global settings instance (singleton pattern)
_settings: ResearchMCPSettings | None = None


def get_settings() -> ResearchMCPSettings:
    """Get global settings instance (singleton pattern).

    Returns:
        ResearchMCPSettings instance with validated configuration
    """
    global _settings
    if _settings is None:
        _settings = ResearchMCPSettings()
    return _settings


def reset_settings() -> None:
    """Reset settings singleton (useful for testing)."""
    global _settings
    _settings = None
