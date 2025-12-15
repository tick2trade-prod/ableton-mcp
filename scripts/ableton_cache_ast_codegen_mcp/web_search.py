#!/usr/bin/env python3
"""Ableton-specific web search for engineering guides and documentation."""

import logging
import time
from typing import Any

logger = logging.getLogger("ableton-codegen-search")

# Optional imports
try:
    from tavily import TavilyClient

    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    TavilyClient = None

try:
    import httpx

    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    httpx = None


# Ableton-focused domains for prioritized search
ABLETON_DOMAINS = [
    "ableton.com",
    "help.ableton.com",
    "studiobrootle.com",
    "musicradar.com",
    "soundonsound.com",
    "productionmusiclive.com",
    "reddit.com/r/ableton",
]

# Device-specific search keywords
ABLETON_DEVICES = [
    "Roar",
    "Meld",
    "Drift",
    "Drum Sampler",
    "Wavetable",
    "Operator",
    "Simpler",
    "Sampler",
    "Analog",
    "Collision",
    "Electric",
    "Tension",
    "Granulator",
]


class AbletonWebSearch:
    """Ableton-specific web search."""

    def __init__(
        self,
        tavily_api_key: str = "",
        max_results: int = 10,
        timeout_seconds: int = 30,
    ):
        self.tavily_api_key = tavily_api_key
        self.max_results = max_results
        self.timeout_seconds = timeout_seconds
        self._tavily_client = None

    def _get_tavily_client(self):
        """Get or create Tavily client."""
        if not TAVILY_AVAILABLE:
            logger.warning("Tavily not available. Install with: uv add tavily-python")
            return None

        if not self.tavily_api_key:
            logger.warning("Tavily API key not set")
            return None

        if self._tavily_client is None:
            self._tavily_client = TavilyClient(api_key=self.tavily_api_key)

        return self._tavily_client

    async def search_ableton_guides(
        self,
        query: str,
        max_results: int | None = None,
    ) -> dict[str, Any]:
        """Search for Ableton engineering guides and tutorials.

        Prioritizes results from Ableton-focused domains.

        Args:
            query: Search query
            max_results: Maximum results (default: self.max_results)

        Returns:
            dict with search results
        """
        client = self._get_tavily_client()
        if not client:
            return {
                "success": False,
                "error": "Tavily client not available",
                "results": [],
            }

        max_results = max_results or self.max_results
        start_time = time.perf_counter()

        # Enhance query with Ableton context
        enhanced_query = f"Ableton Live {query}"

        try:
            response = client.search(
                query=enhanced_query,
                max_results=max_results,
                search_depth="advanced",
                include_domains=ABLETON_DOMAINS,
            )

            results = []
            for r in response.get("results", []):
                # Score boost for Ableton-specific domains
                url = r.get("url", "")
                score = r.get("score", 0)

                if "ableton.com" in url:
                    score *= 1.5
                elif any(domain in url for domain in ABLETON_DOMAINS[:3]):
                    score *= 1.2

                results.append(
                    {
                        "title": r.get("title", ""),
                        "url": url,
                        "content": r.get("content", ""),
                        "score": score,
                    }
                )

            # Re-sort by adjusted score
            results.sort(key=lambda x: x["score"], reverse=True)

            elapsed = time.perf_counter() - start_time

            return {
                "success": True,
                "query": query,
                "enhanced_query": enhanced_query,
                "results": results,
                "result_count": len(results),
                "latency_ms": elapsed * 1000,
            }

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
            }

    async def search_device_documentation(
        self,
        device_name: str,
        aspect: str = "",
    ) -> dict[str, Any]:
        """Search for specific Ableton device documentation.

        Args:
            device_name: Name of device (Roar, Meld, etc.)
            aspect: Specific aspect to search (e.g., "modulation", "filters")

        Returns:
            dict with device-specific results
        """
        # Validate device name
        if device_name not in ABLETON_DEVICES:
            logger.warning(f"Unknown device: {device_name}")

        query = f"{device_name} Ableton Live 12"
        if aspect:
            query += f" {aspect}"

        return await self.search_ableton_guides(query)

    async def search_production_technique(
        self,
        technique: str,
        genre: str = "techno",
    ) -> dict[str, Any]:
        """Search for production techniques.

        Args:
            technique: Technique name (e.g., "sidechain compression", "rumble kick")
            genre: Genre context (default: "techno")

        Returns:
            dict with technique-focused results
        """
        query = f"{technique} {genre} Ableton Live tutorial"
        return await self.search_ableton_guides(query)
