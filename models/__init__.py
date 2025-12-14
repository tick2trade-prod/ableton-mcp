"""Pydantic models package.

Structure:
- v1/: Version 1.0.0 models
- CHANGELOG.md: Track model changes over time
- current: Import from latest version

See CHANGELOG.md for version history.
"""

# Import from current version (v1)
from .v1.test_models import (
    AbletonReference,
    ClassDocstring,
    MethodDocstring,
    ModuleDocstring,
    TestClass,
    TestMethod,
    TestModule,
    ValidationResult,
)

__version__ = "1.0.0"

__all__ = [
    "AbletonReference",
    "ModuleDocstring",
    "ClassDocstring",
    "MethodDocstring",
    "TestMethod",
    "TestClass",
    "TestModule",
    "ValidationResult",
]
