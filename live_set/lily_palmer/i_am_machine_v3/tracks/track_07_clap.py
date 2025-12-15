"""Track 07: clap."""

from .base_track import BaseTrack


class Track07Uclap(BaseTrack):
    """Track 07 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 6):
        super().__init__(mcp_client, track_index)
        self.track_name = "07 - clap"
    
    def create(self) -> "Track07Uclap":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
