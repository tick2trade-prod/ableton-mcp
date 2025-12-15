#!/usr/bin/env python3
"""Core orchestration for Ableton Code Generation MCP.

Integrates PDF embeddings, web search, and code generation
for comprehensive Ableton track creation assistance.
"""

import logging
from typing import Any

from scripts.ableton_cache_ast_codegen_mcp.code_generator import (
    AbletonCodeGenerator,
)
from scripts.ableton_cache_ast_codegen_mcp.pdf_embeddings import AbletonDocEmbeddings
from scripts.ableton_cache_ast_codegen_mcp.settings import (
    AbletonCodegenSettings,
    get_settings,
)
from scripts.ableton_cache_ast_codegen_mcp.web_search import AbletonWebSearch

logger = logging.getLogger("ableton-codegen-core")


class AbletonCodegenCore:
    """Core orchestration for Ableton code generation.

    Combines PDF documentation, web search, and code generation
    to create comprehensive track creation assistance.
    """

    def __init__(self, settings: AbletonCodegenSettings | None = None):
        """Initialize core with settings.

        Args:
            settings: Optional settings instance
        """
        self.settings = settings or get_settings()

        # Lazy-initialized components
        self._embeddings: AbletonDocEmbeddings | None = None
        self._web_search: AbletonWebSearch | None = None
        self._code_generator: AbletonCodeGenerator | None = None

    @property
    def embeddings(self) -> AbletonDocEmbeddings:
        """Get PDF embeddings instance."""
        if self._embeddings is None:
            self._embeddings = AbletonDocEmbeddings(
                pdf_path=self.settings.pdf_path,
                redis_url=self.settings.redis_url,
                index_name=self.settings.redis_index_name,
                embedding_model=self.settings.embedding_model,
                chunk_size=self.settings.chunk_size,
                chunk_overlap=self.settings.chunk_overlap,
            )
        return self._embeddings

    @property
    def web_search(self) -> AbletonWebSearch:
        """Get web search instance."""
        if self._web_search is None:
            self._web_search = AbletonWebSearch(
                tavily_api_key=self.settings.tavily_api_key,
                max_results=self.settings.max_search_results,
            )
        return self._web_search

    @property
    def code_generator(self) -> AbletonCodeGenerator:
        """Get code generator instance."""
        if self._code_generator is None:
            self._code_generator = AbletonCodeGenerator(
                scripts_dir=self.settings.track_scripts_dir,
                mcp_server_path=self.settings.mcp_server_path,
            )
        return self._code_generator

    async def research_topic(
        self,
        topic: str,
        include_docs: bool = True,
        include_web: bool = True,
    ) -> dict[str, Any]:
        """Research a topic using both embedded docs and web search.

        Args:
            topic: Topic to research
            include_docs: Include embedded doc search
            include_web: Include web search

        Returns:
            dict with combined research results
        """
        results = {
            "topic": topic,
            "doc_results": [],
            "web_results": [],
        }

        if include_docs:
            doc_results = await self.embeddings.search_docs(topic)
            results["doc_results"] = doc_results.get("results", [])

        if include_web:
            web_results = await self.web_search.search_ableton_guides(topic)
            results["web_results"] = web_results.get("results", [])

        results["success"] = bool(results["doc_results"] or results["web_results"])

        return results

    async def generate_track_with_research(
        self,
        track_spec: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate track code with research-backed recommendations.

        Args:
            track_spec: Track specification

        Returns:
            dict with code and research
        """
        track_type = track_spec.get("type", "unknown")
        track_name = track_spec.get("name", "New Track")

        # Research the track type
        research = await self.research_topic(f"{track_type} production")

        # Analyze existing patterns
        patterns = await self.code_generator.analyze_all_scripts()
        similar = self.code_generator.find_similar_patterns(track_type, patterns)

        reference = similar[0] if similar else None

        # Generate code
        code = self.code_generator.generate_track_code(track_spec, reference)
        validation = await self.code_generator.validate_code(code)

        return {
            "success": validation["valid"],
            "code": code,
            "validation": validation,
            "research": research,
            "reference_pattern": reference.to_dict() if reference else None,
        }


# Global core instance (singleton)
_core: AbletonCodegenCore | None = None


def get_core() -> AbletonCodegenCore:
    """Get global core instance."""
    global _core
    if _core is None:
        _core = AbletonCodegenCore()
    return _core


def reset_core() -> None:
    """Reset core singleton (for testing)."""
    global _core
    _core = None
