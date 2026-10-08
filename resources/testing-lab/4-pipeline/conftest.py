"""Shared fixtures for the pipeline tests (and the marker of the project root)."""
import pandas as pd
import pytest


@pytest.fixture
def small_reviews() -> pd.DataFrame:
    """Five reviews written by hand, with the problems we have met in real files."""
    # un tableau volontairement imparfait : "FR" en majuscules, "en " avec une espace,
    # un texte manquant (None) et un texte fait seulement d'espaces
    return pd.DataFrame(
        {
            "review_id": [1, 2, 3, 4, 5],
            "product": ["livre", "livre", "lampe", "lampe", "sac"],
            "lang": ["fr", "FR", "en ", "en", "fr"],
            "rating": [5, 3, 4, 2, 1],
            "text": ["  Très bien ", "Bof", "Nice lamp", None, "   "],
        }
    )
