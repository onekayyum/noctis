from handlers.moderation import parse_time

def test_parse_time():
    assert parse_time("30d") == 2592000
    assert parse_time("2w") == 1209600
    assert parse_time("10h") == 36000
    assert parse_time("2m") == 120
    assert parse_time("45s") == 45
    assert parse_time("bad") is None
