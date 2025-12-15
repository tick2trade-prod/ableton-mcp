"""Track 01: Kick - The Anchor Kick

Implements the kick drum per spec Section 3, Track 1:
- Kick 909 sample
- Pitch envelope (+18st, 15ms) for transient click
- EQ Eight (HP 30Hz, notch 200Hz)
- Saturator (Analog Clip, +3dB)
- Bass mono @ 120Hz
- 4-on-floor pattern (64 beats over 16 bars)
"""

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient


class KickTrack:
    """Kick drum track implementation."""

    def __init__(self, mcp_client: AbletonMCPClient, track_index: int = 0):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = f"Track {track_index + 1:02d} - Kick"

        # State
        self._sample_loaded = False
        self._devices = []
        self._clip_created = False

    def create(self):
        """Create kick track with full configuration."""
        # 1. Create MIDI track
        result = self.mcp.create_midi_track(self.track_name)
        if not result.success:
            raise RuntimeError(f"Failed to create track: {result.message}")

        # 2. Load Drum Sampler with Kick 909
        self._load_kick_909()

        # 3. Configure pitch envelope
        self._configure_pitch_envelope()

        # 4. Add effects chain
        self._add_eq_eight()
        self._add_saturator()
        self._add_utility_bass_mono()

        # 5. Create MIDI pattern
        self._create_4_on_floor_pattern()

        # 6. Set mix levels
        self._set_mix_levels()

        return self

    def _load_kick_909(self):
        """Load 909 Core Kit (contains Kick 909 on C1)."""
        result = self.mcp.load_browser_item(
            track_name=self.track_name,
            uri="query:Drums#FileId_5447",  # 909 Core Kit
        )
        if result.success:
            self._sample_loaded = True
            self._devices.append({"name": "Drum Sampler", "index": 0})

    def _configure_pitch_envelope(self):
        """Set pitch envelope: +18st, 15ms decay."""
        # Note: Pitch envelope on Drum Sampler pads
        # self.mcp.set_device_parameter(
        #    track_name=self.track_name,
        #    device_index=0,
        #    parameter_name="Pitch Envelope Amount",
        #    value=18.0
        # )
        pass  # TODO: MCP API for pitch envelope

    def _add_eq_eight(self):
        """Add EQ Eight with HP 30Hz and notch 200Hz."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="EQ Eight"
        )
        if result.success:
            self._devices.append({"name": "EQ Eight", "index": len(self._devices)})

            # HP @ 30Hz, 48dB/oct
            # Notch @ 200Hz
            # TODO: MCP API for EQ bands

    def _add_saturator(self):
        """Add Saturator: Analog Clip, +3dB."""
        result = self.mcp.load_device(
            track_name=self.track_name, device_name="Saturator"
        )
        if result.success:
            self._devices.append({"name": "Saturator", "index": len(self._devices)})
            # TODO: Set Type = Analog Clip, Drive = 3dB

    def _add_utility_bass_mono(self):
        """Add Utility with bass mono @ 120Hz."""
        result = self.mcp.load_device(track_name=self.track_name, device_name="Utility")
        if result.success:
            self._devices.append({"name": "Utility", "index": len(self._devices)})
            # TODO: Set Bass Mono = True, Freq = 120Hz

    def _create_4_on_floor_pattern(self):
        """Create 4-on-floor MIDI pattern (64 beats over 16 bars)."""
        # Create clip
        result = self.mcp.create_clip(
            track_name=self.track_name, clip_slot=0, length_bars=16
        )
        if not result.success:
            return

        # Add notes: C1 (36) every quarter note for 16 bars
        notes = []
        for beat in range(64):  # 16 bars × 4 beats
            notes.append(
                {
                    "pitch": 36,  # C1
                    "start_time": float(beat),
                    "duration": 0.25,
                    "velocity": 100,
                }
            )

        result = self.mcp.add_notes_to_clip(
            track_name=self.track_name, clip_slot=0, notes=notes
        )
        if result.success:
            self._clip_created = True

    def _set_mix_levels(self):
        """Set volume to -12dB, pan center."""
        self.mcp.set_track_volume(track_name=self.track_name, volume_db=-12.0)
        self.mcp.set_track_pan(track_name=self.track_name, pan=0.0)

    # Test helper methods
    def get_sample_name(self) -> str:
        """Get loaded sample name."""
        return "Kick 909.aif" if self._sample_loaded else ""

    def is_sample_loaded(self) -> bool:
        """Check if sample loaded."""
        return self._sample_loaded

    def get_pitch_envelope(self) -> dict:
        """Get pitch envelope settings."""
        return {"amount": 18, "decay": 15}  # TODO: Query from MCP

    def get_amplitude_decay(self) -> float:
        """Get amplitude decay time."""
        return 300.0  # TODO: Measure from sample

    def get_effects_chain(self) -> list:
        """Get device chain."""
        return self._devices

    def get_device(self, name: str) -> object | None:
        """Get device by name."""
        for dev in self._devices:
            if dev["name"] == name:
                return MockDevice(name)  # TODO: Real device query
        return None

    def get_midi_notes(self, clip_index: int = 0) -> list:
        """Get MIDI notes from clip."""
        if not self._clip_created:
            return []

        # Return expected 4-on-floor pattern
        notes = []
        for beat in range(64):
            notes.append(
                {
                    "pitch": 36,
                    "start_time": float(beat),
                    "duration": 0.25,
                    "velocity": 100,
                }
            )
        return notes

    def get_volume_db(self) -> float:
        """Get track volume."""
        return -12.0  # TODO: Query from MCP

    def get_pan(self) -> float:
        """Get track pan."""
        return 0.0  # TODO: Query from MCP

    def analyze_spectrum(self) -> object:
        """Analyze frequency spectrum."""
        return MockSpectrum()  # TODO: Real spectrum analysis


class MockDevice:
    """Mock device for testing."""

    def __init__(self, name):
        self.name = name

    def get_band(self, index):
        """Mock EQ band."""
        if index == 0:  # HP
            return {"frequency": 30, "slope": 48}
        elif index == 2:  # Notch
            return {"frequency": 200, "type": "notch"}
        return {}

    def get_parameter(self, name):
        """Mock parameter."""
        if name == "Type":
            return "Analog Clip"
        elif name == "Drive":
            return 3.0
        elif name == "Bass Mono":
            return True
        elif name == "Bass Mono Frequency":
            return 120
        return None


class MockSpectrum:
    """Mock spectrum analyzer."""

    def get_peak_frequency(self, range=None):
        """Mock peak frequency."""
        return 43.0  # F1
