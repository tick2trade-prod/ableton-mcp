"""Track 06: open hat."""

from .base_track import BaseTrack


class Track06OpenHat(BaseTrack):
    """Track 06 implementation."""
    
    def __init__(self, mcp_client, track_index: int = 5):
        super().__init__(mcp_client, track_index)
        self.track_name = "06 - open hat"
    
    def create(self) -> "Track06UopenUhat":
        """Create track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()
        self._created = True
        return self
