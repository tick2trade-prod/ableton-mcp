"""Track 14: vocal fx."""

from .base_track import BaseTrack


class Track14UvocalUfx(BaseTrack):
    """Track 14 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 13):
        super().__init__(mcp_client, track_index)
        self.track_name = "14 - vocal fx"
    
    def create(self) -> "Track14UvocalUfx":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
