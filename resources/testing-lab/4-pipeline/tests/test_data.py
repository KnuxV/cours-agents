"""Checks on the real data files: every CSV in data/ is checked.

The fixtures below have `params`: each test runs once per file, and the
file name appears in the report, e.g. test_ratings_between_1_and_5[week2.csv].
A new week's file dropped into data/ is checked automatically.
"""
from pathlib import Path

import pandas as pd
import pytest

from pipeline import clean, load

# tous les fichiers .csv du dossier data/
DATA_FILES: list[Path] = sorted((Path(__file__).parent.parent / "data").glob("*.csv"))
# les colonnes qu'un fichier doit avoir, dans cet ordre
EXPECTED_COLUMNS: list[str] = ["review_id", "product", "lang", "rating", "text"]


@pytest.fixture(params=DATA_FILES, ids=lambda path: path.name)
def raw(request: pytest.FixtureRequest) -> pd.DataFrame:
    """The file exactly as it arrived."""
    # request.param : un des fichiers de DATA_FILES, chacun son tour
    return load(request.param)


@pytest.fixture
def reviews(raw: pd.DataFrame) -> pd.DataFrame:
    """The file after clean(). Skipped when the columns are wrong: nothing else can be checked."""
    # si les colonnes ne sont pas les bonnes, on saute le test au lieu de le laisser planter
    if list(raw.columns) != EXPECTED_COLUMNS:
        pytest.skip("wrong columns, see test_expected_columns")
    return clean(raw)


def test_expected_columns(raw: pd.DataFrame) -> None:
    # le fichier a exactement les colonnes attendues
    assert list(raw.columns) == EXPECTED_COLUMNS


def test_languages_are_fr_or_en(reviews: pd.DataFrame) -> None:
    # les langues qui ne sont ni "fr" ni "en" ; on compare à une liste vide
    # pour que le message d'échec montre les valeurs fautives
    unknown = sorted(set(reviews["lang"]) - {"fr", "en"})
    assert unknown == []


def test_ratings_between_1_and_5(reviews: pd.DataFrame) -> None:
    # les avis dont la note n'est pas entre 1 et 5 : il ne doit pas y en avoir
    outside = reviews[~reviews["rating"].between(1, 5)]
    # {review_id: rating} for every rating outside 1-5
    assert dict(zip(outside["review_id"], outside["rating"])) == {}


def test_no_missing_or_empty_text(reviews: pd.DataFrame) -> None:
    # les avis sans texte : valeur manquante ou texte vide
    empty = reviews[reviews["text"].isna() | (reviews["text"] == "")]
    assert empty["review_id"].tolist() == []


def test_review_ids_are_unique(reviews: pd.DataFrame) -> None:
    # les identifiants qui apparaissent plus d'une fois
    duplicated = reviews[reviews["review_id"].duplicated()]
    assert duplicated["review_id"].tolist() == []
