# 2.5 — Polars vs pandas

Lesson: [Session 2 — Python tooling](../sessions/s2.md) · [All exercises](index.md)

**Goal:** feel the difference between expressions and chained indexing, and measure the speed.

1. `uv add pandas` in a scratch branch of your course repo (`git switch -c polars-vs-pandas`).
2. Generate a larger file: 1,000,000 rows of `region, product, units, unit_price` with random values (Python's `random` module is enough), written with `csv` or Polars.
3. Write `bench.py`: read the file and compute revenue per region with pandas, then with Polars; time each with `time.perf_counter()`.
4. In a comment at the top of the script, three sentences on how the *code* differs, not just the timing.

??? note "Solution sketch"
    ```python
    import time, pandas as pd, polars as pl

    t = time.perf_counter()
    pdf = pd.read_csv("big.csv")
    pdf["revenue"] = pdf["units"] * pdf["unit_price"]
    print(pdf.groupby("region")["revenue"].sum().sort_values(ascending=False).head(3))
    print("pandas:", round(time.perf_counter() - t, 2), "s")

    t = time.perf_counter()
    df = pl.read_csv("big.csv")
    print(df.with_columns((pl.col("units") * pl.col("unit_price")).alias("revenue"))
            .group_by("region").agg(pl.col("revenue").sum())
            .sort("revenue", descending=True).head(3))
    print("polars:", round(time.perf_counter() - t, 2), "s")
    ```

    Expect Polars to be several times faster on read and group-by; the exact ratio depends on the machine. The point for the comment: pandas mutates a column in place on a named DataFrame; Polars describes the whole computation as a chain of expressions on immutable frames, which is what lets it optimise (and parallelise) the plan.
