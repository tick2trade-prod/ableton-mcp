#!/usr/bin/env python3
"""Core research logic for Research MCP.

Provides research capabilities with:
- Web search via Tavily API (free tier available)
- Result caching via Redis or local disk cache
- Summarization via Ollama (optional)
- Retry logic and error handling

Independent of MCP protocol. Can be used in CLI, API, or MCP contexts.
"""

import asyncio
import hashlib
import json
import logging
import time
from typing import Any

from scripts.research_mcp.settings import ResearchMCPSettings, get_settings

# Initialize logger
logger = logging.getLogger("research-mcp-core")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Optional imports with graceful fallbacks
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

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

try:
    import diskcache

    DISKCACHE_AVAILABLE = True
except ImportError:
    DISKCACHE_AVAILABLE = False
    diskcache = None

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    tiktoken = None


def _cache_key(prefix: str, *args: Any) -> str:
    """Generate cache key from prefix and arguments."""
    key_parts = [prefix] + [str(arg) for arg in args]
    key_str = ":".join(key_parts)
    return f"research_mcp:{hashlib.md5(key_str.encode()).hexdigest()}"


def _count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken or fallback."""
    if not TIKTOKEN_AVAILABLE or not tiktoken:
        return len(text) // 4  # Approximate

    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4


class ResearchCore:
    """Core research logic with caching and retry support.

    Provides:
    - Web search via Tavily
    - Result caching
    - Summarization via Ollama
    """

    def __init__(self, settings: ResearchMCPSettings | None = None):
        """Initialize research core.

        Args:
            settings: Optional settings (defaults to get_settings())
        """
        self.settings = settings or get_settings()
        self.max_retries = 3
        self.retry_delay = 1.0

        # Lazy initialization
        self._tavily_client: Any = None
        self._redis_client: Any = None
        self._disk_cache: Any = None
        self._http_client: Any = None

    def _get_tavily_client(self) -> Any:
        """Get or create Tavily client."""
        if self._tavily_client is not None:
            return self._tavily_client

        if not TAVILY_AVAILABLE:
            logger.warning("Tavily not available. Install with: uv add tavily-python")
            return None

        if not self.settings.tavily_api_key:
            logger.warning(
                "Tavily API key not set. Set RESEARCH_MCP_TAVILY_API_KEY env var"
            )
            return None

        try:
            self._tavily_client = TavilyClient(api_key=self.settings.tavily_api_key)
            logger.info("Tavily client initialized")
            return self._tavily_client
        except Exception as e:
            logger.error(f"Failed to initialize Tavily client: {e}")
            return None

    def _get_redis_client(self) -> Any:
        """Get or create Redis client."""
        if not self.settings.use_redis or not REDIS_AVAILABLE:
            return None

        if self._redis_client is not None:
            return self._redis_client

        try:
            self._redis_client = redis.from_url(
                self.settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            self._redis_client.ping()
            logger.info(f"Redis connected: {self.settings.redis_url}")
            return self._redis_client
        except Exception as e:
            logger.warning(f"Redis not available: {e}")
            self._redis_client = None
            return None

    def _get_disk_cache(self) -> Any:
        """Get or create disk cache."""
        if not DISKCACHE_AVAILABLE:
            return None

        if self._disk_cache is not None:
            return self._disk_cache

        try:
            self._disk_cache = diskcache.Cache(
                str(self.settings.cache_dir),
                size_limit=100 * 1024 * 1024,  # 100MB
            )
            logger.info(f"Disk cache initialized: {self.settings.cache_dir}")
            return self._disk_cache
        except Exception as e:
            logger.warning(f"Disk cache not available: {e}")
            return None

    async def _get_cached(self, key: str) -> Any:
        """Get cached value."""
        # Try Redis first
        redis_client = self._get_redis_client()
        if redis_client:
            try:
                value = redis_client.get(key)
                if value:
                    return json.loads(value)
            except Exception as e:
                logger.debug(f"Redis get failed: {e}")

        # Fallback to disk cache
        disk_cache = self._get_disk_cache()
        if disk_cache:
            try:
                if key in disk_cache:
                    return disk_cache[key]
            except Exception as e:
                logger.debug(f"Disk cache get failed: {e}")

        return None

    async def _set_cached(self, key: str, value: Any) -> bool:
        """Set cached value."""
        ttl = self.settings.cache_ttl_seconds

        # Try Redis first
        redis_client = self._get_redis_client()
        if redis_client:
            try:
                redis_client.setex(key, ttl, json.dumps(value))
                return True
            except Exception as e:
                logger.debug(f"Redis set failed: {e}")

        # Fallback to disk cache
        disk_cache = self._get_disk_cache()
        if disk_cache:
            try:
                disk_cache.set(key, value, expire=ttl)
                return True
            except Exception as e:
                logger.debug(f"Disk cache set failed: {e}")

        return False

    async def search_web(
        self,
        query: str,
        max_results: int | None = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """Search the web using Tavily API.

        Args:
            query: Search query
            max_results: Maximum results (default: settings.max_results)
            use_cache: Use caching (default: True)

        Returns:
            dict with search results
        """
        if not query or not query.strip():
            return {
                "success": False,
                "error": "Query cannot be empty",
                "results": [],
            }

        max_results = max_results or self.settings.max_results
        start_time = time.perf_counter()

        # Check cache
        if use_cache:
            cache_key = _cache_key("search_web", query, max_results)
            cached = await self._get_cached(cache_key)
            if cached:
                logger.debug(f"Cache hit for query: {query[:50]}...")
                cached["cached"] = True
                return cached

        # Get Tavily client
        client = self._get_tavily_client()
        if not client:
            return {
                "success": False,
                "error": "Tavily client not available. Check API key and installation.",
                "results": [],
            }

        # Search with retry
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = client.search(
                    query=query,
                    max_results=max_results,
                    search_depth="basic",
                )

                results = response.get("results", [])
                latency_ms = (time.perf_counter() - start_time) * 1000

                result = {
                    "success": True,
                    "query": query,
                    "results": [
                        {
                            "title": r.get("title", ""),
                            "url": r.get("url", ""),
                            "content": r.get("content", ""),
                            "score": r.get("score", 0),
                        }
                        for r in results
                    ],
                    "result_count": len(results),
                    "latency_ms": latency_ms,
                    "cached": False,
                }

                # Cache result
                if use_cache:
                    await self._set_cached(cache_key, result)

                logger.info(
                    f"Search completed: {len(results)} results in {latency_ms:.0f}ms"
                )
                return result

            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2**attempt)
                    logger.warning(
                        f"Search failed (attempt {attempt + 1}): {e}. "
                        f"Retrying in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        f"Search failed after {self.max_retries} attempts: {e}"
                    )

        return {
            "success": False,
            "error": str(last_exception),
            "query": query,
            "results": [],
        }

    async def summarize(
        self,
        content: str,
        style: str = "concise",
        max_length: int = 500,
    ) -> dict[str, Any]:
        """Summarize content using Ollama.

        Args:
            content: Content to summarize
            style: Summary style (concise, detailed, bullet_points)
            max_length: Maximum summary length in words

        Returns:
            dict with summary
        """
        if not content or not content.strip():
            return {
                "success": False,
                "error": "Content cannot be empty",
                "summary": "",
            }

        if not self.settings.use_ollama:
            return {
                "success": False,
                "error": "Ollama not enabled in settings",
                "summary": "",
            }

        if not HTTPX_AVAILABLE:
            return {
                "success": False,
                "error": "httpx not available. Install with: uv add httpx",
                "summary": "",
            }

        start_time = time.perf_counter()

        # Build prompt based on style
        style_prompts = {
            "concise": f"Summarize the following in {max_length} words or less:\n\n",
            "detailed": f"Provide a detailed summary ({max_length} words max):\n\n",
            "bullet_points": "Summarize as bullet points:\n\n",
        }
        prompt = style_prompts.get(style, style_prompts["concise"]) + content

        try:
            async with httpx.AsyncClient(
                timeout=self.settings.timeout_seconds
            ) as client:
                response = await client.post(
                    f"{self.settings.ollama_base_url}/api/generate",
                    json={
                        "model": self.settings.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                    },
                )
                response.raise_for_status()
                data = response.json()

                summary = data.get("response", "").strip()
                latency_ms = (time.perf_counter() - start_time) * 1000

                return {
                    "success": True,
                    "summary": summary,
                    "style": style,
                    "model": self.settings.ollama_model,
                    "input_tokens": _count_tokens(content),
                    "output_tokens": _count_tokens(summary),
                    "latency_ms": latency_ms,
                }

        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "summary": "",
            }

    async def research_topic(
        self,
        topic: str,
        questions: list[str] | None = None,
        max_results: int | None = None,
        summarize_results: bool = True,
    ) -> dict[str, Any]:
        """Research a topic comprehensively.

        Args:
            topic: Main research topic
            questions: Optional specific research questions
            max_results: Maximum results per search
            summarize_results: Summarize results (default: True)

        Returns:
            dict with research results and optional summary
        """
        if not topic or not topic.strip():
            return {
                "success": False,
                "error": "Topic cannot be empty",
                "results": [],
            }

        start_time = time.perf_counter()
        all_results = []

        # Search main topic
        main_search = await self.search_web(topic, max_results)
        if main_search.get("success"):
            all_results.extend(main_search.get("results", []))

        # Search each question
        if questions:
            for question in questions:
                q_search = await self.search_web(f"{topic}: {question}", max_results)
                if q_search.get("success"):
                    all_results.extend(q_search.get("results", []))

        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for r in all_results:
            url = r.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(r)

        latency_ms = (time.perf_counter() - start_time) * 1000

        result = {
            "success": len(unique_results) > 0,
            "topic": topic,
            "questions": questions or [],
            "results": unique_results,
            "result_count": len(unique_results),
            "latency_ms": latency_ms,
        }

        # Optionally summarize
        if summarize_results and unique_results and self.settings.use_ollama:
            # Combine content for summarization
            combined = "\n\n".join(
                [
                    f"**{r.get('title', 'Untitled')}**\n{r.get('content', '')}"
                    for r in unique_results[:5]  # Top 5 results
                ]
            )
            summary_result = await self.summarize(combined, style="bullet_points")
            if summary_result.get("success"):
                result["summary"] = summary_result.get("summary", "")

        logger.info(
            f"Research completed: {len(unique_results)} unique results in {latency_ms:.0f}ms"
        )
        return result


# Global core instance (singleton)
_core: ResearchCore | None = None


def get_core() -> ResearchCore:
    """Get global core instance."""
    global _core
    if _core is None:
        _core = ResearchCore()
    return _core


def reset_core() -> None:
    """Reset core singleton (for testing)."""
    global _core
    _core = None
