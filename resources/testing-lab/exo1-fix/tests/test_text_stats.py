import pytest

from text_stats import (
    count_words,
    mean_sentence_length,
    normalize,
    rating_change,
    top_words,
    type_token_ratio,
)


def test_count_words_simple():
    assert count_words("le chat dort") == 3


def test_count_words_empty_text():
    assert count_words("") == 0


def test_count_words_double_spaces():
    assert count_words("le  chat   dort") == 3


def test_normalize():
    assert normalize("  Le Chat ") == "le chat"


def test_type_token_ratio():
    assert type_token_ratio(["le", "chat", "le"]) == pytest.approx(2 / 3)


def test_type_token_ratio_empty():
    assert type_token_ratio([]) == 0.0


def test_top_words_most_frequent_first():
    tokens = ["le", "chat", "le", "chien", "le", "chat"]
    assert top_words(tokens, 2) == ["le", "chat"]


def test_top_words_returns_n_words():
    tokens = ["a", "b", "c", "d"]
    assert len(top_words(tokens, 3)) == 3


def test_rating_change_up():
    assert rating_change(before=2, after=5) == 3


def test_rating_change_down():
    assert rating_change(before=4, after=1) == -3


def test_mean_sentence_length():
    assert mean_sentence_length("Le chat dort. Le chien mange sa soupe.") == 4.0
