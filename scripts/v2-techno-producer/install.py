#!/usr/bin/env python3
"""GAM DeepAgents Memorizer Researcher Planner v3 Installer.

Enhanced installer with improved validation and error handling.
Based on v2 installer with v3-specific updates (KISS improvements, Docker integration).

Installation:
    uv run python scripts/gam_deepagents/v3/install.py --install
Validation:
    uv run python scripts/gam_deepagents/v3/install.py --validate-only
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Import v1 installer functions (reuse most logic)
sys.path.insert(0, str(Path(__file__).parent))
from scripts.gam_deepagents.v1.install import (
    check_gam_components,
    check_gam_package,
    check_java_installation,
    check_mcp_config,
    check_opentelemetry_config,
    check_python_dependencies,
    check_settings_config,
    find_uv_command,
    install_missing_packages,
    print_error,
    print_header,
    print_info,
    print_success,
    print_warning,
)


def update_mcp_config_v3(install: bool = False, java_info: dict | None = None) -> bool:
    """Update MCP configuration for v3 server.

    Args:
        install: Whether to install/update configuration
        java_info: Optional dict with JAVA_HOME and JVM_PATH

    Returns:
        True if configuration updated successfully
    """
    mcp_config_path = Path.home() / ".cursor" / "mcp.json"

    if not mcp_config_path.exists():
        if not install:
            return False
        # Create new config
        config = {"mcpServers": {}}
    else:
        try:
            with open(mcp_config_path) as f:
                config = json.load(f)
        except Exception as e:
            print_error(f"Failed to read MCP config: {e}")
            return False

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Update v3 server config
    uv_command = find_uv_command()
    workspace_folder = Path(__file__).parent.parent.parent

    server_config = {
        "command": uv_command,
        "args": [
            "run",
            "--directory",
            str(workspace_folder),
            "python",
            str(
                workspace_folder
                / "scripts"
                / "gam_deepagents"
                / "mcp_gam_deepagents_memorizer_researcher_planner_v3.py"
            ),
        ],
        "env": {
            "PYTHONPATH": str(workspace_folder),
        },
    }

    # Add Java environment variables if available
    if java_info:
        if java_info.get("JAVA_HOME"):
            server_config["env"]["JAVA_HOME"] = java_info["JAVA_HOME"]
        if java_info.get("JVM_PATH"):
            server_config["env"]["JVM_PATH"] = java_info["JVM_PATH"]
        if java_info.get("JAVA_HOME"):
            java_bin = f"{java_info['JAVA_HOME']}/bin"
            current_path = server_config["env"].get("PATH", os.environ.get("PATH", ""))
            server_config["env"]["PATH"] = f"{java_bin}:{current_path}"

    config["mcpServers"]["gam-deepagents-v3"] = server_config

    try:
        with open(mcp_config_path, "w") as f:
            json.dump(config, f, indent=2)
        print_success("MCP configuration updated for v3")
        return True
    except Exception as e:
        print_error(f"Failed to update MCP config: {e}")
        return False


def main():
    """Main installer function for v3."""
    parser = argparse.ArgumentParser(
        description="Install and validate GAM DeepAgents MCP server v3"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install missing packages and update MCP configuration",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate, do not install or update",
    )
    args = parser.parse_args()

    print_header("GAM DeepAgents Memorizer Researcher Planner v3 Installer")

    all_checks_passed = True
    missing_packages = []

    # Check Python dependencies
    deps_ok, missing_deps = check_python_dependencies()
    if not deps_ok:
        all_checks_passed = False
        missing_packages.extend(missing_deps)

    # Check Java
    java_ok, java_issues, java_info = check_java_installation()
    if not java_ok:
        print_warning("Java 21 is required for GAM BM25 retriever")
        print_info("GAM will work without Java, but BM25 keyword search requires Java 21")

    # Check GAM package
    gam_ok, missing_gam = check_gam_package(java_info if java_ok else None)
    if not gam_ok:
        all_checks_passed = False
        missing_packages.extend(missing_gam)

    # Check GAM components
    components_ok, _ = check_gam_components(java_info if java_ok else None)
    if not components_ok:
        all_checks_passed = False

    # Check OpenTelemetry
    otel_ok, _ = check_opentelemetry_config()
    if not otel_ok:
        all_checks_passed = False

    # Check settings
    settings_ok, _ = check_settings_config()
    if not settings_ok:
        all_checks_passed = False

    # Check MCP config for v3
    mcp_ok, _ = check_mcp_config()
    if not mcp_ok and args.install:
        update_mcp_config_v3(install=True, java_info=java_info if java_ok else None)
    elif args.install and java_ok and java_info:
        update_mcp_config_v3(install=True, java_info=java_info)

    # Install missing packages if requested
    if args.install and missing_packages:
        if install_missing_packages(missing_packages):
            print_success("All packages installed successfully")
            java_ok, _, java_info = check_java_installation()
            deps_ok, _ = check_python_dependencies()
            gam_ok, _ = check_gam_package(java_info if java_ok else None)
            components_ok, _ = check_gam_components(java_info if java_ok else None)
            settings_ok, _ = check_settings_config()
            all_checks_passed = deps_ok and gam_ok and components_ok and otel_ok and settings_ok
        else:
            all_checks_passed = False

    # Final summary
    print_header("Installation Summary (v3)")

    if all_checks_passed:
        print_success("All checks passed! GAM DeepAgents MCP server v3 is ready to use.")
        print_info("Restart Cursor to load the MCP server configuration.")
        return 0
    else:
        print_error("Some checks failed. Please fix the issues above.")
        if missing_packages:
            print_info(f"Missing packages: {', '.join(missing_packages)}")
            print_info("Run with --install to install missing packages")
        return 1


if __name__ == "__main__":
    sys.exit(main())
