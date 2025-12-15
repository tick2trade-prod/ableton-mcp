"""Ableton MCP Integration Agent - Debug and verify MCP commands.

This agent understands the Ableton Remote Script and MCP Server architecture,
can read Ableton logs for debugging, and verifies that commands actually
work in the DAW.

Key Capabilities:
- Verify track state by querying actual DAW
- Read and parse Ableton log files for errors
- Diagnose why commands fail
- List available Remote Script commands
- Execute raw commands for testing

Reference:
- Remote Script: AbletonMCP_Remote_Script/__init__.py
- MCP Server: MCP_Server/server.py
- Log Location: ~/Library/Preferences/Ableton/Live 12.*/Log.txt
"""

from pathlib import Path

from .base_agent import AgentResult, BaseAgent


class AbletonMCPIntegrationAgent(BaseAgent):
    """Agent for debugging and verifying MCP integration with Ableton."""

    # Known commands from Remote Script
    AVAILABLE_COMMANDS = [
        # Session
        "get_session_info",
        "set_tempo",
        "start_playback",
        "stop_playback",
        # Tracks
        "create_midi_track",
        "create_audio_track",
        "delete_track",
        "set_track_name",
        "get_track_info",
        "set_track_volume",
        "set_track_output",
        # Clips
        "create_clip",
        "add_notes_to_clip",
        "set_clip_name",
        "fire_clip",
        "stop_clip",
        # Devices
        "load_browser_item",
        "get_device_parameters",
        "set_device_parameter",
        # Racks
        "create_audio_effect_rack",
        "create_rack_chain",
        # Browser
        "get_browser_tree",
        "get_browser_items",
    ]

    # Default log path pattern
    LOG_PATH_PATTERN = "~/Library/Preferences/Ableton/Live 12.*/Log.txt"

    def __init__(self, **kwargs):
        super().__init__(name="AbletonMCPIntegrationAgent", **kwargs)
        self._log_path = None

    def get_role(self) -> str:
        return "MCP Integration Engineer"

    def get_goal(self) -> str:
        return "Debug and verify Ableton MCP commands work correctly in the DAW"

    def verify_connection(self) -> AgentResult:
        """Verify connection to Ableton via MCP.

        Returns:
            AgentResult with connection status and session info
        """
        mcp = self.get_mcp_client()
        if not mcp:
            return AgentResult(
                success=False,
                message="Could not create MCP client",
                errors=["AbletonMCPClient not available"],
            )

        try:
            result = mcp.get_session_info()
            if result.success:
                self.log(f"Connected! Tempo: {result.data.get('tempo')} BPM")
                return AgentResult(
                    success=True,
                    message="Connected to Ableton Live",
                    data=result.data,
                )
            else:
                return AgentResult(
                    success=False,
                    message=f"Connection failed: {result.message}",
                    errors=[result.message],
                )
        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Connection error: {e}",
                errors=[str(e)],
            )

    def verify_track_state(self, track_index: int) -> AgentResult:
        """Query actual track info from Ableton DAW.

        Args:
            track_index: Index of track to verify (0-based)

        Returns:
            AgentResult with track info or errors
        """
        mcp = self.get_mcp_client()
        if not mcp:
            return AgentResult(
                success=False,
                message="MCP client not available",
            )

        try:
            result = mcp.send_command("get_track_info", {"track_index": track_index})
            if result.success:
                self.log(f"Track {track_index}: {result.data.get('name', 'Unknown')}")
                return AgentResult(
                    success=True,
                    message=f"Track {track_index} verified",
                    data=result.data,
                )
            else:
                return AgentResult(
                    success=False,
                    message=f"Failed to get track info: {result.message}",
                    errors=[result.message],
                )
        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Error verifying track: {e}",
                errors=[str(e)],
            )

    def _find_log_path(self) -> Path | None:
        """Find the Ableton log file path."""
        if self._log_path:
            return self._log_path

        # Expand ~ and glob for version
        home = Path.home()
        prefs_dir = home / "Library" / "Preferences" / "Ableton"

        if not prefs_dir.exists():
            return None

        # Find latest Live version directory
        live_dirs = sorted(prefs_dir.glob("Live 12.*"), reverse=True)
        if not live_dirs:
            live_dirs = sorted(prefs_dir.glob("Live *"), reverse=True)

        if live_dirs:
            log_path = live_dirs[0] / "Log.txt"
            if log_path.exists():
                self._log_path = log_path
                return log_path

        return None

    def read_ableton_log(self, lines: int = 50) -> AgentResult:
        """Read recent entries from Ableton Log.txt.

        Args:
            lines: Number of recent lines to read (default 50)

        Returns:
            AgentResult with log content or error
        """
        log_path = self._find_log_path()
        if not log_path:
            return AgentResult(
                success=False,
                message="Could not find Ableton Log.txt",
                errors=[
                    "Log file not found at ~/Library/Preferences/Ableton/Live */Log.txt"
                ],
            )

        try:
            with open(log_path) as f:
                all_lines = f.readlines()
                recent = all_lines[-lines:] if len(all_lines) > lines else all_lines
                content = "".join(recent)

            self.log(f"Read {len(recent)} lines from {log_path}")
            return AgentResult(
                success=True,
                message=f"Read {len(recent)} lines from Ableton log",
                data={
                    "log_path": str(log_path),
                    "content": content,
                    "lines_read": len(recent),
                },
            )
        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Error reading log: {e}",
                errors=[str(e)],
            )

    def diagnose_command_failure(
        self,
        command: str,
        error: str,
        check_log: bool = True,
    ) -> AgentResult:
        """Analyze why an MCP command failed.

        Args:
            command: The command that failed
            error: The error message received
            check_log: Whether to check Ableton log for details

        Returns:
            AgentResult with diagnosis and suggestions
        """
        diagnosis = []
        suggestions = []

        # Check if command is known
        if command not in self.AVAILABLE_COMMANDS:
            diagnosis.append(f"Command '{command}' is not in known commands list")
            # Find similar commands
            similar = [
                c for c in self.AVAILABLE_COMMANDS if command.lower() in c.lower()
            ]
            if similar:
                suggestions.append(f"Did you mean: {', '.join(similar)}?")

        # Common error patterns
        if "Connection refused" in error or "socket" in error.lower():
            diagnosis.append("Socket connection issue - Ableton may not be running")
            suggestions.append("1. Ensure Ableton Live is running")
            suggestions.append("2. Check AbletonMCP is selected as Control Surface")
            suggestions.append("3. Restart Ableton if Remote Script was updated")

        if "track_index" in error.lower() or "out of range" in error.lower():
            diagnosis.append("Track index issue - track may not exist")
            suggestions.append("Use get_session_info to check track count")

        if "Unknown command" in error:
            diagnosis.append("Command not implemented in Remote Script")
            suggestions.append(
                "Check AbletonMCP_Remote_Script/__init__.py for supported commands"
            )

        # Check Ableton log if requested
        log_excerpt = ""
        if check_log:
            log_result = self.read_ableton_log(lines=20)
            if log_result.success:
                log_excerpt = log_result.data.get("content", "")
                # Look for Python errors
                if "Traceback" in log_excerpt or "Error" in log_excerpt:
                    diagnosis.append("Found errors in Ableton log")

        return AgentResult(
            success=True,
            message=f"Diagnosis for '{command}' failure",
            data={
                "command": command,
                "original_error": error,
                "diagnosis": diagnosis,
                "suggestions": suggestions,
                "log_excerpt": log_excerpt[-500:] if log_excerpt else "",
            },
        )

    def get_available_commands(self) -> AgentResult:
        """List all available Remote Script commands.

        Returns:
            AgentResult with command list
        """
        return AgentResult(
            success=True,
            message=f"{len(self.AVAILABLE_COMMANDS)} commands available",
            data={"commands": self.AVAILABLE_COMMANDS},
        )

    def execute_raw_command(
        self,
        command: str,
        params: dict | None = None,
    ) -> AgentResult:
        """Execute a raw MCP command for testing.

        Args:
            command: Command type to send
            params: Optional parameters

        Returns:
            AgentResult with command response
        """
        mcp = self.get_mcp_client()
        if not mcp:
            return AgentResult(
                success=False,
                message="MCP client not available",
            )

        try:
            result = mcp.send_command(command, params or {})
            self.log(f"Command '{command}': {'OK' if result.success else 'FAILED'}")
            return AgentResult(
                success=result.success,
                message=result.message,
                data=result.data if hasattr(result, "data") else {},
            )
        except Exception as e:
            # Diagnose the failure
            diagnosis = self.diagnose_command_failure(command, str(e))
            return AgentResult(
                success=False,
                message=f"Command failed: {e}",
                data=diagnosis.data,
                errors=[str(e)],
            )

    async def execute(self, **kwargs) -> AgentResult:
        """Execute integration check workflow.

        Args:
            mode: "verify", "diagnose", "log", or "commands"
            track_index: For verify mode
            command: For diagnose mode
            error: For diagnose mode

        Returns:
            AgentResult based on mode
        """
        mode = kwargs.get("mode", "verify")

        if mode == "verify":
            # First check connection
            conn = self.verify_connection()
            if not conn.success:
                return conn

            # Then check specific track if requested
            track_index = kwargs.get("track_index")
            if track_index is not None:
                return self.verify_track_state(track_index)
            return conn

        elif mode == "diagnose":
            command = kwargs.get("command", "")
            error = kwargs.get("error", "")
            return self.diagnose_command_failure(command, error)

        elif mode == "log":
            lines = kwargs.get("lines", 50)
            return self.read_ableton_log(lines)

        elif mode == "commands":
            return self.get_available_commands()

        else:
            return AgentResult(
                success=False,
                message=f"Unknown mode: {mode}",
                errors=["Valid modes: verify, diagnose, log, commands"],
            )
