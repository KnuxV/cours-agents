<!--
PORTED FROM last year's material (KnuxV/slides_cours_git):
  "Part 8 - Unit_testing.md"  — why testing, QA, TDD, CI, the testing pyramid, types of tests
  "Part 9 - Pytest.md"        — pytest, assert, parametrize, fixtures, tmp_path, capsys, coverage, the three GitLab/GitHub practice repos
  "Part 13 - github_actions.md" — the tests workflow (rewritten for uv)
  "Part 15 - exam.md" / Exam.md — the "tests/ folder + pytest" expectation

PROPOSED DESTINATION: site/docs/reference/testing.md
  Nav (site/mkdocs.yml, under "Reference"):
      - Python and quality:
          - Testing your code with pytest: reference/testing.md
  Row for site/docs/reference/index.md, section "Python and quality":
      | [Testing your code with pytest](testing.md) | Writing a test, running pytest, parametrize, fixtures, coverage, tests in CI, and why the test suite is the reliable part of an agent system | [Session 4 — §4.3](../sessions/s4.md) |
  Inbound links to add later (not done here — site/ is owned by another pass):
      sessions/s2.md §5 (importable code is testable code) and sessions/s4.md §4.3.

REWRITTEN, not pasted: `pip install pytest` → `uv add --dev pytest` / `uv run --with pytest pytest`;
every command carries a "where to run it" title; no sudo anywhere; the disaster anecdotes lost
their unverified money figures; the agent framing (SPEC 4.3) is new.
Every output block below was produced on this machine (uv 0.12.10, CPython 3.12.14, pytest 9.1.1).
-->

# Testing your code with pytest

Introduced in [Session 4, §4.3](../sessions/s4.md) — and used from Session 2 onwards, because a script you can test is a script you can hand to someone else, including a machine.

!!! quote "The one sentence to remember"
    The most reliable component of an agent system is not the model — it is the test suite.

An agent that writes code for you is a very fast, very confident junior colleague with no memory. You cannot review every line it produces, and you will not want to. What you *can* do is write down, once, what "working" means, in a form a machine re-checks in half a second. That is a test. Everything on this page exists so that the instruction "run the tests after every edit" has something to run.

## 1. Why anyone bothers

Three arguments, in increasing order of relevance to you.

**The famous disasters.** The Ariane 5 maiden flight (1996) was destroyed shortly after launch because a numeric conversion in code reused from Ariane 4 overflowed in the new flight profile. The Therac-25 radiation machine injured and killed patients because of a race condition nobody had exercised. Knight Capital (2012) lost a very large amount of money in under an hour after deploying a flag that had never been tested in production. These stories are usually told to software engineers; they are not really *your* risk.

!!! note "Figures deliberately absent"
    Last year's slides gave euro and dollar amounts for these accidents. They are widely quoted but were not checked against a primary source for this page, so they are not repeated here. The point survives without them.

**Your actual risk** is quieter: a number in a table that is wrong, and nobody notices. A filter that silently drops the rows with a missing value. A merge that duplicates a third of your observations. A tokeniser that lowercases the text in one branch of the code and not the other. Nothing crashes. The result is simply not true, and it goes into a report, a paper, or a dissertation.

**The agent-era argument.** In [Session 4](../sessions/s4.md) you will let a program edit your files. Two instructions you can put in `AGENTS.md`:

- "Be careful and do not break anything." — an appeal to virtue. Unverifiable, therefore worthless.
- "After every edit, run `uv run pytest`. If a test fails, fix it before continuing." — a loop with a gate in it.

The second one works because the gate is mechanical. Tests are how you delegate without trusting.

## 2. What a test actually is

A function that runs your code and asserts something about the result. That is all. No framework is required to understand it:

```python title="the whole idea, in four lines"
def add_vat(price, rate):
    return price * (1 + rate)

assert add_vat(100, 0.20) == 120
```

Run that file: if the assertion holds, nothing happens; if it does not, Python raises `AssertionError`. A test framework adds three things you would otherwise write yourself: it *finds* your tests, it *runs all of them* even after one fails, and it *explains* the failure. The standard one in Python is **pytest**.

Four things you get in exchange for the typing:

| You get | Because |
|---|---|
| Bugs caught while they are cheap | You find them in the minute you wrote the code, not in the week you present it |
| Permission to change your code | You can restructure a working script and still know it works. Without tests, "it runs" is the only guarantee you have, and refactoring becomes gambling |
| Documentation that cannot rot | `test_add_vat` shows exactly how `add_vat` is meant to be called. Prose comments drift; a failing test shouts |
| A gate a machine can check | CI (section 9) and agents (section 10) both need a command that answers pass or fail |

## 3. Your first test

We work inside a `uv` project, as in [Session 2](../sessions/s2.md#4-a-project-from-scratch). Create a fresh one to follow along:

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
cd ~
uv init --no-package --python 3.12 vat-demo
cd vat-demo
mkdir tests
```

The code under test — one function, one docstring, one deliberate guard:

```python title="vat.py"
"""Value-added tax helpers."""


def add_vat(price: float, rate: float) -> float:
    """Return `price` increased by a VAT `rate` given as a decimal (0.20 = 20 %)."""
    if rate < 0:
        raise ValueError("rate cannot be negative")
    return price * (1 + rate)
```

The tests. The file name **must** start with `test_`, and so must each function inside it — that is how pytest finds them:

```python title="tests/test_vat.py"
from vat import add_vat


def test_twenty_percent():
    assert add_vat(100, 0.20) == 120


def test_zero_rate_changes_nothing():
    assert add_vat(100, 0) == 100
```

Add pytest as a **development dependency** — something the project needs in order to be worked on, not in order to run:

```bash title="Any terminal, inside vat-demo"
uv add --dev pytest
uv run pytest
```

`uv add --dev` writes pytest into a `[dependency-groups]` section of `pyproject.toml` rather than into `dependencies`, so someone who only wants to *use* your code does not have to install your test tools. It is installed into the same `.venv`, and `uv sync` restores it.

### 3.1 The error every single person hits first

```text
E   ModuleNotFoundError: No module named 'vat'
=========================== short test summary info ============================
ERROR tests/test_vat.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

Your code is in the project root; your test is in `tests/`. When pytest imports `tests/test_vat.py`, the folder Python searches is `tests/`, and `vat.py` is not there. The one-line fix is an **empty file called `conftest.py` next to `pyproject.toml`**:

```bash title="Any terminal, inside vat-demo"
touch conftest.py
uv run pytest -v
```

`conftest.py` is pytest's per-project configuration file. Its mere presence at the top of the project tells pytest "this is the root", and the root goes on the import path — so `from vat import add_vat` resolves. (You will also use it in section 7 to share fixtures.) Now:

```text
============================= test session starts ==============================
platform linux -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0 -- /home/you/vat-demo/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/you/vat-demo
configfile: pyproject.toml
collecting ... collected 2 items

tests/test_vat.py::test_twenty_percent PASSED                            [ 50%]
tests/test_vat.py::test_zero_rate_changes_nothing PASSED                 [100%]

============================== 2 passed in 0.00s ===============================
```

!!! tip "Where to put the tests"
    Anything works as long as pytest can find your code. Two conventions:

    - **`tests/` folder + empty `conftest.py` at the root** — what this page uses. Good for scripts and small projects.
    - **`src/` layout** (`uv init --package`, see [modules and packages](modules-and-packages.md#6-making-the-package-installable)) — the project is installed into its own environment, so `from mypackage import x` works from anywhere and no `conftest.py` trick is needed. Right for something you intend to publish.

    Do not put tests *inside* the same file as the code for anything you will keep. A `if __name__ == "__main__":` block with a few prints is a fine first step, but nobody runs it twice.

## 4. `assert`, and what a failure looks like

`assert <expression>` fails the test when the expression is false. There is no `assertEqual`, no `self`, no class to inherit from — plain Python:

```python title="the assertions you will use 95 % of the time"
assert result == 120                    # equality
assert result != 0
assert result > 0                       # comparison
assert isinstance(result, float)        # type
assert result is None                   # identity, for None / True / False
assert "error" in message               # membership, in a string or a list
assert len(rows) == 50
```

Now write a wrong function on purpose, so you see what pytest tells you. A classic: "20 % off" implemented as a multiplication.

```python title="discount.py"
def final_price(price: float, discount: float) -> float:
    """Return `price` after a `discount` given as a decimal (0.20 = 20 % off)."""
    return price * discount
```

```python title="tests/test_discount.py"
from discount import final_price


def test_twenty_percent_off_100():
    assert final_price(100, 0.20) == 80
```

```bash title="Any terminal, inside vat-demo"
uv run pytest tests/test_discount.py
```

```text
=================================== FAILURES ===================================
_________________________ test_twenty_percent_off_100 __________________________

    def test_twenty_percent_off_100():
>       assert final_price(100, 0.20) == 80
E       assert 20.0 == 80
E        +  where 20.0 = final_price(100, 0.2)

tests/test_discount.py:5: AssertionError
=========================== short test summary info ============================
FAILED tests/test_discount.py::test_twenty_percent_off_100 - assert 20.0 == 80
============================== 1 failed in 0.01s ==============================
```

Read the four lines of that report: the test that failed, the line that failed, the two values compared, and *how the left-hand value was produced*. That last line is pytest rewriting your `assert` so the failure explains itself. It is the whole reason people prefer pytest to the standard library's `unittest`.

The fix is `price * (1 - discount)`. Delete the two files afterwards; they were props.

### 4.1 The float trap

```python title="tests/test_float.py"
from vat import add_vat


def test_tiny_price():
    assert add_vat(0.1, 2) == 0.3
```

```text
E       assert 0.30000000000000004 == 0.3
E        +  where 0.30000000000000004 = add_vat(0.1, 2)
```

Your code is right; the test is wrong. Binary floating point cannot represent 0.1 exactly, so `0.1 * 3` is `0.30000000000000004`. Never compare computed decimals with `==`. Use `pytest.approx`:

```python title="tests/test_float.py — corrected"
import pytest

from vat import add_vat


def test_tiny_price():
    assert add_vat(0.1, 2) == pytest.approx(0.3)
```

This matters far beyond toy examples: every mean, rate, share or revenue in a data pipeline is a float.

## 5. Writing tests that are worth having

**Arrange, act, assert.** Three visual blocks, in that order. A test that mixes them is a test nobody can read six months later.

```python
def test_revenue_per_region():
    # Arrange
    rows = [("Alsace", 3, 2.0), ("Alsace", 1, 2.0), ("Bretagne", 5, 1.0)]

    # Act
    result = revenue_by_region(rows)

    # Assert
    assert result == {"Alsace": 8.0, "Bretagne": 5.0}
```

**One reason to fail per test.** If a test asserts five unrelated things, its name cannot describe it and its failure does not localise the bug.

**Independent tests.** No test may depend on another having run first, because pytest may run a subset, and one day it will run them in parallel. Shared module-level state is the usual culprit:

```python title="what not to do"
total = 0  # shared between tests — a trap


def test_increment():
    global total
    total += 1
    assert total == 1


def test_increment_again():
    global total
    total += 1
    assert total == 2      # only passes if the other test ran first
```

**Test the edges, not just the happy path.** The happy path is the case you had in mind while writing the code, so it is the case least likely to be broken. Go looking for:

- empty input — `[]`, `""`, an empty DataFrame, a CSV with only a header;
- one element, because "the first" and "the last" are then the same thing;
- zero and negative numbers, especially as denominators;
- missing values — `None`, `NaN`, an empty cell;
- text that is not ASCII — accents, emoji, a Turkish `İ` (an NLP-room favourite; `"İ".lower()` is not `"i"`);
- inputs that *should* be refused.

**Assert that errors happen.** A function that refuses bad input is a feature, and features get tested:

```python title="tests/test_vat.py — continued"
import pytest

from vat import add_vat


def test_negative_rate_is_refused():
    with pytest.raises(ValueError):
        add_vat(100, -0.1)
```

`pytest.raises` passes when the block raises that exception and **fails when it does not** — that is the point. Use `match=` to pin the message down: `pytest.raises(ValueError, match="negative")`.

## 6. `parametrize`: the same test on many values

Four near-identical tests are four places to change. One parametrised test is one:

```python title="tests/test_vat.py — continued"
@pytest.mark.parametrize(
    "price,rate,expected",
    [
        (100, 0.20, 120),
        (100, 0.055, 105.5),
        (0, 0.20, 0),
        (19.99, 0.0, 19.99),
    ],
)
def test_rates(price, rate, expected):
    assert add_vat(price, rate) == pytest.approx(expected)
```

Each tuple becomes a separate test with its own name, so a single bad case is reported on its own:

```text
tests/test_vat.py::test_rates[100-0.2-120] PASSED                        [ 57%]
tests/test_vat.py::test_rates[100-0.055-105.5] PASSED                    [ 71%]
tests/test_vat.py::test_rates[0-0.2-0] PASSED                            [ 85%]
tests/test_vat.py::test_rates[19.99-0.0-19.99] PASSED                    [100%]
```

The string `"price,rate,expected"` names the parameters; the list supplies one tuple per case, in the same order. This is the cheapest way to turn "I tried a few values by hand in a notebook" into something permanent: paste the values you tried into the list.

## 7. Fixtures: the setup, written once

A **fixture** is a function that prepares something a test needs. Ask for it by writing its name as a parameter of the test, and pytest calls it for you — fresh, for every test.

Two built-in fixtures do most of the work in data code. `tmp_path` hands you an empty directory that pytest deletes afterwards; `capsys` captures what your code printed.

```python title="report.py"
"""Tiny CSV helpers, written so that each piece can be tested on its own."""
from pathlib import Path


def count_rows(csv_path: Path) -> int:
    """Return the number of data rows in `csv_path` (the header does not count)."""
    lines = Path(csv_path).read_text(encoding="utf-8").splitlines()
    return max(len(lines) - 1, 0)


def print_summary(csv_path: Path) -> None:
    """Print one line describing `csv_path`."""
    print(f"{csv_path.name}: {count_rows(csv_path)} rows")
```

```python title="tests/test_io.py"
import pytest

from report import count_rows, print_summary


@pytest.fixture
def sales_csv(tmp_path):
    """Write a two-row CSV in a directory pytest deletes after the test."""
    path = tmp_path / "sales.csv"
    path.write_text("region,units\nAlsace,3\nBretagne,5\n", encoding="utf-8")
    return path


def test_count_rows(sales_csv):
    assert count_rows(sales_csv) == 2


def test_print_summary(sales_csv, capsys):
    print_summary(sales_csv)
    captured = capsys.readouterr()
    assert "2 rows" in captured.out
```

```bash title="Any terminal, inside vat-demo"
uv run pytest -q
```

```text
.........                                                                [100%]
9 passed in 0.01s
```

Three things happened worth naming. `sales_csv` is *your* fixture, and it asks for `tmp_path`, which is pytest's — fixtures compose. Each of the two tests got its own fresh copy of the file, so they cannot interfere. And nothing was left behind on your disk: no `test_output.csv` in your repository, ever.

A fixture used by several test files goes in `conftest.py` — the same empty file you created in section 3.1, now earning its keep:

```python title="conftest.py"
import pytest


@pytest.fixture
def sales_csv(tmp_path):
    """A two-row CSV, available to every test in this project."""
    path = tmp_path / "sales.csv"
    path.write_text("region,units\nAlsace,3\nBretagne,5\n", encoding="utf-8")
    return path
```

!!! note "Fixtures that clean up"
    Replace `return` with `yield`, and everything after the `yield` runs once the test is done — closing a database connection, deleting a temporary table, restoring an environment variable. `tmp_path` needs no such thing, which is exactly why you should prefer it to writing files next to your code.

## 8. Running them

```bash title="Any terminal, inside a uv project"
uv run pytest                       # everything
uv run pytest -v                    # one line per test, with its name
uv run pytest -q                    # one character per test
uv run pytest tests/test_vat.py     # one file
uv run pytest tests/test_vat.py::test_twenty_percent   # one test
uv run pytest -k "rate"             # every test whose name contains "rate"
uv run pytest -x                    # stop at the first failure
uv run pytest --lf                  # only the tests that failed last time
uv run pytest -s                    # do not swallow print() output
uv run pytest -l                    # show local variables in the failure report
```

`-x --lf` is the debugging loop: fix one thing, re-run only what was broken.

!!! tip "Without adding a dependency at all"
    `uv run --with pytest pytest -q` runs pytest in a throwaway overlay of the project's environment, without touching `pyproject.toml`. Useful in someone else's repository, or before you have decided that the project is a project:

    ```text
    Installed 5 packages in 6ms
    .......                                                                  [100%]
    7 passed in 0.01s
    ```

### 8.1 Coverage: which lines were never run

```bash title="Any terminal, inside vat-demo"
uv run --with pytest-cov pytest --cov=vat --cov=report -q
```

```text
.........                                                                [100%]
================================ tests coverage ================================
Name        Stmts   Miss  Cover
-------------------------------
report.py       6      0   100%
vat.py          4      0   100%
-------------------------------
TOTAL          10      0   100%
9 passed in 0.03s
```

Add `--cov-report=html` and open `htmlcov/index.html` to see the un-run lines highlighted in your source. Coverage answers one question honestly — *which lines did the tests never execute* — and is silent on the one you care about, whether the assertions are any good. 100 % coverage with `assert True` everywhere is 100 % coverage. Use it to find the forgotten branch, not as a grade.

## 9. Running the tests on every push (GitHub Actions)

Tests you run when you remember are tests that pass until the day they matter. **Continuous integration** means the tests run on someone else's computer on every push, and the result is visible next to the commit. The concept is in [Git as a collaboration tool, §5](git-collaboration.md); here is the file.

```yaml title=".github/workflows/tests.yml"
name: tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1

      - name: Install uv
        uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0

      - name: Install the project
        run: uv sync --locked --all-extras --dev

      - name: Run the tests
        run: uv run pytest
```

Commit that file, push, then open the **Actions** tab of your repository: one run per push, green or red, with the full log. Four remarks:

- The two `uses:` lines are copied from [uv's own GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/), which pins each action to a commit hash and writes the readable version in the comment. Copy them as they are.
- `uv sync --locked` fails if `uv.lock` does not match `pyproject.toml`. That is the behaviour you want: CI refuses to guess, and the lockfile you committed in Session 2 is what makes this possible.
- Nothing here is Python-version-specific because `.python-version` and `uv.lock` already say what to install. That is the payoff of [Session 2](../sessions/s2.md#1-why-it-works-on-my-machine-is-not-a-result): the same three files make it reproducible on your laptop, on a classmate's, and on GitHub's.
- A workflow file is code like any other: it has to be committed, and a push that only fixes the workflow is a normal commit.

!!! warning "Pushing a workflow file needs the right token scope"
    If `git push` is refused with a message about `workflow` scope, the GitHub credentials stored by `gh` are not allowed to create workflow files. Run `gh auth refresh -h github.com -s workflow`, then push again. TODO(verify): the exact refusal message, which was reported by the instructor but not reproduced for this page.

## 10. Tests and agents

This is why the page exists, and the one section that has no equivalent in last year's material.

An agent's loop is: read some context, propose an edit, run something, read the result, repeat. The quality of the loop is decided by what "run something" is. With no tests, the agent's only feedback is "the script did not crash", so it optimises for not crashing — and a function that returns the wrong number never crashes. With tests, the feedback is a list of named expectations, and a failure tells the agent *which* expectation and *what* it got instead. The [failure report in section 4](#4-assert-and-what-a-failure-looks-like) is as useful to a model as it is to you, for the same reason: it contains the values.

Three habits follow.

1. **Write the assertion before the code**, or make the agent do it. "Add a `--separator` option" is a wish. "Add a `--separator` option; `test_separator_joins_with_dash` must pass" is a specification with a gate. This is the *assertion-before-code* rule of [Session 4, §4.3](../sessions/s4.md), and it is ordinary test-driven development wearing a new hat:

    | Step | | |
    |---|---|---|
    | **Red** | Write a test for behaviour that does not exist yet | It fails — proof that the test can fail |
    | **Green** | Write the least code that makes it pass | No cleverness yet |
    | **Refactor** | Tidy up, with the test still passing | The test is the safety net |

    Step one matters most: a test that has never failed has never been tested.

2. **Put the command in `AGENTS.md`**, not the intention:

    ```markdown title="AGENTS.md — the useful kind of instruction"
    After every change to a `.py` file, run `uv run pytest -q`.
    If anything fails, fix it before making another change.
    Never delete or weaken a test to make the suite pass.
    ```

    That last line is not paranoia. Deleting the failing test is a locally optimal move, and both humans and models find it.

3. **Read the diff of the tests first.** When an agent hands you a change, the tests tell you what it *thinks* it did. If the tests changed and you did not ask for that, start there.

## 11. Where this sits in the bigger picture

Everything above is **unit testing**: one function, in isolation, in milliseconds. There is more, and you should recognise the words:

| Kind | Scope | Speed | How many |
|---|---|---|---|
| Unit | one function, no database, no network | milliseconds | hundreds |
| Integration | several parts together — your code *and* the database, *and* the API | seconds | dozens |
| End-to-end | the whole thing as a user meets it, through the interface | minutes | a handful |

The usual advice is a pyramid: many unit tests, fewer integration tests, very few end-to-end tests — because the slow, fragile ones cost you most when they break for reasons that are not bugs. For the code in this course, unit tests plus one "does the whole script run on a small input file" test is the whole programme.

For a data pipeline or a replication, the highest-value tests are rarely about functions:

- **Shape assertions.** After a join, `assert len(df) == n_before` — a duplicated key in a merge is the single most common silent error in applied work.
- **Domain assertions.** `assert df["share"].is_between(0, 1).all()`, `assert df["year"].min() >= 1990`, no negative prices.
- **Published-value assertions.** In the [replication track](../replication.md): `assert round(coefficient, 3) == 0.412`, taken from the paper's table. A discrepancy is then a finding, not a bug to be smoothed away.

## 12. When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'yourfile'` | Your code is not on the import path when pytest imports `tests/` | Empty `conftest.py` next to `pyproject.toml` (§3.1) |
| `collected 0 items` | The file or the function is not named `test_*` | Rename: `tests/test_thing.py`, `def test_thing()` |
| `fixture 'sales_csv' not found` | The fixture is in another test file | Move it to `conftest.py` (§7) |
| A test passes alone, fails with the others | Shared state between tests | No module-level mutable data; use a fixture (§5, §7) |
| `assert 0.30000000000000004 == 0.3` | Comparing floats with `==` | `pytest.approx` (§4.1) |
| `pytest: command not found` | You typed `pytest`, not `uv run pytest` | `uv run pytest` — or `uv add --dev pytest` first |
| `No module named pytest` inside `uv run` | pytest is not a dependency of *this* project | `uv add --dev pytest`, or `uv run --with pytest pytest` |
| Tests write files into your repository | The code was given a relative path | Pass a path in; use `tmp_path` in tests (§7) |
| CI is red, your machine is green | Different Python or different versions | `uv sync --locked` locally; check `.python-version` is committed |
| A test suddenly passes after an agent's edit | The test may have been changed | `git diff` the test files before the source files (§10) |

## 13. Cheat sheet

| Command / line | What it does |
|---|---|
| `uv add --dev pytest` | pytest as a development dependency of the project |
| `uv run pytest` | Run every test it can find |
| `uv run --with pytest pytest` | Same, without declaring a dependency |
| `uv run pytest -q` / `-v` | Quieter / one line per test |
| `uv run pytest -x --lf` | Stop at the first failure; next time, only re-run the failures |
| `uv run pytest -k "name"` | Only tests whose name matches |
| `uv run --with pytest-cov pytest --cov=mymodule` | Which lines the tests never executed |
| `def test_x():` in `tests/test_y.py` | How pytest finds a test |
| `assert value == expected` | The whole API |
| `assert value == pytest.approx(expected)` | The same, for floats |
| `with pytest.raises(ValueError):` | Assert that a call is refused |
| `@pytest.mark.parametrize("a,b", [(1, 2)])` | One test, many cases |
| `@pytest.fixture` + a parameter of that name | Reusable setup, fresh per test |
| `tmp_path`, `capsys` | Built-in fixtures: a temporary directory, captured output |
| empty `conftest.py` at the project root | Makes `from mycode import x` work from `tests/` |

## 14. Going further

1. [pytest — Get Started](https://docs.pytest.org/en/stable/getting-started.html) — the official five-minute version of section 3.
2. [pytest — How to parametrize tests](https://docs.pytest.org/en/stable/how-to/parametrize.html) and [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) — the two features worth reading properly.
3. [Python docs — `unittest`](https://docs.python.org/3/library/unittest.html) — the standard library's framework. You will meet it in older code; recognise `class TestX(unittest.TestCase)` and `self.assertEqual`, and know that pytest runs those tests too.
4. [uv — Using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/) — the source of the workflow in section 9.
5. Two practice repositories from last year's course, still available: `gitlab.unistra.fr/cours_test/intro_test` (run the suite, repair a broken test, complete a missing one) and `gitlab.unistra.fr/cours_test/testing_username_password` (build a password and an e-mail validator test-first). TODO(verify): both are last year's URLs and were not opened while writing this page; check they are still public before sending students there.
