#!/usr/bin/env python3
"""
Deploy Ableton Remote Script.
Reads configuration from config.yaml and copies the remote script to the correct location.
"""
import shutil
import sys
from pathlib import Path

# Check if PyYAML is installed, simplistic check since we are in a dev environment
try:
    import yaml
except ImportError:
    print("❌ PyYAML not found. Please run 'uv pip install pyyaml' or 'pip install pyyaml'")
    sys.exit(1)

CONFIG_FILE = Path("config.yaml")
SOURCE_DIR = Path("AbletonMCP_Remote_Script")

def load_config():
    if not CONFIG_FILE.exists():
        print(f"❌ Config file not found: {CONFIG_FILE.absolute()}")
        return {}
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def expand_path(path_str):
    if not path_str:
        return None
    path = Path(path_str).expanduser()
    if path_str.startswith("$"):
        # Simple env var expansion if needed, though expanduser handles ~
        pass
    return path

def deploy():
    print("🚀 Starting Deployment...")
    config = load_config()

    # 1. Determine Destination
    raw_path = config.get("REMOTE_SCRIPT_PATH")
    if not raw_path:
        print("❌ REMOTE_SCRIPT_PATH not set in config.yaml")
        sys.exit(1)

    dest_path = expand_path(raw_path)
    print(f"  📂 Destination: {dest_path}")

    # 2. Verify Source
    if not SOURCE_DIR.exists():
        print(f"❌ Source directory not found: {SOURCE_DIR.absolute()}")
        sys.exit(1)

    # 3. Perform Copy
    try:
        # Create destination if it doesn't exist (though usually the parent should exist)
        if not dest_path.exists():
            print(f"  ✨ Creating directory: {dest_path}")
            dest_path.mkdir(parents=True, exist_ok=True)

        # We only want to copy the contents, specifically __init__.py and any other python files
        # The user specifically mentioned replacing __init__.py

        # Check source __init__.py
        src_init = SOURCE_DIR / "__init__.py"
        if not src_init.exists():
             print(f"❌ Source __init__.py not found at {src_init}")
             sys.exit(1)

        dest_init = dest_path / "__init__.py"

        print(f"  Copying {src_init} -> {dest_init}")
        shutil.copy2(src_init, dest_init)

        print("✅ Deployment Successful!")
        print("👉 Please restart Ableton Live or reload the Remote Script.")

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()
