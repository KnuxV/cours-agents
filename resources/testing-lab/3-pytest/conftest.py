"""pytest reads this file first.

1. Its presence tells pytest "this folder is the root", so the tests in
   tests/ can write `from text_tools import ...`.
2. Fixtures written here are available to every test file.
"""
import pytest


@pytest.fixture
def tokens() -> list[str]:
    """A short tokenised sentence, rebuilt fresh for every test that asks for it."""
    # une fixture : pytest appelle cette fonction et donne son résultat
    # à chaque test qui a un paramètre nommé `tokens`
    return ["le", "chat", "voit", "le", "chien"]
