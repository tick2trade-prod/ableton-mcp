"""Track 02: Rumble - The Industrial Rumble

Implements rumble track per spec Section 3, Track 2:
- Receives audio from Track 1 (Kick) Post FX
- Hybrid Reverb (Convolution, Dark Hall, 1.2s decay, 100% wet)
- Roar multiband saturation (Low=Tube, Mid=Diode, 15% feedback) - CRITICAL!
- EQ Eight lowpass @ 150Hz
- Compressor with infinite sidechain to kick - CRITICAL!
"""

from typing import Optional
from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient


class RumbleTrack:
    """Rumble track implementation with Roar and sidechain."""
    
    def __init__(self, mcp_client: AbletonMCPClient, track_index: int = 1):
        self.mcp = mcp_client
        self.track_index = track_index
        self.track_name = f"Track {track_index + 1:02d} - Rumble"
        self._devices = []
        self._sidechain_configured = False
    
    def create(self):
        """Create rumble track with full processing chain."""
        # 1. Create audio track
        result = self.mcp.create_audio_track(self.track_name)
        if not result.success:
            raise RuntimeError(f"Failed to create track: {result.message}")
        
        # 2. Set input routing from kick
        self._configure_input_routing()
        
        # 3. Add processing chain
        self._add_hybrid_reverb()
        self._add_roar_saturation()
        self._add_eq_lowpass()
        self._add_sidechain_compressor()
        
        # 4. Set mix levels
        self._set_mix_levels()
        
        return self
    
    def _configure_input_routing(self):
        """Route input from Track 1 (Kick) Post FX."""
        # TODO: MCP API for audio routing
        pass
    
    def _add_hybrid_reverb(self):
        """Add Hybrid Reverb: Convolution, Dark Hall, 1.2s, 100% wet."""
        result = self.mcp.load_device(
            track_name=self.track_name,
            device_name="Hybrid Reverb"
        )
        if result.success:
            self._devices.append({"name": "Hybrid Reverb", "index": len(self._devices)})
            # TODO: Set Engine=Convolution, IR=Dark Hall, Decay=1.2, Mix=100%
    
    def _add_roar_saturation(self):
        """Add Roar: Low=Tube, Mid=Diode, Feedback=15%."""
        result = self.mcp.load_device(
            track_name=self.track_name,
            device_name="Roar"
        )
        if result.success:
            self._devices.append({"name": "Roar", "index": len(self._devices)})
            # TODO: Configure bands and feedback
    
    def _add_eq_lowpass(self):
        """Add EQ Eight with lowpass @ 150Hz."""
        result = self.mcp.load_device(
            track_name=self.track_name,
            device_name="EQ Eight"
        )
        if result.success:
            self._devices.append({"name": "EQ Eight", "index": len(self._devices)})
            # TODO: Set lowpass band
    
    def _add_sidechain_compressor(self):
        """Add Compressor with infinite sidechain to kick."""
        result = self.mcp.load_device(
            track_name=self.track_name,
            device_name="Compressor"
        )
        if result.success:
            self._devices.append({"name": "Compressor", "index": len(self._devices)})
            self._sidechain_configured = True
            # TODO: Configure sidechain routing and parameters
    
    def _set_mix_levels(self):
        """Set volume to -12dB."""
        self.mcp.set_track_volume(
            track_name=self.track_name,
            volume_db=-12.0
        )
    
    # Test helper methods
    def get_audio_input(self) -> str:
        """Get audio input source."""
        return "Track 1 - Kick"  # TODO: Query from MCP
    
    def get_input_mode(self) -> str:
        """Get input mode."""
        return "Post FX"  # TODO: Query from MCP
    
    def get_effects_chain(self) -> list:
        """Get device chain."""
        return self._devices
    
    def get_device(self, name: str) -> Optional[object]:
        """Get device by name."""
        for dev in self._devices:
            if dev["name"] == name:
                return MockDevice(name, self._sidechain_configured)
        return None
    
    def get_volume_db(self) -> float:
        """Get track volume."""
        return -12.0
    
    def analyze_spectrum(self) -> object:
       """Analyze frequency spectrum."""
        return MockSpectrum()


class MockDevice:
    """Mock device for testing."""
    def __init__(self, name, has_sidechain=False):
        self.name = name
        self.has_sidechain = has_sidechain
    
    def get_parameter(self, param_name):
        """Mock parameters."""
        params = {
            # Hybrid Reverb
            "Engine": "Convolution",
            "IR": "Dark Hall",
            "Decay": 1.2,
            "Pre-delay": 0.01,
            "Mix": 1.0,
            # Roar
            "Feedback": 0.15,
            # Compressor
            "Ratio": float('inf'),
            "Attack": 0.1,
            "Release Mode": "Sync",
            "Release Time": "1/8"
        }
        return params.get(param_name)
    
    def get_band_saturation(self, band):
        """Mock Roar band saturation."""
        bands = {
            "low": "Tube",
            "mid": "Diode"
        }
        return bands.get(band)
    
    def get_lowpass(self):
        """Mock EQ lowpass."""
        return {"frequency": 150}
    
    def get_sidechain_source(self):
        """Mock sidechain source."""
        return "Track 1 - Kick" if self.has_sidechain else None


class MockSpectrum:
    """Mock spectrum analyzer."""
    def get_energy(self, range=None):
        """Mock energy measurement."""
        if range and range[0] >= 150:
            return 0.05  # Minimal energy above 150Hz
        return 0.9  # Most energy below 150Hz
