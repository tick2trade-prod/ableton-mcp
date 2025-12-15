"""Track 08: tom."""

from .base_track import BaseTrack


class Track08Tom(BaseTrack):
    """Track 08 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 7):
        super().__init__(mcp_client, track_index)
        self.track_name = "08 - tom"
    
    def create(self) -> "Track08Utom":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
