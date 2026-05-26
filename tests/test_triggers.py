from engines.trigger_engine import Trigger, matches_condition

def test_wildcards():
    t = Trigger("contains", "*bad*", "delete", None)
    assert matches_condition("very bad thing", t)
