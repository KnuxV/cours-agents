"""Small text helpers, with their examples written inside the docstrings.

Run the examples:   uv run python -m doctest -v text_tools.py
"""


def count_words(text):
    """Count the words in a text (words are separated by whitespace).

    >>> count_words("le chat dort")
    3
    >>> count_words("  le   chat  ")
    2
    >>> count_words("")
    0
    """
    return len(text.split())


def normalize(text):
    """Lowercase a text and remove the spaces around it.

    >>> normalize("  Le Chat ")
    'le chat'
    """
    return text.strip().lower()
