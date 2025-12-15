#!/usr/bin/env python3
"""AST-based code generation for Ableton MCP tool calls.

Parses existing track scripts to extract patterns and generates
new code based on track specifications.
"""

import ast
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("ableton-codegen-generator")


class MCPToolCall:
    """Represents an extracted MCP tool call."""

    def __init__(
        self,
        tool_name: str,
        args: dict[str, Any],
        line_number: int,
        context: str = "",
    ):
        self.tool_name = tool_name
        self.args = args
        self.line_number = line_number
        self.context = context

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_name": self.tool_name,
            "args": self.args,
            "line_number": self.line_number,
            "context": self.context,
        }


class TrackPattern:
    """Pattern extracted from a track script."""

    def __init__(
        self,
        track_type: str,
        track_name: str,
        tool_calls: list[MCPToolCall],
        source_file: str,
    ):
        self.track_type = track_type
        self.track_name = track_name
        self.tool_calls = tool_calls
        self.source_file = source_file

    def to_dict(self) -> dict[str, Any]:
        return {
            "track_type": self.track_type,
            "track_name": self.track_name,
            "tool_calls": [tc.to_dict() for tc in self.tool_calls],
            "source_file": self.source_file,
        }


# Known MCP tools from MCP_Server/server.py
MCP_TOOLS = [
    "get_session_info",
    "get_track_info",
    "create_midi_track",
    "delete_track",
    "set_track_name",
    "create_clip",
    "add_notes_to_clip",
    "set_clip_name",
    "duplicate_clip",
    "empty_clip_slot",
    "relocate_clip",
    "set_tempo",
    "play",
    "stop",
    "fire_clip",
    "stop_clip",
    "get_clip_info",
    "load_device",
    "set_device_parameter",
    "get_device_parameters",
]

# Track type detection patterns (order matters - more specific first)
TRACK_TYPE_PATTERNS = [
    ("kick", ["kick", "bd", "bass drum"]),
    ("snare", ["snare", "sd", "clap"]),
    ("hihat", ["hihat", "hi-hat", "hh", "hat"]),
    ("bass", ["bass", "sub", "low"]),
    ("lead", ["lead", "synth", "melody"]),
    ("pad", ["pad", "atmosphere", "drone"]),
    ("fx", ["fx", "effect", "riser", "impact"]),
    ("vocal", ["vocal", "vox", "voice"]),
    ("percussion", ["perc", "percussion", "tom", "ride"]),
]


class AbletonCodeGenerator:
    """Generate Ableton MCP tool call sequences."""

    def __init__(
        self,
        scripts_dir: str | Path = "live_set/lily_palmer/i_am_machine",
        mcp_server_path: str | Path = "MCP_Server/server.py",
    ):
        self.scripts_dir = Path(scripts_dir)
        self.mcp_server_path = Path(mcp_server_path)
        self._patterns_cache: list[TrackPattern] = []

    def extract_tool_calls(self, source_code: str) -> list[MCPToolCall]:
        """Extract MCP tool calls from Python source code.

        Args:
            source_code: Python source code string

        Returns:
            List of MCPToolCall objects
        """
        tool_calls = []
        seen_lines = set()  # Avoid duplicates from await expressions

        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            logger.warning(f"Failed to parse source: {e}")
            return tool_calls

        for node in ast.walk(tree):
            call_node = None

            # Look for await expressions first (async calls)
            if isinstance(node, ast.Await):
                if isinstance(node.value, ast.Call):
                    call_node = node.value
            # Then look for direct function calls
            elif isinstance(node, ast.Call):
                call_node = node

            if call_node:
                func_name = self._get_func_name(call_node)
                line_num = call_node.lineno

                # Skip if not an MCP tool or already seen this line
                if func_name in MCP_TOOLS and line_num not in seen_lines:
                    args = self._extract_call_args(call_node)
                    tool_calls.append(
                        MCPToolCall(
                            tool_name=func_name,
                            args=args,
                            line_number=line_num,
                        )
                    )
                    seen_lines.add(line_num)

        return tool_calls

    def _get_func_name(self, node: ast.Call) -> str:
        """Extract function name from Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""

    def _extract_call_args(self, node: ast.Call) -> dict[str, Any]:
        """Extract arguments from a Call node."""
        args = {}

        # Positional args
        for i, arg in enumerate(node.args):
            args[f"arg_{i}"] = self._ast_to_value(arg)

        # Keyword args
        for kw in node.keywords:
            if kw.arg:
                args[kw.arg] = self._ast_to_value(kw.value)

        return args

    def _ast_to_value(self, node: ast.expr) -> Any:
        """Convert AST node to Python value."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python 3.7 compatibility
            return node.n
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.List):
            return [self._ast_to_value(el) for el in node.elts]
        elif isinstance(node, ast.Dict):
            return {
                self._ast_to_value(k): self._ast_to_value(v)
                for k, v in zip(node.keys, node.values, strict=False)
                if k is not None
            }
        elif isinstance(node, ast.Name):
            return f"${node.id}"  # Variable reference
        return "<complex>"

    def detect_track_type(self, filename: str, content: str = "") -> str:
        """Detect track type from filename or content."""
        filename_lower = filename.lower()
        content_lower = content.lower() if content else ""

        # Check patterns in order (more specific first)
        for track_type, patterns in TRACK_TYPE_PATTERNS:
            for pattern in patterns:
                if pattern in filename_lower or pattern in content_lower:
                    return track_type

        return "unknown"

    async def analyze_script(self, script_path: str | Path) -> TrackPattern:
        """Analyze a track script and extract patterns.

        Args:
            script_path: Path to Python script

        Returns:
            TrackPattern object
        """
        path = Path(script_path)
        if not path.exists():
            raise FileNotFoundError(f"Script not found: {path}")

        source = path.read_text()
        tool_calls = self.extract_tool_calls(source)

        # Detect track type
        track_type = self.detect_track_type(path.name, source)

        # Extract track name from filename
        track_name = path.stem.replace("track_", "").replace("_", " ").title()

        return TrackPattern(
            track_type=track_type,
            track_name=track_name,
            tool_calls=tool_calls,
            source_file=str(path),
        )

    async def analyze_all_scripts(self) -> list[TrackPattern]:
        """Analyze all track scripts in the scripts directory.

        Returns:
            List of TrackPattern objects
        """
        if not self.scripts_dir.exists():
            logger.warning(f"Scripts directory not found: {self.scripts_dir}")
            return []

        patterns = []
        for script_file in self.scripts_dir.glob("track_*.py"):
            try:
                pattern = await self.analyze_script(script_file)
                patterns.append(pattern)
                logger.info(
                    f"Analyzed {script_file.name}: {len(pattern.tool_calls)} tool calls"
                )
            except Exception as e:
                logger.error(f"Failed to analyze {script_file}: {e}")

        self._patterns_cache = patterns
        return patterns

    def find_similar_patterns(
        self,
        track_type: str,
        patterns: list[TrackPattern] | None = None,
    ) -> list[TrackPattern]:
        """Find patterns matching the given track type.

        Args:
            track_type: Type of track to match
            patterns: Optional list of patterns (uses cache if None)

        Returns:
            List of matching TrackPattern objects
        """
        patterns = patterns or self._patterns_cache
        return [p for p in patterns if p.track_type == track_type]

    def generate_track_code(
        self,
        track_spec: dict[str, Any],
        reference_pattern: TrackPattern | None = None,
    ) -> str:
        """Generate Python code for creating a track.

        Args:
            track_spec: Track specification dict with:
                - name: Track name
                - type: Track type (kick, snare, etc.)
                - index: Track index
                - devices: List of devices to load
                - notes: Optional note data
            reference_pattern: Optional pattern to base code on

        Returns:
            Generated Python code string
        """
        track_name = track_spec.get("name", "New Track")
        track_index = track_spec.get("index", -1)
        track_type = track_spec.get("type", "unknown")
        devices = track_spec.get("devices", [])
        notes = track_spec.get("notes", [])

        lines = [
            '"""Auto-generated track creation script."""',
            "",
            "import asyncio",
            "from MCP_Server.server import (",
            "    create_midi_track,",
            "    set_track_name,",
            "    create_clip,",
            "    add_notes_to_clip,",
            "    load_device,",
            "    set_device_parameter,",
            ")",
            "",
            "",
            f"async def create_{track_type}_track():",
            f'    """Create {track_name} track."""',
            "",
            f"    # Create track at index {track_index}",
            f"    await create_midi_track(index={track_index})",
            f'    await set_track_name(track_index={track_index}, name="{track_name}")',
            "",
        ]

        # Add device loading
        if devices:
            lines.append("    # Load devices")
            for device in devices:
                device_name = device.get("name", "Unknown")
                lines.append(
                    f"    await load_device(track_index={track_index}, "
                    f'device_name="{device_name}")'
                )

                # Add device parameters
                for param, value in device.get("parameters", {}).items():
                    lines.append(
                        f"    await set_device_parameter("
                        f"track_index={track_index}, "
                        f"device_index=0, "
                        f'parameter_name="{param}", '
                        f"value={value})"
                    )
            lines.append("")

        # Add clip creation
        lines.extend(
            [
                "    # Create clip",
                f"    await create_clip(track_index={track_index}, clip_index=0, length=4.0)",
                "",
            ]
        )

        # Add notes if provided
        if notes:
            lines.append("    # Add notes")
            lines.append(f"    notes = {notes}")
            lines.append(
                f"    await add_notes_to_clip("
                f"track_index={track_index}, clip_index=0, notes=notes)"
            )
            lines.append("")

        # Add main block
        lines.extend(
            [
                "",
                'if __name__ == "__main__":',
                f"    asyncio.run(create_{track_type}_track())",
            ]
        )

        return "\n".join(lines)

    async def validate_code(self, code: str) -> dict[str, Any]:
        """Validate generated code.

        Args:
            code: Python code string

        Returns:
            dict with validation results
        """
        errors = []
        warnings = []

        # Syntax check
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"Syntax error: {e}")

        # Check for required imports
        if "create_midi_track" not in code:
            warnings.append("Missing create_midi_track import")

        # Check for MCP tool usage
        tool_calls = self.extract_tool_calls(code)
        if not tool_calls:
            warnings.append("No MCP tool calls detected")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "tool_calls_count": len(tool_calls),
        }
