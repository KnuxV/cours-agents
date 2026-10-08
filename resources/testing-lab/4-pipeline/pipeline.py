"""Weekly review report.

Every week a colleague sends a CSV of product reviews. This script reads it
and prints, for each language, the number of reviews, the mean rating and
the mean length of a review in words.

Run:   uv run pipeline.py data/week1.csv
"""
import sys
from pathlib import Path

import pandas as pd


def load(path: str | Path) -> pd.DataFrame:
    """Step 1 — read the CSV file into a table."""
    # pandas lit le fichier : une ligne par avis, une colonne par information
    return pd.read_csv(path)


def clean(reviews: pd.DataFrame) -> pd.DataFrame:
    """Step 2 — tidy the table. Returns a new table; the input is not modified."""
    # on travaille sur une copie, pour ne pas modifier le tableau reçu
    reviews = reviews.copy()
    # on enlève les espaces au début et à la fin de chaque texte
    reviews["text"] = reviews["text"].str.strip()
    return reviews


def add_n_tokens(reviews: pd.DataFrame) -> pd.DataFrame:
    """Step 3 — add a column with the number of words in each review."""
    reviews = reviews.copy()
    # nouvelle colonne n_tokens : le nombre de mots de chaque avis
    # \S+ matches a run of non-space characters: one word, as in text.split()
    reviews["n_tokens"] = reviews["text"].str.count(r"\S+")
    return reviews


def summarise(reviews: pd.DataFrame) -> pd.DataFrame:
    """Step 4 — one row per language: how many reviews, mean rating, mean length."""
    # on regroupe les avis par langue, puis on calcule trois chiffres par groupe,
    # arrondis à deux décimales
    return (
        reviews.groupby("lang")
        .agg(
            n_reviews=("review_id", "count"),
            mean_rating=("rating", "mean"),
            mean_tokens=("n_tokens", "mean"),
        )
        .round(2)
    )


def main(path: str) -> None:
    # les quatre étapes, l'une après l'autre : lire, nettoyer, compter les mots, résumer
    reviews = load(path)
    reviews = clean(reviews)
    reviews = add_n_tokens(reviews)
    print(summarise(reviews))


if __name__ == "__main__":
    # sys.argv[1] : le chemin du fichier écrit dans la commande, après pipeline.py
    main(sys.argv[1])
