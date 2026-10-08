"""Text statistics for a small corpus.

Some of these functions are wrong. Run the tests, read what fails, fix the code.
Do not change the tests.

Run (inside exo1-fix):   uv run pytest
"""
from collections import Counter


def count_words(text: str) -> int:
    """Number of words in a text. Words are separated by whitespace."""
    # but : le nombre de mots du texte
    return len(text.split(" "))


def normalize(text: str) -> str:
    """Lowercase a text and remove the spaces around it."""
    # but : le même texte, en minuscules, sans espaces au début ni à la fin
    return text.lower()


def type_token_ratio(tokens: list[str]) -> float:
    """Distinct words / total words. An empty list gives 0.0."""
    # but : la part de mots différents (entre 0 et 1), et 0.0 pour une liste vide
    return len(set(tokens)) / len(tokens)


def top_words(tokens: list[str], n: int) -> list[str]:
    """The n most frequent words, most frequent first."""
    # but : compter chaque mot, les classer, garder les n plus fréquents
    counts = Counter(tokens)
    ranked = sorted(counts, key=lambda word: counts[word])
    return ranked[: n + 1]


def rating_change(before: float, after: float) -> float:
    """How much a rating moved: positive if it went up, negative if it went down."""
    # but : la différence entre la note d'après et la note d'avant
    return after + before


def mean_sentence_length(text: str) -> float:
    """Mean number of words per sentence. Sentences end with . ! or ?"""
    # but : découper le texte en phrases, puis faire la moyenne du nombre de mots par phrase
    sentences = [s for s in text.split(".") if s.strip()]
    return sum(count_words(s.strip()) for s in sentences) / len(sentences)
