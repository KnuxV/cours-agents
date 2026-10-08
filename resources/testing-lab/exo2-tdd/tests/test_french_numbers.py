from french_numbers import parse_number


def test_whole_number() -> None:
    # le cas le plus simple : un nombre entier, sans virgule ni espace
    assert parse_number("12") == 12.0


# Next test: a decimal comma, "12,5" -> 12.5
