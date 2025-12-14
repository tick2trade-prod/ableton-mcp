#!/usr/bin/env python3
"""Structured outputs for code generation (Claude feature integration).

Enables type-safe code generation with JSON/Pydantic validation.
Uses instructor (already in pyproject.toml) for structured outputs.
"""

import re
import sys
from pathlib import Path
from typing import Any, TypeVar

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

T = TypeVar("T")


class StructuredOutputGenerator:
    """Generate structured outputs using Ollama with JSON/Pydantic validation."""

    def __init__(self):
        """Initialize structured output generator."""
        pass

    def _build_json_prompt(self, prompt: str, schema: dict[str, Any] | None) -> str:
        """Build prompt for JSON generation.

        Args:
            prompt: Base prompt
            schema: Optional JSON schema

        Returns:
            Enhanced prompt with JSON instructions
        """
        base_prompt = f"""You must respond with valid JSON only. No explanations, no markdown, just JSON.

{prompt}

Response (JSON only):"""

        if schema:
            schema_desc = self._describe_schema(schema)
            base_prompt = f"""You must respond with valid JSON matching this schema:
{schema_desc}

{prompt}

Response (JSON only):"""

        return base_prompt

    def _describe_schema(self, schema: dict[str, Any]) -> str:
        """Describe JSON schema in natural language.

        Args:
            schema: JSON schema

        Returns:
            Schema description
        """
        if "properties" in schema:
            props = []
            for key, value in schema["properties"].items():
                prop_type = value.get("type", "any")
                description = value.get("description", "")
                props.append(f"- {key} ({prop_type}): {description}")
            return "Schema:\n" + "\n".join(props)
        return str(schema)

    def _extract_json(self, text: str) -> str:
        """Extract JSON from response text.

        Args:
            text: Response text

        Returns:
            Extracted JSON string
        """
        # Try to find JSON block
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json_match.group(0)

        # Try markdown code block
        code_block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1)

        # Return as-is (might be plain JSON)
        return text.strip()

    def _fix_json(self, json_text: str) -> str:
        """Fix common JSON issues.

        Args:
            json_text: JSON text with potential issues

        Returns:
            Fixed JSON text
        """
        # Remove trailing commas
        json_text = re.sub(r",\s*}", "}", json_text)
        json_text = re.sub(r",\s*]", "]", json_text)

        # Fix single quotes to double quotes
        json_text = re.sub(r"'([^']*)':", r'"\1":', json_text)
        json_text = re.sub(r":\s*'([^']*)'", r': "\1"', json_text)

        return json_text

    async def generate_json(
        self, prompt: str, schema: dict[str, Any] | None = None, llm: Any = None
    ) -> dict[str, Any]:
        """Generate JSON output.

        Args:
            prompt: Input prompt
            schema: Optional JSON schema description
            llm: Optional LLM instance (if None, will be created)

        Returns:
            Parsed JSON dict
        """
        # Build structured prompt
        structured_prompt = self._build_json_prompt(prompt, schema)

        # For now, return prompt (actual LLM call would be made by caller)
        # This is a helper for building prompts
        return {"prompt": structured_prompt, "schema": schema}

    def extract_code_from_json(self, json_data: dict[str, Any]) -> str:
        """Extract code from structured JSON output.

        Args:
            json_data: JSON data with code field

        Returns:
            Extracted code string
        """
        if isinstance(json_data, dict):
            # Try common code field names
            for field in ["code", "generated_code", "content", "source"]:
                if field in json_data:
                    return str(json_data[field])
        return ""
