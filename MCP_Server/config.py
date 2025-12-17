"""Configuration loader - reads from config.yaml."""

import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

_CONFIG: Optional[dict] = None


def load_config() -> dict[str, Any]:
    """Load config.yaml from project root."""
    global _CONFIG
    if _CONFIG is not None:
        return _CONFIG

    config_path = Path(__file__).parent.parent / "config.yaml"
    template_path = Path(__file__).parent.parent / "config.template.yaml"

    try:
        import yaml
    except ImportError:
        logger.warning("pyyaml not installed, using defaults")
        _CONFIG = {"ableton": {"edition": "auto", "port": 9877}}
        return _CONFIG

    if config_path.exists():
        with open(config_path) as f:
            _CONFIG = yaml.safe_load(f) or {}
    elif template_path.exists():
        logger.warning("config.yaml not found, using template defaults")
        with open(template_path) as f:
            _CONFIG = yaml.safe_load(f) or {}
    else:
        logger.warning("No config found, using defaults")
        _CONFIG = {"ableton": {"edition": "auto", "port": 9877}}

    return _CONFIG


def get(key: str, default: Any = None) -> Any:
    """Get nested config value using dot notation.

    Example: get("ableton.edition") → "auto"
    """
    config = load_config()
    keys = key.split(".")
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default
    return value if value is not None else default


def get_port() -> int:
    """Get MCP port."""
    return int(get("ableton.port", 9877))
