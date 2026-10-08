"""Small text helpers, now tested with pytest (see tests/test_text_tools.py)."""
from pathlib import Path


def count_words(text: str) -> int:
    """Count the words in a text (words are separated by whitespace)."""
    # split() coupe le texte à chaque espace ; len() compte les morceaux obtenus
    return len(text.split())


def normalize(text: str) -> str:
    """Lowercase a text and remove the spaces around it."""
    # strip() enlève les espaces au début et à la fin, lower() met en minuscules
    return text.strip().lower()


def type_token_ratio(tokens: list[str]) -> float:
    """Share of distinct words: 1.0 means no word is repeated."""
    # une liste vide donnerait une division par zéro : on refuse avec une erreur claire
    if not tokens:
        raise ValueError("cannot compute a ratio on an empty list")
    # set() ne garde qu'un exemplaire de chaque mot : mots différents / nombre total de mots
    return len(set(tokens)) / len(tokens)


def count_words_in_file(path: str | Path) -> int:
    """Count the words in a UTF-8 text file."""
    # on lit tout le fichier comme un seul texte, puis on réutilise count_words
    return count_words(Path(path).read_text(encoding="utf-8"))
