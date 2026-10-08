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
    # trois mots séparés par une espace
    assert count_words("le chat dort") == 3


def test_count_words_empty_text() -> None:
    # un texte vide ne contient aucun mot
    assert count_words("") == 0


def test_count_words_double_spaces() -> None:
    # plusieurs espaces de suite ne créent pas de mots en plus
    assert count_words("le  chat   dort") == 3


def test_normalize() -> None:
    # minuscules, et plus d'espaces autour
    assert normalize("  Le Chat ") == "le chat"


def test_type_token_ratio() -> None:
    # 2 mots différents sur 3 ; approx parce que 2 / 3 est un nombre à virgule
    assert type_token_ratio(["le", "chat", "le"]) == pytest.approx(2 / 3)


def test_type_token_ratio_empty() -> None:
    # une liste vide doit donner 0.0, pas une erreur
    assert type_token_ratio([]) == 0.0


def test_top_words_most_frequent_first() -> None:
    # "le" apparaît 3 fois, "chat" 2 fois, "chien" 1 fois : le plus fréquent vient en premier
    tokens = ["le", "chat", "le", "chien", "le", "chat"]
    assert top_words(tokens, 2) == ["le", "chat"]


def test_top_words_returns_n_words() -> None:
    # on demande 3 mots : la liste renvoyée doit en contenir exactement 3
    tokens = ["a", "b", "c", "d"]
    assert len(top_words(tokens, 3)) == 3


def test_rating_change_up() -> None:
    # la note passe de 2 à 5 : elle a monté de 3
    assert rating_change(before=2, after=5) == 3


def test_rating_change_down() -> None:
    # la note passe de 4 à 1 : elle a baissé de 3, donc -3
    assert rating_change(before=4, after=1) == -3


def test_mean_sentence_length() -> None:
    # deux phrases, de 3 et 5 mots : la moyenne est 4
    assert mean_sentence_length("Le chat dort. Le chien mange sa soupe.") == 4.0
