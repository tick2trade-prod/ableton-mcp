"""CrewAI-style agent orchestration schemas."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ableton_lite.schemas.pattern import PatternType, Scale
from ableton_lite.schemas.time import TimePosition


class AgentRole(str, Enum):
    """Specialized agent roles for Ableton production."""

    ARRANGER = "arranger"  # Builds song structure
    SOUND_DESIGNER = "sound_designer"  # Creates patches
    BEAT_MAKER = "beat_maker"  # Drum patterns
    BASSIST = "bassist"  # Bass lines
    LEAD_SYNTH = "lead_synth"  # Lead melodies
    CHORD_WRITER = "chord_writer"  # Chord progressions
    ARP_DESIGNER = "arp_designer"  # Arpeggios
    FX_DESIGNER = "fx_designer"  # FX/risers/impacts
    MIXER = "mixer"  # Mix engineering
    MASTERING = "mastering"  # Final processing


class AgentCapability(str, Enum):
    """What agents can do."""

    CREATE_PATTERN = "create_pattern"
    LOAD_INSTRUMENT = "load_instrument"
    SET_PARAMETERS = "set_parameters"
    ANALYZE_AUDIO = "analyze_audio"
    APPLY_FX = "apply_fx"
    SUGGEST_PATTERN = "suggest_pattern"
    TRANSPOSE = "transpose"
    CREATE_VARIATION = "create_variation"
    MIX_TRACK = "mix_track"


# Default capabilities per role
ROLE_CAPABILITIES = {
    AgentRole.ARRANGER: [
        AgentCapability.CREATE_PATTERN,
        AgentCapability.SUGGEST_PATTERN,
    ],
    AgentRole.SOUND_DESIGNER: [
        AgentCapability.LOAD_INSTRUMENT,
        AgentCapability.SET_PARAMETERS,
        AgentCapability.APPLY_FX,
    ],
    AgentRole.BEAT_MAKER: [
        AgentCapability.CREATE_PATTERN,
        AgentCapability.LOAD_INSTRUMENT,
        AgentCapability.CREATE_VARIATION,
    ],
    AgentRole.BASSIST: [
        AgentCapability.CREATE_PATTERN,
        AgentCapability.TRANSPOSE,
        AgentCapability.CREATE_VARIATION,
    ],
    AgentRole.LEAD_SYNTH: [
        AgentCapability.CREATE_PATTERN,
        AgentCapability.TRANSPOSE,
    ],
    AgentRole.MIXER: [
        AgentCapability.SET_PARAMETERS,
        AgentCapability.APPLY_FX,
        AgentCapability.MIX_TRACK,
    ],
}


class CrewAgent(BaseModel):
    """Agent definition for music production crew."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: AgentRole
    model: str = "llama3.1:8b"

    # Capabilities
    capabilities: list[AgentCapability] = []

    # Context
    backstory: str = ""  # Agent personality/expertise
    goal: str = ""  # What they're trying to achieve

    # Constraints
    max_iterations: int = Field(default=10, ge=1, le=100)
    timeout_seconds: int = Field(default=300, ge=10, le=3600)

    # State
    status: str = "idle"  # idle, working, done, error
    last_output: dict | None = None

    def model_post_init(self, __context: Any) -> None:
        """Set default capabilities based on role."""
        if not self.capabilities:
            object.__setattr__(
                self, "capabilities", ROLE_CAPABILITIES.get(self.role, [])
            )

    @classmethod
    def beat_maker(
        cls, name: str = "Beat Maker", model: str = "llama3.1:8b"
    ) -> "CrewAgent":
        """Create a beat maker agent."""
        return cls(
            name=name,
            role=AgentRole.BEAT_MAKER,
            model=model,
            backstory="You are an expert techno drum programmer with deep knowledge of 909, 808, and modern drum machines.",
            goal="Create compelling, groove-focused drum patterns",
        )

    @classmethod
    def bassist(cls, name: str = "Bassist", model: str = "llama3.1:8b") -> "CrewAgent":
        """Create a bassist agent."""
        return cls(
            name=name,
            role=AgentRole.BASSIST,
            model=model,
            backstory="You are a bass specialist who understands sub frequencies, rumble, and how bass interacts with kick drums.",
            goal="Create driving bass lines that lock with the kick",
        )

    @classmethod
    def mixer(
        cls, name: str = "Mix Engineer", model: str = "llama3.1:8b"
    ) -> "CrewAgent":
        """Create a mixer agent."""
        return cls(
            name=name,
            role=AgentRole.MIXER,
            model=model,
            backstory="You are an experienced mix engineer specializing in techno with a focus on powerful low-end and clean highs.",
            goal="Balance all elements for a punchy, club-ready mix",
        )


class TaskStatus(str, Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class CrewTask(BaseModel):
    """Task for a crew member."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    agent_id: str | None = None  # Assigned agent

    # Musical context
    position: TimePosition | None = None
    length_bars: int | None = None
    pattern_type: PatternType | None = None

    # Dependencies
    depends_on: list[str] = []  # Task IDs that must complete first

    # Execution
    status: TaskStatus = TaskStatus.PENDING
    started_at: str | None = None
    completed_at: str | None = None

    # Output
    expected_output: str = ""
    output: dict | None = None
    error: str | None = None


class Crew(BaseModel):
    """CrewAI-style crew for music production."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    goal: str  # e.g., "Create 4-bar techno loop"

    # Musical context
    tempo: int = Field(default=130, ge=60, le=200)
    key: str = "E"
    scale: Scale = Scale.MINOR
    length_bars: int = Field(default=4, ge=1, le=64)

    # Members
    agents: list[CrewAgent] = []
    tasks: list[CrewTask] = []

    # Execution settings
    verbose: int = Field(default=2, ge=0, le=3)
    max_rpm: int | None = None  # Rate limit (requests per minute)

    # State
    status: str = "pending"  # pending, running, completed, failed
    started_at: str | None = None
    completed_at: str | None = None
    result: dict | None = None

    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def add_agent(self, agent: CrewAgent) -> None:
        """Add an agent to the crew."""
        self.agents.append(agent)

    def add_task(self, task: CrewTask) -> None:
        """Add a task to the crew."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> list[CrewTask]:
        """Get tasks ready to run (no unmet dependencies)."""
        completed_ids = {t.id for t in self.tasks if t.status == TaskStatus.COMPLETED}
        return [
            t
            for t in self.tasks
            if t.status == TaskStatus.PENDING
            and all(dep in completed_ids for dep in t.depends_on)
        ]

    @classmethod
    def techno_4bar(
        cls,
        name: str = "Techno Loop",
        tempo: int = 130,
        key: str = "E",
    ) -> "Crew":
        """Create a standard 4-bar techno loop crew."""
        crew = cls(
            name=name,
            goal="Create a 4-bar techno loop with kick, bass, and hi-hats",
            tempo=tempo,
            key=key,
            length_bars=4,
        )

        # Add agents
        crew.add_agent(CrewAgent.beat_maker())
        crew.add_agent(CrewAgent.bassist())

        # Add tasks
        kick_task = CrewTask(
            description="Create a 4-on-the-floor kick pattern",
            pattern_type=PatternType.KICK,
            length_bars=4,
            expected_output="Kick pattern with 16 notes",
        )
        crew.add_task(kick_task)

        bass_task = CrewTask(
            description=f"Create a rolling bass line in {key} minor",
            pattern_type=PatternType.BASS,
            length_bars=4,
            depends_on=[kick_task.id],
            expected_output="Bass pattern locked to kick",
        )
        crew.add_task(bass_task)

        hat_task = CrewTask(
            description="Create offbeat hi-hat pattern",
            pattern_type=PatternType.HIHAT,
            length_bars=4,
            expected_output="Open hats on offbeats",
        )
        crew.add_task(hat_task)

        return crew
