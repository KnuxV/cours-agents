"""Checks on the real data files: every CSV in data/ is checked.

The fixtures below have `params`: each test runs once per file, and the
file name appears in the report, e.g. test_ratings_between_1_and_5[week2.csv].
A new week's file dropped into data/ is checked automatically.
"""
from pathlib import Path

import pandas as pd
import pytest

from pipeline import clean, load

DATA_FILES: list[Path] = sorted((Path(__file__).parent.parent / "data").glob("*.csv"))
EXPECTED_COLUMNS: list[str] = ["review_id", "product", "lang", "rating", "text"]


@pytest.fixture(params=DATA_FILES, ids=lambda path: path.name)
def raw(request: pytest.FixtureRequest) -> pd.DataFrame:
    """The file exactly as it arrived."""
    return load(request.param)


@pytest.fixture
def reviews(raw: pd.DataFrame) -> pd.DataFrame:
    """The file after clean(). Skipped when the columns are wrong: nothing else can be checked."""
    if list(raw.columns) != EXPECTED_COLUMNS:
        pytest.skip("wrong columns, see test_expected_columns")
    return clean(raw)


def test_expected_columns(raw: pd.DataFrame) -> None:
    assert list(raw.columns) == EXPECTED_COLUMNS


def test_languages_are_fr_or_en(reviews: pd.DataFrame) -> None:
    unknown = sorted(set(reviews["lang"]) - {"fr", "en"})
    assert unknown == []


def test_ratings_between_1_and_5(reviews: pd.DataFrame) -> None:
    outside = reviews[~reviews["rating"].between(1, 5)]
    # {review_id: rating} for every rating outside 1-5
    assert dict(zip(outside["review_id"], outside["rating"])) == {}


def test_no_missing_or_empty_text(reviews: pd.DataFrame) -> None:
    empty = reviews[reviews["text"].isna() | (reviews["text"] == "")]
    assert empty["review_id"].tolist() == []


def test_review_ids_are_unique(reviews: pd.DataFrame) -> None:
    duplicated = reviews[reviews["review_id"].duplicated()]
    assert duplicated["review_id"].tolist() == []
