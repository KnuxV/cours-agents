<!--
PORTED FROM last year's material (KnuxV/advanced_programming_python):
  lessons/06-organization_packaging/061-basic_import.md  — module vs script vs library, __name__ == "__main__", sys.path, import forms, import *
  lessons/06-organization_packaging/062-packages.md      — __init__.py, __all__, relative vs absolute imports, src/ layout, pyproject.toml, [project.scripts]
  lessons/06-organization_packaging/063-building_config.md — pip install -e ., python -m build  (rewritten for uv)
  lessons/06-organization_packaging/064-publishing_and_refs.md — PyPI, sdist/wheel, semantic versioning, TestPyPI, checklists
  exercices/08-project_orgs.md                          — the texttools exercise (its content is folded in as the worked example)
  KnuxV/slides_cours_git "Part 10 - __main__.md"         — the calculator.py demonstration

PROPOSED DESTINATION: site/docs/reference/modules-and-packages.md
  Nav (site/mkdocs.yml, under "Reference"):
      - Python and quality:
          - Modules, packages and imports: reference/modules-and-packages.md
  Row for site/docs/reference/index.md, section "Python and quality":
      | [Modules, packages and imports](modules-and-packages.md) | One file or several, what `import` really does, `__name__ == "__main__"`, packages, and how to make a project installable | [Session 2](../sessions/s2.md) |
  MERGE NOTE: the first two rungs of this page (a script, then a second file you import)
  are also the subject of the planned sessions/s2.md §5.4–5.6 — see INVENTORY.md. This page is
  the deeper reference the session should link to; it must not become the place students first
  meet `import`.

REWRITTEN, not pasted: `pip install -e .` / `python -m build` / hand-written setuptools
configuration → `uv init --package` and `uv build`; `import *` demoted to a warning;
every command has a "where to run it" title and none needs sudo.
Every output block was produced on this machine (uv 0.12.10, CPython 3.12.14).
-->

# Modules, packages and imports

Introduced in [Session 2](../sessions/s2.md). This page answers the questions that session raises and does not have time to finish: what `import` actually does, why every script ends with that `if __name__ == "__main__":` line, and how a folder of `.py` files becomes something you can install.

The through-line: **code you can import is code you can test**, and code you can test is code you can let an agent change. Everything here is in service of that.

## 1. Four words people use interchangeably, and should not

| Word | What it is | How you use it |
|---|---|---|
| **Script** | A `.py` file meant to be *run* | `uv run report.py sales.csv` |
| **Module** | A `.py` file meant to be *imported* | `import report` |
| **Package** | A *folder* of modules with an `__init__.py` file | `import textkit` |
| **Library** | A package (or several) someone publishes for others | `uv add polars`, then `import polars` |

A file can be both a script and a module — that is what section 3 is about — but a file that tries to be both without care surprises whoever imports it.

You have already met all four without the vocabulary: `report.py` from Session 2 is a script; `json` is a module of the standard library; `polars` is a library, and inside it are packages and modules.

## 2. Your first import: a second file

One file is fine until it is 400 lines long. Split it: put the functions in one file, the thing that *runs* in another.

```python title="tools.py — the module"
"""A module: functions meant to be imported, plus a self-test when run directly."""


def shout(text: str) -> str:
    """Return `text` in capitals with an exclamation mark."""
    return text.upper() + "!"


print("tools.py is being read, __name__ is", __name__)

if __name__ == "__main__":
    print(shout("hello"))
```

```python title="use.py — the script"
from tools import shout

print("use.py running, __name__ is", __name__)
print(shout("bonjour"))
```

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal or Codespace terminal"
uv run tools.py
uv run use.py
```

```text
tools.py is being read, __name__ is __main__
HELLO!
```

```text
tools.py is being read, __name__ is tools
use.py running, __name__ is __main__
BONJOUR!
```

Read the second output twice. **Importing a module runs it, top to bottom, once.** The `print` at module level fired even though `use.py` only wanted one function. The difference between the two runs is a single variable.

## 3. `__name__` and `if __name__ == "__main__":`

Python sets `__name__` in every file it reads:

- the file you *ran* gets `__name__ == "__main__"`;
- every file that got *imported* gets `__name__ == "<its module name>"` (`"tools"` above).

So the line you have been typing since Session 2 means exactly: **run this part only when this file is the one being executed.** Without it, every `print`, every test call, every `input()` at the bottom of your module fires the moment somebody imports it — which is what the output above shows, and what the following version fixes.

```python title="calculator.py — the wrong way"
def add(a, b):
    return a + b


print("Testing calculator…")
print(f"2 + 3 = {add(2, 3)}")
```

```python title="calculator.py — the right way"
def add(a, b):
    return a + b


if __name__ == "__main__":
    print("Testing calculator…")
    print(f"2 + 3 = {add(2, 3)}")
```

Both still work as scripts. Only the second can be imported without noise — by `use.py`, by pytest, or by an agent that wants to call `add` in isolation.

The convention goes one step further: put the work in a function called `main()` and leave one line under the guard. Now the file has a front door that tests and other code can knock on:

```python title="the shape of every script in this course"
def main() -> int:
    """Do the thing. Return the process exit code."""
    ...
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`raise SystemExit(main())` makes the function's return value the exit code of the process — `0` for success, anything else for failure. That is what a shell, a CI job or an agent looks at to decide whether your program worked. [Command-line arguments](command-line-arguments.md#8-a-main-that-can-be-tested) takes this further, with a `main(argv)` that a test can call directly.

!!! note "`uv init` already knows"
    The `main.py` that `uv init` generates contains this pattern. It is not decoration.

## 4. What `import` actually does

`import something` sends Python looking for `something`, in this order:

1. **Modules already imported** — a second `import json` in the same process costs nothing.
2. **Built-in modules** compiled into the interpreter (`sys`, `math`).
3. **The folders listed in `sys.path`**, in order.

`sys.path` starts with the folder of the script you ran (or the current directory for `python -c` and the interactive prompt), followed by the standard library and finally `site-packages` — where everything `uv add` installs ends up:

```bash title="Any terminal, inside a uv project"
uv run python -c "
import sys
for p in sys.path: print(repr(p))
"
```

```text
''
'/home/you/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python312.zip'
'/home/you/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python3.12'
'/home/you/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/lib/python3.12/lib-dynload'
'/home/you/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python3.12/site-packages'
```

The first entry, the empty string, is "where I am". That single line explains 90 % of import failures: `from tools import shout` works when you are standing in the folder that contains `tools.py`, and fails when you are not.

Where a module came from is never a mystery — ask it:

```bash title="Any terminal, inside a uv project"
uv run python -c "import json; print(json.__file__)"
uv run python -c "import polars"
```

```text
/home/you/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python3.12/json/__init__.py
```

```text
ModuleNotFoundError: No module named 'polars'
```

`json` is in the standard library, so it is always there. `polars` is not: it has to be installed into *this project's* environment (`uv add polars`). `ModuleNotFoundError` has exactly two causes — the package is not installed in the environment you are using, or your own file is not where Python is looking.

### 4.1 The four import forms

```python
import math                     # math.sqrt(16)
import polars as pl             # pl.read_csv(...)   — an alias, for typing's sake
from math import sqrt, pi       # sqrt(16)           — the names come straight in
from mypackage.sub import thing # reach into a package
```

Which to use is a readability decision. `import polars as pl` keeps the origin of every call visible; `from math import sqrt` is shorter and fine for one or two well-known names.

!!! warning "`from module import *` — don't"
    It copies every public name of the module into yours. Three consequences: nobody reading `result = process(data)` can tell which module `process` came from; two `import *` lines can silently overwrite each other's names (whichever came last wins, including over *your* functions); and your editor can no longer tell you what exists. It is acceptable in a throwaway interactive session and nowhere else. If you see it in code you inherit, replacing it is a safe first commit.

## 5. Packages: a folder of modules

When two files become six, group them. A **package** is a folder containing an `__init__.py` file:

```text
mdemo/
├── main.py
└── textkit/
    ├── __init__.py
    ├── strings.py
    └── stats.py
```

```python title="textkit/strings.py"
"""String transformations."""


def reverse(text: str) -> str:
    """Return `text` backwards."""
    return text[::-1]


def count_vowels(text: str) -> int:
    """Return how many of a, e, i, o, u, y appear in `text` (case-insensitive)."""
    return sum(1 for char in text.lower() if char in "aeiouy")
```

```python title="textkit/stats.py"
"""Counting things in text."""


def longest_word(text: str) -> str:
    """Return the longest whitespace-separated word of `text` (the first one, on a tie)."""
    return max(text.split(), key=len)
```

`__init__.py` is what makes the folder importable, and it is also the package's **front desk**. Empty, it does nothing but mark the folder. Filled, it decides what users of the package see:

```python title="textkit/__init__.py"
"""textkit — small text helpers."""

from .strings import count_vowels, reverse
from .stats import longest_word

__all__ = ["count_vowels", "reverse", "longest_word"]
```

```python title="main.py"
import textkit

print(textkit.reverse("strasbourg"))
print(textkit.count_vowels("meta-programming"))
print(textkit.longest_word("les agents ne sont pas magiques"))
print(textkit.__name__, "->", textkit.__file__)
```

```bash title="Any terminal, inside mdemo"
uv run main.py
```

```text
gruobsarts
5
magiques
textkit -> /home/you/mdemo/textkit/__init__.py
```

Note what the `__init__.py` bought: the caller writes `textkit.reverse(...)`, not `textkit.strings.reverse(...)`. You are free to move `reverse` from `strings.py` to `text.py` tomorrow; as long as `__init__.py` re-exports it, no caller changes. That is the point of a package — an inside and an outside.

`__all__` is the list of names `from textkit import *` would bring in. Its real value is as documentation: it is the package's public surface, written down. Everything else — anything starting with `_`, by convention — is internal, and you may change it without warning.

### 5.1 Relative and absolute imports

Inside a package, a leading dot means "relative to this package":

```python
from .strings import reverse      # sibling module in the same package
from . import stats               # the sibling module itself
from ..other import thing         # up one package (rare, and usually a smell)
```

Without the dot, the import is **absolute** and starts from `sys.path`: `from textkit.strings import reverse` works from anywhere the package is importable. Prefer absolute imports in your own scripts and relative imports inside a package you distribute.

Relative imports only work when the file is part of a package, which produces one of Python's least helpful error messages:

```bash title="Any terminal, inside mdemo"
uv run python textkit/__init__.py
```

```text
Traceback (most recent call last):
  File "/home/you/mdemo/textkit/__init__.py", line 3, in <module>
    from .strings import count_vowels, reverse
ImportError: attempted relative import with no known parent package
```

Running a file *inside* a package as if it were a script tells Python "this file is `__main__`, it has no parent", and the dot has nothing to refer to. You do not run the parts of a package; you run something that imports it, or you use `python -m` (next).

### 5.2 `python -m`: running a package

```bash title="Any terminal, inside mdemo"
uv run python -m textkit
```

```text
No module named textkit.__main__; 'textkit' is a package and cannot be directly executed
```

A package becomes runnable when you add a file called `__main__.py` — the package's script half:

```python title="textkit/__main__.py"
"""Run the package: `python -m textkit "some text"`."""
import sys

from . import count_vowels, longest_word, reverse


def main(argv: list[str] | None = None) -> int:
    """Print the three statistics for the text given on the command line."""
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: python -m textkit TEXT", file=sys.stderr)
        return 2
    text = " ".join(args)
    print("reversed:", reverse(text))
    print("vowels:", count_vowels(text))
    print("longest word:", longest_word(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

```bash title="Any terminal, inside mdemo"
uv run python -m textkit "les agents ne sont pas magiques"
```

```text
reversed: seuqigam sap tnos en stnega sel
vowels: 10
longest word: magiques
```

With no argument it prints its usage to standard error and exits with code 2, the convention for "you used me wrongly" (see [command-line arguments](command-line-arguments.md#9-exit-codes)). This is the same mechanism behind `python -m venv`, `python -m http.server` and `python -m pytest`: each of those is a package with a `__main__.py`.

## 6. Making the package installable

So far everything depends on standing in the right folder. To use `textkit` from anywhere — from a notebook, from another project, from a colleague's laptop — it has to be *installed*. `uv` generates the whole layout:

```bash title="Any terminal"
cd ~
uv init --package --python 3.12 pkgdemo
cd pkgdemo
```

```text
pyproject.toml
.python-version
README.md
src/pkgdemo/__init__.py
```

Two differences from the `uv init --no-package` you used in Session 2. The code lives in `src/pkgdemo/` — a package, with its `__init__.py` — and `pyproject.toml` has gained two sections:

```toml title="pyproject.toml (generated, abridged)"
[project]
name = "pkgdemo"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
requires-python = ">=3.12"
dependencies = []

[project.scripts]
pkgdemo = "pkgdemo:main"

[build-system]
requires = ["uv_build>=0.12.10,<0.13.0"]
build-backend = "uv_build"
```

- **`[build-system]`** names the program that turns your folder into an installable artefact. `uv` uses its own; you will also see `setuptools`, `hatchling`, `flit` and `poetry` in the wild. They are interchangeable from the outside.
- **`[project.scripts]`** creates a *command*. Read the line as `command-name = "module:function"`: after installation, typing `pkgdemo` calls `main()` in `src/pkgdemo/__init__.py`.
- `authors` is filled in from your `git config`; the values above are placeholders.

```bash title="Any terminal, inside pkgdemo"
uv run pkgdemo
```

```text
Installed 1 package in 1ms
Hello from pkgdemo!
```

`uv run <command>` installed the project into its own `.venv` (in *editable* mode — your edits take effect immediately, no reinstalling) and ran the command. The equivalent in the classic toolkit of [Session 2 §2](../sessions/s2.md#2-the-classic-toolkit-pip-venv-requirementstxt) was `pip install -e .`; you will see that line in many READMEs and it means the same thing.

This layout is also the one that makes `import pkgdemo` work in your tests without the `conftest.py` trick from [testing §3.1](testing.md#31-the-error-every-single-person-hits-first).

### 6.1 Building a distribution

```bash title="Any terminal, inside pkgdemo"
uv build
ls dist/
```

```text
Building source distribution...
Building wheel from source distribution...
Successfully built dist/pkgdemo-0.1.0.tar.gz
Successfully built dist/pkgdemo-0.1.0-py3-none-any.whl
```

Two files, two formats:

- **`.tar.gz`, the source distribution (sdist)** — your source plus the metadata, to be built on the target machine.
- **`.whl`, the wheel** — a zip archive laid out so that installing it is a copy. Faster, and the reason `uv add polars` takes a second instead of compiling Rust for ten minutes.

A wheel is self-contained, so you can already hand it to someone:

```bash title="Any terminal, anywhere"
uvx --from ./dist/pkgdemo-0.1.0-py3-none-any.whl pkgdemo
```

```text
Hello from pkgdemo!
```

### 6.2 Publishing, in theory

**PyPI** (the Python Package Index, [pypi.org](https://pypi.org)) is the public catalogue every `uv add` and `pip install` reads. Publishing means uploading the two files from `dist/` to it, after which anybody on earth can install your project by name. The mechanics are one command (`uv publish`, or `twine upload` in the classic toolkit) plus an API token from your PyPI account — but the decisions around it are the interesting part:

- **The name is global and first-come.** Once `requests` is taken, it is taken forever. Hence `requests-oauthlib`, `requests-toolbelt`, and the advice to check availability before you fall in love with a name.
- **Versions are promises.** The convention is semantic versioning, `MAJOR.MINOR.PATCH`: bump the patch for a fix, the minor for a backwards-compatible addition, the major when you break somebody's code. People depend on that promise in their own `pyproject.toml`.
- **A version is forever.** You cannot silently replace `0.1.0` with different contents; you publish `0.1.1`. That is what makes the hashes in a lockfile meaningful.
- **Rehearse on [TestPyPI](https://test.pypi.org)**, a separate copy of the index for exactly this.
- **Publish with a licence.** Code on the internet with no `LICENSE` file is, legally, all rights reserved — nobody may use it. See [choosing a licence](licensing.md).

Nothing in this course requires you to publish anything. The reason it is worth knowing: it demystifies `uv add`. The libraries you import are not special. They are somebody's `src/` folder, a `pyproject.toml`, and a wheel.

## 7. Why any of this matters for agents

An agent reads your repository to work in it, and it reads it the way you would if you were in a hurry. Three practical consequences of the material above.

- **Small, named files are cheap context.** "Change the VAT rate" in a 600-line `analysis.py` means the whole file has to be read, held and rewritten. In a `tax.py` of 30 lines it means one file. Module boundaries are context boundaries.
- **Importable code is testable code, and tests are how you supervise.** A function that only exists inside `if __name__ == "__main__":` cannot be called by a test, so no gate can be put in front of it. Everything that has behaviour goes in a function, above the guard.
- **The public surface is the contract.** `__all__`, the names in `__init__.py`, the `[project.scripts]` entry: these are the things you tell an agent not to change without asking. Internals are free.

## 8. When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'polars'` | The package is not installed in *this* environment | `uv add polars`, and run with `uv run` |
| `ModuleNotFoundError: No module named 'tools'` | Your own file is not in the folder Python starts from | `ls` — are `tools.py` and the script you ran side by side? (§4) |
| Importing your module prints things or asks for input | Code at module level, not under the guard | Move it under `if __name__ == "__main__":` (§3) |
| `ImportError: attempted relative import with no known parent package` | You ran a file that is part of a package as a script | Run something that imports the package, or give it a `__main__.py` and use `python -m` (§5.1) |
| `No module named textkit.__main__` | The package has no `__main__.py` | Add one (§5.2) |
| Your package imports fine in its own folder, nowhere else | It is not installed | `uv init --package` layout, or add the project as a dependency (§6) |
| A name is mysteriously not what you think it is | `from x import *` overwrote it | Replace the star imports (§4.1) |
| `ImportError: cannot import name 'x' from partially initialized module` | Circular import: A imports B and B imports A | Move the shared thing into a third module |
| Tests cannot import your code | `tests/` is not the project root | Empty `conftest.py` at the root, or the `src/` layout (§6) |

## 9. Cheat sheet

| Line | Meaning |
|---|---|
| `import mod` / `import mod as m` | Bring the module in, optionally under a shorter name |
| `from mod import a, b` | Bring two names in directly |
| `from . import sib` | Sibling module, inside a package only |
| `if __name__ == "__main__":` | Run this only when the file is executed, not imported |
| `raise SystemExit(main())` | Make the function's return value the process exit code |
| `__init__.py` | Marks a folder as a package; re-exports its public names |
| `__all__ = [...]` | The package's public surface (and what `import *` would take) |
| `__main__.py` | Makes the package runnable with `python -m package` |
| `uv init --no-package` | Flat project: one `main.py`, right for scripts |
| `uv init --package` | `src/` layout, installable, with a `[project.scripts]` command |
| `uv run <command>` | Run a command declared in `[project.scripts]` |
| `uv build` | Produce `dist/*.whl` and `dist/*.tar.gz` |
| `uv run python -c "import x; print(x.__file__)"` | Where did this module come from? |

## 10. Going further

1. [Python tutorial — Modules](https://docs.python.org/3/tutorial/modules.html) — the official version of sections 2 to 5, including packages.
2. [Python Packaging User Guide](https://packaging.python.org/) — the reference for everything in section 6, maintained by the people who build the tools.
3. [uv — Working on projects](https://docs.astral.sh/uv/guides/projects/) and [Building and publishing](https://docs.astral.sh/uv/guides/package/) — `uv init --package`, `uv build`, `uv publish`.
4. [PEP 621 — project metadata in `pyproject.toml`](https://peps.python.org/pep-0621/) — what each key in `[project]` means, from the source.
5. Last year's version of this material, at class pace: [Python organization and packaging](https://github.com/KnuxV/advanced_programming_python/blob/main/lessons/06-organization_packaging/061-basic_import.md) — written for `pip`, so read the commands with this page's table in hand.
