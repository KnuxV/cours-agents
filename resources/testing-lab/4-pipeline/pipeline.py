"""Weekly review report.

Every week a colleague sends a CSV of product reviews. This script reads it
and prints, for each language, the number of reviews, the mean rating and
the mean length of a review in words.

Run:   uv run python pipeline.py data/week1.csv
"""
import sys

import pandas as pd


def load(path):
    """Step 1 — read the CSV file into a table."""
    return pd.read_csv(path)


def clean(reviews):
    """Step 2 — tidy the table. Returns a new table; the input is not modified."""
    reviews = reviews.copy()
    reviews["text"] = reviews["text"].str.strip()
    return reviews


def add_n_tokens(reviews):
    """Step 3 — add a column with the number of words in each review."""
    reviews = reviews.copy()
    reviews["n_tokens"] = reviews["text"].str.split().str.len()
    return reviews


def summarise(reviews):
    """Step 4 — one row per language: how many reviews, mean rating, mean length."""
    return (
        reviews.groupby("lang")
        .agg(
            n_reviews=("review_id", "count"),
            mean_rating=("rating", "mean"),
            mean_tokens=("n_tokens", "mean"),
        )
        .round(2)
    )


def main(path):
    reviews = load(path)
    reviews = clean(reviews)
    reviews = add_n_tokens(reviews)
    print(summarise(reviews))


if __name__ == "__main__":
    main(sys.argv[1])
