"""Track 13: vocal."""

from .base_track import BaseTrack


class Track13Vocal(BaseTrack):
    """Track 13 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 12):
        super().__init__(mcp_client, track_index)
        self.track_name = "13 - vocal"
    
    def create(self) -> "Track13Uvocal":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
