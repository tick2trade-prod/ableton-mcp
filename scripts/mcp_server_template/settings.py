#!/usr/bin/env python3
"""Type-safe configuration for the MCP server template using pydantic-settings.

Provides centralized configuration management with validation and type safety.
All settings can be overridden via environment variables with MCP_SERVER_ prefix.
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Type-safe configuration for the MCP Server.

    All settings can be overridden via environment variables with
    MCP_SERVER_ prefix (e.g., MCP_SERVER_REQUIRE_VALIDATION=false).
    """

    # Core validation
    require_validation: bool = Field(
        default=True,
        description="Require validation (fail fast if packages missing, no graceful degradation)",
    )

    # Core class to load
    core_class: str = Field(
        default="scripts.mcp_server_template.example_core.ExampleCore",
        description="The core class to load for the server logic.",
    )

    # Generator configuration
    use_ollama: bool = Field(
        default=True,
        description="Use Ollama for cost-free local LLM operations (default: true)",
    )
    ollama_model: str = Field(
        default="codellama-34b-optimized:latest",
        description="Ollama model to use (default: codellama-34b-optimized:latest)",
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434/v1",
        description="Ollama API base URL (default: http://localhost:11434/v1)",
    )
    ollama_api_key: str = Field(
        default="ollama",
        description="Ollama API key (dummy key, Ollama ignores it)",
    )

    # OpenAI fallback (only used if Ollama disabled)
    openai_model: str = Field(
        default="gpt-4o-mini",
        description="OpenAI model to use if Ollama disabled (default: gpt-4o-mini)",
    )
    openai_api_key: str = Field(
        default="",
        description="OpenAI API key (required if Ollama disabled)",
    )
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="OpenAI API base URL (default: https://api.openai.com/v1)",
    )

    # Generator parameters
    generator_temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="Generator temperature (0.0-2.0, default: 0.2 for codellama-34b-optimized)",
    )
    generator_max_tokens: int = Field(
        default=2048,
        ge=1,
        le=4096,
        description="Generator max tokens (1-4096, default: 2048 for 34B model with 16K context)",
    )

    # DeepAgent configuration
    agent_thread_id: str = Field(
        default="default",
        description="Default thread ID for DeepAgent conversations",
    )

    # Docker service configuration
    docker_mlflow_url: str = Field(
        default="http://localhost:5000",
        description="MLflow tracking server URL (default: http://localhost:5000)",
    )
    docker_mindsdb_url: str = Field(
        default="http://localhost:47334",
        description="MindsDB API URL (default: http://localhost:47334)",
    )
    docker_redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL (default: redis://localhost:6379)",
    )
    docker_postgres_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/workflow_orchestrator",
        description="PostgreSQL connection URL (default: postgresql://postgres:postgres@localhost:5432/workflow_orchestrator)",
    )
    use_docker_services: bool = Field(
        default=True,
        description="Use Docker services if available (default: true)",
    )

    # GAM retriever configuration (example-specific)
    gam_index_dir: Path = Field(
        default=Path("./tmp/gam_index"),
        description="Directory for GAM index storage (default: ./tmp/gam_index)",
    )
    gam_research_max_iters: int = Field(
        default=8,
        ge=1,
        le=20,
        description="Maximum research iterations (1-20, default: 8 for powerful hardware)",
    )
    gam_dense_model: str = Field(
        default="BAAI/bge-m3",
        description="Dense retriever model (default: BAAI/bge-m3)",
    )
    gam_bm25_threads: int = Field(
        default=4,
        ge=1,
        le=8,
        description="BM25 retriever threads (1-8, default: 4 for multi-core systems)",
    )

    model_config = SettingsConfigDict(
        env_prefix="MCP_SERVER_",
        case_sensitive=False,
        validate_default=True,
        extra="ignore",  # Ignore unknown fields for flexibility
    )

    @field_validator("ollama_base_url")
    @classmethod
    def validate_ollama_url(cls, v: str) -> str:
        """Validate Ollama base URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("Ollama base URL must start with http:// or https://")
        return v

    @field_validator("openai_base_url")
    @classmethod
    def validate_openai_url(cls, v: str) -> str:
        """Validate OpenAI base URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("OpenAI base URL must start with http:// or https://")
        return v

    @field_validator("docker_mlflow_url", "docker_mindsdb_url")
    @classmethod
    def validate_docker_url(cls, v: str) -> str:
        """Validate Docker service URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("Docker service URL must start with http:// or https://")
        return v

    @field_validator("docker_redis_url")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate Redis URL format."""
        if not v.startswith(("redis://", "rediss://")):
            raise ValueError("Redis URL must start with redis:// or rediss://")
        return v

    @field_validator("docker_postgres_url")
    @classmethod
    def validate_postgres_url(cls, v: str) -> str:
        """Validate PostgreSQL URL format."""
        if not v.startswith(("postgresql://", "postgres://")):
            raise ValueError("PostgreSQL URL must start with postgresql:// or postgres://")
        return v

    @field_validator("gam_index_dir")
    @classmethod
    def validate_index_dir(cls, v: Path) -> Path:
        """Ensure index directory exists."""
        v = Path(v)
        v.mkdir(parents=True, exist_ok=True)
        return v


# Global settings instance (singleton pattern)
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get global settings instance (singleton pattern).

    Returns:
        Settings instance with validated configuration
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
