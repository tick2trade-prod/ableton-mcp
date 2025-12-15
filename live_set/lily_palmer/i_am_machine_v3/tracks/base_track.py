"""Base track class for I Am Machine V3.

All track implementations inherit from this base class.
"""

from typing import Any


class BaseTrack:
    """Base class for all tracks in the 16-bar intro loop."""

    def __init__(self, mcp_client: Any, track_index: int):
        """Initialize track with MCP client and index.

        Args:
            mcp_client: AbletonMCPClient instance for communication
            track_index: Index of this track (0-15)
        """
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = f"Track {track_index + 1:02d}"
        self._created = False
        self._output_routed = False

    def create(self) -> "BaseTrack":
        """Create the track in Ableton. Must be implemented by subclass."""
        raise NotImplementedError

    def route_to_main(self) -> bool:
        """Route track output to Main.

        Returns:
            True if routing successful, False otherwise
        """
        result = self.mcp.set_track_output(self.track_index, "Main")
        self._output_routed = result.success
        return result.success

    def get_output_routing(self) -> str:
        """Get the current output routing.

        Returns:
            Output routing (e.g., "Main", "No Output")
        """
        info = self.mcp.get_track_info(self.track_index)
        if info.success:
            return info.data.get("output_routing", "Unknown")
        return "Unknown"

    def is_audible(self) -> bool:
        """Check if track is audible (routed to Main).

        Returns:
            True if track output is routed to Main
        """
        return self.get_output_routing() == "Main"
