"""
Groove and Humanization Tests

Per Spec 2.1: Swing 16-99 @ 10-15% on hats/ride
"""

import pytest


class TestGrooveHumanization:
    """Test groove template application."""
    
    def test_swing_template_on_hihats(self, song):
        """Closed hats use Swing 16-99."""
        hihat_track = song.get_track(5)
        clip = hihat_track.get_clip(0)
        assert clip.get_groove() == "Swing 16-99"
        assert 0.10 <= clip.get_groove_amount() <= 0.15
    
    def test_kick_no_groove(self, song):
        """Kick stays quantized (no groove)."""
        kick_track = song.get_track(1)
        clip = kick_track.get_clip(0)
        assert clip.get_groove() is None


# TODO: Generate 20 comprehensive groove tests
