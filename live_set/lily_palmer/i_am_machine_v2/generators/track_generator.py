"""Validated track generator for Ableton Live.

Generates Ableton tracks from validated Pydantic configurations.
Connects to Ableton MCP to create tracks, load devices, and add MIDI clips.
"""

import json
import sys
from pathlib import Path
from typing import Any

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "i_am_machine"))

from models.v1.track_models import ProjectConfig, TrackConfig  # noqa: E402

# Import the existing MCP client
try:
    from live_set.lily_palmer.i_am_machine.ableton_client import AbletonMCPClient

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: AbletonMCPClient not available, dry-run mode only")


# Device name to Ableton browser URI mapping
DEVICE_URI_MAP = {
    # Drums - Use pre-loaded kits with samples!
    "Drum Sampler": "query:Drums#FileId_5447",  # 909 Core Kit (kick, snare, hats)
    "Drum Rack": "query:Drums#FileId_5447",  # 909 Core Kit
    "808 Kit": "query:Drums#FileId_5446",  # 808 Core Kit
    "707 Kit": "query:Drums#FileId_5445",  # 707 Core Kit
    "606 Kit": "query:Drums#FileId_5444",  # 606 Core Kit
    "Impulse": "query:Drums#Impulse",
    # Instruments (Suite)
    "Wavetable": "query:Instruments#Wavetable",
    "Operator": "query:Instruments#Operator",
    "Drift": "query:Instruments#Drift",
    # Instruments (All Editions) - Use as fallbacks
    "Simpler": "query:Instruments#Simpler",
    "Sampler": "query:Instruments#Sampler",
    # Audio Effects
    "Auto Filter": "query:AudioFx#Auto%20Filter",
    "Channel EQ": "query:AudioFx#Channel%20EQ",
    "EQ Eight": "query:AudioFx#EQ%20Eight",
    "EQ Three": "query:AudioFx#EQ%20Three",
    "Compressor": "query:AudioFx#Compressor",
    "Reverb": "query:AudioFx#Reverb",
    "Delay": "query:AudioFx#Delay",
    "Chorus": "query:AudioFx#Chorus",
    "Grain Delay": "query:AudioFx#Grain%20Delay",
    "Limiter": "query:AudioFx#Limiter",
    "Saturator": "query:AudioFx#Saturator",
}


class ValidatedTrackGenerator:
    """Generate Ableton tracks from validated JSON configurations."""

    def __init__(self, mcp_client: AbletonMCPClient | None = None):
        """Initialize track generator.

        Args:
            mcp_client: Optional MCP client for Ableton communication.
                       If None and MCP available, creates new client.
                       If MCP not available, runs in dry-run mode.
        """
        if mcp_client:
            self.mcp_client = mcp_client
            self.dry_run = False
        elif MCP_AVAILABLE:
            try:
                self.mcp_client = AbletonMCPClient()
                # Test connection
                result = self.mcp_client.get_session_info()
                if result.success:
                    print(
                        f"✅ Connected to Ableton (Tempo: {result.data.get('tempo')} BPM)"
                    )
                    self.dry_run = False
                else:
                    print(f"⚠️  MCP connection failed: {result.message}")
                    print("   Running in dry-run mode")
                    self.mcp_client = None
                    self.dry_run = True
            except Exception as e:
                print(f"⚠️  Could not connect to Ableton: {e}")
                print("   Running in dry-run mode")
                self.mcp_client = None
                self.dry_run = True
        else:
            self.mcp_client = None
            self.dry_run = True

    def load_config(self, config_path: str | Path) -> ProjectConfig:
        """Load and validate configuration from JSON file.

        Args:
            config_path: Path to JSON configuration file

        Returns:
            Validated ProjectConfig

        Raises:
            ValueError: If config validation fails
        """
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")

        with open(config_path) as f:
            config_data = json.load(f)

        # Validate with Pydantic
        try:
            return ProjectConfig(**config_data)
        except Exception as e:
            raise ValueError(f"Config validation failed: {e}") from e

    def create_track(self, track: TrackConfig) -> dict[str, Any]:
        """Create a single track in Ableton.

        Args:
            track: Validated track configuration

        Returns:
            Result dict with success status and track info
        """
        if self.dry_run:
            print(f"[DRY RUN] Creating track {track.index}: {track.name}")
            return {
                "success": True,
                "track_name": track.name,
                "track_index": track.index,
                "dry_run": True,
            }

        try:
            # Create track via MCP
            result = self.mcp_client.ensure_track(
                target_index=track.index,
                name=track.name,
                track_type="midi",  # Default to MIDI for now
            )

            if not result.success:
                return {
                    "success": False,
                    "error": f"Failed to create track: {result.message}",
                    "track_name": track.name,
                }

            print(f"  ✓ Track {track.index}: {track.name}")

            # Load devices
            device_count = 0
            for device in track.devices:
                # Get browser URI for device
                device_uri = DEVICE_URI_MAP.get(device.name)

                if not device_uri:
                    # Try fallback
                    if device.fallback:
                        device_uri = DEVICE_URI_MAP.get(device.fallback)

                if not device_uri:
                    print(f"    ✗ {device.name} (no URI mapping)")
                    continue

                # Load via browser URI
                device_result = self.mcp_client.load_browser_item(
                    track_index=track.index,
                    item_uri=device_uri,
                )

                if device_result.success:
                    device_count += 1
                    print(f"    ✓ {device.name}")
                else:
                    # Try fallback if available
                    if device.fallback and device.fallback != device.name:
                        fallback_uri = DEVICE_URI_MAP.get(device.fallback)
                        if fallback_uri:
                            device_result = self.mcp_client.load_browser_item(
                                track_index=track.index,
                                item_uri=fallback_uri,
                            )
                            if device_result.success:
                                device_count += 1
                                print(f"    ✓ {device.fallback} (fallback)")
                            else:
                                print(f"    ✗ {device.name} (failed)")
                        else:
                            print(f"    ✗ {device.name} (failed)")
                    else:
                        print(f"    ✗ {device.name} (failed)")

            # Add MIDI clips
            clip_count = 0
            for clip_index, notes in enumerate(track.midi_clips):
                # Clear any existing clip first
                try:
                    clear_result = self.mcp_client.send_command(
                        "remove_clip",
                        {"track_index": track.index, "clip_index": clip_index},
                    )
                except Exception:
                    pass  # Ignore if clip doesn't exist

                # Convert Pydantic MIDINote objects to dicts
                note_dicts = [
                    {
                        "pitch": note.pitch,
                        "start_time": note.start_time,
                        "duration": note.duration,
                        "velocity": note.velocity,
                        "mute": False,
                    }
                    for note in notes
                ]

                clip_result = self.mcp_client.create_pattern(
                    track_index=track.index,
                    clip_index=clip_index,
                    clip_name=f"{track.name} Pattern {clip_index + 1}",
                    notes=note_dicts,
                    length=16.0,
                    fire=False,
                )

                if clip_result.success:
                    clip_count += 1

            if clip_count > 0:
                print(f"    ✓ {clip_count} MIDI clip(s)")

            return {
                "success": True,
                "track_name": track.name,
                "track_index": track.index,
                "devices_loaded": device_count,
                "clips_created": clip_count,
            }

        except Exception as e:
            print(f"  ✗ Error: {e}")
            return {
                "success": False,
                "error": str(e),
                "track_name": track.name,
            }

    def generate_from_config(self, config_path: str | Path) -> dict[str, Any]:
        """Generate full project from configuration file.

        Args:
            config_path: Path to JSON configuration

        Returns:
            Result dict with generation summary
        """
        print(f"\n{'=' * 60}")
        print(f"Loading configuration: {config_path}")
        print(f"{'=' * 60}\n")

        project = self.load_config(config_path)

        print("✅ Configuration validated:")
        print(f"   Project: {project.name}")
        print(f"   Tempo: {project.tempo} BPM")
        print(f"   Tracks: {len(project.tracks)}")
        print(
            f"   Time Signature: {project.time_signature[0]}/{project.time_signature[1]}"
        )

        if self.dry_run:
            print("\n⚠️  DRY RUN MODE (no MCP client)")
        else:
            # Set tempo
            tempo_result = self.mcp_client.set_tempo(project.tempo)
            if tempo_result.success:
                print(f"\n✅ Set tempo to {project.tempo} BPM")

        results = []
        successful = 0
        failed = 0

        print(f"\nGenerating {len(project.tracks)} tracks...\n")

        for track in project.tracks:
            result = self.create_track(track)
            results.append(result)

            if result["success"]:
                successful += 1
            else:
                failed += 1

        print(f"\n{'=' * 60}")
        print("Generation Complete!")
        print(f"Successful: {successful}/{len(project.tracks)}")
        print(f"Failed: {failed}/{len(project.tracks)}")
        print(f"{'=' * 60}\n")

        return {
            "success": failed == 0,
            "project_name": project.name,
            "tracks_generated": successful,
            "tracks_failed": failed,
            "results": results,
        }


# Example usage
if __name__ == "__main__":
    # Try with MCP client
    generator = ValidatedTrackGenerator()

    # Test with example config
    result = generator.generate_from_config(
        "live_set/lily_palmer/i_am_machine_v2/configs/example.json"
    )

    print(f"\nResult: {'✅ Success' if result['success'] else '❌ Failed'}")
