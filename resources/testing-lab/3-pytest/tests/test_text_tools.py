from pathlib import Path

import pytest

from text_tools import count_words, count_words_in_file, normalize, type_token_ratio


# --- The basics: one function, one assert --------------------------------

def test_count_words_simple_sentence() -> None:
    # le cas le plus simple : trois mots séparés par une espace
    assert count_words("le chat dort") == 3


def test_count_words_empty_text() -> None:
    # un cas limite : un texte vide contient zéro mot
    assert count_words("") == 0


def test_normalize_strips_and_lowercases() -> None:
    # les espaces autour disparaissent et les majuscules deviennent des minuscules
    assert normalize("  Le Chat ") == "le chat"


# --- parametrize: the same test on many values ---------------------------

@pytest.mark.parametrize(
    "text, expected",
    [
        ("le chat dort", 3),
        ("  le   chat  ", 2),
        ("", 0),
        ("l'enfant dort", 2),        # a choice: the apostrophe does not split
        ("Bonjour, le monde !", 4),  # a choice: "!" counts as a word
    ],
)
def test_count_words(text: str, expected: int) -> None:
    # ce test tourne une fois par ligne de la liste du dessus : cinq tests pour une seule fonction
    assert count_words(text) == expected


# --- pytest.raises: bad input must be refused -----------------------------

def test_type_token_ratio_refuses_empty_list() -> None:
    # le test réussit si le code dans le bloc lève une ValueError, et échoue sinon
    with pytest.raises(ValueError):
        type_token_ratio([])


# --- pytest.approx: never compare floats with == ---------------------------

def test_type_token_ratio_with_repetitions() -> None:
    # 2 mots différents sur 3 = 0.6666... : approx accepte un petit écart (ici 0.001)
    assert type_token_ratio(["a", "b", "a"]) == pytest.approx(0.667, abs=0.001)


# --- fixtures: `tokens` comes from conftest.py, `tmp_path` from pytest ----

def test_type_token_ratio_on_fixture(tokens: list[str]) -> None:
    # `tokens` est la liste préparée dans conftest.py : 5 mots, dont 4 différents
    assert type_token_ratio(tokens) == pytest.approx(4 / 5)


def test_count_words_in_file(tmp_path: Path) -> None:
    # tmp_path : un dossier temporaire vide, fourni par pytest ; on y écrit un petit fichier
    corpus = tmp_path / "corpus.txt"
    corpus.write_text("le chat dort\nle chien aussi\n", encoding="utf-8")
    # deux lignes de trois mots : la fonction doit en compter 6
    assert count_words_in_file(corpus) == 6
