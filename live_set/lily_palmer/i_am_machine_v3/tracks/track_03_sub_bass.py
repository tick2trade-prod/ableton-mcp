"""Track 03: Sub Bass - FM rolling bass."""

from .base_track import BaseTrack


class Track03SubBass(BaseTrack):
    """Sub bass track with FM synthesis and rolling 16th note pattern."""

    def __init__(self, mcp_client, track_index: int = 2):
        super().__init__(mcp_client, track_index)
        self.track_name = "03 - Sub Bass"

    def create(self) -> "Track03SubBass":
        """Create sub bass track with Operator and pattern."""
        # Ensure track exists
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")

        # Route to Main (critical for audibility)
        self.route_to_main()

        # Load Operator
        self.mcp.load_browser_item(self.track_index, "query:Instruments#FileId_2374")

        # Create rolling 16th note pattern
        notes = self._generate_pattern()
        self.mcp.create_pattern(
            track_index=self.track_index,
            clip_index=0,
            clip_name="FM Rolling (F minor)",
            notes=notes,
            length=64.0,
            fire=True,
        )

        self._created = True
        return self

    def _generate_pattern(self) -> list:
        """Generate rolling 16th note pattern in F minor."""
        notes = []
        f_minor = [53, 55, 56, 58, 60, 61, 63, 65]

        for i in range(256):  # 16 bars × 4 beats × 4 sixteenths
            if i % 4 in [1, 3]:  # Off-beat 16ths
                pitch = f_minor[i % len(f_minor)]
                notes.append(
                    {
                        "pitch": pitch,
                        "start_time": i * 0.25,
                        "duration": 0.2,
                        "velocity": 90,
                    }
                )
        return notes
