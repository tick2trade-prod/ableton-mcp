#!/usr/bin/env python3
"""
Workflow Orchestrator Hybrid v1 Installer

Comprehensive installer and validator for Workflow Orchestrator Hybrid MCP server.
Ensures all required components are properly installed and configured.

This installer:
1. Validates Python dependencies
2. Checks Ollama installation and service
3. Verifies MCP server configurations
4. Tests connectivity to optional services (Redis, PostgreSQL)
5. Validates workflow orchestrator modules
6. Provides clear error messages and fixes

Usage:
    uv run python scripts/deepagents/install_workflow_orchestrator_hybrid_v1.py [--install] [--validate-only]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


# Color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_success(message: str):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_error(message: str):
    """Print error message."""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_warning(message: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


def print_info(message: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")


def print_header(message: str):
    """Print header message."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")


def check_command(command: str, check_output: bool = False) -> tuple[bool, str | None]:
    """Check if a command is available."""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if check_output:
            return result.returncode == 0, result.stdout.strip() if result.returncode == 0 else None
        return result.returncode == 0, None
    except Exception:
        return False, None


def check_python_dependencies() -> tuple[bool, list[str]]:
    """Check if all required Python dependencies are installed."""
    print_header("Checking Python Dependencies")

    required_packages = [
        "mcp",
        "fastmcp",
        "langchain_mcp_adapters",
        "deepagents",
        "langchain_ollama",
    ]

    optional_packages = [
        "celery",
        "dramatiq",
        "ray",
        "fastapi",
        "websockets",
        "prefect",
        "psycopg2",
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            missing.append(package)

    print_info("Checking optional packages...")
    for package in optional_packages:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{package} is installed (optional)")
        except ImportError:
            print_warning(f"{package} is NOT installed (optional, for async task queues)")

    return len(missing) == 0, missing


def check_workflow_orchestrator_modules() -> tuple[bool, list[str]]:
    """Check if workflow orchestrator modules can be imported."""
    print_header("Checking Workflow Orchestrator Modules")

    modules = [
        "scripts.deepagents.workflow_orchestrator_hybrid_v1",
        "scripts.deepagents.workflow_orchestrator_ollama",
        "scripts.deepagents.workflow_orchestrator_state",
        "scripts.deepagents.workflow_orchestrator_tasks",
    ]

    missing = []
    for module in modules:
        try:
            __import__(module)
            print_success(f"{module} can be imported")
        except ImportError as e:
            print_error(f"{module} cannot be imported: {e}")
            missing.append(module)

    return len(missing) == 0, missing


def check_ollama() -> tuple[bool, str | None]:
    """Check if Ollama is installed and running."""
    print_header("Checking Ollama")

    # Check if ollama command exists
    ollama_available, _ = check_command("ollama --version")
    if not ollama_available:
        print_error("Ollama is not installed")
        print_info("Install with: curl -fsSL https://ollama.ai/install.sh | sh")
        return False, None

    print_success("Ollama is installed")

    # Check if Ollama service is running
    try:
        import requests

        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print_success("Ollama service is running")
            models = response.json().get("models", [])
            if models:
                print_info(
                    f"Available models: {', '.join([m.get('name', 'unknown') for m in models])}"
                )
            else:
                print_warning("No models installed. Pull a model with: ollama pull codellama")
            return True, None
        else:
            print_error(f"Ollama service returned status {response.status_code}")
            return False, "Ollama service not responding"
    except ImportError:
        print_warning("requests not available, skipping Ollama service check")
        return True, None
    except Exception as e:
        print_warning(f"Ollama service check failed: {e}")
        print_info("Start Ollama with: ollama serve")
        return False, str(e)


def check_optional_services() -> dict[str, bool]:
    """Check optional services (Redis, PostgreSQL)."""
    print_header("Checking Optional Services")

    services = {}

    # Check Redis
    try:
        import redis

        r = redis.Redis(host="localhost", port=6379, db=0, socket_connect_timeout=1)
        r.ping()
        print_success("Redis is running (optional, for Celery/Dramatiq)")
        services["redis"] = True
    except Exception:
        print_warning("Redis is not running (optional, for Celery/Dramatiq)")
        print_info("Start with: docker run -d -p 6379:6379 redis")
        services["redis"] = False

    # Check PostgreSQL
    try:
        import psycopg2

        conn = psycopg2.connect(
            host="localhost", port=5432, user="postgres", password="postgres", connect_timeout=1
        )
        conn.close()
        print_success("PostgreSQL is running (optional, SQLite is default)")
        services["postgresql"] = True
    except Exception:
        print_warning("PostgreSQL is not running (optional, SQLite is default)")
        print_info("Start with: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres")
        services["postgresql"] = False

    return services


def check_mcp_config() -> tuple[bool, list[str]]:
    """Check MCP server configuration."""
    print_header("Checking MCP Configuration")

    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    if not mcp_config_path.exists():
        print_error(f"MCP config file not found: {mcp_config_path}")
        return False, ["MCP config file missing"]

    print_success(f"MCP config file exists: {mcp_config_path}")

    try:
        with open(mcp_config_path) as f:
            config = json.load(f)

        mcp_servers = config.get("mcpServers", {})

        # Check for workflow-orchestrator-hybrid
        if "workflow-orchestrator-hybrid" in mcp_servers:
            print_success("workflow-orchestrator-hybrid is configured")
        else:
            print_warning("workflow-orchestrator-hybrid is NOT configured")
            print_info("Add to ~/.cursor/mcp.json:")
            print_info('  "workflow-orchestrator-hybrid": {')
            print_info('    "command": "uv",')
            print_info(
                '    "args": ["run", "--directory", "${workspaceFolder}", "python", "${workspaceFolder}/scripts/deepagents/mcp_server_workflow_orchestrator_hybrid_v1.py"]'
            )
            print_info("  }")

        # Check for required MCP servers
        required_servers = [
            "git",
            "filesystem",
            "sequential-thinking",
            "indexing-semantic-search-v2",
        ]
        missing_servers = []
        for server in required_servers:
            if server in mcp_servers:
                print_success(f"{server} MCP server is configured")
            else:
                print_warning(f"{server} MCP server is NOT configured")
                missing_servers.append(server)

        return len(missing_servers) == 0, missing_servers

    except Exception as e:
        print_error(f"Error reading MCP config: {e}")
        return False, [str(e)]


def install_dependencies():
    """Install missing dependencies."""
    print_header("Installing Dependencies")

    print_info("Running: uv sync")
    result = subprocess.run(["uv", "sync"], capture_output=True, text=True)

    if result.returncode == 0:
        print_success("Dependencies installed successfully")
        return True
    else:
        print_error(f"Failed to install dependencies: {result.stderr}")
        return False


def main():
    """Main installer/validator function."""
    parser = argparse.ArgumentParser(description="Workflow Orchestrator Hybrid v1 Installer")
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install missing dependencies",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate, do not install",
    )

    args = parser.parse_args()

    print_header("Workflow Orchestrator Hybrid v1 Installer")

    all_checks_passed = True

    # Check Python dependencies
    deps_ok, missing_deps = check_python_dependencies()
    if not deps_ok:
        all_checks_passed = False
        if args.install and not args.validate_only:
            print_info("Installing missing dependencies...")
            if install_dependencies():
                # Re-check
                deps_ok, missing_deps = check_python_dependencies()
                if deps_ok:
                    print_success("All dependencies installed")
                else:
                    print_error("Some dependencies still missing after installation")
                    all_checks_passed = False
        else:
            print_info("Run with --install to install missing dependencies")

    # Check workflow orchestrator modules
    modules_ok, missing_modules = check_workflow_orchestrator_modules()
    if not modules_ok:
        all_checks_passed = False

    # Check Ollama
    ollama_ok, ollama_error = check_ollama()
    if not ollama_ok:
        all_checks_passed = False
        print_info(
            "Ollama is required for code generation. Install with: curl -fsSL https://ollama.ai/install.sh | sh"
        )

    # Check optional services
    check_optional_services()

    # Check MCP config
    mcp_ok, mcp_errors = check_mcp_config()
    if not mcp_ok:
        all_checks_passed = False

    # Summary
    print_header("Installation Summary")

    if all_checks_passed:
        print_success("✅ All required components are properly configured!")
        print_info("You can now use the Workflow Orchestrator Hybrid v1 MCP server.")
        print_info("Test with: uv run pytest tests/test_workflow_orchestrator_hybrid_v1.py -v")
        return 0
    else:
        print_error("❌ Some components are missing or misconfigured.")
        print_info("Review the errors above and fix them.")
        if not args.install:
            print_info("Run with --install to automatically install missing dependencies")
        return 1


if __name__ == "__main__":
    sys.exit(main())
