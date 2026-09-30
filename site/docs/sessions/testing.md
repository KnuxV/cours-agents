# Testing with pytest — class plan

A two-hour class: why test, then three tools from the simplest to the most complete (**doctest**, **assert**, **pytest**), then a demo everyone runs on their own machine, then two exercises.

- **Slides** (in French): [Tester son code](../slides/testing-pytest.html){target="_blank"} — arrow keys or space to move, `n` for the speaker notes, `t` to switch light/dark, click any code block to copy it.
- **Written lesson** (in English, to reread at home): [Testing your code with pytest](../reference/testing.md).
- **Exercises**: [T.1 Fix the code](../exercises/testing-fix.md) · [T.2 Test first: `parse_number`](../exercises/testing-tdd.md).
- **Needs first**: a terminal, `git`, and `uv` ([Session 2](s2.md)).

## Before the class starts: get the code

Everything you run today is in the course repository, in `resources/testing-lab/`. Copy that folder out of the repository so you can change it freely:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~
git clone https://github.com/KnuxV/cours-agents.git
cp -r ~/cours-agents/resources/testing-lab ~/testing-lab
cd ~/testing-lab
uv sync
```

If you already cloned the course repository in an earlier class, do not clone it again. Replace the first two lines with these, which download what changed since:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~/cours-agents
git pull
```

!!! warning "`git pull` refuses, and the message mentions *stash*"
    You changed or added files inside the course repository, and git will not overwrite them. Put them aside, then pull again:

    ```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/cours-agents"
    git stash -u
    git pull
    ```

    `git stash -u` puts every change aside, new files included. Nothing is lost: `git stash pop` brings it back.

`uv sync` creates a `.venv/` folder inside `testing-lab` and installs pandas and pytest into it. Nothing is installed anywhere else, and nothing needs `sudo`.

!!! tip "No git, or the network is down?"
    Download [testing-lab.zip](../files/testing-lab.zip), unzip it in your home folder, then `cd ~/testing-lab` and `uv sync`.

**Always `cd` into one of the numbered folders before you run anything.** Each folder is a small, separate example.

## The plan

| Time | Part | You run |
|---|---|---|
| 0:00 | Why test: silent errors, the kinds of tests | — |
| 0:12 | **doctest** — examples written in the docstring that Python checks | `1-doctest/` |
| 0:22 | **assert** — the building block; why a script of asserts is not enough | `2-assert/` |
| 0:30 | **pytest** — the `tests/` folder, reading a failure, `parametrize`, `raises`, `approx`, a fixture, a mock | `3-pytest/` |
| 1:00 | **Demo** — a small data pipeline and three weekly files | `4-pipeline/` |
| 1:30 | Exercise 1 — fix the code | `exo1-fix/` |
| 1:45 | Exercise 2 — test first | `exo2-tdd/` |

## Parts 1–3: the commands

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~/testing-lab/1-doctest
uv run python text_tools.py -v                 # 4 passed and 0 failed
uv run python -m doctest -v text_tools.py      # the same, without the block at the end of the file

cd ~/testing-lab/2-assert
uv run python check_text_tools.py              # stops at the 3rd check, on purpose

cd ~/testing-lab/3-pytest
uv run pytest                                  # 15 passed
uv run pytest -v                               # one line per test
```

The third check in `2-assert` fails because `count_words("Bonjour, le monde !")` returns 4: the `!` stands alone between spaces, so it counts as a word. Whether it *should* is a decision, not a fact — and writing a test is what forces you to make it. The checks after it never run: that is the main limit of a plain script of `assert` lines.

In `3-pytest`, the tests of `labeler.py` pass without any network access and without `UNISTRA_API_KEY`: the function that calls the language model is replaced by a fake for the duration of each test. The [written lesson](../reference/testing.md) explains every file.

## Part 4: the demo

A colleague collects product reviews and sends you one CSV file every week. `pipeline.py` reads the file and prints, for each language, the number of reviews, the mean rating and the mean length of a review in words. It was written for week 1. We run each step together.

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~/testing-lab/4-pipeline
uv run python pipeline.py data/week1.csv
uv run python pipeline.py data/week2.csv
uv run python pipeline.py data/week3.csv
```

| Week | What happens |
|---|---|
| 1 | A sensible table: two languages, ratings between 1 and 5. |
| 2 | **No error, wrong result.** Six "languages" instead of two, and a French mean rating above 5 on a 1–5 scale. |
| 3 | **A crash**: `KeyError: 'text'`, which does not say what is wrong. |

Then the tests. `tests/test_data.py` checks every CSV file in `data/`: the columns, the languages, the ratings, the empty texts, the identifiers. Each test runs once per file, and the file name is shown in brackets.

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside 4-pipeline"
uv run pytest tests/test_data.py -v
```

Week 1 passes; week 2 fails three checks, and each message names the rows at fault; week 3 fails the column check, and the other checks are skipped because nothing else can be checked on a file with the wrong columns.

Two of week 2's problems — languages written `FR`, `Fr`, `fr `, and reviews with no text — are the job of `clean()`. The unit tests in `tests/test_clean.py` describe what `clean()` should do, on five reviews written by hand, and two of them fail:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside 4-pipeline"
uv run pytest tests/test_clean.py
```

Fix `clean()` in `pipeline.py` by adding the two highlighted lines:

```python title="pipeline.py" hl_lines="4 5"
def clean(reviews: pd.DataFrame) -> pd.DataFrame:
    reviews = reviews.copy()
    reviews["text"] = reviews["text"].str.strip()
    reviews["lang"] = reviews["lang"].str.strip().str.lower()
    reviews = reviews[reviews["text"].notna() & (reviews["text"] != "")]
    return reviews
```

Run `uv run pytest tests/test_clean.py` again: 4 passed. Run `uv run pytest tests/test_data.py`: two failures are left, and neither is a bug in the code. Week 2 has ratings out of 10 from one annotator; week 3 was saved with `;` as the separator and a column called `note`. Dividing the ratings by two would be guessing. The file goes back to the colleague:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside 4-pipeline"
mkdir data/rejected
mv data/week2.csv data/week3.csv data/rejected/
uv run pytest -v
```

Everything passes: 14 tests. One of them, `test_week1_summary_has_not_changed`, is a **regression test**: it compares today's report for week 1 with a copy that was checked by hand once and saved in `tests/expected/`. It proves that changing `clean()` did not change the result for the week that was already right.

!!! note "What to take away from the demo"
    Tests do not make code correct. They make errors **visible**: the silent error of week 2 became a precise message. And when a data check fails, the fix is not always in the code — a discrepancy in the data is a finding, not something to make disappear.

## Part 5: the exercises

1. [**T.1 Fix the code**](../exercises/testing-fix.md) — 15 minutes. The tests are right, the code is wrong: make every test pass without touching the tests. Then find the bug the tests missed.
2. [**T.2 Test first: `parse_number`**](../exercises/testing-tdd.md) — 15 minutes in class, finish at home. Build a function that reads `"1 234,56"` as `1234.56`, one test at a time.

## Your own project

The recipe for any project of yours, including the exam project:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
uv init --no-package my-project
cd my-project
uv add --dev pytest
mkdir tests
touch conftest.py
uv run pytest
```

Your code goes at the root of the project, your tests in `tests/`, in files named `test_*.py` containing functions named `test_*`. The empty `conftest.py` marks the root of the project so that the tests can import your code; without it, pytest stops with `ModuleNotFoundError`.
