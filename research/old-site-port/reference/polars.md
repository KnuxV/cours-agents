<!--
PORTED FROM last year's material (KnuxV/advanced_programming_python):
  lessons/05-polars_vs_pandas.md          — pandas refresher, why Polars, the expression API,
      SQL-like operations, lazy evaluation, streaming, larger-than-RAM, nested types, pivot/explode,
      string operations, structs
  code-examples/05-polars_vs_pandas.ipynb — the live-coding notebook (Titanic + villes_france.db)

PROPOSED DESTINATION: site/docs/reference/polars.md
  Nav (site/mkdocs.yml, under "Reference"):
      - Python and quality:
          - Polars beyond the basics: reference/polars.md
  Row for site/docs/reference/index.md, section "Python and quality":
      | [Polars beyond the basics](polars.md) | Expressions, `group_by`, window functions, joins and the row-count trap, lazy queries and files bigger than memory | [Session 2 — §7](../sessions/s2.md#7-bonus-polars-in-five-minutes) (bonus) |

REWRITTEN, not pasted: the Titanic and the French-cities SQLite database of last year's notebook are
replaced by `sales.csv`, the file Session 2 already uses, so the page needs no download and no
database; `pip install polars` → `uv add polars`; every claimed output below was produced on this
machine (polars 1.44.2, CPython 3.12.14) and pasted verbatim.
SPEC status: Polars is explicitly "optional/bonus" in SPEC Session 2. This page is reference, not
required reading.
-->

# Polars beyond the basics

[Session 2, §7](../sessions/s2.md#7-bonus-polars-in-five-minutes) gets you as far as `read_csv`, `filter`, `with_columns` and `group_by`. This page is what makes Polars worth switching to rather than merely a different spelling of pandas: **expressions**, window functions, the joins that quietly duplicate your rows, and lazy queries that never load the file you are querying.

Bonus material — nothing in the four sessions depends on it. Read it the week you have a file that is too big or a pipeline you no longer trust.

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
cd ~/agent-lab
uv add polars
curl -LO https://knuxv.github.io/cours-agents/files/sales.csv
```

Nine invented rows, four columns:

```text
region,product,units,unit_price
Alsace,coffee,120,3.5
Alsace,tea,80,2.8
…
```

## 1. An expression is not a result

This is the one idea. In pandas, `df["units"] * df["unit_price"]` immediately computes a column. In Polars, `pl.col("units") * pl.col("unit_price")` computes nothing: it is a **description** of a computation, a value you can name, pass around and reuse. Polars then runs it — possibly in parallel, possibly reordered, possibly on only the columns it turns out to need.

```python title="reuse.py"
import polars as pl

df = pl.read_csv("sales.csv")

revenue = (pl.col("units") * pl.col("unit_price")).alias("revenue")   # a recipe

print(df.with_columns(revenue).head(3))
```

```bash title="Any terminal, inside agent-lab"
uv run reuse.py
```

```text
shape: (3, 5)
┌────────┬─────────┬───────┬────────────┬─────────┐
│ region ┆ product ┆ units ┆ unit_price ┆ revenue │
│ ---    ┆ ---     ┆ ---   ┆ ---        ┆ ---     │
│ str    ┆ str     ┆ i64   ┆ f64        ┆ f64     │
╞════════╪═════════╪═══════╪════════════╪═════════╡
│ Alsace ┆ coffee  ┆ 120   ┆ 3.5        ┆ 420.0   │
│ Alsace ┆ tea     ┆ 80    ┆ 2.8        ┆ 224.0   │
│ Alsace ┆ cocoa   ┆ 45    ┆ 4.1        ┆ 184.5   │
└────────┴─────────┴───────┴────────────┴─────────┘
```

Two side effects of that design you will notice within an hour. The printed frame always tells you the **type** of every column (`str`, `i64`, `f64`) and its **shape**, because Polars tracks a schema — the class of bug where a numeric column silently became text is much harder to have. And there is no index: no `reset_index()`, no `.loc` versus `.iloc`, no `SettingWithCopyWarning`. A frame is a table.

## 2. The four verbs

Almost every pipeline is these four, chained:

| Verb | Question | Example |
|---|---|---|
| `select` | which columns? | `df.select("region", revenue)` |
| `filter` | which rows? | `df.filter(pl.col("units") >= 100)` |
| `with_columns` | add or replace a column | `df.with_columns(revenue)` |
| `group_by … agg` | one row per group | below |

If you know SQL — and you do — the mapping is exact: `select` is `SELECT`, `filter` is `WHERE`, `group_by(...).agg(...)` is `GROUP BY`, `sort` is `ORDER BY`, `head` is `LIMIT`. Polars is a query language wearing Python syntax, which is why it reads better than pandas for anything a SQL query would have expressed.

```python title="grouped.py"
import polars as pl

df = pl.read_csv("sales.csv")
revenue = (pl.col("units") * pl.col("unit_price")).alias("revenue")

print(
    df.with_columns(revenue)
    .group_by("region")
    .agg(
        pl.len().alias("rows"),
        pl.col("revenue").sum().round(2).alias("total"),
        pl.col("revenue").mean().round(2).alias("mean"),
    )
    .sort("total", descending=True)
)
```

```text
shape: (3, 4)
┌──────────┬──────┬───────┬────────┐
│ region   ┆ rows ┆ total ┆ mean   │
│ ---      ┆ ---  ┆ ---   ┆ ---    │
│ str      ┆ u32  ┆ f64   ┆ f64    │
╞══════════╪══════╪═══════╪════════╡
│ Bretagne ┆ 3    ┆ 937.5 ┆ 312.5  │
│ Alsace   ┆ 3    ┆ 828.5 ┆ 276.17 │
│ Lorraine ┆ 3    ┆ 819.5 ┆ 273.17 │
└──────────┴──────┴───────┴────────┘
```

Several aggregations in one `agg`, each named. `pl.len()` is the row count of the group — always include it: a group of size 1 behind an impressive mean is the commonest way to fool yourself.

## 3. Window functions: aggregate without collapsing

`group_by` gives you one row per group. A **window function** gives you the group's statistic *next to every original row* — `over()` is `OVER (PARTITION BY …)` in SQL:

```python title="window.py"
import polars as pl

df = pl.read_csv("sales.csv")
revenue = (pl.col("units") * pl.col("unit_price")).alias("revenue")

print(
    df.with_columns(revenue)
    .with_columns(
        (pl.col("revenue") / pl.col("revenue").sum().over("region") * 100)
        .round(1)
        .alias("pct_of_region")
    )
    .head(4)
)
```

```text
shape: (4, 6)
┌──────────┬─────────┬───────┬────────────┬─────────┬───────────────┐
│ region   ┆ product ┆ units ┆ unit_price ┆ revenue ┆ pct_of_region │
│ ---      ┆ ---     ┆ ---   ┆ ---        ┆ ---     ┆ ---           │
│ str      ┆ str     ┆ i64   ┆ f64        ┆ f64     ┆ f64           │
╞══════════╪═════════╪═══════╪════════════╪═════════╪═══════════════╡
│ Alsace   ┆ coffee  ┆ 120   ┆ 3.5        ┆ 420.0   ┆ 50.7          │
│ Alsace   ┆ tea     ┆ 80    ┆ 2.8        ┆ 224.0   ┆ 27.0          │
│ Alsace   ┆ cocoa   ┆ 45    ┆ 4.1        ┆ 184.5   ┆ 22.3          │
│ Lorraine ┆ coffee  ┆ 95    ┆ 3.5        ┆ 332.5   ┆ 40.6          │
└──────────┴─────────┴───────┴────────────┴─────────┴───────────────┘
```

"Each product's share of its region's revenue", in one expression, no intermediate frame, no merge. In pandas this is `groupby().transform()`; in Polars it is one word. Shares within a group, deviations from a group mean, ranks within a group and year-on-year changes within a panel are all `over()`.

## 4. Conditionals, strings, reshaping

```python title="more.py"
import polars as pl

df = pl.read_csv("sales.csv")

print(
    df.with_columns(
        pl.when(pl.col("units") >= 100)
        .then(pl.lit("high"))
        .otherwise(pl.lit("low"))
        .alias("volume")
    ).head(4)
)

print(
    df.select(
        pl.col("product").str.to_uppercase().alias("P"),
        pl.col("product").str.len_chars().alias("n"),
    ).head(3)
)

print(df.pivot(on="product", index="region", values="units"))
```

```text
shape: (4, 5)
┌──────────┬─────────┬───────┬────────────┬────────┐
│ region   ┆ product ┆ units ┆ unit_price ┆ volume │
│ ---      ┆ ---     ┆ ---   ┆ ---        ┆ ---    │
│ str      ┆ str     ┆ i64   ┆ f64        ┆ str    │
╞══════════╪═════════╪═══════╪════════════╪════════╡
│ Alsace   ┆ coffee  ┆ 120   ┆ 3.5        ┆ high   │
│ Alsace   ┆ tea     ┆ 80    ┆ 2.8        ┆ low    │
│ Alsace   ┆ cocoa   ┆ 45    ┆ 4.1        ┆ low    │
│ Lorraine ┆ coffee  ┆ 95    ┆ 3.5        ┆ low    │
└──────────┴─────────┴───────┴────────────┴────────┘
```

```text
shape: (3, 2)
┌────────┬─────┐
│ P      ┆ n   │
│ ---    ┆ --- │
│ str    ┆ u32 │
╞════════╪═════╡
│ COFFEE ┆ 6   │
│ TEA    ┆ 3   │
│ COCOA  ┆ 5   │
└────────┴─────┘
```

```text
shape: (3, 4)
┌──────────┬────────┬─────┬───────┐
│ region   ┆ coffee ┆ tea ┆ cocoa │
│ ---      ┆ ---    ┆ --- ┆ ---   │
│ str      ┆ i64    ┆ i64 ┆ i64   │
╞══════════╪════════╪═════╪═══════╡
│ Alsace   ┆ 120    ┆ 80  ┆ 45    │
│ Lorraine ┆ 95     ┆ 130 ┆ 30    │
│ Bretagne ┆ 60     ┆ 150 ┆ 75    │
└──────────┴────────┴─────┴───────┘
```

`when/then/otherwise` is the vectorised `if`. The `.str` namespace holds the text operations (`contains`, `replace`, `extract` with a regular expression, `split`, `strip_chars`, `to_lowercase`) — an NLP room will live there. `pivot` goes from long to wide; `unpivot` comes back; `explode` turns a column of lists into one row per element.

## 5. Joins, and the trap worth one assertion

```python title="join.py"
import polars as pl

left = pl.DataFrame({"region": ["Alsace", "Lorraine"], "pop": [1.9, 2.3]})
right = pl.DataFrame(
    {"region": ["Alsace", "Alsace", "Lorraine"], "city": ["Strasbourg", "Mulhouse", "Metz"]}
)

joined = left.join(right, on="region", how="left")
print(left.height, "->", joined.height)
print(joined)
```

```text
2 -> 3
```

```text
shape: (3, 3)
┌──────────┬─────┬────────────┐
│ region   ┆ pop ┆ city       │
│ ---      ┆ --- ┆ ---        │
│ str      ┆ f64 ┆ str        │
╞══════════╪═════╪════════════╡
│ Alsace   ┆ 1.9 ┆ Strasbourg │
│ Alsace   ┆ 1.9 ┆ Mulhouse   │
│ Lorraine ┆ 2.3 ┆ Metz       │
└──────────┴─────┴────────────┘
```

Two rows in, three rows out, no warning — because the key is not unique on the right. Here it is obvious and intended; on a real panel with 400,000 rows it is invisible, and `pop` has just been counted twice in every sum you compute afterwards. This is the single most common silent error in applied data work, in any language.

The fix is one line, and it belongs in your code rather than in your memory:

```python
joined = left.join(right, on="region", how="left")
assert joined.height == left.height, f"the join duplicated rows: {left.height} -> {joined.height}"
```

`how=` takes `"inner"`, `"left"`, `"full"`, `"semi"` (keep left rows that have a match, add no columns), `"anti"` (keep left rows that have *no* match — the fastest way to find what is missing) and `"cross"`. When a join is meant to be one-to-one, say so with an assertion; when it is meant to be one-to-many, assert the count you expect. That is a [shape assertion](testing.md#11-where-this-sits-in-the-bigger-picture), and it is the highest-value test a data pipeline can have.

## 6. Lazy queries

Everything above was **eager**: `read_csv` loads the file, each verb runs when it is called. Replace `read_csv` with `scan_csv` and nothing runs at all until you ask:

```python title="lazy.py"
import polars as pl

q = (
    pl.scan_csv("sales.csv")
    .with_columns((pl.col("units") * pl.col("unit_price")).alias("revenue"))
    .filter(pl.col("revenue") > 200)
    .group_by("region")
    .agg(pl.col("revenue").sum().round(2).alias("total"))
    .sort("total", descending=True)
)

print(type(q).__name__)
print(q.explain())
print(q.collect())
```

```text
LazyFrame
```

```text
SORT BY [descending: [true]] [col("total")]
  AGGREGATE[maintain_order: false]
    [col("revenue").sum().round().alias("total")] BY [col("region")]
    FROM
    FILTER col("revenue") > 200.0
    FROM
      simple π 2/2 ["region", "revenue"]
         WITH_COLUMNS:
         [(col("units").cast(Float64) * col("unit_price")).alias("revenue")] 
          Csv SCAN [sales.csv]
          PROJECT 3/4 COLUMNS
          ESTIMATED ROWS: 10
```

```text
shape: (3, 2)
┌──────────┬───────┐
│ region   ┆ total │
│ ---      ┆ ---   │
│ str      ┆ f64   │
╞══════════╪═══════╡
│ Bretagne ┆ 937.5 │
│ Lorraine ┆ 696.5 │
│ Alsace   ┆ 644.0 │
└──────────┴───────┘
```

Read the plan bottom-up: it is what Polars decided to do, not what you wrote. **`PROJECT 3/4 COLUMNS`** is the interesting line — the query never mentions `product`, so that column is not read from the file at all. On a 40-column CSV where you use three, that alone is most of the win; filters get pushed down to the scan the same way, so rows you discard are often never materialised.

Three practical consequences:

- **`.collect()` is where the work happens.** Build the query, `explain()` it if you are curious, `collect()` when you want the data.
- **`scan_csv` / `scan_parquet` are the default for anything large.** They are also how you query a file you could not open otherwise.
- **`.sink_parquet("out.parquet")`** writes the result straight to disk without building the whole frame in memory, which is how a file bigger than your RAM gets processed at all.

```python title="sink.py"
import polars as pl

pl.scan_csv("sales.csv").filter(pl.col("units") > 50).sink_parquet("out.parquet")
print(pl.read_parquet("out.parquet").shape)
```

```text
(7, 4)
```

!!! tip "Parquet, and when it is not smaller"
    Parquet is columnar and compressed: for a real dataset it is several times smaller than the equivalent CSV, it keeps the types (no more "was that column a string?"), and a `scan_parquet` can skip whole columns and row groups. On a nine-row file the metadata dominates — here the CSV is 224 bytes and the Parquet 1,592 — so do not draw conclusions from toy files. Switch formats when the file stops being comfortable, not before.

## 7. Living with pandas

You will keep meeting pandas: in other people's code, in tutorials, in libraries whose functions expect a `DataFrame`. The bridge is two methods, `df.to_pandas()` and `pl.from_pandas(pdf)`, and the habits worth relearning are few:

| pandas | Polars |
|---|---|
| `df[df["product"] == "tea"]` | `df.filter(pl.col("product") == "tea")` |
| `df["rev"] = df["u"] * df["p"]` | `df.with_columns((pl.col("u") * pl.col("p")).alias("rev"))` |
| `df.groupby("region")["rev"].sum()` | `df.group_by("region").agg(pl.col("rev").sum())` |
| `df.groupby("region")["rev"].transform("sum")` | `pl.col("rev").sum().over("region")` |
| `df.reset_index()`, `.loc`, `.iloc` | — there is no index |
| `pd.read_csv(..., dtype=...)` | schema inferred and *reported*; override with `schema_overrides=` |

The deeper difference is not speed, it is that a Polars pipeline is a **declared query** rather than a sequence of mutations. That is also why it suits this course: a query you can read in one expression is a query you can review — including when a model wrote it.

## 8. Going further

1. [Polars — Coming from pandas](https://docs.pola.rs/user-guide/migration/pandas/) — the official version of section 7.
2. [Polars — Expressions](https://docs.pola.rs/user-guide/expressions/) — the namespaces (`str`, `dt`, `list`, `struct`) this page only pointed at.
3. [Polars — Lazy API](https://docs.pola.rs/user-guide/lazy/) — `scan_*`, `explain`, `collect`, `sink_*` and what the optimiser actually does.
4. [Polars — SQL interface](https://docs.pola.rs/user-guide/sql/intro/) — if you would rather type the SQL you already know against a DataFrame, you can.
5. Last year's version, with the Titanic and a SQLite database of French cities: [Polars vs pandas](https://github.com/KnuxV/advanced_programming_python/blob/main/lessons/05-polars_vs_pandas.md).
6. Practice: [exercise 2.5](../exercises/polars-pandas.md) times the same group-by in both libraries.
