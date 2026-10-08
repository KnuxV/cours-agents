"""Plain assert checks, no test framework.

Run:   uv run check_text_tools.py
"""
from text_tools import count_words, normalize

assert count_words("le chat dort") == 3
assert count_words("") == 0
assert count_words("Bonjour, le monde !") == 3, "punctuation counted as a word?"
assert normalize("  Le Chat ") == "le chat"
assert normalize("ÉTÉ") == "été"

print("All checks passed")
