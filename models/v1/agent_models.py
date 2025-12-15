"""Agent validation models (Pydantic 2.x).

Version: 1.0.0

Models for validating agent file structure, docstrings, type hints, and error handling.
"""

from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator

from .base import ModernBaseModel
from .test_models import AbletonReference


class AgentMethod(ModernBaseModel):
    """Agent method validation.

    Validates individual methods for:
    - Naming convention (snake_case)
    - Docstring presence
    - Type hints on all parameters
    - Returns AgentResult
    - Async/await usage for MCP calls
    - Handles None MCP client
    """

    name: Annotated[str, Field(pattern=r"^[a-z_][a-z0-9_]*$")]
    has_docstring: bool
    has_type_hints: bool
    returns_agent_result: bool
    is_async: bool
    references: list[AbletonReference] = Field(default_factory=list, max_length=3)
    handles_none_mcp: bool = Field(default=False)
    has_error_handling: bool = Field(default=False)

    @field_validator("name")
    @classmethod
    def validate_snake_case(cls, v: str) -> str:
        """Ensure method name follows snake_case convention."""
        if (
            not v.islower()
            or not v.replace("_", "")
            .replace("0", "")
            .replace("1", "")
            .replace("2", "")
            .replace("3", "")
            .replace("4", "")
            .replace("5", "")
            .replace("6", "")
            .replace("7", "")
            .replace("8", "")
            .replace("9", "")
            .isalpha()
        ):
            raise ValueError(f"Method name must be snake_case: {v}")
        return v


class AgentClass(ModernBaseModel):
    """Agent class validation.

    Validates agent classes for:
    - Naming convention (*Agent)
    - Inherits from BaseAgent
    - Required methods (get_role, get_goal, execute)
    - Manual references in docstring
    """

    name: Annotated[str, Field(pattern=r"^[A-Z][a-zA-Z]+Agent$")]
    inherits_base_agent: bool
    has_get_role: bool
    has_get_goal: bool
    has_execute: bool
    methods: list[AgentMethod] = Field(default_factory=list)
    manual_references: list[AbletonReference] = Field(
        default_factory=list, max_length=5
    )
    has_docstring: bool = True


class AgentModule(ModernBaseModel):
    """Agent module validation."""

    filepath: Path
    filename: Annotated[str, Field(pattern=r"^[a-z_]+_agent\.py$")]
    has_docstring: bool
    manual_references: list[AbletonReference] = Field(default_factory=list)
    imports_base_agent: bool
    agent_class: AgentClass


class AgentValidationResult(ModernBaseModel):
    """Agent file validation result.

    Includes weighted scoring:
    - Documentation: 30%
    - Type Safety: 25%
    - Error Handling: 20%
    - Structure: 15%
    - Code Quality: 10%
    """

    filepath: Path
    passed: bool
    score: Annotated[float, Field(ge=0.0, le=100.0)]
    documentation_score: float = 0.0
    type_safety_score: float = 0.0
    error_handling_score: float = 0.0
    structure_score: float = 0.0
    code_quality_score: float = 0.0
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @property
    def status(self) -> str:
        """Return PASS/FAIL status."""
        return "✅ PASS" if self.passed else "❌ FAIL"
