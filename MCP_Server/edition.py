"""Edition-aware tool filtering for FastMCP."""

import logging
import os
from collections.abc import Callable
from enum import IntEnum
from functools import wraps
from typing import Optional

logger = logging.getLogger(__name__)


class Edition(IntEnum):
    """Ableton Live editions (hierarchical: INTRO < STANDARD < SUITE)."""

    INTRO = 1
    STANDARD = 2
    SUITE = 3


# Detected edition (set at startup)
_detected_edition: Optional[Edition] = None


def requires_edition(min_edition: Edition) -> Callable:
    """
    Decorator to tag MCP tools with minimum required edition.

    Attaches _min_edition attribute to function for filtering.
    Place BELOW @mcp.tool() when stacking decorators.

    Example:
        @mcp.tool()
        @requires_edition(Edition.SUITE)
        def separate_stems(...):
            ...
    """

    def decorator(func: Callable) -> Callable:
        func._min_edition = min_edition

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def detect_edition_from_ableton(connection) -> Edition:
    """
    Query Ableton to detect which edition is running.

    Uses available devices/features to infer edition:
    - Roar, Meld, Drift → SUITE
    - Extended instruments → STANDARD
    - Base features → INTRO
    """
    try:
        # Query session info
        result = connection.send_command("get_session_info")

        # Try to detect Suite by querying for Suite-only devices
        try:
            browser_result = connection.send_command(
                "get_browser_tree", {"category_type": "audio_effects"}
            )
            categories = str(browser_result)

            # Suite-only devices
            if "Roar" in categories or "Meld" in categories or "Drift" in categories:
                return Edition.SUITE
        except Exception:
            pass

        # Heuristic: track limit detection
        # Intro: 16 tracks, Standard: unlimited but less devices
        track_count = result.get("track_count", 0)
        if track_count > 16:
            return Edition.STANDARD

        return Edition.INTRO

    except Exception as e:
        logger.warning(f"Could not detect edition: {e}. Defaulting to INTRO.")
        return Edition.INTRO


def get_edition() -> Edition:
    """Get current edition (detected or from env/config)."""
    global _detected_edition

    from .config import get

    # 1. Check env override
    env_edition = os.getenv("ABLETON_EDITION")
    if env_edition:
        try:
            return Edition[env_edition.upper()]
        except KeyError:
            pass

    # 2. Check config (if not 'auto')
    config_edition = get("ableton.edition", "auto")
    if config_edition != "auto":
        try:
            return Edition[config_edition.upper()]
        except KeyError:
            pass

    # 3. Use detected edition
    if _detected_edition:
        return _detected_edition

    # 4. Default to INTRO (safest)
    return Edition.INTRO


def set_detected_edition(edition: Edition) -> None:
    """Set the detected edition (called at startup)."""
    global _detected_edition
    _detected_edition = edition
    logger.info(f"Edition detected: {edition.name}")


def is_tool_available(func: Callable) -> bool:
    """Check if a tool is available for current edition."""
    required = getattr(func, "_min_edition", Edition.INTRO)
    current = get_edition()
    return current >= required
