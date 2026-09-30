"""Small text helpers, with their examples written inside the docstrings.

Run the examples, either way:
    uv run python text_tools.py -v             (the block at the bottom of this file)
    uv run python -m doctest -v text_tools.py  (works on any file, no block needed)
"""


def count_words(text: str) -> int:
    """Count the words in a text (words are separated by whitespace).

    >>> count_words("le chat dort")
    3
    >>> count_words("  le   chat  ")
    2
    >>> count_words("")
    0
    >>> count_words("Je m")
    """
    return len(text.split())


def normalize(text: str) -> str:
    """Lowercase a text and remove the spaces around it.

    >>> normalize("  Le Chat ")
    'le chat'
    """
    return text.strip().lower()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
