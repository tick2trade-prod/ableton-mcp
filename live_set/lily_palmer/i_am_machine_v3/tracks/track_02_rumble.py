#!/usr/bin/env python3
"""Track 02: Rumble - The Industrial Rumble

Creates an audio track that:
- Receives audio from Track 01 (Kick) Post FX
- Processes through: Hybrid Reverb → Roar → EQ Eight → Compressor
- Sidechains to kick for pumping effect

Usage:
    uv run python live_set/lily_palmer/i_am_machine_v3/tracks/track_02_rumble.py

After running, manually configure in Ableton:
    1. Audio From: 01 - Kick → Post FX
    2. Monitor: In
    3. Compressor: Sidechain → 01 - Kick
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

# Track configuration
TRACK_INDEX = 1
TRACK_NAME = "02 - Rumble"
TRACK_TYPE = "audio"

# Device chain in order
DEVICES = [
    "Hybrid Reverb",  # Creates the reverb tail from kick
    "Roar",  # Multiband saturation for industrial texture (or Saturator)
    "EQ Eight",  # Lowpass @ 150Hz to contain rumble
    "Compressor",  # Sidechain to kick for pumping
]

# Fallbacks if premium devices not available
DEVICE_FALLBACKS = {
    "Hybrid Reverb": "Reverb",
    "Roar": "Saturator",
}


class RumbleTrack:
    """Rumble track - creates actual configuration in Ableton."""

    def __init__(self, mcp_client: AbletonMCPClient = None):
        self.mcp = mcp_client or AbletonMCPClient()
        self.track_index = TRACK_INDEX
        self.track_name = TRACK_NAME

    def create(self) -> bool:
        """Create and configure the rumble track in Ableton.

        Returns:
            True if track was configured successfully
        """
        print(f"🌊 Creating {TRACK_NAME}")
        print("=" * 50)

        # 1. Verify connection
        info = self.mcp.get_session_info()
        if not info.success:
            print(f"❌ Cannot connect to Ableton: {info.message}")
            return False
        print(f"✅ Connected at {info.data.get('tempo')} BPM")

        # 2. Ensure audio track exists
        print(f"\n1. Ensuring audio track at index {TRACK_INDEX}...")
        result = self.mcp.ensure_track(TRACK_INDEX, TRACK_NAME, TRACK_TYPE)
        if not result.success:
            print(f"   ❌ Failed: {result.message}")
            return False
        print(f"   ✓ Audio track '{TRACK_NAME}' ready")

        # 3. Load device chain
        print("\n2. Loading device chain...")
        self._load_devices()

        # 4. Print manual setup instructions
        self._print_manual_setup()

        return True

    def _load_devices(self):
        """Load the device chain onto the track."""
        for device in DEVICES:
            fallback = DEVICE_FALLBACKS.get(device)
            result = self.mcp.load_device(
                track_index=TRACK_INDEX,
                device_name=device,
                fallback=fallback,
            )
            if result.success:
                print(f"   ✓ {device}")
            elif fallback:
                print(f"   ↳ {fallback} (fallback)")
            else:
                print(f"   ✗ {device}: {result.message}")

    def _print_manual_setup(self):
        """Print instructions for manual configuration."""
        print("\n" + "=" * 50)
        print("📝 MANUAL SETUP REQUIRED:")
        print("=" * 50)
        print()
        print("1. AUDIO ROUTING:")
        print("   Audio From: '01 - Kick'")
        print("   Audio From Channel: Post FX")
        print("   Monitor: In")
        print()
        print("2. HYBRID REVERB (or Reverb):")
        print("   Engine: Convolution (or Large Hall)")
        print("   Decay: 1.2s")
        print("   Pre-delay: 10ms")
        print("   Mix: 100% Wet")
        print()
        print("3. ROAR (or Saturator):")
        print("   Low Band: Tube saturation")
        print("   Mid Band: Diode clipping")
        print("   Feedback: 15%")
        print()
        print("4. EQ EIGHT:")
        print("   Enable Band 8 as Lowpass")
        print("   Frequency: 150Hz")
        print("   Slope: 24dB/oct")
        print()
        print("5. COMPRESSOR (CRITICAL!):")
        print("   Click 'Sidechain' button")
        print("   Audio From: '01 - Kick'")
        print("   Ratio: Inf:1")
        print("   Attack: 0.1ms")
        print("   Release: 1/8 (sync)")
        print()
        print("=" * 50)
        print("✅ Run tests to verify configuration:")
        print("   uv run pytest tests/i_am_machine_v3/unit/test_track_02_rumble.py -v")
        print("=" * 50)


def main():
    """Main entry point."""
    track = RumbleTrack()
    success = track.create()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
