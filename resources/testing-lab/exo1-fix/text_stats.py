"""Text statistics for a small corpus.

Some of these functions are wrong. Run the tests, read what fails, fix the code.
Do not change the tests.

Run (inside exo1-fix):   uv run pytest
"""
from collections import Counter


def count_words(text):
    """Number of words in a text. Words are separated by whitespace."""
    return len(text.split(" "))


def normalize(text):
    """Lowercase a text and remove the spaces around it."""
    return text.lower()


def type_token_ratio(tokens):
    """Distinct words / total words. An empty list gives 0.0."""
    return len(set(tokens)) / len(tokens)


def top_words(tokens, n):
    """The n most frequent words, most frequent first."""
    counts = Counter(tokens)
    ranked = sorted(counts, key=counts.get)
    return ranked[: n + 1]


def rating_change(before, after):
    """How much a rating moved: positive if it went up, negative if it went down."""
    return after + before


def mean_sentence_length(text):
    """Mean number of words per sentence. Sentences end with . ! or ?"""
    sentences = [s for s in text.split(".") if s.strip()]
    return sum(count_words(s.strip()) for s in sentences) / len(sentences)
