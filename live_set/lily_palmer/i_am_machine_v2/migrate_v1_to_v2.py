"""Migration script: v1 track scripts → v2 JSON configurations.

Analyzes existing v1 track scripts and converts them to validated
v2 JSON configurations using Pydantic models.
"""

import json
import re
from pathlib import Path
from typing import Any


class TrackMigrator:
    """Migrate v1 track scripts to v2 JSON configurations."""

    def __init__(self, v1_dir: Path, v2_dir: Path):
        self.v1_dir = v1_dir
        self.v2_dir = v2_dir
        self.v2_dir.mkdir(parents=True, exist_ok=True)

    def extract_track_info(self, script_path: Path) -> dict[str, Any] | None:
        """Extract track information from v1 script.

        This is a simple extraction - in practice you'd parse AST or
        run the scripts to get actual values.
        """
        content = script_path.read_text()

        # Extract track number from filename
        match = re.search(r"track_(\d+)", script_path.name)
        if not match:
            return None

        track_num = int(match.group(1))

        # Extract track name from filename
        parts = script_path.stem.split("_", 2)
        if len(parts) < 3:
            return None

        track_type = parts[2].replace("_", " ").title()

        return {
            "index": track_num - 1,  # 0-indexed
            "name": f"Track {track_num:02d} - {track_type}",
            "script_path": script_path,
        }

    def create_default_track_config(self, track_info: dict[str, Any]) -> dict[str, Any]:
        """Create default track configuration from extracted info."""
        index = track_info["index"]
        name = track_info["name"]

        # Determine track type and color from name
        name_lower = name.lower()
        if "kick" in name_lower or "rumble" in name_lower:
            track_type = "kick"
            color = "#FF0000"
        elif "bass" in name_lower or "acid" in name_lower:
            track_type = "bass"
            color = "#00FF00"
        elif "hat" in name_lower or "clap" in name_lower or "tom" in name_lower:
            track_type = "drum"
            color = "#FF8800"
        elif "vocal" in name_lower:
            track_type = "vocal"
            color = "#FFAAAA"
        elif "fx" in name_lower or "riser" in name_lower or "impact" in name_lower:
            track_type = "fx"
            color = "#8800FF"
        else:
            track_type = "synth"
            color = "#00FFFF"

        return {
            "index": index,
            "name": name,
            "track_type": track_type,
            "color": color,
            "volume_db": -10.0,
            "pan": 0.0,
            "devices": [],
            "midi_clips": [],
        }

    def migrate_all_tracks(self) -> dict[str, Any]:
        """Migrate all v1 track scripts to v2 configuration."""
        track_scripts = sorted(self.v1_dir.glob("track_*.py"))

        # Filter out duplicates (like track_04_acid_v2.py)
        unique_scripts = []
        seen_tracks = set()

        for script in track_scripts:
            match = re.search(r"track_(\d+)", script.name)
            if match:
                track_num = int(match.group(1))
                if track_num not in seen_tracks:
                    seen_tracks.add(track_num)
                    unique_scripts.append(script)

        print(f"Found {len(unique_scripts)} unique track scripts")

        tracks = []
        for script in unique_scripts:
            track_info = self.extract_track_info(script)
            if track_info:
                track_config = self.create_default_track_config(track_info)
                tracks.append(track_config)
                print(f"  ✅ {track_config['name']}")

        # Create full project configuration
        project_config = {
            "name": "I Am Machine (Migrated)",
            "tempo": 136,
            "time_signature": [4, 4],
            "total_bars": 64,
            "tracks": sorted(tracks, key=lambda t: t["index"]),
        }

        # Save to JSON
        output_path = self.v2_dir / "i_am_machine_migrated.json"
        with open(output_path, "w") as f:
            json.dump(project_config, f, indent=2)

        print(f"\n✅ Migration complete: {output_path}")
        print(f"   {len(tracks)} tracks migrated")

        return project_config


# Example usage
if __name__ == "__main__":
    v1_dir = Path("live_set/lily_palmer/i_am_machine")
    v2_dir = Path("live_set/lily_palmer/i_am_machine_v2/configs")

    migrator = TrackMigrator(v1_dir, v2_dir)
    config = migrator.migrate_all_tracks()

    # Validate with Pydantic
    print("\nValidating migrated configuration...")
    import sys

    sys.path.insert(0, ".")
    from models.v1.track_models import ProjectConfig

    try:
        project = ProjectConfig(**config)
        print("✅ Validation passed!")
        print(f"   Project: {project.name}")
        print(f"   Tracks: {len(project.tracks)}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
