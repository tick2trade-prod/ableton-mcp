"""
Tests for Agentic Workflow Infrastructure

Tests for Docker scripts, configuration files, and Redis connectivity.
"""

import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class TestDockerScripts:
    """Tests for Docker installation and diagnostic scripts."""

    def test_safe_docker_desktop_install_exists(self):
        """Verify the installation script exists and is executable."""
        script = PROJECT_ROOT / "scripts" / "safe_docker_desktop_install.sh"
        assert script.exists(), "Installation script not found"
        assert os.access(script, os.X_OK), "Installation script is not executable"

    def test_doctor_docker_desktop_exists(self):
        """Verify the diagnostic script exists and is executable."""
        script = PROJECT_ROOT / "scripts" / "doctor_docker_desktop.sh"
        assert script.exists(), "Diagnostic script not found"
        assert os.access(script, os.X_OK), "Diagnostic script is not executable"

    def test_install_script_has_shebang(self):
        """Verify script starts with bash shebang."""
        script = PROJECT_ROOT / "scripts" / "safe_docker_desktop_install.sh"
        content = script.read_text()
        assert content.startswith("#!/bin/bash"), "Missing bash shebang"

    def test_doctor_script_has_shebang(self):
        """Verify script starts with bash shebang."""
        script = PROJECT_ROOT / "scripts" / "doctor_docker_desktop.sh"
        content = script.read_text()
        assert content.startswith("#!/bin/bash"), "Missing bash shebang"


class TestDockerComposeConfig:
    """Tests for docker-compose.yml configuration."""

    @pytest.fixture
    def docker_compose_path(self):
        return PROJECT_ROOT / "docker-compose.yml"

    def test_docker_compose_exists(self, docker_compose_path):
        """Verify docker-compose.yml exists."""
        assert docker_compose_path.exists(), "docker-compose.yml not found"

    def test_docker_compose_valid_yaml(self, docker_compose_path):
        """Verify docker-compose.yml is valid YAML."""
        content = docker_compose_path.read_text()
        config = yaml.safe_load(content)
        assert config is not None, "docker-compose.yml is empty"

    def test_docker_compose_has_services(self, docker_compose_path):
        """Verify docker-compose.yml defines required services."""
        content = docker_compose_path.read_text()
        config = yaml.safe_load(content)
        assert "services" in config, "No services defined"
        assert "redis-stack" in config["services"], "redis-stack service missing"
        assert "mcp-redis" in config["services"], "mcp-redis service missing"

    def test_redis_stack_config(self, docker_compose_path):
        """Verify redis-stack service configuration."""
        content = docker_compose_path.read_text()
        config = yaml.safe_load(content)
        redis = config["services"]["redis-stack"]

        assert "image" in redis, "redis-stack missing image"
        assert "redis" in redis["image"].lower(), "Unexpected redis image"
        assert "ports" in redis, "redis-stack missing ports"

    def test_mcp_redis_config(self, docker_compose_path):
        """Verify mcp-redis service configuration."""
        content = docker_compose_path.read_text()
        config = yaml.safe_load(content)
        mcp = config["services"]["mcp-redis"]

        assert "image" in mcp, "mcp-redis missing image"
        assert "depends_on" in mcp, "mcp-redis should depend on redis-stack"


class TestAntigravityConfig:
    """Tests for Antigravity configuration files."""

    def test_extensions_json_exists(self):
        """Verify extensions.json exists."""
        path = PROJECT_ROOT / ".antigravity" / "extensions.json"
        assert path.exists(), "extensions.json not found"

    def test_extensions_json_valid(self):
        """Verify extensions.json is valid JSON."""
        path = PROJECT_ROOT / ".antigravity" / "extensions.json"
        content = path.read_text()
        config = json.loads(content)
        assert "extensions" in config, "Missing extensions key"

    def test_extensions_has_github(self):
        """Verify GitHub extension is configured."""
        path = PROJECT_ROOT / ".antigravity" / "extensions.json"
        config = json.loads(path.read_text())
        assert "github" in config["extensions"], "GitHub extension not configured"
        github = config["extensions"]["github"]
        assert github.get("enabled") is True, "GitHub extension not enabled"

    def test_extensions_has_google_workspace(self):
        """Verify Google Workspace extension is configured."""
        path = PROJECT_ROOT / ".antigravity" / "extensions.json"
        config = json.loads(path.read_text())
        assert "googleWorkspace" in config["extensions"], (
            "Google Workspace extension not configured"
        )
        gw = config["extensions"]["googleWorkspace"]
        assert gw.get("enabled") is True, "Google Workspace not enabled"


class TestWorkflowScript:
    """Tests for the workflow script structure."""

    def test_workflow_script_exists(self):
        """Verify workflow script exists."""
        path = PROJECT_ROOT / ".antigravity" / "workflows" / "spec_driven_loop.py"
        assert path.exists(), "spec_driven_loop.py not found"

    def test_workflow_script_has_docstring(self):
        """Verify workflow script has module docstring."""
        path = PROJECT_ROOT / ".antigravity" / "workflows" / "spec_driven_loop.py"
        content = path.read_text()
        assert content.startswith('"""'), "Missing module docstring"

    def test_workflow_defines_agents(self):
        """Verify workflow defines required agents."""
        path = PROJECT_ROOT / ".antigravity" / "workflows" / "spec_driven_loop.py"
        content = path.read_text()
        for agent in ["architect", "critic", "builder", "qa"]:
            assert f"{agent} = Agent(" in content, f"{agent} agent not defined"

    def test_workflow_defines_audit_gate(self):
        """Verify workflow defines audit_gate function."""
        path = PROJECT_ROOT / ".antigravity" / "workflows" / "spec_driven_loop.py"
        content = path.read_text()
        assert "def audit_gate(" in content, "audit_gate function not defined"

    def test_workflow_defines_main_loop(self):
        """Verify workflow defines main loop function."""
        path = PROJECT_ROOT / ".antigravity" / "workflows" / "spec_driven_loop.py"
        content = path.read_text()
        assert "def spec_driven_loop(" in content, "spec_driven_loop function missing"

    def test_workflow_registers_workflow(self):
        """Verify workflow is registered."""
        path = PROJECT_ROOT / ".antigravity" / "workflows" / "spec_driven_loop.py"
        content = path.read_text()
        assert "Workflow.register(" in content, "Workflow not registered"


class TestPyprojectConfig:
    """Tests for pyproject.toml configuration."""

    @pytest.fixture
    def pyproject_path(self):
        return PROJECT_ROOT / "pyproject.toml"

    def test_pyproject_exists(self, pyproject_path):
        """Verify pyproject.toml exists."""
        assert pyproject_path.exists(), "pyproject.toml not found"

    def test_python_version_requirement(self, pyproject_path):
        """Verify Python 3.12+ is required."""
        content = pyproject_path.read_text()
        assert ">=3.12" in content, "Python 3.12+ requirement not found"

    def test_pydantic_dependency(self, pyproject_path):
        """Verify pydantic is a dependency."""
        content = pyproject_path.read_text()
        assert "pydantic" in content, "pydantic dependency not found"

    def test_redis_dependency(self, pyproject_path):
        """Verify redis is a dependency."""
        content = pyproject_path.read_text()
        assert "redis" in content, "redis dependency not found"

    def test_ruff_config(self, pyproject_path):
        """Verify ruff is configured."""
        content = pyproject_path.read_text()
        assert "[tool.ruff]" in content, "ruff configuration not found"
        assert "line-length = 88" in content, "ruff line-length not set to 88"


class TestDocumentation:
    """Tests for documentation files."""

    def test_agentic_workflow_docs_exists(self):
        """Verify agentic workflow docs exist."""
        path = PROJECT_ROOT / "docs" / "agentic-workflow.md"
        assert path.exists(), "agentic-workflow.md not found"

    def test_readme_mentions_agentic_workflow(self):
        """Verify README mentions agentic workflow."""
        path = PROJECT_ROOT / "README.md"
        content = path.read_text()
        assert "Agentic Workflow" in content, "README missing Agentic Workflow section"


@pytest.mark.skipif(
    not os.path.exists("/Applications/Docker.app"),
    reason="Docker Desktop not installed",
)
class TestDockerIntegration:
    """Integration tests requiring Docker."""

    def test_docker_available(self):
        """Verify Docker CLI is available."""
        docker_path = "/Applications/Docker.app/Contents/Resources/bin/docker"
        result = subprocess.run(
            [docker_path, "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "Docker CLI not working"
        assert "Docker version" in result.stdout

    def test_docker_daemon_running(self):
        """Verify Docker daemon is running."""
        docker_path = "/Applications/Docker.app/Contents/Resources/bin/docker"
        result = subprocess.run(
            [docker_path, "info"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "Docker daemon not running"

    def test_docker_compose_available(self):
        """Verify Docker Compose is available."""
        docker_path = "/Applications/Docker.app/Contents/Resources/bin/docker"
        result = subprocess.run(
            [docker_path, "compose", "version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "Docker Compose not available"


@pytest.mark.skipif(
    not os.path.exists("/Applications/Docker.app"),
    reason="Docker Desktop not installed",
)
class TestRedisIntegration:
    """Integration tests for Redis connectivity (requires running containers)."""

    @pytest.fixture
    def docker_path(self):
        return "/Applications/Docker.app/Contents/Resources/bin/docker"

    def test_redis_container_exists(self, docker_path):
        """Check if redis-stack container exists."""
        result = subprocess.run(
            [docker_path, "compose", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        # This test just checks compose config, not running state
        assert result.returncode == 0, "docker compose ps failed"

    @pytest.mark.skip(reason="Requires containers to be running")
    def test_redis_ping(self, docker_path):
        """Test Redis PING command."""
        result = subprocess.run(
            [docker_path, "exec", "redis-stack", "redis-cli", "PING"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "Redis PING failed"
        assert "PONG" in result.stdout, "Expected PONG response"
