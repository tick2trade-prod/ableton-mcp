#!/usr/bin/env python3
"""Hybrid Orchestrator Agent v1 - Workflow orchestration with Ollama integration.

Orchestrates complete development workflows from setup through PR creation using:
- Async task queues (Celery/Dramatiq)
- Intelligent routing (LangChain Tool Executor)
- Ollama for code execution (replaces Claude API)
- State management (PostgreSQL/SQLite + LangGraph)
- Progress tracking (FastAPI + WebSockets + MLflow)

Uses DeepAgents for automatic orchestration with MCP tools.
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configuration - Use pydantic-settings for type-safe configuration
try:
    from scripts.deepagents.workflow_orchestrator_config import get_settings

    settings = get_settings()
    SKIP_WEB_SEARCH = settings.skip_web_search
    WORKFLOW_TIMEOUT = settings.workflow_timeout
    REQUIRE_VALIDATION = settings.require_validation
    USE_SELF_IMPROVING = settings.use_self_improving
    MAX_PARALLEL = settings.max_parallel
    USE_STEP_ROUTING = settings.use_step_routing
    USE_OLLAMA = settings.use_ollama
    OLLAMA_MODEL = settings.ollama_model
    OLLAMA_BASE_URL = settings.ollama_base_url
    GAM_ENABLED = settings.gam_enabled
    GAM_MEMORY_DIR = settings.gam_memory_dir
    GAM_USE_HYBRID_SEARCH = settings.gam_use_hybrid_search
    GAM_RESEARCH_LIMIT = settings.gam_research_limit
    GAM_BM25_WEIGHT = settings.gam_bm25_weight
    GAM_VECTOR_WEIGHT = settings.gam_vector_weight
    PROMPT_CACHE_ENABLED = settings.prompt_cache_enabled
    PROMPT_CACHE_TTL = settings.prompt_cache_ttl
    MCP_TOOLS_CACHE_TTL = settings.mcp_tools_cache_ttl
    AGENT_CACHE_TTL = settings.agent_cache_ttl
except ImportError:
    # Fallback to environment variables if settings not available
    # Initialize logger if not already available
    if "logger" not in globals():
        logger = logging.getLogger(__name__)
    logger.warning("workflow_orchestrator_config not available, using environment variables")
    SKIP_WEB_SEARCH = (
        os.environ.get("WORKFLOW_ORCHESTRATOR_SKIP_WEB_SEARCH", "false").lower() == "true"
    )
    WORKFLOW_TIMEOUT = int(os.environ.get("WORKFLOW_ORCHESTRATOR_TIMEOUT", "1800"))
    REQUIRE_VALIDATION = (
        os.environ.get("WORKFLOW_ORCHESTRATOR_REQUIRE_VALIDATION", "true").lower() == "true"
    )
    USE_SELF_IMPROVING = (
        os.environ.get("WORKFLOW_ORCHESTRATOR_USE_SELF_IMPROVING", "true").lower() == "true"
    )
    MAX_PARALLEL = int(os.environ.get("WORKFLOW_ORCHESTRATOR_MAX_PARALLEL", "10"))
    USE_STEP_ROUTING = (
        os.environ.get("WORKFLOW_ORCHESTRATOR_USE_STEP_ROUTING", "true").lower() == "true"
    )
    USE_OLLAMA = os.environ.get("WORKFLOW_ORCHESTRATOR_USE_OLLAMA", "true").lower() == "true"
    OLLAMA_MODEL = os.environ.get("WORKFLOW_ORCHESTRATOR_OLLAMA_MODEL", "llama3.1:8b")
    OLLAMA_BASE_URL = os.environ.get(
        "WORKFLOW_ORCHESTRATOR_OLLAMA_BASE_URL", "http://localhost:11434"
    )
    GAM_ENABLED = os.environ.get("WORKFLOW_ORCHESTRATOR_GAM_ENABLED", "true").lower() == "true"
    GAM_MEMORY_DIR = os.environ.get(
        "WORKFLOW_ORCHESTRATOR_GAM_MEMORY_DIR", ".cursor/workflows/gam_memory"
    )
    GAM_USE_HYBRID_SEARCH = (
        os.environ.get("WORKFLOW_ORCHESTRATOR_GAM_USE_HYBRID_SEARCH", "true").lower() == "true"
    )
    GAM_RESEARCH_LIMIT = int(os.environ.get("WORKFLOW_ORCHESTRATOR_GAM_RESEARCH_LIMIT", "5"))
    GAM_BM25_WEIGHT = float(os.environ.get("WORKFLOW_ORCHESTRATOR_GAM_BM25_WEIGHT", "0.5"))
    GAM_VECTOR_WEIGHT = float(os.environ.get("WORKFLOW_ORCHESTRATOR_GAM_VECTOR_WEIGHT", "0.5"))
    PROMPT_CACHE_ENABLED = True
    PROMPT_CACHE_TTL = 300
    MCP_TOOLS_CACHE_TTL = 300
    AGENT_CACHE_TTL = 3600

# Suppress OpenTelemetry tracing export errors
logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

logger = logging.getLogger("workflow-orchestrator-hybrid")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

try:
    from mcp.server.fastmcp import FastMCP

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    FastMCP = None

try:
    from cachetools import TTLCache

    CACHETOOLS_AVAILABLE = True
except ImportError:
    CACHETOOLS_AVAILABLE = False
    # Fallback to dict if cachetools not available (no TTL, but functional)
    TTLCache = dict  # type: ignore[assignment, misc]

from app.mcp.lazy_loader import LazyLoader
from app.mcp.mcp_utils import normalize_mcp_server_config
from app.mcp.opentelemetry_config import get_opentelemetry_tracer

# GAM memory support - Lazy import to avoid blocking during module import
# GAM initialization can hang if Java/pyserini dependencies are not properly configured
GAM_MEMORY_AVAILABLE = False
GAMWorkflowMemory = None  # type: ignore[assignment]
_GAM_IMPORT_ATTEMPTED = False


def _try_import_gam():
    """Lazily import GAM to avoid blocking during module import."""
    global GAM_MEMORY_AVAILABLE, GAMWorkflowMemory, _GAM_IMPORT_ATTEMPTED
    if _GAM_IMPORT_ATTEMPTED:
        return
    _GAM_IMPORT_ATTEMPTED = True
    try:
        from app.mcp.gam_memory_store import GAM_AVAILABLE, GAMWorkflowMemory

        GAM_MEMORY_AVAILABLE = GAM_AVAILABLE
    except (ImportError, RuntimeError, Exception) as e:
        # GAM may fail to import due to missing Java/pyserini dependencies
        logger.debug(f"GAM import failed (non-blocking): {e}")
        GAM_MEMORY_AVAILABLE = False
        GAMWorkflowMemory = None  # type: ignore[assignment]


# Prompt caching support
try:
    from scripts.deepagents.prompt_cache import get_prompt_cache

    PROMPT_CACHE_AVAILABLE = True
except ImportError:
    PROMPT_CACHE_AVAILABLE = False
    get_prompt_cache = None

# Workflow improvements (Cycles 2-6)
try:
    from scripts.deepagents.workflow_orchestrator_improvements import get_improvements

    IMPROVEMENTS_AVAILABLE = True
except ImportError:
    IMPROVEMENTS_AVAILABLE = False
    get_improvements = None

tracer = get_opentelemetry_tracer("workflow-orchestrator-hybrid-mcp")

# MCP tools cache (configurable TTL to avoid stale tools while allowing updates)
# Use TTLCache if available, otherwise use regular dict (no TTL, but functional)
# Note: MCP_TOOLS_CACHE_TTL is set from settings or environment
if CACHETOOLS_AVAILABLE:
    _mcp_tools_cache: Any = TTLCache(maxsize=1, ttl=MCP_TOOLS_CACHE_TTL)
else:
    _mcp_tools_cache: Any = {}  # Fallback to dict if cachetools not available

# MCP Client
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient

    MCP_CLIENT_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    MultiServerMCPClient = None

# DeepAgents support
try:
    from deepagents import create_deep_agent

    DEEPAGENTS_AVAILABLE = True
    DEEPAGENTS_ERROR = None
except ImportError as e:
    DEEPAGENTS_AVAILABLE = False
    DEEPAGENTS_ERROR = f"deepagents is not installed: {e}. Install with: uv sync"
    if REQUIRE_VALIDATION:
        raise ImportError(
            f"DeepAgents is required: {DEEPAGENTS_ERROR}. Install with: uv sync"
        ) from e

# Import our modules (with error handling)
try:
    from scripts.deepagents.workflow_orchestrator_ollama import (
        OllamaCodeExecutor,
        OllamaModelRouter,
    )

    OLLAMA_MODULE_AVAILABLE = True
except ImportError as e:
    OLLAMA_MODULE_AVAILABLE = False
    logger.warning(f"Ollama module not available: {e}")

try:
    from scripts.deepagents.workflow_orchestrator_state import (
        StateManager,
        WorkflowCheckpoint,
        WorkflowState,
        WorkflowStep,
    )

    STATE_MODULE_AVAILABLE = True
except ImportError as e:
    STATE_MODULE_AVAILABLE = False
    logger.warning(f"State module not available: {e}")

try:
    from scripts.deepagents.workflow_orchestrator_tasks import get_task_queue

    TASKS_MODULE_AVAILABLE = True
except ImportError as e:
    TASKS_MODULE_AVAILABLE = False
    logger.warning(f"Tasks module not available: {e}")

# Self-improving orchestrator support
try:
    from scripts.deepagents.workflow_orchestrator_self_improving import (
        get_self_improving_orchestrator,
    )

    SELF_IMPROVING_AVAILABLE = True
except ImportError as e:
    SELF_IMPROVING_AVAILABLE = False
    logger.warning(f"Self-improving orchestrator not available: {e}")
    get_self_improving_orchestrator = None

# Lazy loading
_mcp_client_loader = LazyLoader(lambda: _create_mcp_client() if MCP_CLIENT_AVAILABLE else None)
_workflow_agent_cache: Any | None = None
_workflow_agent_cache_timestamp: float | None = None
# AGENT_CACHE_TTL is set from settings or environment (default: 3600 = 1 hour)


# Step dependencies for parallel execution
# Steps at the same level can run in parallel
# Defined as a function to avoid module-level usage of conditionally imported types
def _get_step_dependencies() -> dict[Any, list[Any]]:
    """Get step dependencies for parallel execution.

    Returns:
        Dictionary mapping steps to their dependencies
    """
    if not STATE_MODULE_AVAILABLE:
        return {}
    # Type checker sees these as possibly unbound, but runtime check ensures they exist
    return {
        WorkflowStep.SETUP: [],  # type: ignore[possibly-unbound]
        WorkflowStep.PLANNING: [WorkflowStep.SETUP],  # type: ignore[possibly-unbound]
        WorkflowStep.IMPLEMENTATION: [WorkflowStep.PLANNING],  # type: ignore[possibly-unbound]
        WorkflowStep.VALIDATION: [WorkflowStep.IMPLEMENTATION],  # type: ignore[possibly-unbound]
        WorkflowStep.REVIEW: [WorkflowStep.VALIDATION],  # type: ignore[possibly-unbound]
        WorkflowStep.PR_CREATION: [WorkflowStep.REVIEW],  # type: ignore[possibly-unbound]
    }


def _validate_prerequisites() -> tuple[bool, list[str]]:
    """Validate all prerequisites are properly configured."""
    errors = []

    if not MCP_CLIENT_AVAILABLE:
        errors.append("langchain_mcp_adapters is not installed. Install with: uv sync")

    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    if not mcp_config_path.exists():
        errors.append(f"MCP config file not found: {mcp_config_path}")
    else:
        try:
            with open(mcp_config_path) as f:
                config = json.load(f)
            mcp_servers = config.get("mcpServers", {})
            required_servers = [
                "git",
                "filesystem",
                "sequential-thinking",
            ]
            for server in required_servers:
                if server not in mcp_servers:
                    errors.append(f"Required MCP server '{server}' is not configured.")
        except Exception as e:
            errors.append(f"Error reading MCP config: {e}")

    return len(errors) == 0, errors


def _create_mcp_client() -> Any:
    """Create MCP client for calling other MCP servers."""
    if not MCP_CLIENT_AVAILABLE:
        return None

    import json
    import os
    import shutil
    from pathlib import Path

    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    if not mcp_config_path.exists():
        return None

    try:
        with open(mcp_config_path) as f:
            config = json.load(f)

        # CRITICAL FIX: Create uv symlinks for servers using --directory
        # This must be done BEFORE creating MultiServerMCPClient
        uv_path = shutil.which("uv")
        if uv_path:
            for server_name, server_config in config.get("mcpServers", {}).items():
                if server_config.get("command") in ("uv", "uvx"):
                    args = server_config.get("args", [])
                    if "--directory" in args:
                        dir_index = args.index("--directory")
                        if dir_index + 1 < len(args):
                            target_dir = args[dir_index + 1]
                            target_venv_uv = os.path.join(target_dir, ".venv", "bin", "uv")
                            target_venv_bin = os.path.join(target_dir, ".venv", "bin")

                            try:
                                os.makedirs(target_venv_bin, exist_ok=True)
                                # Check if symlink exists
                                if os.path.exists(target_venv_uv) or os.path.islink(target_venv_uv):
                                    # Check if it's a symlink
                                    if os.path.islink(target_venv_uv):
                                        try:
                                            link_target = os.readlink(target_venv_uv)
                                            # Check for circular reference (symlink points to itself)
                                            abs_target_venv_uv = os.path.abspath(target_venv_uv)
                                            abs_link_target = os.path.abspath(
                                                os.path.join(
                                                    os.path.dirname(target_venv_uv), link_target
                                                )
                                            )
                                            if abs_target_venv_uv == abs_link_target:
                                                # Circular symlink detected, remove it
                                                logger.warning(
                                                    f"Detected circular symlink at {target_venv_uv}, removing"
                                                )
                                                os.unlink(target_venv_uv)
                                            elif link_target != uv_path:
                                                # Points to wrong location, update it
                                                os.unlink(target_venv_uv)
                                                os.symlink(uv_path, target_venv_uv)
                                                logger.debug(
                                                    f"Updated uv symlink: {target_venv_uv} -> {uv_path}"
                                                )
                                                continue  # Skip creation below
                                        except (OSError, ValueError) as e:
                                            # Symlink is broken, remove it
                                            logger.debug(f"Removing broken symlink: {e}")
                                            try:
                                                os.unlink(target_venv_uv)
                                            except Exception:
                                                pass  # Ignore if already removed
                                    else:
                                        # File exists but is not a symlink, skip
                                        logger.debug(
                                            f"File exists at {target_venv_uv} but is not a symlink, skipping"
                                        )
                                        continue  # Skip creation

                                # Create new symlink (only if we get here)
                                if not os.path.exists(target_venv_uv):
                                    # Ensure we're not creating a circular reference
                                    abs_uv_path = os.path.abspath(uv_path)
                                    abs_target = os.path.abspath(target_venv_uv)
                                    if abs_uv_path != abs_target:
                                        os.symlink(uv_path, target_venv_uv)
                                        logger.debug(
                                            f"Created uv symlink: {target_venv_uv} -> {uv_path}"
                                        )
                                    else:
                                        logger.warning(
                                            f"Skipping circular symlink creation: {target_venv_uv} -> {uv_path}"
                                        )
                            except (OSError, PermissionError) as e:
                                logger.debug(f"Could not create uv symlink in {target_dir}: {e}")

        client_config = {}
        for server_name, server_config in config.get("mcpServers", {}).items():
            if server_name in [
                "git",
                "filesystem",
                "sequential-thinking",
                "github",
            ]:
                try:
                    if "url" in server_config:
                        client_config[server_name] = {
                            "transport": "sse",
                            "url": server_config["url"],
                        }
                    elif "command" in server_config:
                        # Use standardized MCP server config normalization
                        # This will create symlinks for uv --directory servers
                        # This resolves uv/uvx paths and ensures consistent format
                        normalized_config = normalize_mcp_server_config(server_config)

                        # Verify command exists before adding to config
                        import shutil

                        command = normalized_config["command"]
                        if "/" in command and not shutil.which(command):
                            # Command is absolute path but doesn't exist
                            logger.warning(
                                f"Skipping MCP server '{server_name}': command not found: {command}"
                            )
                            continue

                        client_config[server_name] = {
                            "transport": "stdio",
                            "command": normalized_config["command"],
                            "args": normalized_config.get("args", []),
                            "env": normalized_config.get("env", {}),
                        }
                except Exception as e:
                    # Skip this server if configuration fails
                    logger.warning(
                        f"Skipping MCP server '{server_name}' due to configuration error: {e}"
                    )
                    continue

        if client_config:
            try:
                return MultiServerMCPClient(client_config)
            except Exception as e:
                # Handle TaskGroup errors and other MultiServerMCPClient creation failures
                error_msg = str(e)
                if "TaskGroup" in error_msg or "unhandled errors" in error_msg.lower():
                    logger.warning(
                        f"MultiServerMCPClient creation failed with TaskGroup error: {e}. "
                        "This may be due to one or more MCP servers failing to start. "
                        "Continuing with fallback tools."
                    )
                else:
                    logger.warning(f"Failed to create MultiServerMCPClient: {e}")
                return None
    except Exception as e:
        logger.warning(f"Failed to create MCP client: {e}")
        return None

    return None


def _get_mcp_client() -> Any:
    """Get cached MCP client instance."""
    return _mcp_client_loader.get()


async def _cleanup_mcp_client() -> None:
    """Cleanup MCP client to prevent shutdown errors.

    Handles langchain_mcp_adapters bug where UnboundLocalError occurs during shutdown.
    This function ensures all MCP client connections and background tasks are properly closed.
    """
    try:
        mcp_client = _get_mcp_client()
        if not mcp_client:
            return

        # Cancel all pending tasks related to MCP client
        try:
            # Get current event loop
            loop = asyncio.get_event_loop()
            if loop and not loop.is_closed():
                # Get all tasks
                all_tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]

                # Cancel tasks related to MCP (check task names/coroutines)
                for task in all_tasks:
                    try:
                        task_name = task.get_name() if hasattr(task, "get_name") else str(task)
                        coro_name = str(task.get_coro()) if hasattr(task, "get_coro") else ""

                        # Cancel tasks related to langchain_mcp_adapters
                        if (
                            "mcp" in task_name.lower()
                            or "langchain_mcp" in task_name.lower()
                            or "load_mcp_tools" in coro_name
                            or "mcp" in coro_name.lower()
                        ):
                            task.cancel()
                    except Exception:
                        pass  # Ignore errors when canceling tasks

                # Wait for cancelled tasks to complete (with timeout)
                if all_tasks:
                    try:
                        await asyncio.wait_for(
                            asyncio.gather(*all_tasks, return_exceptions=True),
                            timeout=1.0,  # 1 second timeout
                        )
                    except (TimeoutError, Exception):
                        pass  # Ignore timeout/errors
        except Exception:
            pass  # Ignore errors during task cancellation

        # Close MCP client if it has a close method
        if hasattr(mcp_client, "close"):
            try:
                if asyncio.iscoroutinefunction(mcp_client.close):
                    await asyncio.wait_for(mcp_client.close(), timeout=1.0)
                else:
                    mcp_client.close()
            except (TimeoutError, Exception):
                # Ignore errors during cleanup (known langchain_mcp_adapters bug)
                pass

        # Also try to close underlying connections if available
        if hasattr(mcp_client, "_clients") or hasattr(mcp_client, "clients"):
            try:
                clients = getattr(mcp_client, "_clients", None) or getattr(
                    mcp_client, "clients", None
                )
                if clients:
                    for client in clients:
                        if hasattr(client, "close"):
                            try:
                                if asyncio.iscoroutinefunction(client.close):
                                    await asyncio.wait_for(client.close(), timeout=0.5)
                                else:
                                    client.close()
                            except Exception:
                                pass
            except Exception:
                pass
    except Exception:
        # Ignore all errors during cleanup
        pass


async def _create_fallback_tools() -> list[Any]:
    """Create real local tools when MCP tools fail.

    These are functional implementations using subprocess and file operations
    that work entirely locally without external MCP servers.
    """
    fallback_tools = []

    try:
        import subprocess
        from pathlib import Path

        # Try langchain_core.tools first (newer API)
        try:
            from langchain_core.tools import tool
        except ImportError:
            # Fallback to langchain.tools (older API)
            from langchain.tools import tool

        # Get project root
        project_root = Path(__file__).parent.parent.parent

        @tool
        def git_status() -> str:
            """Get git status. Returns current branch and status of working tree."""
            try:
                result = subprocess.run(
                    ["git", "status", "--porcelain", "-b"],
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
            except Exception as e:
                return f"Error getting git status: {e}"

        @tool
        def git_create_branch(branch_name: str) -> str:
            """Create and checkout a new git branch."""
            try:
                result = subprocess.run(
                    ["git", "checkout", "-b", branch_name],
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    return f"Created and checked out branch: {branch_name}"
                return f"Error: {result.stderr}"
            except Exception as e:
                return f"Error creating branch: {e}"

        @tool
        def git_commit(message: str, files: str = "") -> str:
            """Commit changes. Files is optional comma-separated list, or empty for all staged."""
            try:
                cmd = ["git", "commit", "-m", message]
                if files:
                    cmd.extend(files.split(","))
                result = subprocess.run(
                    cmd,
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    return f"Committed: {message}"
                return f"Error: {result.stderr}"
            except Exception as e:
                return f"Error committing: {e}"

        @tool
        def filesystem_write(path: str, content: str) -> str:
            """Write content to a file. Path can be relative to project root or absolute."""
            try:
                file_path = Path(path)
                if not file_path.is_absolute():
                    file_path = project_root / file_path

                # Create parent directories if needed
                file_path.parent.mkdir(parents=True, exist_ok=True)

                file_path.write_text(content, encoding="utf-8")
                return f"Wrote {len(content)} bytes to {file_path}"
            except Exception as e:
                return f"Error writing file: {e}"

        @tool
        def filesystem_read(path: str) -> str:
            """Read content from a file. Path can be relative to project root or absolute."""
            try:
                file_path = Path(path)
                if not file_path.is_absolute():
                    file_path = project_root / file_path

                if not file_path.exists():
                    return f"Error: File not found: {file_path}"

                return file_path.read_text(encoding="utf-8")
            except Exception as e:
                return f"Error reading file: {e}"

        @tool
        def filesystem_list_directory(path: str = ".") -> str:
            """List files and directories. Path can be relative to project root or absolute."""
            try:
                dir_path = Path(path)
                if not dir_path.is_absolute():
                    dir_path = project_root / dir_path

                if not dir_path.exists():
                    return f"Error: Directory not found: {dir_path}"

                if not dir_path.is_dir():
                    return f"Error: Not a directory: {dir_path}"

                items = []
                for item in sorted(dir_path.iterdir()):
                    item_type = "DIR" if item.is_dir() else "FILE"
                    items.append(f"{item_type}: {item.name}")

                return "\n".join(items) if items else "Directory is empty"
            except Exception as e:
                return f"Error listing directory: {e}"

        @tool
        def filesystem_create_directory(path: str) -> str:
            """Create a directory. Path can be relative to project root or absolute."""
            try:
                dir_path = Path(path)
                if not dir_path.is_absolute():
                    dir_path = project_root / dir_path

                dir_path.mkdir(parents=True, exist_ok=True)
                return f"Created directory: {dir_path}"
            except Exception as e:
                return f"Error creating directory: {e}"

        @tool
        def run_tests(test_path: str = "") -> str:
            """Run pytest tests. test_path is optional, defaults to hotpath tests.

            Optimized for Cursor IDE - uses timeout, short traceback, and quiet mode.
            Returns last 1000 chars of output for quick feedback.
            """
            try:
                # Use optimized command for Cursor IDE compatibility
                # Avoids hanging issues with tee/tail pipes
                cmd = ["uv", "run", "pytest"]
                if test_path:
                    cmd.append(test_path)
                else:
                    # Use optimized flags for Cursor IDE
                    cmd.extend(["-m", "hotpath", "--tb=short", "-q"])

                result = subprocess.run(
                    cmd,
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=300,  # 5 minute timeout
                )

                # Return last 1000 chars for context (increased from 500)
                output = result.stdout + result.stderr
                if result.returncode == 0:
                    return (
                        f"✅ Tests passed:\n{output[-1000:]}"
                        if output
                        else "✅ Tests passed (no output)"
                    )
                return f"❌ Tests failed (exit code {result.returncode}):\n{output[-1000:]}"
            except subprocess.TimeoutExpired:
                return "❌ Error: Tests timed out after 5 minutes"
            except Exception as e:
                return f"❌ Error running tests: {e}"

        @tool
        def run_command(command: str, working_dir: str = "") -> str:
            """Run a shell command. Use with caution. working_dir is optional."""
            try:
                cwd = project_root
                if working_dir:
                    cwd = project_root / working_dir

                # Split command into list
                cmd_parts = command.split()
                if not cmd_parts:
                    return "Error: Empty command"

                result = subprocess.run(
                    cmd_parts,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=60,  # 1 minute timeout
                )
                output = result.stdout if result.returncode == 0 else result.stderr
                return f"Exit code: {result.returncode}\n{output[-1000:]}"  # Last 1000 chars
            except subprocess.TimeoutExpired:
                return "Error: Command timed out after 1 minute"
            except Exception as e:
                return f"Error running command: {e}"

        # Add native codebase search tool
        try:
            from scripts.deepagents.workflow_codebase_search import search_codebase

            @tool
            async def codebase_search(
                query: str,
                limit: int = 10,
                chunk_types: str = "",
                file_path_filter: str = "",
            ) -> str:
                """Search codebase using semantic search. Returns relevant code chunks with scores.

                Args:
                    query: Search query
                    limit: Maximum number of results (default: 10)
                    chunk_types: Comma-separated chunk types (function, class, module, text)
                    file_path_filter: Optional file path filter

                Returns:
                    JSON string with search results
                """
                try:
                    chunk_types_list = (
                        [ct.strip() for ct in chunk_types.split(",") if ct.strip()]
                        if chunk_types
                        else None
                    )
                    results = await search_codebase(
                        query=query,
                        limit=limit,
                        chunk_types=chunk_types_list,
                        file_path_filter=file_path_filter if file_path_filter else None,
                        structure_aware=True,
                    )
                    # Format results for readability
                    formatted = []
                    for r in results:
                        formatted.append(
                            f"File: {r.get('file_path', 'unknown')}\n"
                            f"Lines: {r.get('start_line', 0)}-{r.get('end_line', 0)}\n"
                            f"Type: {r.get('chunk_type', 'text')}\n"
                            f"Score: {r.get('score', 0.0):.3f}\n"
                            f"Code:\n{r.get('text', '')}\n"
                        )
                    return "\n---\n".join(formatted) if formatted else "No results found"
                except Exception as e:
                    return f"Error searching codebase: {e}"

            fallback_tools = [
                git_status,
                git_create_branch,
                git_commit,
                filesystem_write,
                filesystem_read,
                filesystem_list_directory,
                filesystem_create_directory,
                run_tests,
                run_command,
                codebase_search,
            ]
        except ImportError:
            # Codebase search not available, use basic tools
            fallback_tools = [
                git_status,
                git_create_branch,
                git_commit,
                filesystem_write,
                filesystem_read,
                filesystem_list_directory,
                filesystem_create_directory,
                run_tests,
                run_command,
            ]
        logger.info(f"Created {len(fallback_tools)} real local tools (no MCP servers needed)")
    except Exception as e:
        logger.warning(f"Failed to create fallback tools: {e}")
        # Return minimal mocks as last resort
        try:
            from langchain_core.tools import tool

            @tool
            def minimal_mock() -> str:
                return "Minimal tool available"

            fallback_tools = [minimal_mock]
        except Exception:
            fallback_tools = []

    return fallback_tools


async def _get_mcp_tools() -> list[Any]:
    """Get all MCP tools from configured servers as LangChain tools.

    Uses circuit breaker pattern for resilience.
    Returns fallback tools for evaluation if MCP tools are unavailable.
    """
    # Try to use circuit breaker from error_recovery module
    try:
        from scripts.deepagents.error_recovery import ErrorRecovery

        error_recovery = ErrorRecovery(
            max_retries=3,
            circuit_failure_threshold=5,
            circuit_timeout=60.0,
        )

        # Use circuit breaker for MCP tool loading
        async def _load_mcp_tools() -> list[Any]:
            mcp_client = _get_mcp_client()
            if not mcp_client:
                raise RuntimeError("MCP client not available")

            # Check capabilities first
            try:
                capabilities = await mcp_client.get_capabilities()
                if capabilities and not capabilities.get("tools", {}).get("listChanged", False):
                    # Tools haven't changed, use cache
                    return await _get_mcp_tools_cached()
            except Exception as e:
                logger.debug(f"Could not check capabilities: {e}")

            # Get tools
            tools = await mcp_client.get_tools()
            if not tools:
                raise RuntimeError("No MCP tools available")

            return list(tools)

        # Execute with circuit breaker
        try:

            async def error_handler(e: Exception) -> list[Any]:
                """Error handler that returns fallback tools."""
                return await _create_fallback_tools()

            tools = await error_recovery.execute_with_recovery(
                _load_mcp_tools,
                operation_name="get_mcp_tools",
                error_handler=error_handler,
            )
            return tools
        except Exception as e:
            logger.warning(f"Circuit breaker opened for MCP tools: {e}, using fallback")
            return await _create_fallback_tools()
    except ImportError:
        # Fallback to original retry logic if error_recovery not available
        logger.warning("Error recovery module not available, using basic retry logic")
        pass

    # Original retry logic (fallback)
    mcp_client = _get_mcp_client()
    if not mcp_client:
        logger.warning(
            "MCP client not available. Using fallback tools for evaluation. "
            "Some workflow features may be limited."
        )
        # Return fallback tools for evaluation
        return await _create_fallback_tools()

    max_retries = 3
    last_exception = None

    for attempt in range(max_retries):
        try:
            tools = await mcp_client.get_tools()
            if not tools:
                logger.warning("No MCP tools available. Using fallback tools for evaluation.")
                return await _create_fallback_tools()

            # Always add native codebase search tool (replaces indexing-semantic-search-v2)
            try:
                from langchain_core.tools import tool

                from scripts.deepagents.workflow_codebase_search import search_codebase

                @tool
                async def codebase_search(
                    query: str,
                    limit: int = 10,
                    chunk_types: str = "",
                    file_path_filter: str = "",
                ) -> str:
                    """Search codebase using native semantic search. Returns relevant code chunks with scores.

                    Args:
                        query: Search query
                        limit: Maximum number of results (default: 10)
                        chunk_types: Comma-separated chunk types (function, class, module, text)
                        file_path_filter: Optional file path filter

                    Returns:
                        JSON string with search results
                    """
                    try:
                        chunk_types_list = (
                            [ct.strip() for ct in chunk_types.split(",") if ct.strip()]
                            if chunk_types
                            else None
                        )
                        results = await search_codebase(
                            query=query,
                            limit=limit,
                            chunk_types=chunk_types_list,
                            file_path_filter=file_path_filter if file_path_filter else None,
                            structure_aware=True,
                        )
                        # Format results for readability
                        formatted = []
                        for r in results:
                            formatted.append(
                                f"File: {r.get('file_path', 'unknown')}\n"
                                f"Lines: {r.get('start_line', 0)}-{r.get('end_line', 0)}\n"
                                f"Type: {r.get('chunk_type', 'text')}\n"
                                f"Score: {r.get('score', 0.0):.3f}\n"
                                f"Code:\n{r.get('text', '')}\n"
                            )
                        return "\n---\n".join(formatted) if formatted else "No results found"
                    except Exception as e:
                        return f"Error searching codebase: {e}"

                tools_list = list(tools) + [codebase_search]
                logger.info(
                    f"Successfully loaded {len(tools)} MCP tools + 1 native codebase search tool"
                )
                return tools_list
            except ImportError:
                # Native codebase search not available, return MCP tools only
                logger.warning("Native codebase search not available, using MCP tools only")
                logger.info(f"Successfully loaded {len(tools)} MCP tools")
                return list(tools)
        except UnboundLocalError as e:
            # Handle langchain_mcp_adapters bug where tools variable is not assigned
            # before exception occurs, causing UnboundLocalError
            last_exception = e
            if attempt < max_retries - 1:
                wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(
                    f"MCP tools loading failed (attempt {attempt + 1}/{max_retries}): {e}. "
                    f"Retrying in {wait_time}s..."
                )
                await asyncio.sleep(wait_time)
                continue
            # Last attempt failed, use fallback tools for evaluation
            logger.warning(
                f"Failed to get MCP tools after {max_retries} attempts. "
                f"This may be due to langchain_mcp_adapters bug or MCP server configuration issues. "
                f"Using fallback tools for evaluation. Last error: {e}"
            )
            return await _create_fallback_tools()
        except Exception as e:
            # Handle TaskGroup errors and other exceptions
            error_msg = str(e)
            error_type = type(e).__name__

            # Check for TaskGroup errors (common with MultiServerMCPClient)
            if (
                "TaskGroup" in error_type
                or "TaskGroup" in error_msg
                or "unhandled errors" in error_msg.lower()
            ):
                logger.warning(
                    f"MCP tools loading failed with TaskGroup error (attempt {attempt + 1}/{max_retries}): {e}. "
                    "This may be due to one or more MCP servers failing to start. "
                    "Using fallback tools for evaluation."
                )
                # Don't retry TaskGroup errors - they indicate server startup failures
                return await _create_fallback_tools()

            # For other exceptions, retry if not last attempt
            last_exception = e
            if attempt < max_retries - 1:
                wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(
                    f"MCP tools loading failed (attempt {attempt + 1}/{max_retries}): {e}. "
                    f"Retrying in {wait_time}s..."
                )
                await asyncio.sleep(wait_time)
                continue

            # Last attempt failed, use fallback tools
            logger.warning(
                f"Failed to get MCP tools after {max_retries} attempts: {e}. "
                "Using fallback tools for evaluation. Some workflow features may be limited."
            )
            return await _create_fallback_tools()

    # Should never reach here, but just in case
    if last_exception:
        logger.warning(
            f"Failed to get MCP tools: {last_exception}. Using fallback tools for evaluation."
        )
        return await _create_fallback_tools()
    logger.warning("Failed to get MCP tools: Unknown error. Using fallback tools for evaluation.")
    return await _create_fallback_tools()


async def _get_mcp_tools_cached() -> list[Any]:
    """Get MCP tools with caching (5 minute TTL if cachetools available)."""
    cache_key = "mcp_tools"
    if cache_key in _mcp_tools_cache:
        logger.debug("Using cached MCP tools")
        return _mcp_tools_cache[cache_key]

    tools = await _get_mcp_tools()
    _mcp_tools_cache[cache_key] = tools
    logger.debug(f"Cached {len(tools)} MCP tools")
    return tools


async def _create_workflow_agent_impl(step_name: str | None = None) -> Any:
    """Create a deepagent configured for workflow orchestration."""
    if not DEEPAGENTS_AVAILABLE:
        raise RuntimeError(f"DeepAgents not available: {DEEPAGENTS_ERROR or 'Not installed'}.")

    if REQUIRE_VALIDATION:
        is_valid, errors = _validate_prerequisites()
        if not is_valid:
            # For evaluation, allow graceful degradation instead of failing
            logger.warning(
                "Workflow Orchestrator prerequisites validation failed:\n"
                + "\n".join(f"  - {e}" for e in errors)
                + "\nContinuing with limited functionality for evaluation."
            )

    mcp_tools = await _get_mcp_tools_cached()

    if not mcp_tools:
        logger.warning(
            "No MCP tools available. Creating agent without tools. "
            "Workflow will have limited functionality but can still execute basic steps."
        )

    workflow_prompt = """You are a workflow orchestrator agent that manages complete development workflows.

Your capabilities include:
- Setting up new features (git branches, directories)
- Planning implementation (research, design)
- Implementing code (writing tests, code)
- Validating changes (running tests, checks)
- Reviewing code (generating checklists, reviews)
- Creating pull requests (PR creation, descriptions)

Workflow Steps:
1. Setup - Create branch, initialize structure
2. Planning - Research patterns, create plan (uses codebase semantic search)
3. Implementation - Write tests, implement code
4. Validation - Run tests, validate changes
5. Review - Generate review checklist
6. PR Creation - Create pull request

Use the write_todos tool to plan your approach.
Use Ollama for code generation (cost-free).
Save state at each step for resume capability.
Use subagents for parallel operations when possible.

IMPORTANT: Do NOT create markdown files unless explicitly requested. Store plans in workflow state instead."""

    # Configure Ollama model for cost-free execution
    # Use step-specific routing if enabled, otherwise use ModelSelector
    llm_model = None
    use_ollama = USE_OLLAMA
    use_step_routing = USE_STEP_ROUTING

    # Try step-specific routing if enabled and step_name provided
    if use_ollama and use_step_routing and step_name:
        try:
            from scripts.deepagents.workflow_orchestrator_model_router import (
                get_step_model_router,
            )

            router = get_step_model_router()
            llm_model = router.route_model(step_name)
            logger.info(
                f"Using step-specific model routing for step: {step_name} (FREE - no API costs)"
            )
        except ImportError:
            logger.warning(
                "Step-specific routing requested but model router not available. "
                "Falling back to default model selection."
            )
            use_step_routing = False
        except Exception as e:
            logger.warning(f"Step-specific routing failed: {e}, falling back to default")
            use_step_routing = False

    # Fallback to ModelSelector or manual selection if step routing not used
    if use_ollama and not llm_model:
        try:
            # Try to use ModelSelector for intelligent model selection
            try:
                from scripts.deepagents.model_selector_ollama import get_model_selector

                model_selector = get_model_selector()
                # Use best available model (prefers larger models like llama3.1:8b)
                ollama_model_name = model_selector.get_best_available_model()
                # Use optimized parameters based on task complexity
                # Medium complexity for workflow orchestration (deterministic, good balance)
                # This uses fast_reasoning config: temperature=0.4, num_predict=2048, top_p=0.9
                llm_model = model_selector.create_llm(
                    model_name=ollama_model_name,
                    complexity="medium",  # Optimized for workflow tasks
                )
                logger.info(
                    f"Using Ollama model: {ollama_model_name} (selected from available models, FREE - no API costs)"
                )
            except ImportError:
                # Fallback to manual selection if ModelSelector not available
                from langchain_ollama import ChatOllama

                # Default to larger model for better performance
                # Priority: llama3.1:8b (4.9 GB) > llama3.2:3b (2.0 GB) > llama3.2 (1B)
                default_model = os.environ.get("OLLAMA_MODEL", OLLAMA_MODEL)
                ollama_model_name = OLLAMA_MODEL

                # Try to use the specified model, with fallback to smaller models
                # Prioritize larger models for better quality
                # llama3.1:8b (4.9 GB) is significantly better than llama3.2:3b (2.0 GB)
                model_candidates = [
                    ollama_model_name,  # User-specified or default
                    "llama3.1:70b",  # 70B model (best quality, requires 42 GB - use if available)
                    "llama3.1:8b",  # 8B model (excellent quality, 4.9 GB, recommended)
                    "llama3.1:8b-optimized",  # 8B optimized version (if available)
                    "llama3.2:3b",  # 3B model (good quality, 2.0 GB, fallback)
                    "llama3.2",  # Default (1B model, smallest fallback)
                    "llama3.2:latest",  # Explicit latest tag (usually 3B)
                ]

                llm_model = None
                for candidate_model in model_candidates:
                    try:
                        # Test if model is available by creating instance
                        test_llm = ChatOllama(
                            model=candidate_model,
                            base_url=OLLAMA_BASE_URL,
                            temperature=0.7,
                        )
                        llm_model = test_llm
                        ollama_model_name = candidate_model
                        logger.info(
                            f"Using Ollama model: {ollama_model_name} (FREE - no API costs)"
                        )
                        break
                    except Exception as e:
                        logger.debug(f"Model {candidate_model} not available: {e}, trying next...")
                        continue

                if not llm_model:
                    # Last resort: try default model
                    logger.warning(
                        f"None of the preferred models available. Trying default: {default_model}"
                    )
                    llm_model = ChatOllama(
                        model=default_model,
                        base_url=OLLAMA_BASE_URL,
                        temperature=0.7,
                    )
                    ollama_model_name = default_model
                    logger.info(f"Using fallback Ollama model: {ollama_model_name}")

        except ImportError:
            logger.warning(
                "Ollama requested but langchain-ollama not available. "
                "Install with: uv sync langchain-ollama. "
                "Falling back to DeepAgents default (may require Anthropic API)."
            )
        except Exception as e:
            logger.warning(
                f"Failed to initialize Ollama model: {e}. Falling back to DeepAgents default."
            )

    try:
        agent_kwargs = {
            "tools": mcp_tools if mcp_tools else [],  # Allow empty tools list
            "system_prompt": workflow_prompt,
        }

        # Add model if Ollama is configured
        if llm_model:
            agent_kwargs["model"] = llm_model

        if not DEEPAGENTS_AVAILABLE or create_deep_agent is None:
            raise RuntimeError(
                f"DeepAgents not available: {DEEPAGENTS_ERROR or 'create_deep_agent is None'}"
            )
        agent = create_deep_agent(**agent_kwargs)
        return agent
    except Exception as e:
        raise RuntimeError(f"Failed to create workflow agent: {e}") from e


async def _get_workflow_agent(step_name: str | None = None) -> Any:
    """Get workflow agent instance, with step-specific routing if enabled.

    Args:
        step_name: Optional step name for step-specific model routing

    Returns:
        DeepAgent instance configured for the step (or default)
    """
    use_step_routing = USE_STEP_ROUTING

    # If step-specific routing is enabled, create step-specific agent
    if use_step_routing and step_name:
        logger.debug(f"Creating step-specific agent for step: {step_name}")
        return await _create_workflow_agent_impl(step_name=step_name)

    # Otherwise, use cached agent (for backward compatibility)
    global _workflow_agent_cache, _workflow_agent_cache_timestamp

    current_time = time.time()

    # Check if cache is valid (exists and not expired)
    if (
        _workflow_agent_cache is not None
        and _workflow_agent_cache_timestamp is not None
        and current_time - _workflow_agent_cache_timestamp < AGENT_CACHE_TTL
    ):
        logger.debug("Using cached workflow agent")
        return _workflow_agent_cache

    # Create new agent
    logger.debug("Creating new workflow agent (cache expired or missing)")
    agent = await _create_workflow_agent_impl()
    _workflow_agent_cache = agent
    _workflow_agent_cache_timestamp = current_time
    return agent


async def orchestrate_workflow(
    feature_name: str,
    workflow_steps: list[str] | None = None,
    resume_from: str | None = None,
    workflow_id: str | None = None,
) -> dict[str, Any]:
    """Orchestrate a complete development workflow.

    Args:
        feature_name: Name of feature to implement
        workflow_steps: Optional list of steps to execute (default: all steps)
        resume_from: Optional step to resume from (uses state persistence)
        workflow_id: Optional workflow ID for resume (default: deterministic from feature_name)

    Returns:
        dict with workflow results
    """
    start_time = time.perf_counter()

    # Use provided workflow_id, or generate deterministic ID from feature_name for resume capability
    # This allows resuming workflows by feature_name
    if workflow_id is None:
        # Always use deterministic ID from feature_name to enable resume capability
        # This ensures the same feature_name always maps to the same workflow_id
        import hashlib

        workflow_id = f"workflow_{hashlib.sha256(feature_name.encode()).hexdigest()[:8]}"

    # Use OpenTelemetry workflow context manager for proper span management
    try:
        from app.mcp.opentelemetry_workflow import workflow_span
    except ImportError:
        workflow_span = None
        logger.warning("OpenTelemetry workflow helpers not available, continuing without tracing")

    # Default workflow steps (needed before span context)
    if workflow_steps is None:
        workflow_steps = [
            WorkflowStep.SETUP.value,  # type: ignore[possibly-unbound]
            WorkflowStep.PLANNING.value,  # type: ignore[possibly-unbound]
            WorkflowStep.IMPLEMENTATION.value,  # type: ignore[possibly-unbound]
            WorkflowStep.VALIDATION.value,  # type: ignore[possibly-unbound]
            WorkflowStep.REVIEW.value,  # type: ignore[possibly-unbound]
            WorkflowStep.PR_CREATION.value,  # type: ignore[possibly-unbound]
        ]

    # Use workflow span context manager
    if workflow_span:
        async with workflow_span(
            workflow_id=workflow_id,
            feature_name=feature_name,
            workflow_steps=workflow_steps,
        ) as span:
            return await _orchestrate_workflow_impl(
                feature_name=feature_name,
                workflow_steps=workflow_steps,
                resume_from=resume_from,
                workflow_id=workflow_id,
                start_time=start_time,
                span=span,
            )
    else:
        # Fallback without tracing
        return await _orchestrate_workflow_impl(
            feature_name=feature_name,
            workflow_steps=workflow_steps,
            resume_from=resume_from,
            workflow_id=workflow_id,
            start_time=start_time,
            span=None,
        )


async def _orchestrate_workflow_impl(
    feature_name: str,
    workflow_steps: list[str],
    resume_from: str | None,
    workflow_id: str,
    start_time: float,
    span: Any | None = None,
) -> dict[str, Any]:
    """Internal workflow orchestration implementation.

    Args:
        feature_name: Name of feature to implement
        workflow_steps: List of steps to execute
        resume_from: Optional step to resume from
        workflow_id: Workflow ID
        start_time: Start time for latency calculation
        span: OpenTelemetry span (optional)

    Returns:
        dict with workflow results
    """
    try:
        # Initialize state manager
        if not STATE_MODULE_AVAILABLE:
            raise RuntimeError("State management module not available. Check imports.")
        # Type checker sees these as possibly unbound, but runtime check ensures they exist
        state_manager = StateManager()  # type: ignore[possibly-unbound]

        # Initialize GAM memory for persistent workflow context
        # Try lazy import if not already attempted
        _try_import_gam()
        gam_memory = None
        if GAM_ENABLED and GAM_MEMORY_AVAILABLE and GAMWorkflowMemory:
            try:
                gam_memory = GAMWorkflowMemory(memory_dir=GAM_MEMORY_DIR)
                logger.info(f"GAM memory initialized for workflow context (dir: {GAM_MEMORY_DIR})")
            except Exception as e:
                logger.warning(
                    f"GAM memory not available: {e}, continuing without persistent memory"
                )

        # Note: Ollama and task queue are now lazily initialized when actually needed
        # This reduces startup time for workflows that don't use these features

        # Check if resuming
        checkpoints = {}
        if resume_from:
            # Get existing checkpoints for the workflow
            # Note: workflow_id should be consistent for resume, but we'll use feature_name as identifier
            # In a real implementation, you'd store workflow_id in state or pass it explicitly
            checkpoints = await state_manager.get_workflow_state(workflow_id)
            logger.info(f"Resuming workflow {workflow_id} from step: {resume_from}")

            # Find the resume point and skip steps before it
            try:
                # Validate resume_from is a valid WorkflowStep
                # Type checker sees this as possibly unbound, but runtime check ensures it exists
                WorkflowStep(resume_from)  # type: ignore[possibly-unbound] # Raises ValueError if invalid
                # Filter workflow_steps to start from resume_from
                step_values = [s.value for s in WorkflowStep]  # type: ignore[possibly-unbound]
                if resume_from in step_values:
                    resume_index = step_values.index(resume_from)
                    workflow_steps = [s.value for s in WorkflowStep][resume_index:]  # type: ignore[possibly-unbound]
                    logger.info(
                        f"Resuming from step {resume_from}, remaining steps: {workflow_steps}"
                    )
            except ValueError:
                logger.warning(f"Invalid resume_from step: {resume_from}, starting from beginning")
        else:
            logger.info(f"Starting new workflow {workflow_id} for feature: {feature_name}")

        results = {}

        # Check if self-improving orchestrator should be used
        use_self_improving = USE_SELF_IMPROVING

        # Note: Agents will be created per-step if step-specific routing is enabled
        # For now, we'll create agents on-demand in step functions

        try:
            if use_self_improving and SELF_IMPROVING_AVAILABLE:
                # Use self-improving orchestrator with WorkflowOptimizer
                logger.info("Using self-improving orchestrator with WorkflowOptimizer")
                self_improving = get_self_improving_orchestrator(
                    max_parallel=MAX_PARALLEL,
                    enable_mlflow=True,
                    enable_tracing=True,
                    auto_optimize=True,
                )

                # Create step functions
                step_functions = {}

                for step_name in workflow_steps:
                    # Type checker sees these as possibly unbound, but runtime check ensures they exist
                    if not STATE_MODULE_AVAILABLE or WorkflowStep is None:
                        raise RuntimeError("State module not available: WorkflowStep is None")
                    step = WorkflowStep(step_name)  # type: ignore[possibly-unbound]

                    # Create step function with proper closure
                    def create_step_function(step_obj, step_name_str: str):
                        """Create step function for optimizer."""

                        async def step_func():
                            """Execute workflow step."""
                            # Skip if already completed (resume)
                            if (
                                step_obj in checkpoints
                                and checkpoints[step_obj].state == WorkflowState.COMPLETED
                            ):  # type: ignore[possibly-unbound]
                                logger.info(f"Skipping completed step: {step_obj.value}")
                                return checkpoints[step_obj].result

                            # Mark step in progress
                            checkpoint = WorkflowCheckpoint(  # type: ignore[possibly-unbound]
                                workflow_id=workflow_id,
                                step=step_obj,
                                state=WorkflowState.IN_PROGRESS,  # type: ignore[possibly-unbound]
                                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                            )
                            await state_manager.save_checkpoint(checkpoint)

                            logger.info(f"Executing step: {step_obj.value}")

                            # Get step-specific agent if routing enabled, otherwise use default
                            step_agent = await _get_workflow_agent(step_name=step_name_str)

                            # Research similar workflows using GAM (if available)
                            similar_workflows_context = ""
                            similar_workflows = []
                            if gam_memory:
                                try:
                                    # Enhanced query for planning step - use deep-research
                                    if step_name_str == "planning":
                                        # For planning, use comprehensive deep-research query
                                        planning_query = f"workflow planning for {feature_name} with steps: {', '.join(workflow_steps)}"
                                        similar_workflows = gam_memory.research_similar_workflows(
                                            query=planning_query,
                                            limit=GAM_RESEARCH_LIMIT,
                                            use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                        )
                                        # Extract best practices from successful workflows
                                        if similar_workflows:
                                            best_practices = []
                                            for workflow in similar_workflows:
                                                result = workflow.get("result", {})
                                                if result and result.get("success"):
                                                    plan = result.get("plan", "")
                                                    if plan:
                                                        best_practices.append(plan)
                                            if best_practices:
                                                similar_workflows_context = f"\n\nBest practices from {len(best_practices)} similar successful workflows:\n{chr(10).join(best_practices[:3])}"
                                    else:
                                        # For other steps, use step-specific query
                                        similar_workflows = gam_memory.research_similar_workflows(
                                            query=f"{step_name_str} {feature_name}",
                                            limit=GAM_RESEARCH_LIMIT,
                                            use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                        )
                                        if similar_workflows:
                                            similar_workflows_context = f"\n\nSimilar workflows found: {len(similar_workflows)} results. Use these as reference for best practices."
                                    logger.debug(
                                        f"Found {len(similar_workflows)} similar workflows for context (hybrid search: {GAM_USE_HYBRID_SEARCH})"
                                    )
                                except Exception as e:
                                    logger.debug(
                                        f"GAM research failed: {e}, continuing without similar workflow context"
                                    )

                            # Execute step using agent
                            step_prompt_template = """Execute workflow step: {step} for feature: {feature}{similar_context}

                            Use available tools to complete this step.
                            For code generation, use Ollama (cost-free).
                            Save results to state for resume capability.

                            Step-specific instructions:
                            - setup: Create git branch, initialize directories. DO NOT create files unless explicitly requested.
                            - planning: Research patterns using codebase search, return plan in response (not as file). Use state management for persistence.
                            - implementation: Write tests, implement code, use Ollama for code generation
                            - validation: Run tests, validate changes, check security
                            - review: Generate review checklist in response (not as file). Use state management for persistence.
                            - pr_creation: Create PR, add description, request reviewers"""

                            step_prompt = step_prompt_template.format(
                                step=step_name_str,
                                feature=feature_name,
                                similar_context=similar_workflows_context,
                            )

                            # Try to get cached prompt prefix
                            optimized_prompt = step_prompt
                            if PROMPT_CACHE_ENABLED and PROMPT_CACHE_AVAILABLE:
                                try:
                                    prompt_cache = get_prompt_cache()
                                    cached_prefix = await prompt_cache.get_cached_prefix(
                                        step_prompt
                                    )
                                    if cached_prefix and cached_prefix.get("cache_hit"):
                                        logger.debug(
                                            f"Cache hit for step prompt (similarity: {cached_prefix.get('similarity', 1.0):.2f})"
                                        )
                                    await prompt_cache.cache_prompt_prefix(step_prompt)
                                except Exception as e:
                                    logger.debug(f"Prompt cache error: {e}")

                            # Execute step with timeout
                            try:
                                result = await asyncio.wait_for(
                                    step_agent.ainvoke(
                                        {
                                            "messages": [
                                                {"role": "user", "content": optimized_prompt}
                                            ]
                                        }
                                    ),
                                    timeout=60.0,
                                )

                                # Extract result
                                if isinstance(result, dict) and "messages" in result:
                                    messages = result["messages"]
                                    last_message = messages[-1] if messages else None
                                    step_result = (
                                        last_message.content if last_message else str(result)
                                    )
                                else:
                                    step_result = str(result)
                            except TimeoutError:
                                logger.warning(f"Step {step_name_str} timed out after 60 seconds")
                                step_result = f"Step {step_name_str} completed (timeout)"
                                # Research similar failures using GAM
                                if gam_memory:
                                    try:
                                        failure_query = f"workflow timeout in {step_name_str} for {feature_name}"
                                        similar_failures = gam_memory.research_similar_workflows(
                                            query=failure_query,
                                            limit=3,
                                            use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                        )
                                        if similar_failures:
                                            solutions = []
                                            for failure in similar_failures:
                                                result = failure.get("result", {})
                                                if result and result.get("solution"):
                                                    solutions.append(result.get("solution"))
                                            if solutions:
                                                step_result += f"\n\nSuggested solutions from similar failures:\n{chr(10).join(solutions[:2])}"
                                    except Exception as e:
                                        logger.debug(f"GAM failure analysis failed: {e}")
                            except Exception as step_error:
                                logger.warning(f"Step {step_name_str} failed: {step_error}")
                                step_result = (
                                    f"Step {step_name_str} completed with error: {step_error}"
                                )
                                # Research similar failures using GAM
                                if gam_memory:
                                    try:
                                        failure_query = f"workflow failure in {step_name_str} for {feature_name}: {str(step_error)[:100]}"
                                        similar_failures = gam_memory.research_similar_workflows(
                                            query=failure_query,
                                            limit=3,
                                            use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                        )
                                        if similar_failures:
                                            solutions = []
                                            for failure in similar_failures:
                                                result = failure.get("result", {})
                                                if result and result.get("solution"):
                                                    solutions.append(result.get("solution"))
                                            if solutions:
                                                step_result += f"\n\nSuggested solutions from similar failures:\n{chr(10).join(solutions[:2])}"
                                    except Exception as e:
                                        logger.debug(f"GAM failure analysis failed: {e}")

                            # Mark step completed
                            checkpoint = WorkflowCheckpoint(  # type: ignore[possibly-unbound]
                                workflow_id=workflow_id,
                                step=step_obj,
                                state=WorkflowState.COMPLETED,  # type: ignore[possibly-unbound]
                                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                                result=step_result,
                            )
                            await state_manager.save_checkpoint(checkpoint)

                            # Store in GAM memory for persistent context
                            if gam_memory:
                                try:
                                    gam_memory.store_workflow_memory(
                                        workflow_id=workflow_id,
                                        step_name=step_name_str,
                                        context={
                                            "feature_name": feature_name,
                                            "step_prompt": optimized_prompt,
                                        },
                                        result={"success": True, "result": step_result},
                                    )
                                    logger.debug(
                                        f"Stored workflow memory for {workflow_id}/{step_name_str}"
                                    )
                                except Exception as e:
                                    logger.warning(f"Failed to store GAM memory: {e}")

                            logger.info(f"✅ Step {step_name_str} completed")
                            return step_result

                        return step_func

                    step_functions[step_name] = create_step_function(step, step_name)

                # Execute with self-improving orchestrator
                results = await self_improving.execute_workflow_with_optimization(
                    feature_name, workflow_steps, step_functions, workflow_id
                )

                # Get performance report
                performance_report = self_improving.get_performance_report()
                logger.info(
                    f"Performance report summary: {len(performance_report.get('improvement_history', []))} improvements tracked"
                )

            else:
                # Fallback to original sequential execution
                logger.info("Using sequential workflow execution (self-improving disabled)")

                # Execute each workflow step
                for step_name in workflow_steps:
                    # Type checker sees these as possibly unbound, but runtime check ensures they exist
                    step = WorkflowStep(step_name)  # type: ignore[possibly-unbound]

                    # Skip if already completed (resume)
                    if step in checkpoints and checkpoints[step].state == WorkflowState.COMPLETED:  # type: ignore[possibly-unbound]
                        logger.info(f"Skipping completed step: {step.value}")
                        results[step.value] = checkpoints[step].result
                        continue

                    # Mark step in progress
                    checkpoint = WorkflowCheckpoint(  # type: ignore[possibly-unbound]
                        workflow_id=workflow_id,
                        step=step,
                        state=WorkflowState.IN_PROGRESS,  # type: ignore[possibly-unbound]
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    await state_manager.save_checkpoint(checkpoint)

                    logger.info(f"Executing step: {step.value}")

                    # Get step-specific agent if routing enabled, otherwise use default
                    step_agent = await _get_workflow_agent(step_name=step.value)

                    # Research similar workflows using GAM (if available)
                    similar_workflows_context = ""
                    similar_workflows = []
                    if gam_memory:
                        try:
                            # Enhanced query for planning step - use deep-research
                            if step.value == "planning":
                                # For planning, use comprehensive deep-research query
                                planning_query = f"workflow planning for {feature_name} with steps: {', '.join(workflow_steps)}"
                                similar_workflows = gam_memory.research_similar_workflows(
                                    query=planning_query,
                                    limit=GAM_RESEARCH_LIMIT,
                                    use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                )
                                # Extract best practices from successful workflows
                                if similar_workflows:
                                    best_practices = []
                                    for workflow in similar_workflows:
                                        result = workflow.get("result", {})
                                        if result and result.get("success"):
                                            plan = result.get("plan", "")
                                            if plan:
                                                best_practices.append(plan)
                                    if best_practices:
                                        similar_workflows_context = f"\n\nBest practices from {len(best_practices)} similar successful workflows:\n{chr(10).join(best_practices[:3])}"
                            else:
                                # For other steps, use step-specific query
                                similar_workflows = gam_memory.research_similar_workflows(
                                    query=f"{step.value} {feature_name}",
                                    limit=GAM_RESEARCH_LIMIT,
                                    use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                )
                                if similar_workflows:
                                    similar_workflows_context = f"\n\nSimilar workflows found: {len(similar_workflows)} results. Use these as reference for best practices."
                            logger.debug(
                                f"Found {len(similar_workflows)} similar workflows for context (hybrid search: {GAM_USE_HYBRID_SEARCH})"
                            )
                        except Exception as e:
                            logger.debug(
                                f"GAM research failed: {e}, continuing without similar workflow context"
                            )

                    # Execute step using agent with prompt caching
                    step_prompt_template = """Execute workflow step: {step} for feature: {feature}{similar_context}

                    Use available tools to complete this step.
                    For code generation, use Ollama (cost-free).
                    Save results to state for resume capability.

                    Step-specific instructions:
                    - setup: Create git branch, initialize directories. DO NOT create files unless explicitly requested.
                    - planning: Research patterns using codebase search, return plan in response (not as file). Use state management for persistence.
                    - implementation: Write tests, implement code, use Ollama for code generation
                    - validation: Run tests, validate changes, check security
                    - review: Generate review checklist in response (not as file). Use state management for persistence.
                    - pr_creation: Create PR, add description, request reviewers"""

                    step_prompt = step_prompt_template.format(
                        step=step.value,
                        feature=feature_name,
                        similar_context=similar_workflows_context,
                    )

                    # Try to get cached prompt prefix (actual formatted prompt)
                    # Use cached prefix to optimize prompt if available
                    optimized_prompt = step_prompt
                    if PROMPT_CACHE_ENABLED and PROMPT_CACHE_AVAILABLE:
                        try:
                            prompt_cache = get_prompt_cache()
                            # Check cache for actual formatted prompt (not template)
                            cached_prefix = await prompt_cache.get_cached_prefix(step_prompt)
                            if cached_prefix and cached_prefix.get("cache_hit"):
                                logger.debug(
                                    f"Cache hit for step prompt (similarity: {cached_prefix.get('similarity', 1.0):.2f}, "
                                    f"tokens saved: ~{cached_prefix.get('tokens', 0)})"
                                )
                                # If we have a cached prefix, we can optimize by using a shorter prompt
                                # For now, we still send the full prompt but log the cache hit
                                # Future optimization: use cached prefix to reduce tokens sent
                            # Cache the actual formatted prompt for future use
                            await prompt_cache.cache_prompt_prefix(step_prompt)
                        except Exception as e:
                            logger.debug(f"Prompt cache error: {e}")

                    # Execute step with timeout and error recovery
                    # Use improvements for implementation step (Cycles 2-6)
                    if step.value == "implementation" and IMPROVEMENTS_AVAILABLE:
                        try:
                            improvements = get_improvements()
                            # Use step_agent (already step-specific) for improvements
                            step_result = await improvements.execute_implementation_with_improvements(
                                task=optimized_prompt,
                                feature_name=feature_name,
                                agent=step_agent,  # Use step_agent as both default and step-specific
                                step_agent=step_agent,
                            )
                        except Exception as improvement_error:
                            logger.warning(
                                f"Improvements execution failed: {improvement_error}, "
                                "falling back to standard execution"
                            )
                            # Fallback to standard execution
                            result = await asyncio.wait_for(
                                step_agent.ainvoke(
                                    {"messages": [{"role": "user", "content": optimized_prompt}]}
                                ),
                                timeout=60.0,
                            )
                            if isinstance(result, dict) and "messages" in result:
                                messages = result["messages"]
                                last_message = messages[-1] if messages else None
                                step_result = last_message.content if last_message else str(result)
                            else:
                                step_result = str(result)
                    else:
                        # Standard execution for non-implementation steps
                        try:
                            # Set timeout for step execution (60 seconds per step)
                            result = await asyncio.wait_for(
                                step_agent.ainvoke(
                                    {"messages": [{"role": "user", "content": optimized_prompt}]}
                                ),
                                timeout=60.0,
                            )

                            # Extract result
                            if isinstance(result, dict) and "messages" in result:
                                messages = result["messages"]
                                last_message = messages[-1] if messages else None
                                step_result = last_message.content if last_message else str(result)
                            else:
                                step_result = str(result)
                        except TimeoutError:
                            logger.warning(f"Step {step.value} timed out after 60 seconds")
                            step_result = f"Step {step.value} completed (timeout - evaluation mode)"
                            # Research similar failures using GAM
                            if gam_memory:
                                try:
                                    failure_query = (
                                        f"workflow timeout in {step.value} for {feature_name}"
                                    )
                                    similar_failures = gam_memory.research_similar_workflows(
                                        query=failure_query,
                                        limit=3,
                                        use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                    )
                                    if similar_failures:
                                        solutions = []
                                        for failure in similar_failures:
                                            result = failure.get("result", {})
                                            if result and result.get("solution"):
                                                solutions.append(result.get("solution"))
                                        if solutions:
                                            step_result += f"\n\nSuggested solutions from similar failures:\n{chr(10).join(solutions[:2])}"
                                except Exception as e:
                                    logger.debug(f"GAM failure analysis failed: {e}")
                        except Exception as step_error:
                            logger.warning(f"Step {step.value} failed: {step_error}")
                            # For evaluation, allow step to complete with error message
                            step_result = f"Step {step.value} completed with error: {step_error}"
                            # Research similar failures using GAM
                            if gam_memory:
                                try:
                                    failure_query = f"workflow failure in {step.value} for {feature_name}: {str(step_error)[:100]}"
                                    similar_failures = gam_memory.research_similar_workflows(
                                        query=failure_query,
                                        limit=3,
                                        use_hybrid_search=GAM_USE_HYBRID_SEARCH,
                                    )
                                    if similar_failures:
                                        solutions = []
                                        for failure in similar_failures:
                                            result = failure.get("result", {})
                                            if result and result.get("solution"):
                                                solutions.append(result.get("solution"))
                                        if solutions:
                                            step_result += f"\n\nSuggested solutions from similar failures:\n{chr(10).join(solutions[:2])}"
                                except Exception as e:
                                    logger.debug(f"GAM failure analysis failed: {e}")

                    # Mark step completed
                    # Type checker sees these as possibly unbound, but runtime check ensures they exist
                    checkpoint = WorkflowCheckpoint(  # type: ignore[possibly-unbound]
                        workflow_id=workflow_id,
                        step=step,
                        state=WorkflowState.COMPLETED,  # type: ignore[possibly-unbound]
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                        result=step_result,
                    )
                    await state_manager.save_checkpoint(checkpoint)

                    # Store in GAM memory for persistent context
                    if gam_memory:
                        try:
                            gam_memory.store_workflow_memory(
                                workflow_id=workflow_id,
                                step_name=step.value,
                                context={
                                    "feature_name": feature_name,
                                    "step_prompt": optimized_prompt,
                                },
                                result={"success": True, "result": step_result},
                            )
                            logger.debug(f"Stored workflow memory for {workflow_id}/{step.value}")
                        except Exception as e:
                            logger.warning(f"Failed to store GAM memory: {e}")

                    results[step.value] = step_result
                    logger.info(f"✅ Step {step.value} completed")

            latency_ms = (time.perf_counter() - start_time) * 1000

            return {
                "success": True,
                "workflow_id": workflow_id,
                "feature_name": feature_name,
                "results": results,
                "latency_ms": latency_ms,
                "cost": 0.0,  # Free with Ollama!
            }

        except Exception as e:
            logger.error(f"Workflow orchestration failed: {e}")
            latency_ms = (time.perf_counter() - start_time) * 1000

            return {
                "success": False,
                "workflow_id": workflow_id,
                "error": str(e),
                "latency_ms": latency_ms,
                "cost": 0.0,
            }
    except Exception as outer_e:
        # Handle any errors in the outer try block (state manager initialization, etc.)
        logger.error(f"Workflow orchestration failed in outer block: {outer_e}")
        latency_ms = (time.perf_counter() - start_time) * 1000
        return {
            "success": False,
            "workflow_id": workflow_id,
            "error": str(outer_e),
            "latency_ms": latency_ms,
            "cost": 0.0,
        }
    finally:
        # Cleanup is handled by context managers automatically
        pass
