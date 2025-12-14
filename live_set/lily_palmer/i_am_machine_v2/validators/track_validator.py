"""Track configuration validator.

Validates track configurations against Pydantic models and project standards.
"""

import json
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from models.v1.track_models import (  # noqa: E402
    ProjectConfig,
    TrackConfig,
    TrackType,
)


class TrackValidator:
    """Validate track configurations against standards."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.score = 100.0

    def load_config(self) -> dict[str, Any] | None:
        """Load JSON configuration."""
        try:
            with open(self.config_path) as f:
                return json.load(f)
        except Exception as e:
            self.errors.append(f"Failed to load config: {e}")
            return None

    def validate_project(self, config_data: dict[str, Any]) -> bool:
        """Validate entire project configuration."""
        try:
            # Validate with Pydantic
            project = ProjectConfig(**config_data)

            # Additional validation rules
            if not (130 <= project.tempo <= 140):
                self.warnings.append(
                    f"Tempo {project.tempo} outside techno range (130-140)"
                )
                self.score -= 5

            if len(project.tracks) < 8:
                self.warnings.append(
                    f"Only {len(project.tracks)} tracks - consider adding more"
                )
                self.score -= 5

            # Validate each track
            for track in project.tracks:
                self._validate_track(track)

            return len(self.errors) == 0

        except Exception as e:
            self.errors.append(f"Validation error: {e}")
            self.score = 0.0
            return False

    def _validate_track(self, track: TrackConfig) -> None:
        """Validate individual track."""
        # Check devices
        if not track.devices:
            self.warnings.append(f"{track.name}: No devices configured")
            self.score -= 2

        # Check MIDI clips for non-audio tracks
        if track.track_type != TrackType.AUDIO and not track.midi_clips:
            self.warnings.append(f"{track.name}: No MIDI clips configured")
            self.score -= 2

        # Check color variety
        if track.color == "#FFFFFF":
            self.warnings.append(f"{track.name}: Using default white color")
            self.score -= 1

    def generate_report(self) -> str:
        """Generate validation report."""
        lines = ["# Track Configuration Validation Report\\n"]

        lines.append(f"**Configuration**: {self.config_path.name}")
        lines.append(f"**Score**: {max(0, self.score):.1f}/100\\n")

        if self.errors:
            lines.append("## Errors\\n")
            for error in self.errors:
                lines.append(f"- ❌ {error}")
            lines.append("")

        if self.warnings:
            lines.append("## Warnings\\n")
            for warning in self.warnings:
                lines.append(f"- ⚠️ {warning}")
            lines.append("")

        if not self.errors and not self.warnings:
            lines.append("✅ Configuration valid with no issues!")

        return "\\n".join(lines)


# Example usage
if __name__ == "__main__":
    # Example configuration for testing
    example_config = {
        "name": "I Am Machine",
        "tempo": 136,
        "time_signature": [4, 4],
        "total_bars": 64,
        "tracks": [
            {
                "index": 0,
                "name": "Track 01 - Kick",
                "track_type": "kick",
                "color": "#FF0000",
                "volume_db": -6.0,
                "pan": 0.0,
                "devices": [
                    {"name": "Drum Sampler", "parameters": {}},
                    {"name": "Channel EQ", "parameters": {"low_gain": 3.0}},
                ],
                "midi_clips": [
                    [
                        {
                            "pitch": 36,
                            "start_time": 0.0,
                            "duration": 0.25,
                            "velocity": 100,
                        }
                    ]
                ],
            }
        ],
    }

    # Save example
    example_path = Path("live_set/lily_palmer/i_am_machine_v2/configs/example.json")
    example_path.parent.mkdir(parents=True, exist_ok=True)
    with open(example_path, "w") as f:
        json.dump(example_config, f, indent=2)

    # Validate
    validator = TrackValidator(example_path)
    config = validator.load_config()

    if config:
        is_valid = validator.validate_project(config)
        report = validator.generate_report()

        # Save report
        report_path = Path("artifacts/report/track_structure_report.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report)

        print(f"✅ Track validation complete: {report_path}")
        print(f"Valid: {is_valid}")
        print(f"Score: {validator.score:.1f}/100")
