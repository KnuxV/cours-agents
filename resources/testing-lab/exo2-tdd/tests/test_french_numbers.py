from french_numbers import parse_number


def test_whole_number() -> None:
    assert parse_number("12") == 12.0


# Next test: a decimal comma, "12,5" -> 12.5
