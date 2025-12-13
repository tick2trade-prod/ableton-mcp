"""Ableton MCP Configuration.

Environment-specific settings for Ableton Live integration.
"""
import os
import platform
from pathlib import Path

# === Ableton Live Settings ===
ABLETON_VERSION = os.getenv("ABLETON_VERSION", "12.3.1")
ABLETON_EDITION = os.getenv("ABLETON_EDITION", "Intro")  # Intro, Standard, Suite

# Track limits by edition
EDITION_MAX_TRACKS = {
    "Intro": 16,
    "Standard": 256,
    "Suite": 256,
}
ABLETON_MAX_TRACKS = EDITION_MAX_TRACKS.get(ABLETON_EDITION, 16)

# === Connection Settings ===
ABLETON_HOST = os.getenv("ABLETON_HOST", "localhost")
ABLETON_PORT = int(os.getenv("ABLETON_PORT", "9877"))
SOCKET_TIMEOUT = int(os.getenv("SOCKET_TIMEOUT", "10"))

# === Paths (Platform-specific) ===
HOME = Path.home()

# macOS paths
MACOS_LOG_PATH = HOME / "Library/Preferences/Ableton" / f"Live {ABLETON_VERSION}" / "Log.txt"
MACOS_REMOTE_SCRIPT_PATH = HOME / "Music/Ableton/User Library/Remote Scripts/AbletonMCP"

# Windows paths (untested)
WINDOWS_LOG_PATH = Path(os.getenv("APPDATA", "")) / "Ableton" / f"Live {ABLETON_VERSION}" / "Preferences" / "Log.txt"
WINDOWS_REMOTE_SCRIPT_PATH = Path(os.getenv("APPDATA", "")) / "Ableton" / f"Live {ABLETON_VERSION}" / "Preferences" / "User Remote Scripts" / "AbletonMCP"

# Select based on platform
if platform.system() == "Darwin":
    LOG_PATH = MACOS_LOG_PATH
    REMOTE_SCRIPT_PATH = MACOS_REMOTE_SCRIPT_PATH
elif platform.system() == "Windows":
    LOG_PATH = WINDOWS_LOG_PATH
    REMOTE_SCRIPT_PATH = WINDOWS_REMOTE_SCRIPT_PATH
else:
    LOG_PATH = MACOS_LOG_PATH  # Default to macOS
    REMOTE_SCRIPT_PATH = MACOS_REMOTE_SCRIPT_PATH

# === Debug Settings ===
DEBUG = os.getenv("ABLETON_MCP_DEBUG", "false").lower() == "true"


def get_config():
    """Return config dict for debugging."""
    return {
        "version": ABLETON_VERSION,
        "edition": ABLETON_EDITION,
        "max_tracks": ABLETON_MAX_TRACKS,
        "host": ABLETON_HOST,
        "port": ABLETON_PORT,
        "log_path": str(LOG_PATH),
        "remote_script_path": str(REMOTE_SCRIPT_PATH),
        "debug": DEBUG,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(get_config(), indent=2))
