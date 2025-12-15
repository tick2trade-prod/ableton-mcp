"""Track 09: glitch."""

from .base_track import BaseTrack


class Track09Glitch(BaseTrack):
    """Track 09 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 8):
        super().__init__(mcp_client, track_index)
        self.track_name = "09 - glitch"
    
    def create(self) -> "Track09Uglitch":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
