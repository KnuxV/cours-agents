"""Plain assert checks, no test framework.

Run:   uv run check_text_tools.py
"""
from text_tools import count_words, normalize

# chaque assert compare ce que la fonction renvoie à ce qu'on attend ;
# si un assert échoue, le script s'arrête là et les lignes suivantes ne tournent pas
assert count_words("le chat dort") == 3
assert count_words("") == 0
# le texte après la virgule s'affiche si la vérification échoue
assert count_words("Bonjour, le monde !") == 3, "punctuation counted as a word?"
assert normalize("  Le Chat ") == "le chat"
assert normalize("ÉTÉ") == "été"

# affiché seulement si aucun assert n'a échoué
print("All checks passed")
