#!/usr/bin/env python3
"""
MCP Server Template.

This script provides a generalizable template for creating a FastMCP server.
It features:
- Pluggable core logic via a BaseCore interface.
- Dynamic tool registration based on the core's public methods.
- Type-safe configuration using pydantic-settings.
- Optional integrations for caching (Redis, diskcache), and performance (uvloop, etc.).
"""

import hashlib
import importlib
import inspect
import json
import logging
from functools import wraps
from pathlib import Path
from typing import Any

# Optional integrations
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    mlflow = None

try:
    from opentelemetry import trace
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    trace = None

try:
    import uvloop
    UVLOOP_AVAILABLE = True
except ImportError:
    UVLOOP_AVAILABLE = False
    uvloop = None

try:
    import msgpack
    MSGPACK_AVAILABLE = True
except ImportError:
    MSGPACK_AVAILABLE = False
    msgpack = None

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

try:
    import orjson
    ORJSON_AVAILABLE = True
except ImportError:
    ORJSON_AVAILABLE = False
    orjson = None

try:
    import nest_asyncio
    NEST_ASYNCIO_AVAILABLE = True
except ImportError:
    NEST_ASYNCIO_AVAILABLE = False
    nest_asyncio = None

# Local imports
from .base_core import BaseCore
from .settings import get_settings

# Strict MCP import
try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise ImportError(f"FastMCP is required: {e}. Install with: uv add fastmcp") from e


# Initialize logger
logger = logging.getLogger("mcp-server-template")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

if NEST_ASYNCIO_AVAILABLE and nest_asyncio:
    try:
        nest_asyncio.apply()
        logger.debug("nest_asyncio enabled.")
    except Exception:
        pass

# Lazy core initialization
_core: BaseCore | None = None
_redis_client: Any = None

def _get_core() -> BaseCore:
    """Get or create core instance (lazy initialization and dynamic loading)."""
    global _core
    if _core is None:
        settings = get_settings()
        module_path, class_name = settings.core_class.rsplit('.', 1)
        try:
            module = importlib.import_module(module_path)
            core_class = getattr(module, class_name)
            _core = core_class(settings)
            logger.info(f"Core instance of {settings.core_class} created.")
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load core class '{settings.core_class}': {e}")
            raise
    return _core

def _get_redis_client() -> Any:
    """Get or create Redis client."""
    global _redis_client
    if not REDIS_AVAILABLE:
        return None
    if _redis_client is None:
        try:
            redis_url = get_settings().docker_redis_url
            _redis_client = redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=2)
            _redis_client.ping()
            logger.info(f"Redis cache connected: {redis_url}")
        except Exception as e:
            logger.warning(f"Redis not available: {e}, using local cache only")
            _redis_client = None
    return _redis_client


def _cache_key(prefix: str, *args: Any) -> str:
    key_parts = [prefix] + [str(arg) for arg in args]
    key_str = ":".join(key_parts)
    return hashlib.md5(key_str.encode()).hexdigest()

async def _get_cached_result(key: str, ttl: int = 3600) -> Any:
    """Get cached result from Redis or diskcache."""
    redis_client = _get_redis_client()
    if redis_client:
        try:
            value = redis_client.get(key)
            if value:
                return (orjson or json).loads(value)
        except Exception as e:
            logger.debug(f"Redis get failed: {e}")

    if DISKCACHE_AVAILABLE and diskcache:
        try:
            cache_dir = Path.home() / ".cache" / "mcp-server-template"
            cache_dir.mkdir(parents=True, exist_ok=True)
            with diskcache.Cache(str(cache_dir)) as cache:
                return cache.get(key)
        except Exception as e:
            logger.debug(f"Diskcache get failed: {e}")
    return None

async def _set_cached_result(key: str, value: Any, ttl: int = 3600) -> bool:
    """Set cached result in Redis or diskcache."""
    redis_client = _get_redis_client()
    if redis_client:
        try:
            value_json = (orjson or json).dumps(value)
            redis_client.setex(key, ttl, value_json)
            return True
        except Exception as e:
            logger.debug(f"Redis set failed: {e}")

    if DISKCACHE_AVAILABLE and diskcache:
        try:
            cache_dir = Path.home() / ".cache" / "mcp-server-template"
            cache_dir.mkdir(parents=True, exist_ok=True)
            with diskcache.Cache(str(cache_dir)) as cache:
                cache.set(key, value, expire=ttl)
            return True
        except Exception as e:
            logger.debug(f"Diskcache set failed: {e}")
    return False

def _count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    if not TIKTOKEN_AVAILABLE or not tiktoken:
        return len(text) // 4
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4

# Initialize FastMCP
mcp = FastMCP("mcp-server-template", json_response=True)

def register_core_tools(mcp_instance: FastMCP, core_instance: BaseCore):
    """Dynamically registers public methods of the core instance as MCP tools."""
    for name, method in inspect.getmembers(core_instance, predicate=inspect.iscoroutinefunction):
        if not name.startswith("_"):

            @wraps(method)
            async def tool_wrapper(*args, **kwargs):
                try:
                    return await method(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error executing tool '{name}': {e}", exc_info=True)
                    return {"success": False, "error": str(e), "error_type": "execution_error"}

            # Register the wrapped method as an MCP tool
            mcp_instance.tool(name=name)(tool_wrapper)
            logger.info(f"Registered tool: {name}")

# Initialize and register tools
core = _get_core()
register_core_tools(mcp, core)

if __name__ == "__main__":
    if UVLOOP_AVAILABLE and uvloop:
        try:
            uvloop.install()
            logger.info("Using uvloop for faster event loop.")
        except Exception:
            logger.debug("uvloop installation failed, using default asyncio.")

    mcp.run(transport="stdio")
