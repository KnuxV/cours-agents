<!--
PORTED FROM last year's material (KnuxV/slides_cours_git):
  "Part 6 - Docstrings.md"      — what a docstring is, Google vs NumPy style, help(), __doc__
  "Part 7 - Type Hints.md"      — strong/weak, static/dynamic, hints do not enforce, collections,
                                   unions with |, Optional, Iterable, Callable, classes as types, mypy
  "Part 12 - pdoc.md"           — docstrings → HTML, where to put them, variable docstrings, pdoc usage
  "Part 13 - github_actions.md" — the docs workflow (rewritten: uv + pdoc's own published workflow)
  "Part 15 - exam.md" / Exam.md — the grading criterion "docstrings + type hints on every function"

PROPOSED DESTINATION: site/docs/reference/docstrings-and-type-hints.md
  Nav (site/mkdocs.yml, under "Reference"):
      - Python and quality:
          - Docstrings, type hints and generated docs: reference/docstrings-and-type-hints.md
  Row for site/docs/reference/index.md, section "Python and quality":
      | [Docstrings, type hints and generated docs](docstrings-and-type-hints.md) | Writing the two lines that tell a reader — or a model — what a function expects, checking them with mypy, and publishing them with pdoc | [Session 2](../sessions/s2.md), used in [Session 4](../sessions/s4.md) |

REWRITTEN, not pasted: `pip install mypy` / `pip install pdoc` → `uv run --with …`; the
JavaScript/Java typing-spectrum slides are cut to two sentences; the agent argument (a docstring is
the cheapest context you can give a model) is new.
Every output block below was produced on this machine (uv 0.12.10, CPython 3.12.14, mypy and
pdoc 16.0.0 installed on the fly with `uv run --with`).
-->

# Docstrings, type hints and generated docs

Two habits that cost one line each and pay for themselves within a week: saying what a function does, and saying what it takes and returns. A third section turns both into a website you did not write.

They matter more now than they did two years ago. A docstring and a signature are the cheapest, most reliable context you can hand a coding agent: they are next to the code, they cannot be forgotten in a separate document, and a model reading `def add_vat(price: float, rate: float) -> float` with one sentence under it does not have to guess what `rate` is — or invent an answer.

## 1. Docstrings

A **docstring** is a string literal placed as the first statement of a module, function, class or method. Python keeps it, at runtime, as `__doc__`.

```python title="vat.py"
"""Value-added tax helpers."""


def add_vat(price: float, rate: float) -> float:
    """Return `price` increased by a VAT `rate` given as a decimal (0.20 = 20 %)."""
    if rate < 0:
        raise ValueError("rate cannot be negative")
    return price * (1 + rate)
```

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
uv run python -c "import vat; help(vat.add_vat)"
```

```text
Help on function add_vat in module vat:

add_vat(price: float, rate: float) -> float
    Return `price` increased by a VAT `rate` given as a decimal (0.20 = 20 %).
```

That is the entire mechanism, and it is why a docstring beats a `#` comment for describing *what* a thing is: `help()` shows it, your editor shows it on hover, `pdoc` (section 4) turns it into a web page, and every tool that reads code — including an agent — finds it in the obvious place. Comments explain *why* a particular line is strange; docstrings explain *what* the unit does.

### 1.1 Where they go

```python title="all four positions"
"""Module docstring: what this file is for. First line of the file."""


CACHE_SIZE = 128
"""A string right after a module-level variable documents it (pdoc reads this)."""


def clean(text: str) -> str:
    """Function docstring."""


class Corpus:
    """Class docstring: what this object represents."""

    def __init__(self, path: str) -> None:
        """Constructor docstring."""
        self.path = path
        """Instance attribute docstring."""

    def tokenise(self) -> list[str]:
        """Method docstring."""
```

Python only officially recognises the first three positions; the variable docstrings are a convention that documentation generators read. All of them are optional. **The module docstring and one line per public function are the version you should never skip.**

### 1.2 One line, or several

For a function whose signature already says everything, one line is the right answer — a sentence in the imperative ("Return the…", not "This function returns the…"), ending with a full stop:

```python
def count_vowels(text: str) -> int:
    """Return how many of a, e, i, o, u, y appear in `text` (case-insensitive)."""
```

When there is more to say, the convention is: one summary line, a blank line, then the detail. Two layouts dominate. **Google style** is the more readable of the two and the one this course uses:

```python
def revenue_by_region(rows: list[tuple[str, int, float]], top: int = 3) -> dict[str, float]:
    """Total revenue per region.

    Args:
        rows: triples of (region, units, unit price).
        top: how many regions to keep, highest revenue first.

    Returns:
        A mapping from region name to revenue, at most `top` entries long.

    Raises:
        ValueError: if `top` is not positive.
    """
```

**NumPy style** says the same thing with underlines, and is what you will meet in scientific libraries:

```python
def revenue_by_region(rows, top=3):
    """Total revenue per region.

    Parameters
    ----------
    rows : list of tuple
        Triples of (region, units, unit price).
    top : int, optional
        How many regions to keep.

    Returns
    -------
    dict
        Region name to revenue.
    """
```

Pick one and be consistent within a project; documentation generators need to be told which one you chose (`pdoc --docformat google`). Notice that the Google version does not repeat the types in prose — the signature already has them, which is section 2.

!!! tip "The honest way to use AI for this"
    Writing forty docstrings by hand is exactly the sort of task worth delegating to a model, and last year's course said so explicitly. Two conditions. **Read every one** — a generated docstring that says "Return the result of the computation" is worse than nothing, because it looks like documentation. And **check the claims**: models happily document the function they expected rather than the one you wrote, and a docstring that contradicts the code is a trap for the next reader. A docstring you did not verify is an assertion you did not test.

## 2. Type hints

Python is **strongly typed** (it will not add a string to a number) but **dynamically typed** (a name can hold anything, and nothing is checked until it runs). A type hint adds the missing information without changing that:

```python
def process(data: str) -> str:
    return data.upper()
```

Read it as: `data` is expected to be a `str`, the function is expected to return a `str`.

### 2.1 They are not enforced

```python
def add(a: int, b: int) -> int:
    return a + b


result = add("hello", "world")
print(result)          # helloworld
```

Python ignores the annotations at runtime. They exist for **readers** and for **tools** — your editor, and a type checker.

### 2.2 The syntax you need

```python
# Variables (rarely necessary — the value usually says it)
name: str = "Alice"
rate: float = 0.20
ready: bool = False

# Collections, with their contents (Python 3.9+)
scores: list[int] = []
lookup: dict[str, float] = {}
pair: tuple[str, int] = ("Alsace", 3)
tags: set[str] = set()

# Functions
def greet(name: str) -> str: ...
def show(items: list[str]) -> None: ...        # -> None: returns nothing

# "One of these" — the pipe, Python 3.10+
def parse(value: int | float) -> str: ...
middle_name: str | None = None                 # may be absent

# Paths and other classes are types like any other
from pathlib import Path
def load(path: Path) -> list[str]: ...
```

`str | None` is the one to internalise: it is how you say "this may be missing", and it is the honest signature of every function that returns `None` when it finds nothing. In older code the same thing is written `Optional[str]`, imported from `typing`; they mean exactly the same.

Two more that are worth knowing when you see them:

```python
from collections.abc import Callable, Iterable


def total(items: Iterable[int]) -> int:
    """`Iterable` = anything you can loop over: list, tuple, set, range, generator."""
    return sum(items)


def apply_twice(func: Callable[[int], int], value: int) -> int:
    """`Callable[[argument types], return type]` — a function as an argument."""
    return func(func(value))
```

`Iterable` in a parameter position is a small kindness: it lets the caller pass a generator without building a list first.

### 2.3 What they buy you, concretely

```python title="loose.py — no hints"
def average(numbers):
    return sum(numbers) / len(numbers)


print(average("abc"))
```

```python title="tight.py — hinted"
def average(numbers: list[float]) -> float:
    """Return the arithmetic mean of `numbers`."""
    return sum(numbers) / len(numbers)


print(average("abc"))
```

**mypy** is a type checker: it reads the code without running it and reports contradictions. It is not installed in your project; `uv run --with` fetches it for one command:

```bash title="Any terminal, inside the project"
uv run --with mypy mypy loose.py
uv run --with mypy mypy tight.py
```

```text
Success: no issues found in 1 source file
```

```text
tight.py:6: error: Argument 1 to "average" has incompatible type "str"; expected "list[float]"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

Read that pair carefully, because it is the whole argument. Both files contain the same bug. Without hints, mypy has nothing to compare and cheerfully says everything is fine. With hints, the bug is found before the program runs. And if you run it anyway:

```bash title="Any terminal"
uv run python tight.py
```

```text
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

The error arrives in the end — but at runtime, from inside `sum`, three frames away from the mistake. The hint moved the diagnosis from "after it ran, somewhere in the internals" to "before it ran, on line 6".

To check a whole package:

```bash title="Any terminal, inside the project"
uv run --with mypy mypy textkit
```

```text
Success: no issues found in 4 source files
```

If you want mypy on every run, `uv add --dev mypy` makes it part of the project, and it becomes another step in the [CI workflow](testing.md#9-running-the-tests-on-every-push-github-actions).

### 2.4 How much is enough

- **Every function and method you write**: parameters and return. That is the rule last year's exam applied, and it is the right one.
- **Variables**: only when the value does not make the type obvious — an empty `list[str]` being the usual case.
- **Do not fight the checker.** If a hint gets complicated, that is usually a sign the function is doing two things. Split it before reaching for the exotic corners of `typing`.

## 3. Why an agent cares

A model working in your repository has to answer, for every function it touches: what goes in, what comes out, what is optional, what raises. It has three ways to find out — read the whole call graph, guess, or read the signature and the docstring. Only the third is cheap and reliable.

This is the same argument as the one for tests, one rung lower. A test states a behaviour mechanically. A type hint states an interface mechanically. A docstring states an intention in prose. The three together are what lets you say "add an option to this function" and get back something that fits, rather than something that compiles.

And the failure mode has a name: a docstring that no longer matches the code is worse than no docstring, because both you and the model will believe it. Keep them next to the thing they describe, and update them in the same commit.

## 4. Generated documentation with pdoc

`help()` is for one function at a time. **pdoc** reads a module or a package and writes a small website out of the docstrings and signatures you already have — no configuration, no separate source files to keep in sync.

```bash title="Any terminal, inside the project"
uv run --with pdoc pdoc vat.py report.py --docformat google -o docs
ls docs
```

```text
index.html  report.html  search.js  vat.html
```

Open `docs/vat.html` in a browser: one page per module, one entry per public function with its signature and its docstring, cross-links between them, and a working search box. `--docformat google` tells pdoc to render the `Args:`/`Returns:` sections of section 1.2 as structured blocks instead of a paragraph.

Without `-o`, pdoc starts a small local server and opens the documentation in your browser, rebuilding it as you edit — useful while writing. With `-o`, it writes the files and exits, which is what you want in CI.

```bash title="Any terminal — the whole package at once"
uv run --with pdoc pdoc textkit --docformat google -o docs
```

Three consequences worth noticing. The documentation cannot drift from the code, because it *is* the code. Names with a leading underscore get no entry of their own (they may still be visible in the rendered source of a function that calls them), so `__all__` and the underscore convention from [modules and packages, §5](modules-and-packages.md#5-packages-a-folder-of-modules) decide what the world sees. And the `docs/` folder is generated output: add it to `.gitignore` and build it in CI rather than committing it — the same reasoning as `.venv/`.

### 4.1 Publishing it on GitHub Pages

Every GitHub repository can serve a website. The workflow below builds the documentation on each push to `main` and publishes it to `https://<your-username>.github.io/<your-repo>/`.

```yaml title=".github/workflows/docs.yml"
name: docs

on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
      - run: uv sync --locked
      - run: uv run --with pdoc pdoc mymodule.py --docformat google -o docs/
      - uses: actions/upload-pages-artifact@v4
        with:
          path: docs/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v5
```

Then, once: repository **Settings → Pages → Source: GitHub Actions**. The next push builds and publishes.

- The structure and the action versions of the two `pages` steps are taken from [pdoc's own published workflow](https://github.com/mitmproxy/pdoc/blob/main/.github/workflows/docs.yml); the install and build steps are replaced with the `uv` equivalents from [uv's GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/). Replace `mymodule.py` with your module or package.
- The `build` job needs no write permission; only `deploy` does. Keeping them in two jobs is the reason.
- TODO(verify): this exact file has not been run on GitHub from this repository. Each piece is copied from a published, working workflow, but the combination is untested — run it once on a scratch repository before telling students it works.

!!! note "This site is built the same way"
    The pages you are reading are MkDocs, not pdoc, published by `.github/workflows/site.yml` in the course repository. pdoc documents *code*; MkDocs publishes *prose*. Most projects that need both use both.

## 5. When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `help(f)` shows nothing but the signature | The string is not the *first* statement of the function | Move it directly under the `def` line, before any code |
| Your docstring is not a docstring | You used `#` comments | A docstring is a `"""string"""`, not a comment |
| pdoc shows a function but no description | No docstring on it | Add one; pdoc invents nothing |
| pdoc renders `Args:` as one grey paragraph | The format was not declared | `--docformat google` (or `numpy`) |
| pdoc documents things you consider internal | They have no leading underscore and are not excluded | Rename to `_helper`, or set `__all__` |
| mypy says `Success` on obviously broken code | The code has no hints, so there is nothing to check | Add hints (§2.3) |
| mypy complains about a library you installed | It ships no type information | `# type: ignore[import-untyped]` on that import line, or move on — mypy is advice, not law |
| `error: Incompatible return value type (got "None", expected "str")` | The function can return nothing | That is true: the hint should be `str \| None` |
| `str \| None` raises a `TypeError` on an old Python | The pipe syntax needs Python 3.10+ | You pin 3.12 in this course; in older code use `Optional[str]` |
| Pages workflow runs green, the site is 404 | Pages source is not set to GitHub Actions | Settings → Pages → Source (§4.1) |

## 6. Cheat sheet

| Line | Meaning |
|---|---|
| `"""One sentence."""` under a `def` | Function docstring |
| `"""…"""` as the first line of a file | Module docstring |
| `help(obj)` / `obj.__doc__` | Read a docstring at runtime |
| `Args:` / `Returns:` / `Raises:` | Google style sections |
| `def f(x: int) -> str:` | Parameter and return hints |
| `list[str]`, `dict[str, float]`, `tuple[str, int]` | Contents of a collection |
| `str \| None` | May be missing (older spelling: `Optional[str]`) |
| `-> None` | Returns nothing |
| `Iterable[int]`, `Callable[[int], int]` | Anything loopable; a function as an argument |
| `uv run --with mypy mypy .` | Check the hints without installing anything |
| `uv add --dev mypy` | Make the checker part of the project |
| `uv run --with pdoc pdoc mymodule.py --docformat google -o docs` | Generate the HTML documentation |
| `uv run --with pdoc pdoc mymodule.py` | Live preview in the browser |

## 7. Going further

1. [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/) — the short, official statement of what a docstring is and how to lay it out.
2. [Google Python Style Guide — Comments and docstrings](https://google.github.io/styleguide/pyguide.html) — the `Args:`/`Returns:` convention at the source, with good and bad examples.
3. [Python docs — `typing`](https://docs.python.org/3/library/typing.html) and [mypy — Getting started](https://mypy.readthedocs.io/en/stable/getting_started.html) — the reference and the gentle introduction.
4. [pdoc documentation](https://pdoc.dev/docs/pdoc.html) — every option in section 4, including how to customise the output and deploy it.
5. [Testing your code with pytest](testing.md) — the next rung: from "I said what it should do" to "a machine checks that it does".
