# 2.2 — Notebook → script with argparse

Lesson: [Session 2 — Python tooling](../sessions/s2.md) · [All exercises](index.md)

**Goal:** lift hard-coded values out of a notebook cell into command-line arguments.

1. Do [S2 §5](../sessions/s2.md#5-from-a-notebook-cell-to-a-script-with-arguments) with `report.py` and `sales.csv`; check the four runs (`--top 2`, `--help`, missing argument, `--top two`).
2. Add a third argument: `--region` (keep only one region) **or** `--csv` (a flag: print the result as CSV instead of a table — `result.write_csv()` with no path returns a string).
3. Commit and push.

**Done when** `uv run report.py --help` documents three arguments and each behaves as advertised.

??? note "Solution (the `--csv` variant)"
    Add one line to the parser and change the `print`:

    ```python
    parser.add_argument("--csv", action="store_true", help="print CSV instead of a table")
    ...
    if args.csv:
        print(result.write_csv(), end="")
    else:
        print(result)
    ```

    `action="store_true"` makes `--csv` a flag: `args.csv` is `False` unless the flag is present. Check: `uv run report.py sales.csv --top 2 --csv` prints `region,revenue` followed by two lines.
