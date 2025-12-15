"""Ollama client for AbletonLite."""

from typing import Any

import ollama

from ableton_lite.config import Config


class OllamaClient:
    """Async Ollama client wrapper."""

    def __init__(self, config: Config | None = None):
        """Initialize Ollama client."""
        self.config = config or Config.from_env()
        self._client: ollama.AsyncClient | None = None

    @property
    def client(self) -> ollama.AsyncClient:
        """Get or create Ollama client."""
        if self._client is None:
            self._client = ollama.AsyncClient(host=self.config.ollama_host)
        return self._client

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
        system: str | None = None,
    ) -> str:
        """Generate a response from Ollama."""
        if not self.config.ollama_enabled:
            return "[Ollama disabled]"

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat(
            model=model or self.config.ollama_model,
            messages=messages,
        )
        return response["message"]["content"]

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
    ) -> dict[str, Any]:
        """Chat with Ollama using message history."""
        if not self.config.ollama_enabled:
            return {"content": "[Ollama disabled]"}

        response = await self.client.chat(
            model=model or self.config.ollama_model,
            messages=messages,
        )
        return response["message"]

    async def list_models(self) -> list[str]:
        """List available models."""
        response = await self.client.list()
        return [m["name"] for m in response.get("models", [])]

    async def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            await self.client.list()
            return True
        except Exception:
            return False
