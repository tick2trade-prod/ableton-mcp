"""Track 04: Acid - 303-style acid line."""

from .base_track import BaseTrack


class Track04Acid(BaseTrack):
    """Acid track with Drift synth and acid pattern."""

    def __init__(self, mcp_client, track_index: int = 3):
        super().__init__(mcp_client, track_index)
        self.track_name = "04 - Acid"

    def create(self) -> "Track04Acid":
        """Create acid track."""
        self.mcp.ensure_track(self.track_index, self.track_name, "midi")
        self.route_to_main()

        # Load synth and create pattern
        notes = self._generate_pattern()
        self.mcp.create_pattern(
            track_index=self.track_index,
            clip_index=0,
            clip_name="Acid Line (F minor)",
            notes=notes,
            length=64.0,
            fire=True,
        )

        self._created = True
        return self

    def _generate_pattern(self) -> list:
        """Generate 303-style acid pattern."""
        notes = []
        f_minor = [53, 55, 56, 58, 60, 61, 63, 65]

        for bar in range(16):
            for beat in range(4):
                for sixteenth in range(4):
                    if sixteenth % 2 == 0:
                        pitch = f_minor[(bar * 4 + beat) % len(f_minor)]
                        time = bar * 4 + beat + sixteenth * 0.25
                        notes.append(
                            {
                                "pitch": pitch,
                                "start_time": time,
                                "duration": 0.2,
                                "velocity": 100,
                            }
                        )
        return notes
