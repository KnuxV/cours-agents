"""Small text helpers, with their examples written inside the docstrings.

Run the examples, either way:
    uv run text_tools.py -v                    (the block at the bottom of this file)
    uv run -m doctest -v text_tools.py         (works on any file, no block needed)
"""


def count_words(text: str) -> int:
    """Count the words in a text (words are separated by whitespace).

    >>> count_words("le chat dort")
    3
    >>> count_words("  le   chat  ")
    2
    >>> count_words("")
    0
    """
    # split() coupe le texte à chaque espace ; len() compte les morceaux obtenus
    return len(text.split())


def normalize(text: str) -> str:
    """Lowercase a text and remove the spaces around it.

    >>> normalize("  Le Chat ")
    'le chat'
    """
    # strip() enlève les espaces au début et à la fin, lower() met en minuscules
    return text.strip().lower()


if __name__ == "__main__":
    # ce bloc ne tourne que si on lance ce fichier lui-même : il vérifie les exemples >>>
    import doctest

    doctest.testmod()
