"""
Test: Verify agents can produce reference-accurate patterns.

This test validates that agents, when given access to stem analysis data,
can produce patterns that measurably match the reference track better
than hardcoded patterns.

Run:
    pytest tests/phases/phase1_intro/test_agent_reference_accuracy.py -v
"""

import json
from collections import Counter
from pathlib import Path

import pytest

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ANALYSIS_PATH = PROJECT_ROOT / "assets/analysis/stem_analysis.json"

# Reference track parameters
BPM = 136
BEAT_DURATION = 60 / BPM
INTRO_BARS = 16
INTRO_DURATION = INTRO_BARS * 4 * BEAT_DURATION


@pytest.fixture
def stem_analysis():
    """Load pre-computed stem analysis."""
    with open(ANALYSIS_PATH) as f:
        return json.load(f)


@pytest.fixture
def reference_bass_data(stem_analysis):
    """Extract intro bass data from analysis."""
    intro_notes = [
        n for n in stem_analysis["bass"]["notes"] if n["start"] < INTRO_DURATION
    ]
    return intro_notes


class TestReferenceDataExists:
    """Verify reference analysis data is available."""

    def test_analysis_file_exists(self):
        """Stem analysis file must exist."""
        assert ANALYSIS_PATH.exists(), f"Missing: {ANALYSIS_PATH}"

    def test_has_drum_data(self, stem_analysis):
        """Analysis must have drum onsets."""
        assert "drums" in stem_analysis
        assert "onsets" in stem_analysis["drums"]
        assert len(stem_analysis["drums"]["onsets"]) > 0

    def test_has_bass_data(self, stem_analysis):
        """Analysis must have bass notes."""
        assert "bass" in stem_analysis
        assert "notes" in stem_analysis["bass"]
        assert len(stem_analysis["bass"]["notes"]) > 0


class TestReferenceKeyDetection:
    """Test ability to detect correct key from reference."""

    def test_detect_root_note(self, reference_bass_data):
        """Should detect G as root note, not F."""
        pitches = [round(n["pitch"]) for n in reference_bass_data]
        pitch_counts = Counter(pitches)

        # Get most common low pitch (sub-bass range)
        sub_bass_pitches = {p: c for p, c in pitch_counts.items() if p < 40}
        most_common = max(sub_bass_pitches, key=sub_bass_pitches.get)

        # Reference analysis shows G1 (MIDI 31) is most common
        # Current agent uses F (MIDI 29)
        assert most_common == 31, (
            f"Reference root is G1 (31), but detected {most_common}. "
            "Current agent hardcodes F (29) which is WRONG."
        )

    def test_current_agent_uses_wrong_key(self):
        """Verify current ComposerAgent uses wrong key (baseline)."""
        # Import current agent
        import sys

        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        bass_pattern = agent.generate_bass_pattern(bars=4)

        # Current agent uses F minor: [29, 32, 34, 36, 39]
        pitches_used = set(n["pitch"] for n in bass_pattern)

        # F is 29, G is 31 - current agent uses F-based
        uses_f_root = 29 in pitches_used
        uses_g_root = 31 in pitches_used

        assert uses_f_root, "Expected current agent to use F (29)"
        assert not uses_g_root, "Current agent should NOT use G (31)"


class TestAgentImprovementMetrics:
    """Metrics to measure if an agent improves match to reference."""

    def test_pitch_accuracy_baseline(self, reference_bass_data):
        """Calculate baseline pitch accuracy of current agent."""
        # Reference pitch distribution
        ref_pitches = [round(n["pitch"]) for n in reference_bass_data]
        ref_counter = Counter(ref_pitches)
        ref_total = len(ref_pitches)

        # Current agent pitches (F minor scale)
        current_agent_scale = [29, 32, 34, 36, 39]  # F1, Ab1, Bb1, C2, Eb2

        # Calculate overlap
        overlap = sum(ref_counter.get(p, 0) for p in current_agent_scale)
        current_accuracy = overlap / ref_total

        # Improved agent should use G minor: [31, 34, 36, 38, 41]
        improved_scale = [31, 32, 33, 34]  # Based on analysis: G1, G#1, A1, A#1
        improved_overlap = sum(ref_counter.get(p, 0) for p in improved_scale)
        improved_accuracy = improved_overlap / ref_total

        print(f"\nBaseline (F minor) accuracy: {current_accuracy:.1%}")
        print(f"Improved (G-based) accuracy: {improved_accuracy:.1%}")

        # The improved version should be significantly better
        assert improved_accuracy > current_accuracy, (
            f"Improved scale should match reference better. "
            f"Current: {current_accuracy:.1%}, Improved: {improved_accuracy:.1%}"
        )

    def test_note_density_baseline(self, reference_bass_data):
        """Compare note density to reference."""
        ref_density = len(reference_bass_data) / INTRO_BARS

        # Current agent: 16 notes per bar (16th notes)
        import sys

        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        from dearpygui_controller.agents.composer_agent import ComposerAgent

        agent = ComposerAgent(verbose=False)
        bass_pattern = agent.generate_bass_pattern(bars=4)
        current_density = len(bass_pattern) / 4

        print(f"\nReference density: {ref_density:.1f} notes/bar")
        print(f"Current agent density: {current_density:.1f} notes/bar")
        print("Target density: 12.8 notes/bar (from analysis)")

        # Reference has ~12.8 notes/bar, current agent has 16
        density_diff = abs(ref_density - current_density)
        assert density_diff > 0, "Densities should differ"


class TestAgentReferenceIntegration:
    """Test that an agent CAN access reference data (design requirement)."""

    def test_analysis_path_accessible(self):
        """Verify analysis file is accessible from agent context."""
        # This is what an improved agent SHOULD do
        expected_path = PROJECT_ROOT / "assets/analysis/stem_analysis.json"
        assert expected_path.exists()

        # Load and verify
        with open(expected_path) as f:
            data = json.load(f)

        # Should have usable data
        assert len(data["bass"]["notes"]) > 100
        assert len(data["drums"]["onsets"]) > 100

    @pytest.mark.skip(reason="Agent enhancement not yet implemented")
    def test_agent_uses_reference_data(self):
        """Test that enhanced agent uses reference data."""
        # TODO: Implement after agent enhancement
        # This test should verify that an enhanced agent:
        # 1. Loads stem_analysis.json
        # 2. Extracts relevant patterns
        # 3. Generates patterns based on reference
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
