#!/usr/bin/env python3
"""MCP server for GAM DeepAgents v3.

FastMCP protocol setup and tool exposure with enhanced features:
- Better error handling (v2)
- Enhanced observability (v2)
- Improved tool validation (v2)
- Better MCP protocol compliance (v2)
- KISS performance improvements (v3)
- Docker integration (v3)
- Enhanced code generation (v3)
- Claude features integration (v3):
  * Token-efficient tool use (selective info, result compression)
  * Structured outputs support (JSON/Pydantic validation)
  * Better async/await patterns
  * Enhanced error handling with specific error types

Core logic is delegated to GAMDeepAgentsCoreV3.
"""

import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Optional Redis integration for distributed caching
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None  # type: ignore[assignment, misc]

# Optional MLflow integration for experiment tracking
try:
    import mlflow

    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    mlflow = None  # type: ignore[assignment, misc]

# Optional OpenTelemetry integration for observability
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    trace = None  # type: ignore[assignment, misc]

# Optional performance optimizations
try:
    import uvloop

    UVLOOP_AVAILABLE = True
except ImportError:
    UVLOOP_AVAILABLE = False
    uvloop = None  # type: ignore[assignment, misc]

try:
    import msgpack

    MSGPACK_AVAILABLE = True
except ImportError:
    MSGPACK_AVAILABLE = False
    msgpack = None  # type: ignore[assignment, misc]

try:
    import diskcache

    DISKCACHE_AVAILABLE = True
except ImportError:
    DISKCACHE_AVAILABLE = False
    diskcache = None  # type: ignore[assignment, misc]

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    tiktoken = None  # type: ignore[assignment, misc]

try:
    import orjson

    ORJSON_AVAILABLE = True
except ImportError:
    ORJSON_AVAILABLE = False
    orjson = None  # type: ignore[assignment, misc]

try:
    import nest_asyncio

    NEST_ASYNCIO_AVAILABLE = True
except ImportError:
    NEST_ASYNCIO_AVAILABLE = False
    nest_asyncio = None  # type: ignore[assignment, misc]

# Initialize logger
logger = logging.getLogger("gam-deepagents-mcp-v3")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Suppress OpenTelemetry tracing export errors (non-critical)
logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

# Enable nest_asyncio for better async performance if available (after logger init)
if NEST_ASYNCIO_AVAILABLE and nest_asyncio:
    try:
        nest_asyncio.apply()
        logger.debug("nest_asyncio enabled for improved async performance")
    except Exception:
        pass  # Already applied or not needed

# Strict imports: Fail immediately if packages not available
try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise ImportError(f"FastMCP is required: {e}. Install with: uv add fastmcp") from e

from scripts.gam_deepagents.v3.core import GAMDeepAgentsCoreV3
from scripts.gam_deepagents.v3.settings import get_settings_v3

# Lazy core initialization
_core: GAMDeepAgentsCoreV3 | None = None
_redis_client: Any = None


def _get_core() -> GAMDeepAgentsCoreV3:
    """Get or create core instance (lazy initialization).

    Returns:
        GAMDeepAgentsCoreV3 instance
    """
    global _core
    if _core is None:
        settings = get_settings_v3()
        _core = GAMDeepAgentsCoreV3(settings)
        logger.info("Core instance created (lazy initialization, v3)")
    return _core


def _get_redis_client() -> Any:
    """Get or create Redis client (lazy initialization).

    Returns:
        Redis client or None if unavailable
    """
    global _redis_client
    if not REDIS_AVAILABLE:
        return None
    if _redis_client is None:
        try:
            redis_host = os.environ.get("REDIS_HOST", "localhost")
            redis_port = int(os.environ.get("REDIS_PORT", "6379"))
            _redis_client = redis.Redis(
                host=redis_host, port=redis_port, decode_responses=True, socket_connect_timeout=2
            )
            # Test connection
            _redis_client.ping()
            logger.info(f"Redis cache connected: {redis_host}:{redis_port}")
        except Exception as e:
            logger.warning(f"Redis not available: {e}, using local cache only")
            _redis_client = None
    return _redis_client


def _cache_key(prefix: str, *args: Any) -> str:
    """Generate cache key from prefix and arguments.

    Args:
        prefix: Cache key prefix
        *args: Arguments to hash

    Returns:
        Cache key string
    """
    key_parts = [prefix] + [str(arg) for arg in args]
    key_str = ":".join(key_parts)
    return hashlib.md5(key_str.encode()).hexdigest()


async def _get_cached_result(key: str, ttl: int = 3600) -> Any:
    """Get cached result from Redis or diskcache.

    Uses Redis for distributed caching, falls back to diskcache for local caching.

    Args:
        key: Cache key
        ttl: Time to live in seconds (default: 1 hour)

    Returns:
        Cached value or None
    """
    # Try Redis first (distributed cache)
    redis_client = _get_redis_client()
    if redis_client:
        try:
            value = redis_client.get(key)
            if value:
                # Try msgpack for faster deserialization
                if MSGPACK_AVAILABLE and msgpack:
                    try:
                        return msgpack.unpackb(
                            value.encode() if isinstance(value, str) else value, raw=False
                        )
                    except Exception:
                        pass
                # Try orjson for faster JSON deserialization
                if ORJSON_AVAILABLE and orjson:
                    try:
                        return orjson.loads(value.encode() if isinstance(value, str) else value)
                    except Exception:
                        pass
                # Fallback to standard JSON
                return json.loads(value)
        except Exception as e:
            logger.debug(f"Redis get failed: {e}")

    # Fallback to diskcache (local persistent cache)
    if DISKCACHE_AVAILABLE and diskcache:
        try:
            cache_dir = Path.home() / ".cache" / "gam-deepagents-mcp-v3"
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache = diskcache.Cache(str(cache_dir), size_limit=100 * 1024 * 1024)  # 100MB limit
            if key in cache:
                return cache[key]
        except Exception as e:
            logger.debug(f"Diskcache get failed: {e}")

    return None


async def _set_cached_result(key: str, value: Any, ttl: int = 3600) -> bool:
    """Set cached result in Redis or diskcache.

    Uses Redis for distributed caching, falls back to diskcache for local caching.

    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds (default: 1 hour)

    Returns:
        True if successful, False otherwise
    """
    # Try Redis first (distributed cache)
    redis_client = _get_redis_client()
    if redis_client:
        try:
            # Try msgpack for faster serialization
            if MSGPACK_AVAILABLE and msgpack:
                try:
                    value_packed = msgpack.packb(value, use_bin_type=True)
                    redis_client.setex(key, ttl, value_packed)
                    return True
                except Exception:
                    pass
            # Try orjson for faster JSON serialization
            if ORJSON_AVAILABLE and orjson:
                try:
                    value_json = orjson.dumps(value).decode()
                    redis_client.setex(key, ttl, value_json)
                    return True
                except Exception:
                    pass
            # Fallback to standard JSON
            value_json = json.dumps(value)
            redis_client.setex(key, ttl, value_json)
            return True
        except Exception as e:
            logger.debug(f"Redis set failed: {e}")

    # Fallback to diskcache (local persistent cache)
    if DISKCACHE_AVAILABLE and diskcache:
        try:
            cache_dir = Path.home() / ".cache" / "gam-deepagents-mcp-v3"
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache = diskcache.Cache(str(cache_dir), size_limit=100 * 1024 * 1024)  # 100MB limit
            cache.set(key, value, expire=ttl)
            return True
        except Exception as e:
            logger.debug(f"Diskcache set failed: {e}")

    return False


def _count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken.

    Args:
        text: Text to count tokens for

    Returns:
        Number of tokens
    """
    if not TIKTOKEN_AVAILABLE or not tiktoken:
        # Fallback: approximate token count (4 chars per token)
        return len(text) // 4

    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        # Fallback: approximate token count
        return len(text) // 4


# MCP Server
# Initialize FastMCP early so it can respond to handshake immediately
mcp = FastMCP("gam-deepagents-v3", json_response=True)


@mcp.tool()
async def create_agent_with_gam(
    agent_name: str,
    description: str,
    system_prompt: str | None = None,  # noqa: UP007
) -> dict[str, Any]:
    """Create a new DeepAgent with GAM memory capabilities.

    Args:
        agent_name: Name for the agent
        description: What the agent should do
        system_prompt: Optional custom system prompt

    Returns:
        dict with agent_id and status
    """
    try:
        core = _get_core()
        return await core.create_agent(agent_name, description, system_prompt)
    except Exception as e:
        logger.error(
            f"create_agent_with_gam failed for agent '{agent_name}': {e}",
            exc_info=True,  # Include full traceback for debugging
        )
        return {
            "success": False,
            "error": str(e),
            "agent_name": agent_name,
        }


@mcp.tool()
async def memorize_content(content: str) -> dict[str, Any]:
    """Memorize content using GAM MemoryAgent.memorize().

    Args:
        content: Content to memorize

    Returns:
        dict with success status
    """
    try:
        if not content or not content.strip():
            return {
                "success": False,
                "error": "Content cannot be empty",
            }
        core = _get_core()
        return await core.memorize(content)
    except Exception as e:
        logger.error(
            f"memorize_content failed (content length: {len(content)}): {e}",
            exc_info=True,
        )
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
async def research_memory(query: str) -> dict[str, Any]:
    """Research from memory using GAM ResearchAgent.research().

    Args:
        query: Research query

    Returns:
        dict with research results
    """
    try:
        if not query or not query.strip():
            return {
                "success": False,
                "error": "Query cannot be empty",
            }
        core = _get_core()
        return await core.research(query)
    except Exception as e:
        logger.error(
            f"research_memory failed (query: '{query[:100]}...'): {e}",
            exc_info=True,
        )
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
async def run_agent_with_gam(
    task: str,
    agent_name: str | None = None,  # noqa: UP007
    use_cache: bool = True,
) -> dict[str, Any]:
    """Run DeepAgent task with GAM memory integration.

    Enhanced with:
    - Redis caching for repeated tasks
    - MLflow tracking for experiment monitoring

    Args:
        task: Task description
        agent_name: Optional agent name
        use_cache: Use Redis cache for repeated tasks (default: True)

    Returns:
        dict with agent response
    """
    try:
        if not task or not task.strip():
            return {
                "success": False,
                "error": "Task cannot be empty",
                "error_type": "validation_error",
            }

        # Check cache if enabled
        if use_cache:
            cache_key = _cache_key("run_agent", task, agent_name or "default")
            cached_result = await _get_cached_result(cache_key, ttl=3600)
            if cached_result:
                logger.debug(f"Cache hit for task: {task[:50]}...")
                return cached_result

        core = _get_core()
        result = await core.run_agent(task, agent_name)

        # Cache result if successful
        if use_cache and result.get("success"):
            await _set_cached_result(cache_key, result, ttl=3600)

        # Track with MLflow if available
        if MLFLOW_AVAILABLE and mlflow is not None:
            try:
                mlflow.log_metric("run_agent_success", 1.0 if result.get("success") else 0.0)
                if "latency_ms" in result:
                    mlflow.log_metric("run_agent_latency_ms", result["latency_ms"])
                # Track token usage if available
                if "response" in result and TIKTOKEN_AVAILABLE:
                    token_count = _count_tokens(result["response"])
                    mlflow.log_metric("run_agent_tokens", float(token_count))
            except Exception as e:
                logger.debug(f"MLflow tracking failed: {e}")

        # Add token count to result if tiktoken available
        if TIKTOKEN_AVAILABLE and "response" in result:
            result["token_count"] = _count_tokens(result["response"])

        return result
    except ValueError as e:
        logger.error(f"run_agent_with_gam validation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
        }
    except Exception as e:
        logger.error(
            f"run_agent_with_gam failed (agent: {agent_name}, task length: {len(task)}): {e}",
            exc_info=True,
        )
        return {
            "success": False,
            "error": str(e),
            "error_type": "execution_error",
        }


@mcp.tool()
async def run_agent_stream(
    task: str,
    agent_name: str | None = None,  # noqa: UP007
) -> dict[str, Any]:
    """Run DeepAgent task with streaming support (collects stream and returns result).

    Enhanced with Claude features:
    - Token-efficient result handling (selective metrics)
    - Early return optimizations
    - Better error categorization

    Note: For true streaming, use the core method directly in Python code.
    This MCP tool collects the stream and returns the complete result.

    Args:
        task: Task description
        agent_name: Optional agent name

    Returns:
        dict with complete streaming result:
            - success: bool - Whether streaming succeeded
            - response: str - Complete accumulated response
            - tokens_so_far: int - Total tokens generated
            - elapsed_ms: float - Total elapsed time
            - first_token_latency_ms: float - Time to first token
            - tokens_per_second: float - Generation rate
    """
    try:
        # Input validation with early return
        if not task or not task.strip():
            return {
                "success": False,
                "error": "Task cannot be empty",
                "error_type": "validation_error",
            }
        core = _get_core()

        # Collect stream with token-efficient pattern
        accumulated = ""
        tokens_so_far = 0
        elapsed_ms = 0.0
        first_token_latency_ms = None
        tokens_per_second = 0.0

        async for chunk in core.run_agent_stream(task, agent_name):
            # Early return optimization: skip empty chunks
            if not chunk.get("chunk"):
                if chunk.get("done"):
                    break
                continue

            accumulated += chunk["chunk"]
            # Token-efficient: only update metrics when available
            if "tokens_so_far" in chunk:
                tokens_so_far = chunk["tokens_so_far"]
            if "elapsed_ms" in chunk:
                elapsed_ms = chunk["elapsed_ms"]
            if first_token_latency_ms is None and "first_token_latency_ms" in chunk:
                first_token_latency_ms = chunk["first_token_latency_ms"]
            if "tokens_per_second" in chunk:
                tokens_per_second = chunk["tokens_per_second"]

            if chunk.get("done"):
                break

        return {
            "success": True,
            "response": accumulated,
            "tokens_so_far": tokens_so_far,
            "elapsed_ms": elapsed_ms,
            "first_token_latency_ms": first_token_latency_ms,
            "tokens_per_second": tokens_per_second,
        }
    except ValueError as e:
        logger.error(f"run_agent_stream validation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
        }
    except Exception as e:
        logger.error(f"run_agent_stream failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "error_type": "execution_error",
        }


@mcp.tool()
async def generate_code_stream(
    task: str,
    language: str = "python",
    agent_name: str | None = None,  # noqa: UP007
    use_structured_output: bool = False,
) -> dict[str, Any]:
    """Generate code with streaming support (collects stream and returns result).

    Enhanced with Claude features:
    - Structured outputs (JSON/Pydantic) for better code quality
    - Token-efficient result handling (selective metrics, early returns)
    - Better package utilization from pyproject.toml
    - Enhanced error categorization

    Note: For true streaming, use the core method directly in Python code.
    This MCP tool collects the stream and returns the complete result.

    Args:
        task: Code generation task description
        language: Programming language (default: python)
        agent_name: Optional agent name
        use_structured_output: Use structured output format (default: False)

    Returns:
        dict with complete code generation result:
            - success: bool - Whether generation succeeded
            - code: str - Complete generated code
            - language: str - Programming language
            - tokens_so_far: int - Total tokens generated
            - elapsed_ms: float - Total elapsed time
            - first_token_latency_ms: float - Time to first token
            - tokens_per_second: float - Generation rate
    """
    try:
        # Input validation with early return
        if not task or not task.strip():
            return {
                "success": False,
                "error": "Task cannot be empty",
                "error_type": "validation_error",
            }
        core = _get_core()

        # Collect stream with token-efficient pattern
        accumulated_code = ""
        tokens_so_far = 0
        elapsed_ms = 0.0
        first_token_latency_ms = None
        tokens_per_second = 0.0

        async for chunk in core.generate_code_stream(
            task, language, agent_name, None, use_structured_output
        ):
            # Early return optimization: skip empty chunks
            if not chunk.get("code_chunk"):
                if chunk.get("done"):
                    break
                continue

            accumulated_code += chunk["code_chunk"]
            # Token-efficient: only update metrics when available
            if "tokens_so_far" in chunk:
                tokens_so_far = chunk["tokens_so_far"]
            if "elapsed_ms" in chunk:
                elapsed_ms = chunk["elapsed_ms"]
            if first_token_latency_ms is None and "first_token_latency_ms" in chunk:
                first_token_latency_ms = chunk["first_token_latency_ms"]
            if "tokens_per_second" in chunk:
                tokens_per_second = chunk["tokens_per_second"]

            if chunk.get("done"):
                break

        return {
            "success": True,
            "code": accumulated_code,
            "language": language,
            "tokens_so_far": tokens_so_far,
            "elapsed_ms": elapsed_ms,
            "first_token_latency_ms": first_token_latency_ms,
            "tokens_per_second": tokens_per_second,
        }
    except ValueError as e:
        logger.error(f"generate_code_stream validation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
        }
    except Exception as e:
        logger.error(f"generate_code_stream failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "error_type": "execution_error",
        }


@mcp.tool()
async def generate_code_batch(
    tasks: list[str],
    language: str = "python",
    agent_name: str | None = None,  # noqa: UP007
    max_concurrent: int = 5,
) -> dict[str, Any]:
    """Generate multiple code features in parallel (Claude batch processing feature).

    Processes multiple code generation tasks in parallel for 5-20x speedup.
    Uses asyncio.gather() for concurrent execution.

    Enhanced with Claude features:
    - Better async/await patterns
    - Token-efficient result aggregation
    - Enhanced error handling with partial success support

    Args:
        tasks: List of code generation task descriptions
        language: Programming language (default: python)
        agent_name: Optional agent name
        max_concurrent: Maximum concurrent operations (default: 5)

    Returns:
        dict with batch generation results:
            - success: bool - Whether batch generation succeeded (true if any task succeeded)
            - results: list[dict] - List of code generation results
            - total_tasks: int - Total number of tasks
            - successful_tasks: int - Number of successful tasks
            - failed_tasks: int - Number of failed tasks
            - total_elapsed_ms: float - Total elapsed time
            - avg_latency_ms: float - Average latency per task
    """
    try:
        # Input validation with early return
        if not tasks:
            return {
                "success": False,
                "error": "Tasks list cannot be empty",
                "error_type": "validation_error",
            }
        if not all(isinstance(task, str) and task.strip() for task in tasks):
            return {
                "success": False,
                "error": "All tasks must be non-empty strings",
                "error_type": "validation_error",
            }
        if max_concurrent < 1:
            return {
                "success": False,
                "error": "max_concurrent must be >= 1",
                "error_type": "validation_error",
            }

        core = _get_core()

        # Batch processing with timing
        start_time = time.perf_counter()
        results = await core.generate_code_batch(tasks, language, agent_name, max_concurrent)
        total_elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Token-efficient: aggregate only necessary metrics
        successful_tasks = sum(1 for r in results if r.get("success", False))
        failed_tasks = len(results) - successful_tasks
        total_latency = sum(r.get("elapsed_ms", 0) for r in results if r.get("success", False))
        avg_latency_ms = total_latency / successful_tasks if successful_tasks > 0 else 0

        logger.info(
            f"generate_code_batch completed: {len(results)} tasks, "
            f"{successful_tasks} successful, {failed_tasks} failed, "
            f"{total_elapsed_ms:.2f}ms total, {avg_latency_ms:.2f}ms avg"
        )

        # Partial success is acceptable for batch operations
        return {
            "success": successful_tasks > 0,  # True if any task succeeded
            "results": results,
            "total_tasks": len(tasks),
            "successful_tasks": successful_tasks,
            "failed_tasks": failed_tasks,
            "total_elapsed_ms": total_elapsed_ms,
            "avg_latency_ms": avg_latency_ms,
        }
    except ValueError as e:
        logger.error(f"generate_code_batch validation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
        }
    except Exception as e:
        logger.error(f"generate_code_batch failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "error_type": "execution_error",
        }


if __name__ == "__main__":
    # Use uvloop for faster event loop if available (2-4x faster on Linux)
    if UVLOOP_AVAILABLE and uvloop:
        try:
            uvloop.install()
            logger.info("Using uvloop for faster event loop (2-4x performance boost)")
        except Exception:
            logger.debug("uvloop installation failed, using default asyncio")
    mcp.run(transport="stdio")
