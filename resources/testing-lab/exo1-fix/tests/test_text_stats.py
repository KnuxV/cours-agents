import pytest

from text_stats import (
    count_words,
    mean_sentence_length,
    normalize,
    rating_change,
    top_words,
    type_token_ratio,
)


def test_count_words_simple() -> None:
    assert count_words("le chat dort") == 3


def test_count_words_empty_text() -> None:
    assert count_words("") == 0


def test_count_words_double_spaces() -> None:
    assert count_words("le  chat   dort") == 3


def test_normalize() -> None:
    assert normalize("  Le Chat ") == "le chat"


def test_type_token_ratio() -> None:
    assert type_token_ratio(["le", "chat", "le"]) == pytest.approx(2 / 3)


def test_type_token_ratio_empty() -> None:
    assert type_token_ratio([]) == 0.0


def test_top_words_most_frequent_first() -> None:
    tokens = ["le", "chat", "le", "chien", "le", "chat"]
    assert top_words(tokens, 2) == ["le", "chat"]


def test_top_words_returns_n_words() -> None:
    tokens = ["a", "b", "c", "d"]
    assert len(top_words(tokens, 3)) == 3


def test_rating_change_up() -> None:
    assert rating_change(before=2, after=5) == 3


def test_rating_change_down() -> None:
    assert rating_change(before=4, after=1) == -3


def test_mean_sentence_length() -> None:
    assert mean_sentence_length("Le chat dort. Le chien mange sa soupe.") == 4.0
