"""
Arrangement Timeline Tests

7 sections × 16 bars = 112 bars total
"""

import pytest


class TestArrangementStructure:
    """Test song structure per spec Section 7.1."""
    
    def test_intro_bars_1_to_16(self, song):
        """Intro section spans bars 1-16."""
        intro = song.get_section("intro")
        assert intro.start_bar == 1
        assert intro.end_bar == 16
    
    def test_intro_active_tracks(self, song):
        """Only kick, rumble, hats active in intro."""
        intro = song.get_section("intro")
        active = intro.get_active_tracks()
        assert 1 in active  # Kick
        assert 2 in active  # Rumble
        assert 5 in active  # Closed Hats
        assert len(active) == 3
    
    def test_breakdown1_kick_removed(self, song):
        """Breakdown 1: Kick removed per spec."""
        breakdown1 = song.get_section("breakdown_1")
        active = breakdown1.get_active_tracks()
        assert 1 not in active  # Kick removed!


# TODO: Generate 50 comprehensive arrangement tests
