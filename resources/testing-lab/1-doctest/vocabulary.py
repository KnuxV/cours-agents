"""Vocabulary helpers, with doctests that check an exact value, then a property.

A doctest compares what Python prints. The first example of each function
prints the answer itself, as in text_tools.py. The next ones do not: they
print True, because they are questions about the answer — with `in`,
`not in`, `>`, `<=`...

Run the examples, either way:
    uv run python vocabulary.py -v
    uv run python -m doctest -v vocabulary.py
"""


def tokenize(text: str) -> list[str]:
    """Split a text into lowercase words, without the punctuation around them.

    >>> tokenize("Le chat dort.")
    ['le', 'chat', 'dort']
    >>> "chat" in tokenize("Le chat dort.")
    True
    >>> "Le" in tokenize("Le chat dort.")
    False
    >>> "dort." not in tokenize("Le chat dort.")
    True
    """
    words = [word.strip(".,;:!?") for word in text.lower().split()]
    return [word for word in words if word != ""]


def longest_word(text: str) -> str:
    """The longest word of a text. When several are equally long, any of them.

    >>> longest_word("il dort profondément")
    'profondément'
    >>> len(longest_word("il dort profondément")) > 5
    True
    >>> longest_word("le chat dort") in ["chat", "dort"]
    True
    """
    return max(tokenize(text), key=len)


def type_token_ratio(tokens: list[str]) -> float:
    """Share of distinct words: 1.0 means no word is repeated.

    >>> type_token_ratio(["le", "chat", "le", "chien"])
    0.75
    >>> 0 < type_token_ratio(["le", "chat", "le"]) <= 1
    True
    >>> type_token_ratio(["le", "chat", "le"]) < type_token_ratio(["le", "chat"])
    True
    """
    return len(set(tokens)) / len(tokens)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
