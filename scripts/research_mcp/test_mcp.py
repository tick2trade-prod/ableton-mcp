#!/usr/bin/env python3
"""Tests for Research MCP.

Tests cover:
- Settings loading and validation
- Core research methods (with mocked APIs)
- MCP tool validation
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.research_mcp.core import ResearchCore, _cache_key, _count_tokens
from scripts.research_mcp.settings import (
    ResearchMCPSettings,
    get_settings,
    reset_settings,
)


class TestSettings:
    """Test settings module."""

    def setup_method(self):
        """Reset settings before each test."""
        reset_settings()

    def test_default_settings(self):
        """Test default settings values."""
        settings = ResearchMCPSettings()
        assert settings.max_results == 10
        assert settings.timeout_seconds == 60
        assert settings.use_ollama is True
        assert settings.use_redis is False

    def test_settings_singleton(self):
        """Test settings singleton pattern."""
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2

    def test_settings_env_override(self, monkeypatch):
        """Test environment variable override."""
        reset_settings()
        monkeypatch.setenv("RESEARCH_MCP_MAX_RESULTS", "20")
        settings = ResearchMCPSettings()
        assert settings.max_results == 20


class TestCacheKey:
    """Test cache key generation."""

    def test_cache_key_basic(self):
        """Test basic cache key generation."""
        key = _cache_key("test", "arg1", "arg2")
        assert key.startswith("research_mcp:")
        assert len(key) > 20

    def test_cache_key_deterministic(self):
        """Test cache key is deterministic."""
        k1 = _cache_key("test", "arg1")
        k2 = _cache_key("test", "arg1")
        assert k1 == k2

    def test_cache_key_different_args(self):
        """Test cache key differs with different args."""
        k1 = _cache_key("test", "arg1")
        k2 = _cache_key("test", "arg2")
        assert k1 != k2


class TestTokenCount:
    """Test token counting."""

    def test_count_tokens_fallback(self):
        """Test token count fallback (no tiktoken)."""
        # Should work even without tiktoken
        count = _count_tokens("Hello world")
        assert count > 0

    def test_count_tokens_empty(self):
        """Test token count for empty string."""
        count = _count_tokens("")
        assert count == 0


class TestResearchCore:
    """Test ResearchCore class."""

    def test_core_initialization(self):
        """Test core initialization."""
        core = ResearchCore()
        assert core.settings is not None
        assert core.max_retries == 3

    async def test_search_web_empty_query(self):
        """Test search_web with empty query."""
        core = ResearchCore()
        result = await core.search_web("")
        assert result["success"] is False
        assert "empty" in result["error"].lower()

    async def test_search_web_no_client(self):
        """Test search_web without Tavily client."""
        core = ResearchCore()
        core._tavily_client = None
        # Mock settings to have no API key
        core.settings.tavily_api_key = ""
        result = await core.search_web("test query")
        assert result["success"] is False
        assert "not available" in result["error"].lower()

    async def test_search_web_mocked(self):
        """Test search_web with mocked Tavily client."""
        core = ResearchCore()
        mock_client = MagicMock()
        mock_client.search.return_value = {
            "results": [
                {
                    "title": "Test Result",
                    "url": "https://example.com",
                    "content": "Test content",
                    "score": 0.9,
                }
            ]
        }
        core._tavily_client = mock_client

        result = await core.search_web("test query")
        assert result["success"] is True
        assert result["result_count"] == 1
        assert result["results"][0]["title"] == "Test Result"

    async def test_summarize_empty_content(self):
        """Test summarize with empty content."""
        core = ResearchCore()
        result = await core.summarize("")
        assert result["success"] is False
        assert "empty" in result["error"].lower()

    async def test_summarize_ollama_disabled(self):
        """Test summarize when Ollama is disabled."""
        core = ResearchCore()
        core.settings.use_ollama = False
        result = await core.summarize("Some content to summarize")
        assert result["success"] is False
        assert "not enabled" in result["error"].lower()

    async def test_research_topic_empty(self):
        """Test research_topic with empty topic."""
        core = ResearchCore()
        result = await core.research_topic("")
        assert result["success"] is False
        assert "empty" in result["error"].lower()


class TestMCPServer:
    """Test MCP server imports and tools."""

    def test_mcp_import(self):
        """Test MCP server can be imported."""
        from scripts.research_mcp.mcp_server import mcp

        assert mcp is not None
        assert mcp.name == "research_mcp"

    def test_tools_registered(self):
        """Test tools are registered."""
        from scripts.research_mcp.mcp_server import research, search_web, summarize_text

        assert search_web is not None
        assert research is not None
        assert summarize_text is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
