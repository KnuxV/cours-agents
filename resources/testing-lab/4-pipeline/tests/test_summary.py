from pathlib import Path

import pandas as pd

from pipeline import add_n_tokens, clean, load, summarise

HERE = Path(__file__).parent


def test_summarise_by_hand() -> None:
    reviews = pd.DataFrame(
        {
            "review_id": [1, 2, 3],
            "lang": ["fr", "fr", "en"],
            "rating": [5, 2, 4],
            "n_tokens": [10, 4, 6],
        }
    )
    summary = summarise(reviews)
    assert summary.loc["fr", "n_reviews"] == 2
    assert summary.loc["fr", "mean_rating"] == 3.5
    assert summary.loc["en", "mean_tokens"] == 6


def test_week1_summary_has_not_changed() -> None:
    """Regression test: week 1's report was checked by hand once and saved.

    To save it again (only after checking the new numbers by hand):
    uv run python -c "import pipeline as p; p.summarise(p.add_n_tokens(p.clean(p.load('data/week1.csv')))).to_csv('tests/expected/week1_summary.csv')"
    """
    result = summarise(add_n_tokens(clean(load(HERE.parent / "data" / "week1.csv"))))
    expected = pd.read_csv(HERE / "expected" / "week1_summary.csv", index_col="lang")
    pd.testing.assert_frame_equal(result, expected)
