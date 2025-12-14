"""Validated track generator for Ableton Live.

Generates Ableton tracks from validated Pydantic configurations.
Connects to Ableton MCP to create tracks, load devices, and add MIDI clips.
"""

import json
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from models.v1.track_models import ProjectConfig, TrackConfig  # noqa: E402


class ValidatedTrackGenerator:
    """Generate Ableton tracks from validated JSON configurations."""

    def __init__(self, mcp_client=None):
        """Initialize track generator.

        Args:
            mcp_client: Optional MCP client for Ableton communication.
                       If None, runs in dry-run mode.
        """
        self.mcp_client = mcp_client
        self.dry_run = mcp_client is None

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

    async def create_track(self, track: TrackConfig) -> dict[str, Any]:
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
            result = await self.mcp_client.create_track(
                name=track.name, index=track.index
            )

            if not result.get("success"):
                return {"success": False, "error": "Failed to create track"}

            # Set track properties
            await self.mcp_client.set_track_color(track.index, track.color)
            await self.mcp_client.set_track_volume(track.index, track.volume_db)
            await self.mcp_client.set_track_pan(track.index, track.pan)

            # Load devices
            for device in track.devices:
                device_result = await self.mcp_client.load_device(
                    track_index=track.index,
                    device_name=device.name,
                    parameters=device.parameters,
                )

                if not device_result.get("success") and device.fallback:
                    # Try fallback device
                    await self.mcp_client.load_device(
                        track_index=track.index,
                        device_name=device.fallback,
                        parameters=device.parameters,
                    )

            # Add MIDI clips
            for clip_index, notes in enumerate(track.midi_clips):
                await self.mcp_client.create_midi_clip(
                    track_index=track.index, clip_index=clip_index, notes=notes
                )

            return {
                "success": True,
                "track_name": track.name,
                "track_index": track.index,
                "devices_loaded": len(track.devices),
                "clips_created": len(track.midi_clips),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "track_name": track.name}

    async def generate_from_config(self, config_path: str | Path) -> dict[str, Any]:
        """Generate full project from configuration file.

        Args:
            config_path: Path to JSON configuration

        Returns:
            Result dict with generation summary
        """
        print(f"Loading configuration: {config_path}")
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

        results = []
        successful = 0
        failed = 0

        print(f"\nGenerating {len(project.tracks)} tracks...")

        for track in project.tracks:
            result = await self.create_track(track)
            results.append(result)

            if result["success"]:
                successful += 1
                status = "✅"
            else:
                failed += 1
                status = "❌"

            print(f"{status} Track {track.index + 1:02d}: {track.name}")

        print(f"\n{'=' * 60}")
        print("Generation Complete!")
        print(f"Successful: {successful}/{len(project.tracks)}")
        print(f"Failed: {failed}/{len(project.tracks)}")
        print(f"{'=' * 60}")

        return {
            "success": failed == 0,
            "project_name": project.name,
            "tracks_generated": successful,
            "tracks_failed": failed,
            "results": results,
        }


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        # Dry run mode (no MCP client)
        generator = ValidatedTrackGenerator()

        # Test with example config
        result = await generator.generate_from_config(
            "live_set/lily_palmer/i_am_machine_v2/configs/example.json"
        )

        print(f"\nResult: {'Success' if result['success'] else 'Failed'}")

    asyncio.run(main())
