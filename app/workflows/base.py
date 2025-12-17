"""Base workflow class for TDD-based track creation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class TDDPhase(Enum):
    """TDD cycle phases."""

    RED = "red"  # Write failing test
    GREEN = "green"  # Implement to pass
    REFACTOR = "refactor"  # Clean up


class TrackStatus(Enum):
    """Track creation status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TrackSpec:
    """Specification for a single track."""

    name: str
    index: int
    device: str
    device_uri: str
    pattern_type: str = ""
    needs_sidechain: bool = False
    sidechain_source: str | None = None
    effects: list[dict] = field(default_factory=list)
    test_file: str = ""
    status: TrackStatus = TrackStatus.PENDING


@dataclass
class WorkflowResult:
    """Result of a workflow execution."""

    success: bool
    message: str
    tracks_created: list[str] = field(default_factory=list)
    tracks_failed: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)


class BaseWorkflow(ABC):
    """Base class for TDD workflows.

    Implements the TDD cycle:
    1. RED: Generate/run failing test
    2. GREEN: Implement minimum code to pass
    3. REFACTOR: Clean up and verify
    """

    def __init__(self, section: str = "intro"):
        """Initialize workflow.

        Args:
            section: Song section (intro, build1, drop1, etc.)
        """
        self.section = section
        self.tracks: list[TrackSpec] = []
        self.current_phase = TDDPhase.RED

    @property
    @abstractmethod
    def name(self) -> str:
        """Workflow name."""
        ...

    @property
    @abstractmethod
    def lane(self) -> int:
        """Lane number (1-4)."""
        ...

    @abstractmethod
    def define_tracks(self) -> list[TrackSpec]:
        """Define tracks for this workflow."""
        ...

    @abstractmethod
    async def execute_red(self, track: TrackSpec) -> bool:
        """RED phase: Write/verify failing test.

        Args:
            track: Track specification

        Returns:
            True if test correctly fails (expected behavior)
        """
        ...

    @abstractmethod
    async def execute_green(self, track: TrackSpec) -> bool:
        """GREEN phase: Implement to pass test.

        Args:
            track: Track specification

        Returns:
            True if implementation passes test
        """
        ...

    @abstractmethod
    async def execute_refactor(self, track: TrackSpec) -> bool:
        """REFACTOR phase: Clean up and verify.

        Args:
            track: Track specification

        Returns:
            True if refactoring successful
        """
        ...

    async def execute(self) -> WorkflowResult:
        """Execute the full TDD workflow for all tracks.

        Returns:
            WorkflowResult with success status and details
        """
        self.tracks = self.define_tracks()
        created = []
        failed = []
        errors = []

        for track in self.tracks:
            try:
                track.status = TrackStatus.IN_PROGRESS

                # RED: Write/verify failing test
                self.current_phase = TDDPhase.RED
                if not await self.execute_red(track):
                    errors.append(f"{track.name}: RED phase failed")
                    # Continue anyway - test might already pass

                # GREEN: Implement to pass
                self.current_phase = TDDPhase.GREEN
                if not await self.execute_green(track):
                    track.status = TrackStatus.FAILED
                    failed.append(track.name)
                    errors.append(f"{track.name}: GREEN phase failed")
                    continue

                # REFACTOR: Clean up
                self.current_phase = TDDPhase.REFACTOR
                if not await self.execute_refactor(track):
                    errors.append(f"{track.name}: REFACTOR phase had issues")
                    # Continue - track is still created

                track.status = TrackStatus.COMPLETED
                created.append(track.name)

            except Exception as e:
                track.status = TrackStatus.FAILED
                failed.append(track.name)
                errors.append(f"{track.name}: {e!s}")

        success = len(failed) == 0
        total = len(self.tracks)
        message = f"Lane {self.lane} ({self.name}): {len(created)}/{total} tracks"

        return WorkflowResult(
            success=success,
            message=message,
            tracks_created=created,
            tracks_failed=failed,
            errors=errors,
        )

    def get_state_path(self, track_name: str) -> Path:
        """Get path to track state file.

        Args:
            track_name: Name of track

        Returns:
            Path to state/tracks/{track_name}.json
        """
        return Path("state/tracks") / f"{track_name.lower().replace(' ', '_')}.json"

    def get_test_path(self, track_name: str) -> Path:
        """Get path to track test file.

        Args:
            track_name: Name of track

        Returns:
            Path to tests/phases/test_{section}_{track_name}.py
        """
        clean_name = track_name.lower().replace(" ", "_")
        return Path("tests/phases") / f"test_{self.section}_{clean_name}.py"
