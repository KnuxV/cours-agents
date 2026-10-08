"""Unit tests for clean(), on a small table written by hand (see conftest.py)."""
import pandas as pd

from pipeline import clean


def test_clean_strips_text(small_reviews: pd.DataFrame) -> None:
    # le premier avis vaut "  Très bien " : après clean, plus d'espaces autour
    cleaned = clean(small_reviews)
    assert cleaned["text"].iloc[0] == "Très bien"


def test_clean_normalizes_lang(small_reviews: pd.DataFrame) -> None:
    # "FR" et "en " doivent devenir "fr" et "en" : il ne reste que deux langues
    cleaned = clean(small_reviews)
    assert set(cleaned["lang"]) == {"fr", "en"}


def test_clean_drops_missing_and_blank_text(small_reviews: pd.DataFrame) -> None:
    # les avis 4 (texte manquant) et 5 (texte vide) doivent être retirés
    cleaned = clean(small_reviews)
    assert cleaned["review_id"].tolist() == [1, 2, 3]


def test_clean_does_not_modify_its_input(small_reviews: pd.DataFrame) -> None:
    # on garde une copie du tableau, on appelle clean, puis on vérifie que l'original n'a pas bougé
    before = small_reviews.copy()
    clean(small_reviews)
    pd.testing.assert_frame_equal(small_reviews, before)
