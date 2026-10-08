from pathlib import Path

import pandas as pd

from pipeline import add_n_tokens, clean, load, summarise

HERE = Path(__file__).parent


def test_summarise_by_hand() -> None:
    # un tableau assez petit pour calculer le résumé de tête
    reviews = pd.DataFrame(
        {
            "review_id": [1, 2, 3],
            "lang": ["fr", "fr", "en"],
            "rating": [5, 2, 4],
            "n_tokens": [10, 4, 6],
        }
    )
    summary = summarise(reviews)
    # fr : 2 avis, note moyenne (5 + 2) / 2 = 3.5 ; en : un seul avis de 6 mots
    assert summary.loc["fr", "n_reviews"] == 2
    assert summary.loc["fr", "mean_rating"] == 3.5
    assert summary.loc["en", "mean_tokens"] == 6


def test_week1_summary_has_not_changed() -> None:
    """Regression test: week 1's report was checked by hand once and saved.

    To save it again (only after checking the new numbers by hand):
    uv run python -c "import pipeline as p; p.summarise(p.add_n_tokens(p.clean(p.load('data/week1.csv')))).to_csv('tests/expected/week1_summary.csv')"
    """
    # on refait tout le calcul sur le fichier de la semaine 1...
    result = summarise(add_n_tokens(clean(load(HERE.parent / "data" / "week1.csv"))))
    # ...et on le compare au résultat enregistré : le moindre chiffre différent fait échouer le test
    expected = pd.read_csv(HERE / "expected" / "week1_summary.csv", index_col="lang")
    pd.testing.assert_frame_equal(result, expected)
