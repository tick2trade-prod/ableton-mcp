"""
Full Song End-to-End Tests
"""

import pytest


class TestFullSong:
    """Complete song tests."""
    
    def test_all_16_tracks_exist(self, song):
        """All 16 tracks created."""
        assert song.track_count() == 16
    
    def test_tempo_136_bpm(self, song):
        """Tempo is 136 BPM."""
        assert abs(song.get_tempo() - 136.0) < 0.1
    
    def test_song_length_112_bars(self, song):
        """Song is 112 bars (7 sections × 16 bars)."""
        assert song.get_length_bars() == 112


# TODO: Generate 10 comprehensive E2E tests
