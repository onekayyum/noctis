from engines.xp_engine import level_for_xp

def test_level_thresholds():
    assert level_for_xp(0) == 1
    assert level_for_xp(100) >= 2
