"""Base models for validation (Pydantic 2.x).

Version: 1.0.0
"""

from pydantic import BaseModel, ConfigDict


class ModernBaseModel(BaseModel):
    """Base model with Pydantic 2.x configuration.

    Applies consistent configuration across all validation models.
    Future-proof for Pydantic 3.0.
    """

    model_config = ConfigDict(
        # Pydantic 2.x: use model_config instead of Config class
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
        # Future-proof for Pydantic 3.0
        use_attribute_docstrings=True,
        arbitrary_types_allowed=False,
        # Serialization
        ser_json_timedelta="float",
        ser_json_bytes="base64",
    )
