"""Track 05: closed hat."""

from .base_track import BaseTrack


class Track05UclosedUhat(BaseTrack):
    """Track 05 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 4):
        super().__init__(mcp_client, track_index)
        self.track_name = "05 - closed hat"
    
    def create(self) -> "Track05UclosedUhat":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
