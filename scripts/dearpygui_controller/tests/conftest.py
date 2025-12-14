"""Pytest configuration for DearPyGUI controller tests."""

import sys
from pathlib import Path

# Add scripts path to sys.path for imports
# This runs before test collection
scripts_path = Path(__file__).parent.parent.parent / "scripts"
if str(scripts_path) not in sys.path:
    sys.path.insert(0, str(scripts_path))
