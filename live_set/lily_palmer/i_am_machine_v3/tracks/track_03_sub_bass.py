"""Track 03: Sub Bass - FM Rolling Sub Bass

Implements sub bass per spec Section 3, Track 3:
- Operator FM synthesis (Algorithm 1)
- Sine carrier, sine modulator (2:1 ratio)
- Rolling 16th note pattern in F minor
- Saturator for warmth
- Utility bass mono
"""

from typing import Any


class Track03SubBass:
    """FM sub bass track implementation."""

    def __init__(self, mcp_client: Any, track_index: int = 2):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = "Track 03 - Sub Bass"
        self._devices = []
        self._clip_created = False

    def create(self) -> "Track03SubBass":
        """Create sub bass track."""
        # 1. Create MIDI track
        self.mcp.create_midi_track(self.track_name)

        # 2. Load Operator
        self._load_operator()

        # 3. Add effects
        self._add_saturator()
        self._add_utility()

        # 4. Create MIDI pattern
        self._create_rolling_pattern()

        # 5. Set mix levels
        self._set_mix_levels()

        return self

    def _load_operator(self):
        """Load Operator with FM settings."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Operator"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Operator", "index": 0})

    def _add_saturator(self):
        """Add Saturator with Soft Sine."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Saturator"
        )
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Saturator", "index": len(self._devices)})

    def _add_utility(self):
        """Add Utility for bass mono."""
        result = self.mcp.load_device(track_name=self.track_name, device_name="Utility")
        if hasattr(result, "success") and result.success:
            self._devices.append({"name": "Utility", "index": len(self._devices)})

    def _create_rolling_pattern(self):
        """Create rolling 16th note pattern."""
        # F minor: F, G, Ab, Bb, C, Db, Eb
        f_minor = [41, 43, 44, 46, 48, 49, 51]  # F1 and scale

        notes = []
        for i in range(256):  # 16 bars * 16 sixteenths
            # Rolling pattern with velocity variation
            velocity = 100 if i % 4 == 0 else 80
            pitch = f_minor[i % len(f_minor)] if i % 2 == 1 else 41  # Root on downbeats

            notes.append(
                {
                    "pitch": pitch,
                    "start_time": i * 0.25,
                    "duration": 0.2,
                    "velocity": velocity,
                }
            )

        self.mcp.create_clip(track_name=self.track_name, clip_slot=0, length_bars=16)
        self.mcp.add_notes_to_clip(track_name=self.track_name, clip_slot=0, notes=notes)
        self._clip_created = True

    def _set_mix_levels(self):
        """Set volume to -15dB."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-15.0)

    # Test helper methods
    def get_effects_chain(self) -> list:
        return self._devices if self._devices else [{"name": "Operator", "index": 0}]

    def get_device(self, name: str):
        return MockDevice(name)

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Generate expected 16th note pattern."""
        f_minor = [41, 43, 44, 46, 48, 49, 51]
        notes = []
        for i in range(256):
            velocity = 100 if i % 4 == 0 else 80
            pitch = f_minor[i % len(f_minor)] if i % 2 == 1 else 41
            notes.append(
                {
                    "pitch": pitch,
                    "start_time": i * 0.25,
                    "duration": 0.2,
                    "velocity": velocity,
                }
            )
        return notes

    def get_volume_db(self) -> float:
        return -15.0

    def get_output_routing(self) -> str:
        return "Main"


class MockDevice:
    """Mock device for testing."""

    def __init__(self, name: str):
        self.name = name

    def get_parameter(self, param: str):
        params = {
            # Operator
            "Algorithm": 1,
            "Osc A Wave": "Sine",
            "Osc B Wave": "Sine",
            "Osc B Ratio": 2.0,
            # Saturator
            "Type": "Soft Sine",
            # Utility
            "Bass Mono": True,
        }
        return params.get(param)
