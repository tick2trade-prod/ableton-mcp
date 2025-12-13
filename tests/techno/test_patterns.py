
from tests.techno.patterns import get_kick_pattern, get_bass_pattern, get_lead_pattern

def test_kick_pattern():
    notes = get_kick_pattern(4.0)
    assert len(notes) == 16 # 4 bars of 4/4
    assert notes[0]["pitch"] == 36
    assert notes[0]["velocity"] > 100

def test_bass_pattern():
    notes = get_bass_pattern(4.0)
    assert len(notes) > 0
    # Check offbeat placement (none on exactly X.0)
    # Actually my logic put them on X.25, X.5, X.75
    for note in notes:
        assert note["start_time"] % 1.0 != 0.0

def test_lead_pattern():
    notes = get_lead_pattern(4.0)
    assert len(notes) > 0
    allowed = [40, 43, 47, 52] # E Minor
    for note in notes:
        assert note["pitch"] in allowed

def test_stab_pattern():
    from tests.techno.patterns import get_stab_pattern
    notes = get_stab_pattern(4.0)
    assert len(notes) > 0
    # Check for chord characteristic (multiple notes at same time)
    # Actually my pattern generator adds them sequentially in the list,
    # but share start_times.
    start_times = [n["start_time"] for n in notes]
    # Check duplicates in start_times (chords)
    assert len(start_times) > len(set(start_times))
