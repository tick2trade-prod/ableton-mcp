"""Tests for V3 schemas."""


from ableton_lite.schemas.crew import (
    AgentRole,
    Crew,
    CrewAgent,
    CrewTask,
    TaskStatus,
)
from ableton_lite.schemas.instrument import (
    Instrument,
    InstrumentCategory,
    get_instrument_catalog,
)
from ableton_lite.schemas.pattern import (
    Note,
    Pattern,
    PatternType,
    midi_to_note_name,
    note_name_to_midi,
)
from ableton_lite.schemas.processing import (
    TECHNO_CHAINS,
    DynamicsOperation,
    EQOperation,
    ProcessingChain,
    SaturationOperation,
)
from ableton_lite.schemas.time import Duration, TimePosition


class TestTimeSchemas:
    """Tests for time-based schemas."""

    def test_time_position_to_beats(self):
        """Test TimePosition to beats conversion."""
        pos = TimePosition(bar=1, beat=2, tick=48)
        assert pos.to_beats() == 6.5  # 1*4 + 2 + 48/96

    def test_time_position_from_beats(self):
        """Test creating TimePosition from beats."""
        pos = TimePosition.from_beats(6.5)
        assert pos.bar == 1
        assert pos.beat == 2
        assert pos.tick == 48

    def test_time_position_to_seconds(self):
        """Test TimePosition to seconds at tempo."""
        pos = TimePosition(bar=1, beat=0, tick=0)  # 4 beats (1 full bar)
        assert pos.to_seconds(tempo=120) == 2.0  # 4 beats at 120 BPM = 2 seconds

    def test_duration_from_unit(self):
        """Test Duration creation from units."""
        dur = Duration.bars(2)
        assert dur.beats == 8.0

        dur = Duration.sixteenths(4)
        assert dur.beats == 1.0


class TestPatternSchemas:
    """Tests for pattern schemas."""

    def test_midi_to_note_name(self):
        """Test MIDI to note name conversion."""
        assert midi_to_note_name(60) == "C4"
        assert midi_to_note_name(36) == "C2"  # Standard: C-1=0, C0=12, C1=24, C2=36
        assert midi_to_note_name(69) == "A4"

    def test_note_name_to_midi(self):
        """Test note name to MIDI conversion."""
        assert note_name_to_midi("C4") == 60
        assert note_name_to_midi("C2") == 36  # Standard: C-1=0, C0=12, C1=24, C2=36
        assert note_name_to_midi("A4") == 69

    def test_note_creation(self):
        """Test Note creation."""
        note = Note(
            pitch=36,
            position=TimePosition(bar=0, beat=0, tick=0),
            duration=Duration(beats=0.5),
            velocity=110,
        )
        assert note.note_name == "C2"  # MIDI 36 = C2
        assert note.pitch == 36

    def test_note_to_ableton_dict(self):
        """Test Note to Ableton format conversion."""
        note = Note(
            pitch=36,
            position=TimePosition(bar=0, beat=0, tick=0),
            duration=Duration(beats=0.5),
            velocity=110,
        )
        d = note.to_ableton_dict()
        assert d["pitch"] == 36
        assert d["start_time"] == 0.0
        assert d["duration"] == 0.5
        assert d["velocity"] == 110

    def test_pattern_creation(self):
        """Test Pattern creation."""
        notes = [
            Note(
                pitch=36,
                position=TimePosition(bar=0, beat=i, tick=0),
                duration=Duration(beats=0.5),
            )
            for i in range(4)
        ]
        pattern = Pattern(
            name="Test Kick",
            type=PatternType.KICK,
            notes=notes,
            length_bars=1,
        )
        assert len(pattern.notes) == 4
        assert pattern.type == PatternType.KICK

    def test_pattern_transpose(self):
        """Test pattern transposition."""
        note = Note(
            pitch=40,  # E2
            position=TimePosition(bar=0, beat=0, tick=0),
            duration=Duration(beats=0.5),
        )
        pattern = Pattern(
            name="Test",
            type=PatternType.BASS,
            key="E",
            notes=[note],
        )

        transposed = pattern.shift_to_key("G")
        assert transposed.key == "G"
        assert transposed.notes[0].pitch == 43  # E + 3 semitones = G


class TestInstrumentSchemas:
    """Tests for instrument schemas."""

    def test_instrument_creation(self):
        """Test Instrument creation."""
        inst = Instrument(
            name="Test Kick",
            category=InstrumentCategory.DRUM_MACHINE,
            frequency_min=30,
            frequency_max=200,
        )
        assert inst.name == "Test Kick"
        assert inst.category == InstrumentCategory.DRUM_MACHINE

    def test_instrument_catalog(self):
        """Test instrument catalog has expected entries."""
        catalog = get_instrument_catalog()
        assert "909_kick" in catalog
        assert "sub_bass" in catalog
        assert catalog["909_kick"].category == InstrumentCategory.DRUM_MACHINE


class TestProcessingSchemas:
    """Tests for processing schemas."""

    def test_eq_operation(self):
        """Test EQ operation creation."""
        eq = EQOperation.highpass(30)
        assert eq.frequency == 30
        assert eq.filter_type.value == "highpass"

    def test_dynamics_presets(self):
        """Test dynamics preset methods."""
        glue = DynamicsOperation.glue()
        assert glue.ratio == 4.0

        punch = DynamicsOperation.punch()
        assert punch.attack_ms == 10

    def test_processing_chain(self):
        """Test ProcessingChain creation."""
        chain = ProcessingChain(
            name="Test Chain",
            eq=[EQOperation.highpass(30)],
            saturation=SaturationOperation.warm(),
        )
        assert len(chain.eq) == 1
        assert chain.saturation is not None

    def test_techno_chains_exist(self):
        """Test techno chains are defined."""
        assert "kick_punch" in TECHNO_CHAINS
        assert "sub_bass" in TECHNO_CHAINS


class TestCrewSchemas:
    """Tests for crew schemas."""

    def test_crew_agent_factory(self):
        """Test CrewAgent factory methods."""
        beat_maker = CrewAgent.beat_maker()
        assert beat_maker.role == AgentRole.BEAT_MAKER
        assert len(beat_maker.capabilities) > 0

    def test_crew_task_dependencies(self):
        """Test CrewTask dependency tracking."""
        task = CrewTask(
            description="Create kick pattern",
            depends_on=["task-1", "task-2"],
        )
        assert len(task.depends_on) == 2
        assert task.status == TaskStatus.PENDING

    def test_crew_techno_factory(self):
        """Test Crew factory for techno loop."""
        crew = Crew.techno_4bar(tempo=128, key="G")
        assert crew.tempo == 128
        assert crew.key == "G"
        assert len(crew.agents) == 2  # beat_maker, bassist
        assert len(crew.tasks) == 3  # kick, bass, hihat

    def test_crew_pending_tasks(self):
        """Test getting pending tasks with resolved dependencies."""
        crew = Crew.techno_4bar()

        # Initially, kick and hihat have no deps
        pending = crew.get_pending_tasks()
        pending_types = [t.pattern_type for t in pending]
        assert PatternType.KICK in pending_types
        assert PatternType.HIHAT in pending_types
        assert PatternType.BASS not in pending_types  # Has dep on kick
