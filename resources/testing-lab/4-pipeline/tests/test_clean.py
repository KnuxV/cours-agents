"""Unit tests for clean(), on a small table written by hand (see conftest.py)."""
import pandas as pd

from pipeline import clean


def test_clean_strips_text(small_reviews: pd.DataFrame) -> None:
    cleaned = clean(small_reviews)
    assert cleaned["text"].iloc[0] == "Très bien"


def test_clean_normalizes_lang(small_reviews: pd.DataFrame) -> None:
    cleaned = clean(small_reviews)
    assert set(cleaned["lang"]) == {"fr", "en"}


def test_clean_drops_missing_and_blank_text(small_reviews: pd.DataFrame) -> None:
    cleaned = clean(small_reviews)
    assert cleaned["review_id"].tolist() == [1, 2, 3]


def test_clean_does_not_modify_its_input(small_reviews: pd.DataFrame) -> None:
    before = small_reviews.copy()
    clean(small_reviews)
    pd.testing.assert_frame_equal(small_reviews, before)
