"""Small text helpers, now tested with pytest (see tests/test_text_tools.py)."""
from pathlib import Path


def count_words(text):
    """Count the words in a text (words are separated by whitespace)."""
    return len(text.split())


def normalize(text):
    """Lowercase a text and remove the spaces around it."""
    return text.strip().lower()


def type_token_ratio(tokens):
    """Share of distinct words: 1.0 means no word is repeated."""
    if not tokens:
        raise ValueError("cannot compute a ratio on an empty list")
    return len(set(tokens)) / len(tokens)


def count_words_in_file(path):
    """Count the words in a UTF-8 text file."""
    return count_words(Path(path).read_text(encoding="utf-8"))
