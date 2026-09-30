"""pytest reads this file first.

1. Its presence tells pytest "this folder is the root", so the tests in
   tests/ can write `from text_tools import ...`.
2. Fixtures written here are available to every test file.
"""
import pytest


@pytest.fixture
def tokens():
    """A short tokenised sentence, rebuilt fresh for every test that asks for it."""
    return ["le", "chat", "voit", "le", "chien"]
