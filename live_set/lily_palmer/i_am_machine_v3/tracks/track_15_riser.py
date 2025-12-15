"""Track 15: riser."""

from .base_track import BaseTrack


class Track15Uriser(BaseTrack):
    """Track 15 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 14):
        super().__init__(mcp_client, track_index)
        self.track_name = "15 - riser"
    
    def create(self) -> "Track15Uriser":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
