# Testing your code with pytest

This page is the written companion of the testing class: the [class plan](../sessions/testing.md) says what happens in the room, the [slides](../slides/testing-pytest.html) are what is on the screen, and the two exercises — [fix the code the tests point at](../exercises/testing-fix.md) and [build a function test first](../exercises/testing-tdd.md) — are what you do afterwards. Testing is used from [Session 2](../sessions/s2.md) onwards, because a script you can test is a script you can hand to someone else, including a machine, and it becomes the anchor of [Session 4](../sessions/s4.md).

!!! quote "The one sentence to remember"
    The most reliable component of an agent system is not the model — it is the test suite.

An agent that writes code for you is a very fast, very confident junior colleague with no memory. You cannot review every line it produces, and you will not want to. What you *can* do is write down, once, what "working" means, in a form a machine re-checks in half a second. That is a test. Everything on this page exists so that the instruction "run the tests after every edit" has something to run.

## 1. Why anyone bothers

Four arguments, in increasing order of relevance to you.

**The famous disasters.** The Ariane 5 maiden flight (1996) was destroyed shortly after launch because a numeric conversion in code reused from Ariane 4 overflowed in the new flight profile. The Therac-25 radiation machine injured and killed patients because of a race condition nobody had exercised. Knight Capital (2012) lost a very large amount of money in under an hour after deploying a flag that had never been tested in production. These stories are usually told to software engineers; they are not really *your* risk.

!!! note "Figures deliberately absent"
    Last year's slides gave euro and dollar amounts for these accidents. They are widely quoted but were not checked against a primary source for this page, so they are not repeated here. The point survives without them.

**Closer to research.** [The Turing Way's chapter on code testing](https://book.the-turing-way.org/reproducible-research/testing) opens with two cases that happened to scientists, not to engineers. The first is a 2006 news piece in *Science*: Geoffrey Chang's group had to retract five papers on protein structures because the in-house software used to process their data had a sign error. The second is the loss of NASA's Mars Climate Orbiter in 1999, because two pieces of software written by different teams did not use the same units. The Turing Way sums them up this way:

> "One of the examples above was caused by a plus sign which should have been a minus. Another was caused by one piece of code working in meters while a piece of code written by another researcher worked in feet."

For the record, the Mars mix-up was not literally metres and feet: one program produced thruster impulse in pound-force seconds where the other expected newton-seconds. Same lesson — nobody had written down, in a form a machine checks, which unit the numbers were in.

!!! note "For economists: Reinhart and Rogoff"
    Reinhart and Rogoff's 2010 paper on public debt and growth was widely cited in the debate on austerity. In 2013, Herndon, Ash and Pollin tried to reproduce it from the authors' spreadsheet ([PERI Working Paper 322](https://peri.umass.edu/publication/does-high-public-debt-consistently-stifle-economic-growth-a-critique-of-reinhart-and-rogoff/)) and found, among other problems, that one average was computed over rows 30 to 44 instead of 30 to 49 — which silently dropped five countries: Australia, Austria, Belgium, Canada and Denmark. No error message, no crash: a range in a formula that was five rows too short. A single check — "the average is over every country in the table" — would have caught it.

**Your actual risk** is quieter: a number in a table that is wrong, and nobody notices. A filter that silently drops the rows with a missing value. A merge that duplicates a third of your observations. A tokeniser that lowercases the text in one branch of the code and not the other. Nothing crashes. The result is simply not true, and it goes into a report, a paper, or a dissertation.

**The agent-era argument.** In [Session 4](../sessions/s4.md) you will let a program edit your files. Two instructions you can put in `AGENTS.md`:

- "Be careful and do not break anything." — an appeal to virtue. Unverifiable, therefore worthless.
- "After every edit, run `uv run pytest`. If a test fails, fix it before continuing." — a loop with a gate in it.

The second one works because the gate is mechanical. Tests are how you delegate without trusting.

And if the objection is time, The Turing Way has the answer: "You should not skip writing tests because you are short on time, you should write tests *because* you are short on time."

## 2. What a test actually is

A function that runs your code and asserts something about the result. That is all. No framework is required to understand it:

```python title="the whole idea, in four lines"
def add_vat(price: float, rate: float) -> float:
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
| A gate a machine can check | CI (section 13) and agents (section 14) both need a command that answers pass or fail |

## 3. Kinds of tests

You will meet these words in documentation and in job descriptions. The list below follows [The Turing Way's overview](https://book.the-turing-way.org/reproducible-research/testing/testing-overview), plus one kind that matters a lot in data work.

- **Smoke test** — the quickest possible check that the thing runs at all, before looking at anything finer ("does the script start and finish on a tiny file?").
- **Unit test** — one small piece of code, usually one function, checked on its own.
- **Integration test** — several pieces checked together, to see that they fit: your function *and* the file it reads, your code *and* the database.
- **System test (end-to-end)** — the whole program, run the way a user would run it, from input to final output.
- **Acceptance test** — does the result meet what was asked for? It checks the requirement, not the code.
- **Regression test** — in The Turing Way's words: "Regression testing is a style of testing that focuses on retesting after changes are made. The results of tests after the changes are compared to the results before, and errors are raised if these are different." ([source](https://book.the-turing-way.org/reproducible-research/testing/testing-acceptance-regression))
- **Data checks** — tests on the *input files* rather than on the code: the columns are the expected ones, ratings are between 1 and 5, no text is empty. They are written with the same tools (`assert`, pytest) and run the same way.

This course is mostly about unit tests, because they are the ones you write every day. Section 12 adds data checks and one regression test on a small pipeline; section 15 says how the kinds fit together.

## 4. doctest: examples that check themselves

The lightest test there is needs no test file at all. You write, inside a function's docstring, what you would type in the Python console and what it answered. The `doctest` module, which comes with Python, runs those lines and compares the answers.

The examples in this section and the next ones come from the course's testing lab. Copy it once:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~
git clone https://github.com/KnuxV/cours-agents.git     # already cloned? instead: cd ~/cours-agents && git pull
cp -r ~/cours-agents/resources/testing-lab ~/testing-lab
cd ~/testing-lab
uv sync
```

If `git pull` refuses and mentions *stash*, run `git stash -u` then `git pull` again ([details](../sessions/testing.md#before-the-class-starts-get-the-code)). `uv sync` creates a `.venv/` folder inside `testing-lab` and installs pandas and pytest into it. Nothing is installed outside the folder. If you have no git, [testing-lab.zip](../files/testing-lab.zip) contains the same folder: unzip it in your home folder, then `cd ~/testing-lab` and `uv sync`. Always `cd` into one of the numbered folders before running anything.

```python title="1-doctest/text_tools.py" linenums="1"
--8<-- "resources/testing-lab/1-doctest/text_tools.py"
```

Each line starting with `>>>` is a call; the line below it is the answer you expect, written exactly as the console would print it. There are two ways to run the examples.

**From the script itself.** The block at the end of the file runs the examples when you launch the file:

```python
if __name__ == "__main__":
    import doctest

    doctest.testmod()
```

`__name__` is `"__main__"` only when the file is the one you launched; when another file imports it — pytest will, in section 5 — the block is skipped. `doctest.testmod()` checks the examples of the current file.

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/testing-lab/1-doctest"
uv run python text_tools.py -v
```

**Without adding anything.** The `doctest` module can be run on any file, block or no block:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/testing-lab/1-doctest"
uv run python -m doctest -v text_tools.py
```

With `-v` (verbose), either command lists every example it tried and ends with:

```text
4 tests in 3 items.
4 passed and 0 failed.
Test passed.
```

Three examples in `count_words` and one in `normalize` make four tests; the three "items" are the module and its two functions. Without `-v`, a passing run prints **nothing at all** — silence means success.

Now break it on purpose: change the first expected answer from `3` to `4` and run either command again, without `-v`. With `python -m doctest`:

```text
**********************************************************************
File "text_tools.py", line 12, in text_tools.count_words
Failed example:
    count_words("le chat dort")
Expected:
    4
Got:
    3
**********************************************************************
1 items had failures:
   1 of   3 in text_tools.count_words
***Test Failed*** 1 failures.
```

(Python prints the full path to the file on the `File` line; it is shortened here. Run as a script, the only other difference is that the function is called `__main__.count_words`.) The report names the line, the call, what you wrote and what the code actually returned. Put the `3` back.

**When to use doctest.** For short examples that *are* documentation: someone reading the docstring learns how to call the function, and the example cannot silently go out of date, because it is checked.

**When not to use it.** doctest compares *printed text*, character for character. That makes it a poor fit for:

- many cases — ten `>>>` lines bury the explanation; use `parametrize` (section 8);
- floats — `0.1 * 3` prints `0.30000000000000004`, and a rounding change breaks the example (section 6.1);
- DataFrames and other large objects — how they print depends on the library version and the width of the display.

pytest can run doctests alongside your other tests:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/testing-lab/1-doctest"
uv run pytest --doctest-modules
```

```text
text_tools.py ..                                                         [100%]

============================== 2 passed in 0.01s ===============================
```

pytest counts one test per function that has examples, hence 2.

## 5. Your first test

We work inside a `uv` project, as in [Session 2](../sessions/s2.md#4-a-project-from-scratch). Create a fresh one to follow along:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
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


def test_twenty_percent() -> None:
    assert add_vat(100, 0.20) == 120


def test_zero_rate_changes_nothing() -> None:
    assert add_vat(100, 0) == 100
```

Add pytest as a **development dependency** — something the project needs in order to be worked on, not in order to run:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside vat-demo"
uv add --dev pytest
uv run pytest
```

`uv add --dev` writes pytest into a `[dependency-groups]` section of `pyproject.toml` rather than into `dependencies`, so someone who only wants to *use* your code does not have to install your test tools. It is installed into the same `.venv`, and `uv sync` restores it.

### 5.1 The error every single person hits first

```text
E   ModuleNotFoundError: No module named 'vat'
=========================== short test summary info ============================
ERROR tests/test_vat.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

Your code is in the project root; your test is in `tests/`. When pytest imports `tests/test_vat.py`, the folder Python searches is `tests/`, and `vat.py` is not there. The one-line fix is an **empty file called `conftest.py` next to `pyproject.toml`**:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside vat-demo"
touch conftest.py
uv run pytest -v
```

`conftest.py` is pytest's per-project configuration file. Its mere presence at the top of the project tells pytest "this is the root", and the root goes on the import path — so `from vat import add_vat` resolves. (You will also use it in section 9 to share fixtures.) Now:

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
    - **`src/` layout** (`uv init --package`) — the project is installed into its own environment, so `from mypackage import x` works from anywhere and no `conftest.py` trick is needed. Right for something you intend to publish.

    Do not put tests *inside* the same file as the code for anything you will keep. A `if __name__ == "__main__":` block with a few prints is a fine first step, but nobody runs it twice.

## 6. `assert`, and what a failure looks like

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


def test_twenty_percent_off_100() -> None:
    assert final_price(100, 0.20) == 80
```

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside vat-demo"
uv run pytest tests/test_discount.py
```

```text
=================================== FAILURES ===================================
_________________________ test_twenty_percent_off_100 __________________________

    def test_twenty_percent_off_100() -> None:
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

### 6.1 The float trap

```python title="tests/test_float.py"
from vat import add_vat


def test_tiny_price() -> None:
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


def test_tiny_price() -> None:
    assert add_vat(0.1, 2) == pytest.approx(0.3)
```

This matters far beyond toy examples: every mean, rate, share or revenue in a data pipeline is a float.

## 7. Writing tests that are worth having

**Arrange, act, assert.** Three visual blocks, in that order. A test that mixes them is a test nobody can read six months later.

```python
def test_revenue_per_region() -> None:
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


def test_increment() -> None:
    global total
    total += 1
    assert total == 1


def test_increment_again() -> None:
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


def test_negative_rate_is_refused() -> None:
    with pytest.raises(ValueError):
        add_vat(100, -0.1)
```

`pytest.raises` passes when the block raises that exception and **fails when it does not** — that is the point. Use `match=` to pin the message down: `pytest.raises(ValueError, match="negative")`.

## 8. `parametrize`: the same test on many values

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
def test_rates(price: float, rate: float, expected: float) -> None:
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

## 9. Fixtures: the setup, written once

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
from pathlib import Path

import pytest

from report import count_rows, print_summary


@pytest.fixture
def sales_csv(tmp_path: Path) -> Path:
    """Write a two-row CSV in a directory pytest deletes after the test."""
    path = tmp_path / "sales.csv"
    path.write_text("region,units\nAlsace,3\nBretagne,5\n", encoding="utf-8")
    return path


def test_count_rows(sales_csv: Path) -> None:
    assert count_rows(sales_csv) == 2


def test_print_summary(sales_csv: Path, capsys: pytest.CaptureFixture[str]) -> None:
    print_summary(sales_csv)
    captured = capsys.readouterr()
    assert "2 rows" in captured.out
```

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside vat-demo"
uv run pytest -q
```

```text
.........                                                                [100%]
9 passed in 0.01s
```

Three things happened worth naming. `sales_csv` is *your* fixture, and it asks for `tmp_path`, which is pytest's — fixtures compose. Each of the two tests got its own fresh copy of the file, so they cannot interfere. And nothing was left behind on your disk: no `test_output.csv` in your repository, ever.

A fixture used by several test files goes in `conftest.py` — the same empty file you created in section 5.1, now earning its keep:

```python title="conftest.py"
from pathlib import Path

import pytest


@pytest.fixture
def sales_csv(tmp_path: Path) -> Path:
    """A two-row CSV, available to every test in this project."""
    path = tmp_path / "sales.csv"
    path.write_text("region,units\nAlsace,3\nBretagne,5\n", encoding="utf-8")
    return path
```

!!! note "Fixtures that clean up"
    Replace `return` with `yield`, and everything after the `yield` runs once the test is done — closing a database connection, deleting a temporary table, restoring an environment variable. `tmp_path` needs no such thing, which is exactly why you should prefer it to writing files next to your code.

## 10. Mocking: replace what you are not testing

Some code talks to the outside world: a web API, a language model, a database. Testing it for real is slow, costs money, needs an API key, and — for a language model — does not even give the same answer twice. A test that sometimes passes and sometimes fails is worse than no test.

The way out is to notice what you are actually responsible for. You are not testing the LLM; somebody else wrote it. You are testing **your code around it**: the prompt you build, and what you do with the answer. So, for the duration of a test, you replace the function that makes the network call with a fake that returns a fixed answer. That fake is called a **mock**, and pytest's built-in `monkeypatch` fixture does the replacing.

The lab's example labels a review as positive or negative by asking the Unistra API. All the network code is in `ask_llm()`; the decision logic is in `label_review()`:

```python title="3-pytest/labeler.py"
--8<-- "resources/testing-lab/3-pytest/labeler.py"
```

The tests replace `ask_llm` and check only `label_review`:

```python title="3-pytest/tests/test_labeler.py"
--8<-- "resources/testing-lab/3-pytest/tests/test_labeler.py"
```

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/testing-lab/3-pytest"
uv run pytest tests/test_labeler.py -v
```

```text
tests/test_labeler.py::test_positive_answer PASSED                       [ 33%]
tests/test_labeler.py::test_answer_with_capital_and_full_stop PASSED     [ 66%]
tests/test_labeler.py::test_unexpected_answer PASSED                     [100%]

============================== 3 passed in 0.01s ===============================
```

`monkeypatch.setattr(labeler, "ask_llm", ...)` swaps the function *inside the module `labeler`* — which is where `label_review` looks it up — and puts the real one back when the test ends. The `lambda prompt: "positive"` is a one-line function that ignores its argument and always answers `"positive"`. Because the real `ask_llm` is never called, the tests make no network request, never read `UNISTRA_API_KEY`, cost nothing, and give the same result every time. What they do check is real: that `"Negative."` with a capital and a full stop is still understood, and that an answer you did not plan for becomes `"unknown"` instead of a crash.

Two rules keep mocking honest. Keep the part you replace **small** — one function that only does the call, like `ask_llm` — so that almost all of your logic is still tested for real. And do not mock the thing you are trying to test: a test in which everything is fake proves only that the fakes agree with each other.

## 11. Running them

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside a uv project"
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

### 11.1 Coverage: which lines were never run

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside vat-demo"
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

## 12. Testing code vs checking data

Everything so far tests **code**. In data work, half the surprises come from the **data**: a file saved with the wrong separator, a column renamed, a scale that changed from 1–5 to 1–10. The lab's `4-pipeline/` folder is the demo of the class, and it shows both kinds of test side by side.

The story: a colleague sends one CSV of product reviews every week (`data/week1.csv`, `week2.csv`, `week3.csv`). `pipeline.py` loads a file, cleans it, counts the words of each review, and prints, per language, the number of reviews, the mean rating and the mean length. Run it on each week:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/testing-lab/4-pipeline"
uv run python pipeline.py data/week1.csv
uv run python pipeline.py data/week2.csv
uv run python pipeline.py data/week3.csv
```

Week 1 works. Week 3 crashes with a `KeyError`, which is at least honest. Week 2 *works* — it prints a table — and the table is wrong, which you only see if you read it closely. That is the dangerous case, and it is the one tests are for.

**Unit tests on small, hand-written tables.** `tests/test_clean.py` checks what `clean()` should do, on five rows written by hand in `conftest.py` (the `small_reviews` fixture), each row carrying one of the problems met in real files: a language written `FR`, a trailing space, a missing text, a text made only of spaces. The table is tiny, so the right answer can be worked out by hand and written in the test. These tests are about the *code*: they would still make sense if no real file existed yet.

**Data checks on every real file.** `tests/test_data.py` is different. It does not invent data; it opens every CSV in `data/` and asserts what must be true of any file you are willing to analyse:

```python title="4-pipeline/tests/test_data.py"
--8<-- "resources/testing-lab/4-pipeline/tests/test_data.py"
```

The key line is `@pytest.fixture(params=DATA_FILES, ...)`. A fixture with `params` runs every test that uses it once per value — here, once per file — and the file name appears in brackets in the report. Drop a fourth week into `data/` and it is checked without changing a line. The `reviews` fixture builds on `raw` and *skips* the other checks when the columns are wrong, because nothing else can be checked on such a file.

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/testing-lab/4-pipeline"
uv run pytest tests/test_data.py
```

On the files as they arrive, the report ends with:

```text
FAILED tests/test_data.py::test_expected_columns[week3.csv] - AssertionError:...
FAILED tests/test_data.py::test_languages_are_fr_or_en[week2.csv] - Assertion...
FAILED tests/test_data.py::test_ratings_between_1_and_5[week2.csv] - assert {...
FAILED tests/test_data.py::test_no_missing_or_empty_text[week2.csv] - assert ...
==================== 4 failed, 7 passed, 4 skipped in 0.05s ====================
```

Every failure names a check and a file. Week 3 has the wrong columns (it was saved with `;` as the separator). Week 2 has languages that are not `fr` or `en`, ratings outside 1–5, and empty reviews — and the assertion shows *which* reviews, because each test compares a list of offending rows with `[]`.

**What to do with a failing data check.** Some of these problems are the code's job: `clean()` should turn `FR` and `fr ` into `fr`, and drop reviews with no text — that is exactly what `test_clean.py` asks for, and fixing `clean()` is the class's live exercise. What remains after that is not a code problem. Ratings of 8 in a 1–5 scale mean somebody rated out of 10; a file with `;` and a column called `note` came from a different export. You could "fix" these in the code — divide by two, guess the separator — but you would be inventing an answer to a question only the sender can answer.

!!! quote "The lesson"
    A discrepancy in the data is a finding, not a bug to make disappear.

So you **refuse the file**: move it to `data/rejected/`, tell the colleague what is wrong, and keep the tests exactly as strict as they were. The checks only read `data/*.csv`, so a rejected file is no longer analysed — and no longer silently mixed into your results.

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside ~/testing-lab/4-pipeline"
mkdir data/rejected
mv data/week2.csv data/week3.csv data/rejected/
```

**A regression test.** One more file, `tests/test_summary.py`, contains `test_week1_summary_has_not_changed`. Week 1's report was checked by hand once and saved as `tests/expected/week1_summary.csv`; the test recomputes the report and compares it with the saved one, cell by cell, using `pd.testing.assert_frame_equal`. It does not say the numbers are *right* — a human decided that once — it says they have *not changed*. When you edit `clean()` to fix week 2, this test is what tells you whether you also changed week 1. If a change is intended, you re-check the numbers by hand and re-save the file; the command is in the test's docstring.

**Other checks worth writing** on your own data, in the same style:

- **Shape assertions.** After a join, `assert len(df) == n_before` — a duplicated key in a merge is the single most common silent error in applied work.
- **Domain assertions.** `assert df["share"].between(0, 1).all()`, `assert df["year"].min() >= 1990`, no negative prices.
- **Published-value assertions.** In the [replication track](../replication.md): `assert round(coefficient, 3) == 0.412`, taken from the paper's table. A discrepancy is then a finding, too.

## 13. Running the tests on every push (GitHub Actions)

Tests you run when you remember are tests that pass until the day they matter. **Continuous integration** means the tests run on someone else's computer on every push, and the result is visible next to the commit. The concept is in [Git as a collaboration tool, §5](git-collaboration.md#5-cicd-robots-that-run-on-every-push); here is the file.

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
    If `git push` is refused with a message about `workflow` scope, the GitHub credentials stored by `gh` are not allowed to create workflow files. Run `gh auth refresh -h github.com -s workflow`, then push again. UNVERIFIED: the exact refusal message, which was reported by the instructor but not reproduced for this page.

## 14. Tests and agents

This is why the page exists.

An agent's loop is: read some context, propose an edit, run something, read the result, repeat. The quality of the loop is decided by what "run something" is. With no tests, the agent's only feedback is "the script did not crash", so it optimises for not crashing — and a function that returns the wrong number never crashes. With tests, the feedback is a list of named expectations, and a failure tells the agent *which* expectation and *what* it got instead. The [failure report in section 6](#6-assert-and-what-a-failure-looks-like) is as useful to a model as it is to you, for the same reason: it contains the values.

Three habits follow.

1. **Write the assertion before the code**, or make the agent do it. "Add a `--separator` option" is a wish. "Add a `--separator` option; `test_separator_joins_with_dash` must pass" is a specification with a gate. This is the *assertion-before-code* rule of [Session 4](../sessions/s4.md), and it is ordinary test-driven development wearing a new hat:

    | Step | | |
    |---|---|---|
    | **Red** | Write a test for behaviour that does not exist yet | It fails — proof that the test can fail |
    | **Green** | Write the least code that makes it pass | No cleverness yet |
    | **Refactor** | Tidy up, with the test still passing | The test is the safety net |

    Step one matters most: a test that has never failed has never been tested. The [test-first exercise](../exercises/testing-tdd.md) walks through the loop once.

2. **Put the command in `AGENTS.md`**, not the intention:

    ```markdown title="AGENTS.md — the useful kind of instruction"
    After every change to a `.py` file, run `uv run pytest -q`.
    If anything fails, fix it before making another change.
    Never delete or weaken a test to make the suite pass.
    ```

    That last line is not paranoia. Deleting the failing test is a locally optimal move, and both humans and models find it. The same goes for data checks (section 12): loosening a check so that a bad file passes is deleting a test by another name.

3. **Read the diff of the tests first.** When an agent hands you a change, the tests tell you what it *thinks* it did. If the tests changed and you did not ask for that, start there.

Mocks (section 10) matter here too: an agent can run a test suite that needs no network and no key hundreds of times, for free, and get the same answer each time.

## 15. Where this sits in the bigger picture

Most of this page is **unit testing**: one function, in isolation, in milliseconds. Section 3 listed the other kinds; here is how the three most common ones compare:

| Kind | Scope | Speed | How many |
|---|---|---|---|
| Unit | one function, no database, no network | milliseconds | hundreds |
| Integration | several parts together — your code *and* the database, *and* the API | seconds | dozens |
| End-to-end | the whole thing as a user meets it, through the interface | minutes | a handful |

The usual advice is a pyramid: many unit tests, fewer integration tests, very few end-to-end tests — because the slow, fragile ones cost you most when they break for reasons that are not bugs. For the code in this course, unit tests, data checks on your input files, and one "does the whole script run on a small input file" test are the whole programme.

## 16. When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'yourfile'` | Your code is not on the import path when pytest imports `tests/` | Empty `conftest.py` next to `pyproject.toml` (§5.1) |
| `collected 0 items` | The file or the function is not named `test_*` | Rename: `tests/test_thing.py`, `def test_thing() -> None` |
| `fixture 'sales_csv' not found` | The fixture is in another test file | Move it to `conftest.py` (§9) |
| A test passes alone, fails with the others | Shared state between tests | No module-level mutable data; use a fixture (§7, §9) |
| `assert 0.30000000000000004 == 0.3` | Comparing floats with `==` | `pytest.approx` (§6.1) |
| `python text_tools.py` or `python -m doctest` prints nothing | All examples passed — silence is success | Add `-v` to see the list (§4) |
| A test needs the network or an API key | The code under test calls the outside world directly | Put the call in one small function and replace it with `monkeypatch` (§10) |
| A data check fails on one file | The file is not what the code expects | Decide whether it is a code problem or a data problem; refuse the file rather than loosen the check (§12) |
| `pytest: command not found` | You typed `pytest`, not `uv run pytest` | `uv run pytest` — or `uv add --dev pytest` first |
| `No module named pytest` inside `uv run` | pytest is not a dependency of *this* project | `uv add --dev pytest`, or `uv run --with pytest pytest` |
| Tests write files into your repository | The code was given a relative path | Pass a path in; use `tmp_path` in tests (§9) |
| CI is red, your machine is green | Different Python or different versions | `uv sync --locked` locally; check `.python-version` is committed |
| A test suddenly passes after an agent's edit | The test may have been changed | `git diff` the test files before the source files (§14) |

## 17. Cheat sheet

| Command / line | What it does |
|---|---|
| `uv run python -m doctest -v file.py` | Run the `>>>` examples in the docstrings of `file.py` |
| `if __name__ == "__main__": doctest.testmod()` | The same, from inside the file: `uv run python file.py -v` |
| `uv run pytest --doctest-modules` | Let pytest run the doctests too |
| `uv add --dev pytest` | pytest as a development dependency of the project |
| `uv run pytest` | Run every test it can find |
| `uv run --with pytest pytest` | Same, without declaring a dependency |
| `uv run pytest -q` / `-v` | Quieter / one line per test |
| `uv run pytest -x --lf` | Stop at the first failure; next time, only re-run the failures |
| `uv run pytest -k "name"` | Only tests whose name matches |
| `uv run --with pytest-cov pytest --cov=mymodule` | Which lines the tests never executed |
| `def test_x() -> None:` in `tests/test_y.py` | How pytest finds a test |
| `assert value == expected` | The whole API |
| `assert value == pytest.approx(expected)` | The same, for floats |
| `with pytest.raises(ValueError):` | Assert that a call is refused |
| `@pytest.mark.parametrize("a,b", [(1, 2)])` | One test, many cases |
| `@pytest.fixture` + a parameter of that name | Reusable setup, fresh per test |
| `@pytest.fixture(params=[...])` | Every test using the fixture runs once per value — e.g. once per data file |
| `tmp_path`, `capsys` | Built-in fixtures: a temporary directory, captured output |
| `monkeypatch.setattr(module, "name", fake)` | Replace a function for one test, e.g. the API call |
| empty `conftest.py` at the project root | Makes `from mycode import x` work from `tests/` |

## 18. Going further

1. [The Turing Way — Code Testing](https://book.the-turing-way.org/reproducible-research/testing) — the research-oriented guide this page borrows its examples and its list of test kinds from; written for researchers of every field.
2. [CodeRefinery — Automated testing](https://coderefinery.github.io/testing/) — a lesson built for researchers, with exercises on test design and continuous integration.
3. [Testing for Beginners, by hasankanaan26](https://github.com/hasankanaan26/Unit-Testing-Python) — six short runnable lessons: why test, pytest basics, fixtures, mocking, what to test, and a bonus on testing LLM agents with a fake LLM. A good second pass over sections 5 to 10.
4. [pytest — Get Started](https://docs.pytest.org/en/stable/getting-started.html) — the official five-minute version of section 5.
5. [pytest — How to parametrize tests](https://docs.pytest.org/en/stable/how-to/parametrize.html) and [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) — the two features worth reading properly.
6. [pytest — How to monkeypatch/mock modules and environments](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) and [How to run doctests](https://docs.pytest.org/en/stable/how-to/doctest.html) — the official pages behind sections 10 and 4.
7. [Python docs — `doctest`](https://docs.python.org/3/library/doctest.html) and [`unittest`](https://docs.python.org/3/library/unittest.html) — the standard library's two testing tools. You will meet `unittest` in older code; recognise `class TestX(unittest.TestCase)` and `self.assertEqual`, and know that pytest runs those tests too.
8. [uv — Using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/) — the source of the workflow in section 13.
9. Two practice repositories from last year's course, still available: `gitlab.unistra.fr/cours_test/intro_test` (run the suite, repair a broken test, complete a missing one) and `gitlab.unistra.fr/cours_test/testing_username_password` (build a password and an e-mail validator test-first). UNVERIFIED: both are last year's URLs and were not opened while writing this page; check they are still public before sending students there.
