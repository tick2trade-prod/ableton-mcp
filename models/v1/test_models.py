"""Test validation models (Pydantic 2.x).

Version: 1.0.0

Models for validating test file structure, docstrings, and TDD compliance.
"""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, field_validator

from .base import ModernBaseModel


class AbletonReference(ModernBaseModel):
    """Ableton Manual reference validation.

    Validates manual section, title, and page number format.

    Attributes:
        section: Section number (e.g., "28.9.2" or "4.7")
        title: Section title from manual
        page: Page number in manual (1-999)

    Example:
        >>> ref = AbletonReference(
        ...     section="28.9.2",
        ...     title="Compressor Tips",
        ...     page=521
        ... )
        >>> ref.reference_string
        'Section 28.9.2 "Compressor Tips" (page 521)'
    """

    section: Annotated[str, Field(pattern=r"^\\d+\\.\\d+(\\.\\d+)?$")]
    title: Annotated[str, Field(min_length=1, max_length=200)]
    page: Annotated[int, Field(gt=0, lt=1000)]

    @field_validator("section")
    @classmethod
    def validate_section_format(cls, v: str) -> str:
        """Ensure section follows X.Y or X.Y.Z format."""
        parts = v.split(".")
        if not (2 <= len(parts) <= 3):
            raise ValueError(f"Section must be X.Y or X.Y.Z format, got: {v}")
        return v

    @property
    def reference_string(self) -> str:
        """Format as: 'Section 28.9.2 \"Title\" (page 521)'"""
        return f'Section {self.section} "{self.title}" (page {self.page})'


class ModuleDocstring(ModernBaseModel):
    """Module-level docstring validation.

    Validates test module docstrings for:
    - Description
    - Ableton Manual references
    - TDD workflow markers
    """

    description: Annotated[str, Field(min_length=10)]
    references: Annotated[list[AbletonReference], Field(min_length=1, max_length=3)]
    has_tdd_workflow: bool = Field(default=True)
    tdd_markers: list[Literal["RED", "GREEN", "REFACTOR"]] = Field(
        default_factory=lambda: ["RED", "GREEN", "REFACTOR"]
    )

    @field_validator("has_tdd_workflow")
    @classmethod
    def validate_tdd_section(cls, v: bool) -> bool:
        """Ensure TDD workflow section exists."""
        if not v:
            raise ValueError("Module docstring must include TDD Workflow section")
        return v


class ClassDocstring(ModernBaseModel):
    """Class-level docstring validation."""

    description: Annotated[str, Field(min_length=10)]
    references: list[AbletonReference] = Field(default_factory=list, max_length=2)
    excerpt: str | None = Field(None, min_length=20)


class MethodDocstring(ModernBaseModel):
    """Method-level docstring validation."""

    description: Annotated[str, Field(min_length=10)]
    references: list[AbletonReference] = Field(default_factory=list, max_length=2)
    tdd_marker: Literal["RED", "GREEN", "REFACTOR"] | None = None


class TestMethod(ModernBaseModel):
    """Individual test method validation.

    Validates test methods for:
    - Naming convention (test_*)
    - Docstring quality
    - AAA structure (Arrange/Act/Assert)
    - Fixture usage
    """

    name: Annotated[str, Field(pattern=r"^test_[a-z_]+$")]
    docstring: MethodDocstring
    has_arrange: bool = Field(default=True)
    has_act: bool = Field(default=True)
    has_assert: bool = Field(default=True)
    uses_fixtures: list[str] = Field(default_factory=list)

    @field_validator("uses_fixtures")
    @classmethod
    def validate_fixture_names(cls, v: list[str]) -> list[str]:
        """Ensure only valid fixtures used."""
        valid_fixtures = {"mock_mcp_client", "mock_agent_logger"}
        invalid = set(v) - valid_fixtures
        if invalid:
            raise ValueError(f"Invalid fixtures: {invalid}")
        return v


class TestClass(ModernBaseModel):
    """Test class validation."""

    name: Annotated[str, Field(pattern=r"^Test[A-Za-z]+$")]
    docstring: ClassDocstring
    methods: list[TestMethod] = Field(..., min_length=1)


class TestModule(ModernBaseModel):
    """Entire test module validation."""

    filepath: Path
    filename: Annotated[str, Field(pattern=r"^test_[a-z_]+_agent\\.py$")]
    docstring: ModuleDocstring
    classes: list[TestClass] = Field(..., min_length=1)
    imports_pytest: bool = Field(default=True)
    imports_mock: bool = Field(default=True)

    @field_validator("imports_pytest")
    @classmethod
    def validate_pytest_import(cls, v: bool) -> bool:
        """Ensure pytest is imported."""
        if not v:
            raise ValueError("Must import pytest")
        return v


class ValidationResult(ModernBaseModel):
    """Validation result for a test file.

    Attributes:
        filepath: Path to test file
        passed: Whether validation passed
        errors: List of error messages
        warnings: List of warning messages
        score: Quality score (0-100)
    """

    filepath: Path
    passed: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    score: Annotated[float, Field(ge=0.0, le=100.0)]

    @property
    def status(self) -> str:
        """Return PASS/FAIL status."""
        return "✅ PASS" if self.passed else "❌ FAIL"
